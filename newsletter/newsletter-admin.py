#!/usr/local/bin/python3.6

import os
import re
import cgi
import cgitb
import sqlite3
import random
import hashlib

# errors and debugging info to browser
cgitb.enable()

# Print necessary headers.
print("Content-Type: text/html")
print()


##########################
# Copy of common functions
##########################
def checkRunningOnServer() -> bool:
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        return True
    else:
        return False


def genHash(email: str) -> str:
    s = email + str(random.random())
    return gen_SHA256_string(s)


def updateHash(email) -> str:
    h = genHash(email)
    sql = "UPDATE newsletter SET hash = ? WHERE email = ?"
    cur.execute(sql, (h, email))
    con.commit()
    return h


def gen_SHA256_string(s: str) -> str:
    m = hashlib.sha256()
    m.update(s.encode('ascii'))
    return m.hexdigest()


def checkValidEMail(email: str) -> bool:
    # from https://stackoverflow.com/posts/719543/timeline bottom edit
    if not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        print("Error: invalid email")
        quit()
    return True


def insertNewEMail(email: str):
    email = email.lower()  # ensure mail in lower case
    checkValidEMail(email)
    h = genHash(email)
    cur.execute(f"INSERT INTO newsletter(email, verified, hash) VALUES (?,?,?)",
                (email, 0, h))
    con.commit()
    return h

##########################


def connectDB():
    # check I running on entorb.net webserver
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        pathToDb = '/home/entorb/data-web-pages/covid-19/newsletter.db'
    else:
        pathToDb = 'cache/newsletter.db'

    con = sqlite3.connect(pathToDb)
    con.row_factory = sqlite3.Row  # allows for access via row["name"]
    return con


def checkFormParameterSet(para: str) -> str:
    value = form.getvalue(para)
    if value == "":
        print(f"Error: parameter {para} missing")
        quit()
    return value


def checkEMailInDB(email: str) -> int:
    """
    returns verified column if found
    returns -1 if not found
    -1: not found
    0 : un-verified
    1 : verified
    """
    sql = f"SELECT verified FROM newsletter WHERE email = ?"
    res = cur.execute(sql, (email,)).fetchone()
    if res:
        return res[0]
    else:
        return -1


con = connectDB()
cur = con.cursor()

if os.environ.get('QUERY_STRING') == "":
    print("Error: no parameters given")
    quit()

# Create instance of FieldStorage
form = cgi.FieldStorage()

action = checkFormParameterSet("action")

if action == "register":
    email = checkFormParameterSet("email")
    email = email.lower()
    checkValidEMail(email)
    emailVerifyStatus = checkEMailInDB(email)
    if emailVerifyStatus == 1:
        print("Warn: email already registered")
    elif emailVerifyStatus == 0:
        print("Warn: re-registering unverified email")
        h = updateHash(email)
        # TODO: resend mail
    elif emailVerifyStatus == -1:
        h = insertNewEMail(email)
        # TODO: send mail

elif action == "unsubscribe":
    h = checkFormParameterSet("hash")
    email = checkFormParameterSet("email")
    email = email.lower()
    checkValidEMail(email)
    emailVerifyStatus = checkEMailInDB(email)
    if emailVerifyStatus != -1:
        unsubscribeEMail(email)

print("<p>Ende</p>")
