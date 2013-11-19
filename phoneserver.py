import sys
from flask import Flask, request, redirect, g
import twilio.twiml
from itertools import product, chain
from mdb import *
import random

#Translate keys on the phone pad to the possible numbers
keys = {
    '1' : "",
    '2' : "ABC",
    '3' : "DEF",
    '4' : "GHI",
    '5' : "JKL",
    '6' : "MNO",
    '7' : "PQRS",
    '8' : "TUV",
    '9' : "WXYZ",
    '0' : "",
    ""  : "",
}
#probably not needed
keys = { k : v + k + v.lower() for (k, v) in keys.items()}


app = Flask(__name__)

def getMDB():
    myMDB = getattr(g, '_mdb', None)
    if myMDB is None:
        g._mdb = MdbDatabase()
        mdbFile = open(app.config['MDB_FILE'], 'rb+')
        g._mdb.loadFile(mdbFile)
        myMDB = g._mdb
    return myMDB

 
@app.route("/", methods=['GET', 'POST'])
def welcome():
    """
    Respond to incoming voice requests. Right now only offer the option of looking up.
    """

    resp = twilio.twiml.Response()
    resp.say("Thank you for calling the M D B message database!")
    resp.say("To add an entry or perform text based lookups you may send me a text message at this number.")
    resp.redirect("/lookup")
    return str(resp)

def sayMsg(resp, mdbrec, prompt="an"):
    """
    Helper function for formatting messages to be said below
    """

    resp.say("In %s entry, number %s, \"%s\", said, \"%s\". ." % (prompt, mdbrec[0], mdbrec[1], mdbrec[2]))

@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    """
    Handle a voice mdb lookup
    """

    myMDB = getMDB()
    resp = twilio.twiml.Response()
    keypresses = request.values.get('Digits', None)
    if keypresses is not None:
        # turn the numberic keypresses into a set of possible strings they want to search for
        combos = list("".join(y) for y in product(*[keys[x] for x in keypresses])) or [""]
        matchSet = set()
        for c in combos:
            matches = myMDB.lookup(c)
            for match in matches:
                matchSet.add(match)
        matching = list(matchSet)
        matching.sort(reverse=True)
        
        resp.say("There are %s matching entries." % len(matching) or 0)
        if len(matching) == 1:
            sayMsg(resp, matching[0], "the only")
        elif len(matching) == 2:
            sayMsg(resp, matching[1], "the first")
            sayMsg(resp, matching[0], "the last")
        elif len(matching) > 2:
            sayMsg(resp, matching[0], "the last")
            sayMsg(resp, random.choice(matching[1:]), "a random")
            sayMsg(resp, random.choice(matching[1:]), "another random")
    resp.pause(length=1)
    with resp.gather(numDigits=5, finishOnKey="#", timeout=15, method="GET", action="/lookup") as g:
        g.say("To search the database please enter up to 5 letters using your digital keypad. Press pound when complete.")
    resp.redirect("/lookup?Digits=", method="GET")
    return str(resp)



@app.route("/sms", methods=["GET", "POST"])
def sms():
    """Handle a sms message"""
    myMDB = getMDB()

    resp = twilio.twiml.Response()
    body = request.values.get("Body", None)
    print "Body was", body

    if body is not None and body.lower().startswith("add"):
        #We're in mdb-add mode
        try:
            value = body.split(" ", 1)[1]
            name, msg = value.split("#")
        except IndexError:
            return str(resp)

        name = name.strip()
        msg = msg.strip()
        myMDB.add(name,  msg)
        myMDB.save()

    elif body is not None and any(body.lower().startswith(x) for x in ["lookup", "lu"]):
        #we're in mdb-lookup mode
        try:
            key = body.split(" ", 1)[1]
        except IndexError:
            key = ""
        matching = myMDB.lookup(key)
        matching.sort(reverse=True)
        message = ["%s matches|" % len(matching)]
        if len(matching) > 0:
            message.append("%s:{%s}said{%s}" % matching[0])
        while len(matching) > len(message)-1:
            newmsg = "%s:{%s}said{%s}" % random.choice(matching)
            if newmsg in message:
                continue
            if len(newmsg) + 1 + len(" ".join(message)) <= 160:
                message.append(newmsg)
            else:
                break
        resp.sms(" ".join(message))
    else:
        #We can't figure out what's up, so let's give them a hint
        resp.sms("Search the database by texting me with \"lookup <key>\" (or \"lu <key>\"). Add with \"add name # msg\".")
    return str(resp)
 
if __name__ == "__main__":
    try:
        mdbFileName = sys.argv[1]
	app.config['MDB_FILE'] = mdbFileName
    except KeyError:
        print "please execute as %s <mdb file>" % sys.argv[0]
        exit(1)
    app.run(debug=True, host="0.0.0.0")

