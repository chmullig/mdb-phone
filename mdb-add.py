from mdb import *
import sys


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        mdbFile = open(filename, 'rb+')
        mdbFile.seek(0)
    except IOError, e:
        if e.errno == 2:
            mdbFile = open(filename, 'ab+')
            mdbFile.seek(0)
    except:
        print "Usage: python mdb-add.py <filename>"
        exit(1)
    myrecords = MdbDatabase(mdbFile)

    name = raw_input("name: ")
    msg = raw_input("msg: ")

    myrecords.add(name, msg)
    last = myrecords[-1]
    print "%4d: {%s} said {%s}" % (len(myrecords), last.name, last.msg)
    myrecords.save()

