import os
import re
import sqlite3
import hashlib
# import bcrypt
import random

# TODO
# columns to add
# frequency of sending: 1, 7, 30, threshhold
# date created


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


def insertNewEMail(email: str):
    email = email.lower()  # ensure mail in lower case
    checkValidEMail(email)
    h = genHash(email)
    cur.execute(f"INSERT INTO newsletter(email, verified, hash) VALUES (?,?,?)",
                (email, 1, h))
    con.commit()
    return h


def checkValidEMail(email: str) -> bool:
    # from https://stackoverflow.com/posts/719543/timeline bottom edit
    if not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        print("Error: invalid email")
        quit()
    return True

##########################


def deleteDB():
    if not checkRunningOnServer() and os.path.isfile(pathToDb):
        os.remove(pathToDb)


def create_table():
    cur.execute("""
      CREATE TABLE newsletter (email text, verified int, hash text, threshhold int, regions text)
      """
                )


def test_select():
    for row in cur.execute("SELECT * FROM newsletter"):
        print(row)
    print("%s rows in the DB table" %
          cur.execute("SELECT count(*) FROM newsletter").fetchone()[0])


# check I runnung on entorb.net webserver
if checkRunningOnServer():
    pathToDb = '/home/entorb/data-web-pages/covid-19/newsletter.db'
else:
    pathToDb = 'cache/newsletter.db'


deleteDB()

con = sqlite3.connect(pathToDb)
cur = con.cursor()

create_table()
test_insert("test@entorb.net")
test_select()


cur.close()
con.close()
