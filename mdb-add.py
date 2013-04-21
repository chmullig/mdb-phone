from mdb import *
import sys


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        mdbFile = open(filename, 'ab')
    except:
        print "Usage: python mdb-add.py <filename>"
        exit(1)
    myrecords = MdbDatabase()

    name = raw_input("name: ")
    msg = raw_input("msg: ")

    myrecords.add(name, msg)
    myrecords.writeFile(mdbFile)


