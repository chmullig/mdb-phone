Mdb Python + Twilio
===================
This project is an extension to the COMSW3157 course, through the assignment
"Lab 8." Labs 1-7 are building up C and networking skills, through a simple
Message Database. It consists of a list of Mdb Records that consist of a 15
character name, and a 23 character message. There are programs to add messages
to a shared class database, and to search it.

Mdb
---
This implements a Python version of mdb-lookup and mdb-add, which is capable of
reading and writing to the same files interchangeably with the original C
programs.

I use `ctypes` to read/write and store the structs. See `mdb.py`.

The programs mdb-lookup.py and mdb-add.py behave almost identically to the C
programs.


Twilio
------
To actually do something new with these, I decided to use the Twilio APis to
make the database accessible over phone and SMS. `phoneserver.py` is a flask application that responds to twilio calls.


Installation & Usage
-----
mdb-add and mdb-lookup depend only on ctypes.  The phoneserver depends on the
python modules for twilio and flask. The specific versions are listed in
`requirements.txt`, although later versions probably work.

To use the phone server call it with an argument, and it will start a flask
server at port 5000. Then tell twilio to look to `http://server:5000/` for
Messaging and `http://server:5000/sms` for Messaging.


Demo
----
There's a shitty YouTube video of me testing it at:
http://www.youtube.com/watch?v=8qASnc1hJLM