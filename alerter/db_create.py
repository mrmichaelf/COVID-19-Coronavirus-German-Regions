import sqlite3

# TODO: move away from web dir
pathToDb = 'alerter/covid-19-alert.db'
con = sqlite3.connect(pathToDb)
# con = sqlite3.connect(":memory:")
# con.row_factory = sqlite3.Row  # allows for access via row["name"]
cur = con.cursor()


def create_table():
    cur.execute("""
      CREATE TABLE alerts (mail text, activated int, hash text, threshhold int, regions text)
      """
                )


def test_insert():
    myTuple = ("test@entorb.net", 1, "<hash>", 250,
               "09562,09572,09563,09564,03353,02000,14612")
    cur.execute(f"INSERT INTO alerts VALUES (?,?,?,?,?)", myTuple)
    con.commit()


def test_select():
    for row in cur.execute("SELECT * FROM alerts"):
        print(row)
    print("We now have %s rows in the DB table" %
          cur.execute("SELECT count(*) FROM alerts").fetchone()[0])


create_table()
test_insert()
test_select()


cur.close()
con.close()
