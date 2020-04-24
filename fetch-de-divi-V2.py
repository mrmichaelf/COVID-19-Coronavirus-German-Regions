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
# if d_data_all['Bayern'][-1]['Date'] == datestr:
#     print(f"WARNING: Date: {datestr} already in data file: {filename+'.json'}")
#     sys.exit()


def extractAreaTagTitleData(cont: str) -> list:
    # Example
    # <area shape="RECT" title="Thüringen
    # Anzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung: 63
    # Anteil COVID-19 Patienten/innen pro Intensivbett: 6,0%" coords="380,430,423,447">
    myPattern = 'title="([^"]+)"'
    myRegExp = re.compile(myPattern)
    myMatches = myRegExp.findall(cont)
    del cont, myPattern, myRegExp
    # remove duplicates
    d = {}
    for match in myMatches:
        d[match] = 1
    myMatches = list(sorted(d.keys()))
    del d, match
    return myMatches


def extractBundeslandKeyValueData(s1: str) -> list:
    # 'Baden-Württemberg\rAnzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung: 456\rAnteil COVID-19 Patienten/innen pro Intensivbett: 11,9%'

    return l


def fetch_betten():
    # fetch data per bundesland, having many duplicates
    cont = read_from_url(
        "https://diviexchange.z6.web.core.windows.net/gmap_betten.htm").decode('utf-8')
    myMatches = extractAreaTagTitleData(cont)
    # example
    # 'Schleswig-Holstein\rFreie Betten: 507\rBelegte Betten: 536\rAnteil freier Betten an Gesamtzahl: 48.6%'

    global d_data_all

# 'Baden-Württemberg\rAnzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung: 456\rAnteil COVID-19 Patienten/innen pro Intensivbett: 11,9%'

    # extract data
    for s1 in myMatches:
        l = []
        # l = extractBundeslandKeyValueData(s1)
        l1 = s1.split("\r")
        bundesland = l1.pop(0)
        l.append((bundesland))
        if bundesland not in d_data_all:
            d_data_all[bundesland] = []
        d1 = {}
        for s2 in l1:
            l2 = s2.split(': ')
            key = l2[0]
            value = l2[1]

            # remove percent sign from end
            if value[-1] == '%':
                print("Percent found")
                value = value[0: -1]

            # remove 1000 separator .
            pattern = re.compile(r'(?<=\d)\.(?=\d)')
            value = pattern.sub('', value)
            if value.isdigit():
                value = int(value)
            elif value.isnumeric():
                value = float(value)
            if isinstance(value, str):
                if value[-1] == '%':
                    print("Percent found")

            d1[key] = value
        l.append(d1)
        d2 = {}
        d2['Date'] = datestr
        d2['Betten belegt'] = d1['Belegte Betten']
        d2['Betten gesamt'] = d1['Freie Betten'] + d1['Belegte Betten']
        d_data_all[bundesland].append(d2)
        1
    del myMatches, s1, s2, l1, l2, d1, d2, key, value, bundesland


def export_data():
    global d_data_all
    helper.write_json(filename+'.json',
                      d_data_all, sort_keys=False, indent=1)

    # TODO write csv per state
    # # Test for Bayern
    # with open(filename+'.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
    #     csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
    #                             'date', 'occupied_percent', 'Belegte Betten', 'Betten gesamt'])
    #     csvwriter.writeheader()
    #     l = d_data_all['Bayern']
    #     for d in l:
    #         d['occupied_percent'] = round(100*d['Belegte Betten'] / d['Betten gesamt'], 1)
    #         csvwriter.writerow(d)

    # TODO: write csv for DE Sum


def fetch_covid():
    # fetch data per bundesland, having many duplicates
    cont = read_from_url(
        "https://diviexchange.z6.web.core.windows.net/gmap_covid.htm").decode('utf-8')
    myMatches = extractAreaTagTitleData(cont)
    1
    # example
    # 'Schleswig-Holstein\rFreie Betten: 507\rBelegte Betten: 536\rAnteil freier Betten an Gesamtzahl: 48.6%'


fetch_betten()
fetch_covid()

export_data()
