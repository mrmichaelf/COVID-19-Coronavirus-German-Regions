#!/usr/local/bin/python3.6

import os
import sqlite3
import json
import hashlib
import random
from datetime import date

# TODO

##########################
# Copy of common functions
##########################


def checkRunningOnServer() -> bool:
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        return True
    else:
        return False


def db_connect():
    # check I running on entorb.net webserver
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        pathToDb = '/home/entorb/data-web-pages/covid-19/newsletter.db'
    else:
        pathToDb = 'cache/newsletter.db'
    con = sqlite3.connect(pathToDb)
    con.row_factory = sqlite3.Row  # allows for access via row["name"]
    cur = con.cursor()
    return con, cur


SENDMAIL = "/usr/lib/sendmail"


def sendmail(to: str, body: str, subject: str, sender: str = 'no-reply@entorb.net'):
    mail = f"To: {to}\nSubject: {subject}\nFrom: {sender}\nContent-Type: text/plain; charset=\"utf-8\"\n\n{body}"
    if checkRunningOnServer():
        p = os.popen(f"{SENDMAIL} -t -i", "w")
        p.write(mail)
        # status = p.close()
        p.close()
    else:
        print(mail)


##########################


# set path variables
if checkRunningOnServer():
    pathToData = '/home/entorb/html/COVID-19-coronavirus/data/de-districts/de-districts-results.json'
else:
    pathToData = 'data/de-districts/de-districts-results.json'

# connect to DB
con, cur = db_connect()


# loop over subscriptions
for row in cur.execute("SELECT email, verified, hash, threshold, regions, frequency, date_registered FROM newsletter WHERE verified = 0 AND regions IS NOT NULL"):
    # for row in cur.execute("SELECT email, verified, hash, threshold, regions, frequency, date_registered FROM newsletter WHERE verified = 1 AND regions IS NULL"):
    mailBody = ""

    mailTo = row["email"]

    print(mailTo)

    mailBody += "\nNeu anmelden: https://entorb.net/COVID-19-coronavirus/newsletter-register.html\n"

    mailBody += f"\nentorb's Coronavirus Auswertungen: https://entorb.net/COVID-19-coronavirus/\n"

    # sendmail(to=mailTo, body=mailBody,
    #             subject=f"[COVID-19 Landkreis Benachrichtigung] - {reason_for_sending}")
