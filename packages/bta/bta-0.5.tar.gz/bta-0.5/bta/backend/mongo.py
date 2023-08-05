# This file is part of the BTA toolset
# (c) Airbus Group CERT, Airbus Group Innovations and Airbus DS CyberSecurity

import pymongo
import struct
from bta.normalization import TypeFactory, Normalizer
from bta.backend import Backend, RawTable, VirtualTable
import bson.binary
import bta.sd
import bta.datatable
import bta.tools.decoding
import bta.tools.expr
import bta.dbmeta
import logging
import functools
import re
from datetime import datetime, timedelta

log = logging.getLogger("bta.backend.mongo")

def vectorize(f):
    @functools.wraps(f)
    def vect(self, val):
        if type(val) is tuple or type(val) is list:
            return [f(self, v) for v in val]
        return f(self, val)
    return vect

class MongoNormalizer(Normalizer):
    def empty(self, val):
        return not bool(val)

class MongoTextNormalizer(MongoNormalizer):
    pass

class MongoIntNormalizer(MongoNormalizer):
    def normal(self, val):
        if -0x8000000000000000 <= val < 0x8000000000000000:
            return val
        return str(val)

class MongoBinaryNormalizer(MongoNormalizer):
    @vectorize
    def normal(self, val):
        return bson.binary.Binary(val)

class MongoUnknownNormalizer(MongoNormalizer):
    @vectorize
    def normal(self, val):
        if type(val) in [int, long]:
            if -0x8000000000000000 <= val < 0x8000000000000000:
                return val
            return str(val)
        if type(val) in [list]:
            return val
        if type(val) is tuple:
            return list(val)
        if type(val) is unicode:
            return val
        return bson.binary.Binary(val)

class MongoTimestampNormalizer(MongoNormalizer):
    @vectorize
    def normal(self, val):
        try:
            ts = int(val)-11644473600 # adjust windows timestamp (from 01/01/1601) to unix epoch
            return datetime.fromtimestamp(ts)
        except ValueError:
            return datetime.fromtimestamp(0)

class MongoNTSecDesc(MongoNormalizer):
    def normal(self, val):
        return struct.unpack("Q", val)[0]

class MongoSID(MongoNormalizer):
    @vectorize
    def normal(self, val):
        if val:
            return bta.tools.decoding.decode_sid(val, ">")
        return None

class MongoGUID(MongoNormalizer):
    @vectorize
    def normal(self, val):
        if val:
            return bta.tools.decoding.decode_guid(val)
        return None

class MongoTrustAttributes(MongoNormalizer):
    def normal(self, val):
        if val is not None:
            return bta.datatable.TrustAttributes(val).to_json()
        return None

class MongoTrustType(MongoNormalizer):
    def normal(self, val):
        if val is not None:
            return bta.datatable.TrustType(val).to_json()
        return None

class MongoTrustDirection(MongoNormalizer):
    def normal(self, val):
        if val is not None:
            return bta.datatable.TrustDirection(val).to_json()
        return None

class MongoUserAccountControl(MongoNormalizer):
    def normal(self, val):
        if val is not None:
            return bta.datatable.UserAccountControl(val).to_json()
        return None

class MongoSecurityDescriptor(MongoNormalizer):
    def normal(self, val):
        if val:
            return bta.sd.sd_to_json(val)
        return None

class MongoAncestors(MongoNormalizer):
    def normal(self, val):
        if val:
            return bta.tools.decoding.decode_ancestors(val)
        return None

class MongoOID(MongoNormalizer):
    @vectorize
    def normal(self, val):
        if val is not None:
            return bta.tools.decoding.decode_OID(val)
        return None

class MongoWindowsTimestamp(MongoNormalizer):
    def normal(self, val):
        val = val^0xffffffffffffffff
        try:
            return datetime.fromtimestamp(0)+timedelta(microseconds=(val/10))
        except:
            return datetime.fromtimestamp(0)

class MongoLogonHours(MongoNormalizer):
    def normal(self, val):
        hours = ''.join(bin(x)[2:].zfill(8)[::-1] for x in bytearray(val))
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        if len(hours) > 0:
            hours = hours[-1]+hours[:-1]
            hours = re.findall('........................', hours)
        else:
            hours = ['x', 'x', 'x', 'x', 'x', 'x', 'x']
        return dict(zip(days, hours))

class MongoWindowsEnlaspedTime(MongoNormalizer):
    def normal(self, val):
        try:
            val = int(val)
            return datetime.fromtimestamp(0)+timedelta(microseconds=(val/10-11644473600000000))
        except:
            return datetime.fromtimestamp(0)


class MongoReplPropMeta(MongoNormalizer):
    def normal(self, val):
        return bta.tools.decoding.decode_ReplPropMeta(val)

class MongoTypeFactory(TypeFactory):
    def Text(self):
        return MongoTextNormalizer()
    def Int(self):
        return MongoIntNormalizer()
    def Binary(self):
        return MongoBinaryNormalizer()
    def Timestamp(self):
        return MongoTimestampNormalizer()
    def NTSecDesc(self):
        return MongoNTSecDesc()
    def SID(self):
        return MongoSID()
    def GUID(self):
        return MongoGUID()
    def SecurityDescriptor(self):
        return MongoSecurityDescriptor()
    def TrustAttributes(self):
        return MongoTrustAttributes()
    def TrustType(self):
        return MongoTrustType()
    def TrustDirection(self):
        return MongoTrustDirection()
    def UserAccountControl(self):
        return MongoUserAccountControl()
    def UnknownType(self):
        return MongoUnknownNormalizer()
    def Ancestors(self):
        return MongoAncestors()
    def OID(self):
        return MongoOID()
    def WindowsTimestamp(self):
        return MongoWindowsTimestamp()
    def WindowsEnlapsedTime(self):
        return MongoWindowsEnlaspedTime()
    def LogonHours(self):
        return MongoLogonHours()
    def ReplPropMeta(self):
        return MongoReplPropMeta()

class MongoTable(RawTable):
    def __init__(self, options, db, name):
        RawTable.__init__(self, options, db, name)
        self.typefactory = MongoTypeFactory()
        self.col = db[name]
        self.fields = None
        self.append = getattr(options, "append", False)
        self.overwrite = getattr(options, "overwrite", False)

    def create_index(self, colname):
        self.col.create_index(colname)

    def ensure_index(self, colname):
        self.col.ensure_index(colname)

    def create(self):
        if self.name in self.db.collection_names():
            if self.append:
                log.info("Collection [%s] already exists. Appending." % self.name)
                return
            elif self.overwrite:
                log.info("Collection [%s] already exists. Overwriting." % self.name)
                self.db.drop_collection(self.name)
            else:
                raise Exception("Collection [%s] already exists in database [%s]" % (self.name, self.db.name))
        self.col = self.db.create_collection(self.name)

    def ensure_created(self):
        if self.name not in self.db.collection_names():
            self.col = self.db.create_collection(self.name)

    def create_with_fields(self, columns):
        self.fields = [(c.name, getattr(self.typefactory, c.type)())  for c in columns]
        self.create()
        for c in columns:
            if c.index:
                self.create_index(c.name)

    def insert(self, values):
        return self.col.insert(values)

    def update(self, *args, **kargs):
        return self.col.update(*args, **kargs)

    def insert_fields(self, values):
        try:
            d = {name:norm.normal(v) for (name, norm), v in zip(self.fields, values) if not norm.empty(v)}
        except Exception,e:
            # Do it again to find which field failed
            for (name, norm), v in zip(self.fields, values):
                if not norm.empty(v):
                    try:
                        norm.normal(v)
                    except Exception,e2:
                        log.error("Normalization failed on field %s (value=%r)" % (name,v))
                        break
            else:
                raise
            raise e
        return self.insert(d)

    def count(self):
        return self.col.count()

    def find(self, *args, **kargs):
        return self.col.find(*args, **kargs)
    def find_one(self, *args, **kargs):
        return self.col.find_one(*args, **kargs)
    def assert_consistency(self):
        assert self.col.count() > 0, ("%s is empty" % self.name)

class categories(object):
    def __init__(self, ct):
        self._ct = ct
        for entry in ct.find():
            setattr(self, entry['name'].lower().replace('-', '_'), int(entry['id']))
    def assert_consistency(self):
        self._ct.assert_consistency()



@Backend.register("mongo")
class Mongo(Backend):
    # data format version.
    # to be incremented each time the import format changes
    # ex. added/removed extracted attributes, type changes...
    data_format_version = 1

    @classmethod
    def connect(cls, options):
        ip,port,_ = (options.connection+"::").split(":",2)
        ip = ip if ip else "127.0.0.1"
        port = int(port) if port else 27017
        return pymongo.Connection(ip, port)

    def __init__(self, options, connection=None, database=None):
        Backend.__init__(self, options, connection, database)
        if self.db is None:
            ip, port, self.dbname, _ = (self.connection+":::").split(":", 3)
            ip = ip if ip else "127.0.0.1"
            port = int(port) if port else 27017
            self.cnxstr = (ip, port)
            self.cnx = pymongo.Connection(*self.cnxstr)
            self.db = self.cnx[self.dbname]
        else:
            self.cnx = self.db.connection

        self.dbmetaentry = bta.dbmeta.DBMetadataEntry(self)
        if self.isFormatMismatch():
            raise Exception("Data format version mismatch.")
        self.dbmetaentry.set_value("data_format_version", self.data_format_version)


    def isFormatMismatch(self):
        """
        Format version mismatch iff all following criteria are met:
        * stored version is not None
        * stored version != data_format_version
        * --ignore-version-mismatch has not been passed
        * --overwrite has not been passed
        """
        db_data_format_version = self.dbmetaentry.get_value("data_format_version")
        if db_data_format_version is None:
            return False
        if db_data_format_version == self.data_format_version:
            return False
        if getattr(self.options, "ignore_version_mismatch", False):
            log.info("Format version mismatch (stored: %d, supported: %d) \
ignored." % (db_data_format_version, self.data_format_version))
            return False
        if getattr(self.options, "overwrite", False):
            log.info("Re-creating tables with updated data format version \
(%d -> %d)." % (db_data_format_version, self.data_format_version))
            return False
        log.error("Importer version mismatch. Database %s has already been \
imported using version %d importer format version. This program uses format \
version %d. You should either re-import the database using --overwrite, or \
continue with an older version of this tool. \n\
Using --ignore-version-mismatch might lead to incorrect results." %
(self.dbname, db_data_format_version, self.data_format_version))
        return True


    def open_raw_table(self, name):
        return MongoTable(self.options, self.db, name)
    def open_virtual_table(self, name):
        if name == "datasd":
            return VirtualDataSD(self.options, self, name)
    def open_special_table(self, name):
        if name == "categories":
            return categories(self.open_raw_table("category"))
        raise Exception("unknown special table [%s]" % name)
    def list_tables(self):
        return self.db.collection_names()


class MongoReqBuilder(bta.tools.expr.Builder):
    @classmethod
    def _field_(cls, name):
        return name
    @classmethod
    def _and_(cls, op1, op2):
        d = op1.copy()
        d.update(op2)
        return d
    @classmethod
    def _or_(cls, op1, op2):
        return { "$or": [ op1, op2 ]}
    @classmethod
    def _eq_(cls, op1, op2):
        return {op1: op2}
    @classmethod
    def _ne_(cls, op1, op2):
        return {op1: {"$ne":op2}}
    @classmethod
    def _present_(cls, op1):
        return {op1: {"$exists":True}}
    @classmethod
    def _absent_(cls, op1):
        return {op1: {"$exists":False}}
    @classmethod
    def _flagon_(cls, op1, op2):
        return {"%s.flags.%s" % (op1, op2) : True }
    @classmethod
    def _flagoff_(cls, op1, op2):
        return {"%s.flags.%s" % (op1, op2) : False }


class VirtualDataSD(VirtualTable):
    def __init__(self, options, backend, name):
        VirtualTable.__init__(self, options, backend, name)
        self.datatable = self.backend.open_raw_table("datatable")
        self.sd_table = self.backend.open_raw_table("sd_table")

    def find(self, req, proj={}):
        dtreq = req.build(MongoReqBuilder)
        log.debug("Mongo Request: %r" % dtreq)
        sdreq = {}
        for attr in ['sd_id', 'sd_value', 'sd_hash', 'sd_refcount']:
            if attr in dtreq:
                sdreq[attr] = dtreq.pop(attr)

        if sdreq:
            for sdres in self.sd_table.find(sdreq):
                dtreq2 = dtreq.copy()
                dtreq2["nTSecurityDescriptor"] = sdres["sd_id"]
                for dtres in self.datatable.find(dtreq2):
                    dtres.update(sdres)
                    resp = dtres if not proj else {dtres[x] for x in proj}
                    yield resp
        elif dtreq:
            for dtres in self.datatable.find(dtreq):
                sdreq2 = sdreq.copy()
                sdreq2["sd_id" ] = dtres["nTSecurityDescriptor"]
                for sdres in self.sd_table.find(sdreq2):
                    sdres.update(dtres)
                    resp = sdres if not proj else {sdres[x] for x in proj}
                    yield resp
                    
    def assert_consistency(self):
        self.datatable.assert_consistency()
        self.sd_table.assert_consistency()
