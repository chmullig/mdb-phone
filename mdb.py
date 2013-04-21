from ctypes import *
from copy import copy

class MdbRec(Structure):
    _fields_ = [
        ("name", c_char * 16),
        ("msg", c_char * 24),
    ]

class MdbDatabase(object):
    def __init__(self, msgFile=None):
        self.messages = []
        if msgFile:
            self.loadFile(msgFile)

    def __len__(self):
        return len(self.messages)

    def loadFile(self, msgFile):
        self.messages = []
        record = MdbRec()
        i = 0
        while msgFile.readinto(record) != 0:
            self.messages.append(copy(record))
            i += 1
        return i

    def writeFile(self, msgFile):
        for rec in self.messages:
            msgFile.write(rec)
    
    def lookup(self, key=""):
        results = []
        for i, rec in enumerate(self.messages):
            if key[:5] in rec.name or key[:5] in rec.msg:
                results.append((i, rec.name, rec.msg))
        return results

    def add(self, name, msg):
        newmdb = MdbRec(name, msg)
        self.messages.append(newmdb)

