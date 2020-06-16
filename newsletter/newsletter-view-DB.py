#!/usr/local/bin/python3.6

import os
import re
import sqlite3


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

print("DB Dump")
print("%16s %1s %64s %3s %45s %1s" %
      ('email', 'v', 'hash', 't', 'regions', 'f')
      )
for row in cur.execute("SELECT email, verified, hash, threshold, regions, frequency FROM newsletter ORDER BY email"):

    print("%16s %1s %64s %3s %45s %1s" % (
        row['email'], row['verified'], row['hash'], row['threshold'], row['regions'], row['frequency']))

cur.close()
con.close()
