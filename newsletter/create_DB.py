import os
import sqlite3


# TODO
# columns to add
# frequency of sending: 1, 7, 30, threshhold
# date created

# check I runnung on entorb.net webserver
if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
    pathToDb = '/home/entorb/data-web-pages/covid-19/newsletter.db'
else:
    pathToDb = 'cache/newsletter.db'

if os.path.isfile(pathToDb):
    os.remove(pathToDb)

con = sqlite3.connect(pathToDb)
# con = sqlite3.connect(":memory:")
# con.row_factory = sqlite3.Row  # allows for access via row["name"]
cur = con.cursor()


def create_table():
    cur.execute("""
      CREATE TABLE newsletter (email text, activated int, hash text, threshhold int, regions text)
      """
                )


def test_insert():
    cur.execute(f"INSERT INTO newsletter(email, activated, hash, threshhold, regions) VALUES (?,?,?,?,?)",
                ("test@entorb.net", 1, "<hash>", 250,
                 "09562,09572,09563,09564,03353,02000,14612"))
    con.commit()


def test_select():
    for row in cur.execute("SELECT * FROM newsletter"):
        print(row)
    print("We now have %s rows in the DB table" %
          cur.execute("SELECT count(*) FROM newsletter").fetchone()[0])


create_table()
test_insert()
test_select()


cur.close()
con.close()
