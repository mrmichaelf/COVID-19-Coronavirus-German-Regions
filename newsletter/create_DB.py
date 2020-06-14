import os
import sqlite3
import hashlib
import random

# TODO
# columns to add
# frequency of sending: 1, 7, 30, threshhold
# date created


def checkRunningOnServer() -> bool:
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        return True
    else:
        return False


def deleteDB():
    if not checkRunningOnServer() and os.path.isfile(pathToDb):
        os.remove(pathToDb)


def create_table():
    cur.execute("""
      CREATE TABLE newsletter (email text, verified int, hash text, threshhold int, regions text)
      """
                )


def gen_MD5_string(s: str) -> str:
    m = hashlib.md5()
    m.update(s.encode('ascii'))
    return m.hexdigest()


def test_insert(email: str):
    s = email + str(random.random())
    h = gen_MD5_string(s)
    cur.execute(f"INSERT INTO newsletter(email, verified, hash, threshhold, regions) VALUES (?,?,?,?,?)",
                (email, 1, h, 250,
                 "09562,09572,09563,09564,03353,02000,14612"))
    con.commit()


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
