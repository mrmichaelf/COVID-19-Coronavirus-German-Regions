import os
import sqlite3
import json

# my helper modules
# import helper

# check I runnung on entorb.net webserver
if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
    pathToDb = '/home/entorb/data-web-pages/covid-19/newsletter.db'
    pathToData = '/home/entorb/html/COVID-19-coronavirus/data/de-districts/de-districts-results.json'
else:
    pathToDb = 'cache/newsletter.db'
    pathToData = 'data/de-districts/de-districts-results.json'

con = sqlite3.connect(pathToDb)
con.row_factory = sqlite3.Row  # allows for access via row["name"]
cur = con.cursor()

# load latest data
d_districts_latest = {}
with open(pathToData, mode='r', encoding='utf-8') as fh:
    d_districts_latest = json.load(fh)

# loop over subscriptions
for row in cur.execute("SELECT email, threshhold, regions FROM newsletter WHERE activated = 1"):
    s_this_email = row["email"]
    s_this_threshhold = row["threshhold"]
    s_this_regions = row["regions"]
    l_this_regions = row["regions"].split(',')

    # for sorting by value
    d_this_regions_cases_PM = {}
    for id in l_this_regions:
        d_this_regions_cases_PM[id] = d_districts_latest[id]["Cases_Last_Week_Per_Million"]

    # table header
    print("Infektionen* : Landkreis")
    # table body
    for id, value in sorted(d_this_regions_cases_PM.items(), key=lambda item: item[1], reverse=True):
        d = d_districts_latest[id]
        print("%3d (%3d)    : %s" % (
            d["Cases_Last_Week_Per_Million"], d["Cases_Last_Week"], d["Landkreis"]))
    # table footer
    print("* Neu-Infektionen letzte Woche pro Millionen Einwohner und Neu-Infektionen letzte Woche absolut")
    print(
        f"Chart ULR = https://entorb.net/COVID-19-coronavirus/?yAxis=Cases_Last_Week_Per_Million&DeDistricts={s_this_regions}#DeDistrictChart")
