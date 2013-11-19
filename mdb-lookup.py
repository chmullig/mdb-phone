from mdb import *
import sys


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        mdbFile = open(filename, 'rb')
    except:
        print "Usage: python mdb-lookup.py <filename>"
        exit(1)
    myrecords = MdbDatabase(mdbFile)
    mdbFile.close()

    while True:
        try:
            key = raw_input("lookup: ")
        except EOFError:
            print
            break  
        for i, name, msg in myrecords.lookup(key):
                print "%4d: {%s} said {%s}" % (i, name, msg)
        print
