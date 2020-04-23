"""
Source: https://www.intensivregister.de/#/intensivregister
"""

import sys
import requests
import csv
from datetime import datetime
import re

# my helper modules
import helper


def read_from_url(url: str) -> str:
    page = requests.get(url)
    return page.content


filename = 'data/de-divi/de-divi-V2'

# now = datetime.now() # current date and time
datestr = datetime.now().strftime("%Y-%m-%d")

# d_data_all = {}
d_data_all = helper.read_json_file(filename+'.json')
# d_data_all[Bayern] -> list of dicts: data, occupied, total

# check if date is already in data set
if d_data_all['Bayern'][-1]['date'] == datestr:
    print(f"WARNING: Date: {datestr} already in data file: {filename+'.json'}")
    sys.exit()

# fetch data per bundesland, having many duplicates
cont = read_from_url(
    "https://diviexchange.z6.web.core.windows.net/gmap_betten.htm").decode('utf-8')

myPattern = 'title="([^"]+)"'
myRegExp = re.compile(myPattern)
myMatches = myRegExp.findall(cont)
del cont, myPattern, myRegExp
# example
# 'Schleswig-Holstein\rFreie Betten: 507\rBelegte Betten: 536\rAnteil freier Betten an Gesamtzahl: 48.6%'

# remove duplicates
d = {}
for match in myMatches:
    d[match] = 1
myMatches = list(sorted(d.keys()))
del d, match

# extract data
for s1 in myMatches:
    l1 = s1.split("\r")
    bundesland = l1.pop(0)
    if bundesland not in d_data_all:
        d_data_all[bundesland] = []
    d1 = {}
    d2 = {}
    for s2 in l1:
        l2 = s2.split(': ')
        key = l2[0]
        value = l2[1]
        d1[key] = value
    d1['Freie Betten'] = int(d1['Freie Betten'].replace('.', ''))
    d1['Belegte Betten'] = int(d1['Belegte Betten'].replace('.', ''))
    d2['date'] = datestr
    d2['occupied'] = d1['Belegte Betten']
    d2['total'] = d1['Freie Betten'] + d1['Belegte Betten']
    d_data_all[bundesland].append(d2)
    1
del myMatches, s1, s2, l1, l2, d1, d2, key, value, bundesland

helper.write_json(filename+'.json',
                  d_data_all, sort_keys=False, indent=1)


# TODO write csv per state
# # Test for Bayern
# with open(filename+'.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
#     csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
#                             'date', 'occupied_percent', 'occupied', 'total'])
#     csvwriter.writeheader()
#     l = d_data_all['Bayern']
#     for d in l:
#         d['occupied_percent'] = round(100*d['occupied'] / d['total'], 1)
#         csvwriter.writerow(d)

# TODO: write csv for DE Sum
