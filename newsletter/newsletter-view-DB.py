#!/usr/local/bin/python3.6

import os
import sqlite3
# import datetime


##########################
# Copy of common functions
##########################
def checkRunningOnServer() -> bool:
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        return True
    else:
        return False


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

##########################


con, cur = db_connect()

# cur.execute("ALTER TABLE newsletter ADD date_registered date")
# cur.execute("UPDATE newsletter set date_registered  = ?",
#             (datetime.date.today(),))
# con.commit()

print("DB Dump")
print("%20s %1s %64s %3s %45s %1s" %
      ('email', 'v', 'hash', 't', 'regions', 'f')
      )
for row in cur.execute("SELECT email, verified, hash, threshold, regions, frequency, date_registered FROM newsletter ORDER BY email"):

    print("%20s %1s %64s %3s %45s %1s %s" % (
        row['email'], row['verified'], row['hash'], row['threshold'], row['regions'], row['frequency'], row['date_registered']))


cur.close()
con.close()
