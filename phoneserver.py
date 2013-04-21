import sys
from flask import Flask, request, redirect
import twilio.twiml
from itertools import product, chain
from mdb import *
import random


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
myMDB = MdbDatabase()
 
@app.route("/", methods=['GET', 'POST'])
def welcome():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Thank you for calling the M D B!")
    with resp.gather(numDigits=1, action="/mainmenu") as g:
        g.say("Press 1 to lookup messages, or 2 to add a new message")
    return str(resp)

@app.route("/mainmenu", methods=["GET", "POST"])
def menu():
    """Handle the main menu."""
    resp = twilio.twiml.Response()
    keypress = request.values.get('Digits', None)
    print keypress
    if keypress == '1':
        return redirect("/lookup")
    elif keypress == '2':
        return redirect("/add")
    else:
        with resp.gather(numDigits=1, action="/mainmenu") as g:
            g.say("Press 1 to lookup messages, or 2 to add a new message")
        return str(resp)

@app.route("/add", methods=["GET", "POST"])
def add():
    """Add a new entry"""
    resp = twilio.twiml.Response()
    resp.say("Let's record a new entry!")
    resp.say("What is your name?")
    resp.record(transcribeCallback="/addname")


@app.route("/addname", methods=["GET", "POST"])
def addname():
    """Callback for transcribed name"""
    print request.values

@app.route("/addmsg", methods=["GET", "POST"])
def addmsg():
    """Callback for transcribed msg"""
    print request.values

def sayMsg(resp, mdbrec, prompt="an"):
    resp.say("In %s entry, number %s, \"%s\", said, \"%s\"." % (prompt, mdbrec[0], mdbrec[1], mdbrec[2]))

@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    """Handle a mdb lookup"""
    resp = twilio.twiml.Response()
    keypresses = request.values.get('Digits', None)
    if keypresses is not None:
        combos = list("".join(y) for y in product(*[keys[x] for x in keypresses])) or [""]
        print "Keypress: %s. Possible Values: %s" % (keypresses, ", ".join(combos))

        #matching = list(set(rec for rec in myMDB.messages if (any(True for c in combos if c in rec.name.upper()) or any(True for c in combos if c in rec.msg.upper()))))
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
            #resp.say("In the only entry, number %s, \"%s\", said, \"%s\"." % matching[0])
        elif len(matching) == 2:
            sayMsg(resp, matching[0], "the last")
            sayMsg(resp, matching[1], "the first")
            #resp.say("In the last entry, number %s, \"%s\" said \"%s\"." % matching[0])
            #resp.say("In the first entry, number %s, \"%s\" said \"%s\"." % matching[1])
        elif len(matching) > 2:
            sayMsg(resp, matching[0], "the last")
            sayMsg(resp, random.choice(matching[1:]), "a random")
            #resp.say("In the last entry, number %s, \"%s\" said \"%s\"." % matching[0])
            #resp.say("In a random entry, number %s, \"%s\" said \"%s\"." % random.choice(matching[1:]))
    resp.pause(length=1)
    with resp.gather(numDigits=5, finishOnKey="#", timeout=15, method="GET", action="/lookup") as g:
        g.say("To search the database please enter up to 5 letters using your digital keypad. Press pound when complete.")
    resp.redirect("/lookup?Digits=", method="GET")
    return str(resp)

 
if __name__ == "__main__":
    try:
        mdbFileName = sys.argv[1]
        mdbFile = open(mdbFileName, 'rb')
        myMDB.loadFile(mdbFile)
        mdbFile.close()
    except KeyError:
        print "please execute as %s <mdb file>" % sys.argv[0]
        exit(1)
    app.run(debug=True, host="0.0.0.0")

