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
        self._msgFile = msgFile
        if msgFile:
            self.loadFile(msgFile)

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, key):
        return self.messages[key]

    def loadFile(self, msgFile):
        self.messages = []
        self._msgFile = msgFile
        record = MdbRec()
        i = 0
        while msgFile.readinto(record) != 0:
            self.messages.append(copy(record))
            i += 1
        return i

    def save(self):
        """NOTE: seeks to 0 and dumps the whole thing!"""
        self._msgFile.seek(0)
        self.writeFile(self._msgFile)
        

    def writeFile(self, msgFile):
        for rec in self.messages:
            txt = string_at(byref(rec), sizeof(rec))
            msgFile.write(txt)
    
    def lookup(self, key=""):
        results = []
        for i, rec in enumerate(self.messages):
            if key[:5] in rec.name or key[:5] in rec.msg:
                results.append((i+1, rec.name, rec.msg))
        return results

    def add(self, name, msg):
        newmdb = MdbRec(name[:16], msg[:24])
        self.messages.append(newmdb)

