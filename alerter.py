import sqlite3

# my helper modules
import helper


# TODO: ensure when deploying to webserver, that DB is outside of html dir
pathToDb = 'alerter/covid-19-alert.db'
con = sqlite3.connect(pathToDb)
con.row_factory = sqlite3.Row  # allows for access via row["name"]
cur = con.cursor()

# load latest data
d_districts_latest = helper.read_json_file(
    "data/de-districts/de-districts-results.json")

# loop over subscriptions
for row in cur.execute("SELECT mail, threshhold, regions FROM alerts WHERE activated = 1"):
    s_this_mail = row["mail"]
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
    print("* Neu-Infektionen letzte Woche pro Millionen Einwohner (Neu-Infektionen letzte Woche absolut)")
    print(
        f"Chart ULR = https://entorb.net/COVID-19-coronavirus/?yAxis=Cases_Last_Week_Per_Million&DeDistricts={s_this_regions}#DeDistrictChart")
