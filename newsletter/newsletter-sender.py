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


def genHash(email: str) -> str:
    s = email + str(random.random())
    return gen_SHA256_string(s)


def gen_SHA256_string(s: str) -> str:
    m = hashlib.sha256()
    m.update(s.encode('ascii'))
    return m.hexdigest()


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


def db_updateHash(email) -> str:
    h = genHash(email)
    sql = "UPDATE newsletter SET hash = ? WHERE email = ?"
    cur.execute(sql, (h, email))
    con.commit()
    return h


SENDMAIL = "/usr/lib/sendmail"


def sendmail(to: str, body: str, subject: str = "[COVID-19 Landkreis Newsletter]", sender: str = 'no-reply@entorb.net'):
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

# load latest data
d_districts_latest = {}
with open(pathToData, mode='r', encoding='utf-8') as fh:
    d_districts_latest = json.load(fh)
dataDate = d_districts_latest["02000"]["Date"]


# loop over subscriptions
for row in cur.execute("SELECT email, verified, hash, threshold, regions, frequency FROM newsletter WHERE verified = 1 AND regions IS NOT NULL"):
    mailBody = "entorb's COVID-19 Landkreis Newsletter\n\n"
    mailTo = row["email"]
    s_this_regions = row["regions"]
    l_this_regions = row["regions"].split(',')

    # for sorting by value
    d_this_regions_cases_PM = {}
    for lk_id in l_this_regions:
        d_this_regions_cases_PM[lk_id] = d_districts_latest[lk_id]["Cases_Last_Week_Per_Million"]

    toSend = False
    # check if notification is due, based on threshold and frequency
    # daily sending
    if row["frequency"] == 1:
        toSend = True
    # sunday sending
    elif row["frequency"] == 7 and date.today().isoweekday() == 7:
        toSend = True
    elif row["threshold"] <= max(d_this_regions_cases_PM.values()):
        toSend = True

    if toSend:
        # table header
        mailBody += "Infektionen* : Landkreis\n"
        # table body
        for lk_id, value in sorted(d_this_regions_cases_PM.items(), key=lambda item: item[1], reverse=True):
            d = d_districts_latest[lk_id]
            mailBody += "%3d (%3d)    : %s\n" % (
                d["Cases_Last_Week_Per_Million"], d["Cases_Last_Week"], d["Landkreis"])
        # table footer
        mailBody += f"Datenstand: {dataDate}\n"
        mailBody += "\n* Neu-Infektionen letzte Woche pro Millionen Einwohner und Neu-Infektionen letzte Woche absolut\n"
        mailBody += f"\nCustom Chart: https://entorb.net/COVID-19-coronavirus/?yAxis=Cases_Last_Week_Per_Million&DeDistricts={s_this_regions}#DeDistrictChart\n"

        # create a new hash
        # add management link including new hash
        h = db_updateHash(mailTo)
        mailBody += f"\nAbmelden/Einstellungen ändern: https://entorb.net/COVID-19-coronavirus/newsletter-frontend.html?hash={h}\n"

        mailBody += "Neu anmelden: https://entorb.net/COVID-19-coronavirus/newsletter-register.html\n"

        sendmail(to=mailTo, body=mailBody)
