from ctypes import *
from copy import copy

class MdbRec(Structure):
    """
    C struct identical to Jae's struct, a 16 character name (allowing 1 byte
    for null), and a 24 character message (again allowing 1 byte for null).
    """
    _fields_ = [
        ("name", c_char * 16),
        ("msg", c_char * 24),
    ]

class MdbDatabase(object):
    """
    The Database object. Internally it maintains a python list of MdbRec
    ctypes structs, and for convenience internally stores the file it was
    loaded from.
    """
    def __init__(self, msgFile=None):
        """
        Initializes the database, and if a file is given calls loadFile
        """
        self.messages = []
        self._msgFile = msgFile
        if msgFile:
            self.loadFile(msgFile)

    def __len__(self):
        """
        Returns the length of the internal messages list
        """
        return len(self.messages)

    def __getitem__(self, key):
        """
        Passes through to get an item by key value. Note that this is 0 indexed,
        while the lookup functionality is 1 indexed.
        """
        return self.messages[key]

    def loadFile(self, msgFile):
        """
        Replaces the contents of the database with what's read from the file!
        Also saves the given file as the msgFile. This is quite brute force,
        and likely not what you want.
        """
        self.messages = []
        self._msgFile = msgFile
        record = MdbRec()
        i = 0
        while msgFile.readinto(record) != 0:
            self.messages.append(copy(record))
            i += 1
        return i

    def save(self):
        """
        NOTE: seeks to 0 on the internally saved file object,
        and calls writeFile to dump the whole thing! 
        """
        self._msgFile.seek(0)
        self.writeFile(self._msgFile)
        

    def writeFile(self, msgFile):
        """
        Save record-by-record into the file.
        """
        for rec in self.messages:
            txt = string_at(byref(rec), sizeof(rec))
            print txt
            msgFile.write(txt)
    
    def lookup(self, key=""):
        """
        Search the database for the given key, using the first 5 characters
        of the key. Returns a list of matches where key[:5] appears in either
        the name or the message, plus the a 1-indexed id number for the record.
        """
        results = []
        for i, rec in enumerate(self.messages):
            if key[:5] in rec.name or key[:5] in rec.msg:
                results.append((i+1, rec.name, rec.msg))
        return results

    def add(self, name, msg):
        """
        Append a newly created mdb rec to the internal database.
        """
        newmdb = MdbRec(name[:15], msg[:23])
        self.messages.append(newmdb)

