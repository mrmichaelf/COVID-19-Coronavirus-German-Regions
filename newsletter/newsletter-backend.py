#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-

import os
import re
import sqlite3
import random
import hashlib
import datetime
import cgi
import cgitb
import json

# errors and debugging info to browser
cgitb.enable()

# Print necessary headers.
print("Content-type: application/json")
print()
# see https://stackoverflow.com/questions/4315900/how-can-i-send-a-json-object-from-a-python-script-to-jquery/4315936


# TODO


"""
Features


subscribe
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=subscribe&email=test2@entorb.net

unsubscribe
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=unsubscribe&hash=2c73929451c7e6e062594d114f081c79658313939694ff0348ba0ff05988e644

verify
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=verify&hash=822a384fdc5757f2020a886caa9db5f11686e41d895e33c56167c0d9a19a1c34

list
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=list&hash=822a384fdc5757f2020a886caa9db5f11686e41d895e33c56167c0d9a19a1c34

setThreshold
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=setThreshold&threshold=20&hash=178d6ad95bc5cf0e8bb200c723b5aaf28bfe840c6a759c449e09b669eb13dc50

setFrequency
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=setFrequency&frequency=7&hash=178d6ad95bc5cf0e8bb200c723b5aaf28bfe840c6a759c449e09b669eb13dc50

addRegion
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=addRegion&region=02000&hash=822a384fdc5757f2020a886caa9db5f11686e41d895e33c56167c0d9a19a1c34

removeRegion
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=removeRegion&region=02000&hash=822a384fdc5757f2020a886caa9db5f11686e41d895e33c56167c0d9a19a1c34

setRegions
https://entorb.net/COVID-19-coronavirus/newsletter-backend.py?action=setRegions&region=09562,02000&hash=822a384fdc5757f2020a886caa9db5f11686e41d895e33c56167c0d9a19a1c34
"""

##########################
# Copy of common functions
##########################

response = {}
response['status'] = "ok"


def checkRunningOnServer() -> bool:
    "am I running on the webserver entorb.net?"
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        return True
    else:
        return False


def genHash(email: str) -> str:
    "generate SHA256 hash based on email and random number"
    s = email + str(random.random())
    return gen_SHA256_string(s)


def gen_SHA256_string(s: str) -> str:
    m = hashlib.sha256()
    m.update(s.encode('ascii'))
    return m.hexdigest()


def assert_valid_email_format(email: str):
    # from https://stackoverflow.com/posts/719543/timeline bottom edit
    assert re.fullmatch(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email), "Error: invalid email format"


def db_connect():
    "connect to sqlite DB"
    # check I running on entorb.net webserver
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        pathToDb = '/home/entorb/data-web-pages/covid-19/newsletter.db'
    else:
        pathToDb = 'cache/newsletter.db'
    con = sqlite3.connect(pathToDb)
    con.row_factory = sqlite3.Row  # allows for access via row["name"]
    cur = con.cursor()
    return con, cur


def db_updateHash(email) -> str:
    "in DB: update hash of email. returns hash"
    h = genHash(email)
    sql = "UPDATE newsletter SET hash = ? WHERE email = ?"
    cur.execute(sql, (h, email))
    con.commit()
    return h


SENDMAIL = "/usr/lib/sendmail"


def sendmail(to: str, body: str, subject: str = "[COVID-19 Landkreis Newsletter]", sender: str = "no-reply@entorb.net"):
    mail = f"To: {to}\nSubject: {subject}\nFrom: {sender}\nContent-Type: text/plain; charset=\"utf-8\"\n\n{body}"
    if checkRunningOnServer():
        p = os.popen(f"{SENDMAIL} -t -i", "w")
        p.write(mail)
        # status = p.close()
        p.close()
    else:
        print(mail)

##########################


def send_email_register(email: str, h: str):
    # body = f"Bitte diesen Link öffnen um die Anmeldung abzuschließen und die Einstellungen vorzunehmen:\n ... "
    # TODO: BUG: Umlaute funktioniere hier nicht
    body = f"Bitte diesen Link oeffnen um die Anmeldung abzuschliessen und die Einstellungen vorzunehmen:\n https://entorb.net/COVID-19-coronavirus/newsletter-frontend.html?action=verify&hash={h}"
    sendmail(to=email, body=body,
             subject="[COVID-19 Landkreis Newsletter] - Anmeldung")


def get_form_parameter(para: str) -> str:
    "asserts that a given parameter is set and returns its value"
    value = form.getvalue(para)
    assert value, f"Error: parameter {para} missing"
    assert value != "", f"Error: parameter {para} missing"
    return value


def db_check_email_is_verified(email: str) -> int:
    """
    returns verified column if found
    returns -1 if not found
    -1: not found
    0 : un-verified
    1 : verified
    """
    sql = "SELECT email, verified FROM newsletter WHERE email = ? LIMIT 1"
    row = cur.execute(sql, (email,)).fetchone()
    if row:
        return row["verified"]
    else:
        return -1


def db_check_hash_is_verified(h: str) -> int:
    """
    returns verified column if found
    returns -1 if not found
    -1: not found
    0 : un-verified
    1 : verified
    """
    sql = "SELECT email, verified FROM newsletter WHERE hash = ? LIMIT 1"
    row = cur.execute(sql, (h,)).fetchone()
    if row:
        return row["email"], row["verified"]
    else:
        return "unknown", -1


def db_assert_hash_correct(email: str, h: str) -> bool:
    "checks if hash and mail fit"
    sql = "SELECT 1 FROM newsletter WHERE email = ? AND hash = ? LIMIT 1"
    row = cur.execute(sql, (email, h)).fetchone()
    assert row, "Error: invalid hash"


def db_assert_hash_exists(h: str) -> bool:
    "checks if hash is in DB"
    sql = "SELECT 1 FROM newsletter WHERE hash = ? LIMIT 1"
    row = cur.execute(sql, (h,)).fetchone()
    assert row, "Error: invalid hash"


def db_insertNewEMail(email: str):
    "in DB: insert new row of verified = 0 and a generated hash. returns hash"
    email = email.lower()  # ensure mail in lower case
    assert_valid_email_format(email)
    h = genHash(email)
    cur.execute(f"INSERT INTO newsletter(email, verified, hash, threshold, frequency, date_registered) VALUES (?,?,?,?,?,?)",
                (email, 0, h, 300, 1, datetime.date.today()))
    con.commit()
    return h


try:

    con, cur = db_connect()

    # ensure that this script is accessed using url parameters
    assert os.environ.get('QUERY_STRING') != "", "Error: no parameters given"

    # Create instance of FieldStorage
    form = cgi.FieldStorage()

    action = get_form_parameter("action")
    response['action'] = action

    # for all actions except subscribe the parameter hash needs to be set and present in the db
    if action != "subscribe":
        h = get_form_parameter("hash")
        db_assert_hash_exists(h)

    if action == "subscribe":
        email = get_form_parameter("email")
        email = email.lower()
        assert_valid_email_format(email)
        emailVerifyStatus = db_check_email_is_verified(email)
        if emailVerifyStatus == 1:
            sql = "SELECT hash FROM newsletter WHERE email = ? LIMIT 1"
            row = cur.execute(sql, (email,)).fetchone()
            h = row["hash"]
            send_email_register(email=email, h=h)
            response["message"] = f"Warn: {email} already registered and verified"
        elif emailVerifyStatus == 0:
            sql = "SELECT hash FROM newsletter WHERE email = ? LIMIT 1"
            row = cur.execute(sql, (email,)).fetchone()
            h = row["hash"]
            send_email_register(email=email, h=h)
            response["message"] = f"{email} re-subscribed"
        elif emailVerifyStatus == -1:
            h = db_insertNewEMail(email)
            send_email_register(email=email, h=h)
            response["hash"] = h
            response["message"] = f"{email} added"

    elif action == "unsubscribe":
        email, emailVerifyStatus = db_check_hash_is_verified(h=h)
        if emailVerifyStatus == 0 or emailVerifyStatus == 1:
            sql = "DELETE FROM newsletter WHERE email = ? AND hash = ?"
            cur.execute(sql, (email, h))
            con.commit()
            response["message"] = f"{email} unsubscribed"

    elif action == "verify":
        email, emailVerifyStatus = db_check_hash_is_verified(h=h)
        if emailVerifyStatus == 0:
            sql = "UPDATE newsletter SET verified = 1 WHERE hash = ?"
            cur.execute(sql, (h,))
            con.commit()
            response["message"] = f"{email} verified"
        elif emailVerifyStatus == 1:
            response["message"] = f"{email} was already verified"

    elif action == "setThreshold":
        threshold = int(get_form_parameter("threshold"))
        assert threshold > 0
        assert threshold < 1000
        sql = "UPDATE newsletter SET threshold = ? WHERE hash = ?"
        cur.execute(sql, (threshold, h))
        con.commit()
        response["message"] = f"threshold set to {threshold}"

    elif action == "setFrequency":
        frequency = int(get_form_parameter("frequency"))
        assert frequency in (0, 1, 7)
        sql = "UPDATE newsletter SET frequency = ? WHERE hash = ?"
        cur.execute(sql, (frequency, h))
        con.commit()
        response["message"] = f"frequency set to {frequency}"

    elif action == "setRegions":
        regions = get_form_parameter("regions")
        l_regions = regions.split(',')
        # ensure all regions are numeric
        for r in l_regions:
            assert r.isnumeric()
            assert len(r) == 5
        sql = "UPDATE newsletter SET regions = ? WHERE hash = ?"
        cur.execute(sql, (regions, h))
        con.commit()
        response["message"] = f"regions set to {regions}"

    elif action == "addRegion":
        region = get_form_parameter("region")
        assert region.isnumeric()
        assert len(region) == 5
        sql = "SELECT regions FROM newsletter WHERE hash = ? LIMIT 1"
        row = cur.execute(sql, (h,)).fetchone()
        if row["regions"]:
            l_regions = row["regions"].split(',')
        else:
            l_regions = []
        if region not in l_regions:
            l_regions.append(region)
            l_regions = sorted(l_regions)
            regions = ",".join(l_regions)
            sql = "UPDATE newsletter SET regions = ? WHERE hash = ?"
            cur.execute(sql, (regions, h))
            con.commit()
            response["message"] = f"region {region} added"

    elif action == "removeRegion":
        region = get_form_parameter("region")
        assert region.isnumeric()
        assert len(region) == 5
        sql = "SELECT regions FROM newsletter WHERE hash = ? LIMIT 1"
        row = cur.execute(sql, (h,)).fetchone()
        if row["regions"]:
            l_regions = row["regions"].split(',')
            if region in l_regions:
                l_regions.remove(region)
                if len(l_regions) > 0:
                    regions = ",".join(l_regions)
                else:
                    regions = None
                sql = "UPDATE newsletter SET regions = ? WHERE hash = ?"
                cur.execute(sql, (regions, h))
                con.commit()
                response["message"] = f"region {region} removed"

    elif action == "list":
        h = get_form_parameter("hash")

        sql = "SELECT email, verified, hash, threshold, regions, frequency FROM newsletter WHERE hash = ? LIMIT 1"
        row = cur.execute(sql, (h,)).fetchone()
        userdata = {
            "email": row['email'],
            "verified": row['verified'],
            "threshold": row['threshold'],
            "regions": row['regions'],
            "frequency": row['frequency']
        }
        response["userdata"] = userdata

    else:
        response['status'] = "error"
        response["message"] = f"unknown action {action}"

except Exception as e:
    response['status'] = "error"
    d = {"type": str(type(e)), "text": str(e)}
    response["exception"] = d

finally:
    response_json = json.dumps(response)
    print(response_json)
    cur.close()
    con.close()
