
from mdb import *
import sys


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        mdbFile = open(filename, 'rb+')
    except:
        print "Usage: python mdb-filter.py <filename>"
        exit(1)
    myrecords = MdbDatabase(mdbFile)
    mdbFile.close()
    try:
        key = raw_input("filter query: ")
    except EOFError:
        print
        exit  

    res = myrecords.lookup(key)
    res.reverse()
    for i, name, msg in res:
        print "%4d %s said %s <- deleting..." % (i, name, msg)
        myrecords.messages.pop(i-1)
    mdbFile = open(filename, 'w')
    myrecords.writeFile(mdbFile)
