import sqlite3

# my helper modules
import helper


# TODO: move away from web dir
pathToDb = 'alerter/covid-19-alert.db'
con = sqlite3.connect(pathToDb)
# con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row  # allows for access via row["name"]
cur = con.cursor()

d_districts_latest = helper.read_json_file(
    "data/de-districts/de-districts-results.json")

for row in cur.execute("SELECT mail, threshhold, regions FROM alerts WHERE activated = 1"):
    s_this_mail = row["mail"]
    s_this_threshhold = row["threshhold"]
    s_this_regions = row["regions"]
    l_this_regions = row["regions"].split(',')

    # TODO: sorting of output by Landkreis name
    # TODO: format columns text-compatible
    # IDEA: use HTML formatted email?
    print("Infektionen* : Landkreis")
    for id in l_this_regions:
        # print(d_districts_latest[id])
        d = d_districts_latest[id]
        print("%3d (%3d)    : %s" % (
            d["Cases_Last_Week_Per_Million"], d["Cases_Last_Week"], d["Landkreis"]))
    print("* Neu-Infektionen letzte Woche pro Millionen Einwohner (Neu-Infektionen letzte Woche absolut)")
    print(
        f"Chart ULR = https://entorb.net/COVID-19-coronavirus/?yAxis=Cases_Last_Week_Per_Million&DeDistricts={s_this_regions}#DeDistrictChart")
