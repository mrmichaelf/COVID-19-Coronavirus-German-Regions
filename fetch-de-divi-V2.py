"""
Source: https://www.intensivregister.de/#/intensivregister
"""

import sys
# import requests
import csv
from datetime import datetime
import re

# my helper modules
import helper

filename = 'data/de-divi/de-divi-V2'

# now = datetime.now() # current date and time
datestr = datetime.now().strftime("%Y-%m-%d")

# d_data_all = {}
d_data_all = helper.read_json_file(filename+'.json')
# d_data_all[Bayern] -> list of dicts: data, occupied, total

# check if date is already in data set
if d_data_all['Bayern'][-1]['Date'] == datestr:
    print(f"WARNING: Date: {datestr} already in data file: {filename+'.json'}")
    sys.exit()


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
    l1 = s1.split("\r")
    if len(l1) == 1:
        l1 = s1.split("\n")
    bundesland = l1.pop(0)
    global d_data_all
    if bundesland not in d_data_all:
        d_data_all[bundesland] = []
    d = {}
    for s2 in l1:
        l2 = s2.split(': ')
        key = l2[0]
        value = l2[1]

        # remove percent sign from end
        if value[-1] == '%':
            value = value[0: -1]

        # remove 1000 separator .
        pattern = re.compile(r'(?<=\d)\.(?=\d)')
        value = pattern.sub('', value)

        # fix decimal separator 0,5 -> 0.5
        pattern = re.compile(r'(?<=\d),(?=\d)')
        value = pattern.sub('.', value)
        test = float('11.9')
        # convert value to numeric format
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                1

        if isinstance(value, str):
            print("ERROR: values is string")

        d[key] = value
    return (bundesland, d)


def fetch_betten():
    # fetch data per bundesland, having many duplicates
    cont = helper.read_from_url_or_cache(
        url="https://diviexchange.z6.web.core.windows.net/gmap_betten.htm", cache_file='cache/de-divi/gmap_betten.htm', cache_max_age=3600, verbose=True)
    myMatches = extractAreaTagTitleData(cont)
    del cont
    # example
    # 'Schleswig-Holstein\rFreie Betten: 507\rBelegte Betten: 536\rAnteil freier Betten an Gesamtzahl: 48.6%'

    global d_data_all

    # extract data
    for s1 in myMatches:
        bundesland, d1 = extractBundeslandKeyValueData(s1)

        d2 = {}
        d2['Date'] = datestr
        d2['Int Betten belegt'] = d1['Belegte Betten']
        d2['Int Betten gesamt'] = d1['Freie Betten'] + d1['Belegte Betten']
        d_data_all[bundesland].append(d2)
        1
    del myMatches, s1, bundesland, d1, d2


def fetch_covid():
    # fetch data per bundesland, having many duplicates
    cont = helper.read_from_url_or_cache(
        url="https://diviexchange.z6.web.core.windows.net/gmap_covid.htm", cache_file='cache/de-divi/gmap_covid.htm', cache_max_age=3600, verbose=True)
    myMatches = extractAreaTagTitleData(cont)
    del cont
    # 'Baden-Württemberg\rAnzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung: 456\rAnteil COVID-19 Patienten/innen pro Intensivbett: 11,9%'

    global d_data_all

    # extract data
    for s1 in myMatches:
        bundesland, d1 = extractBundeslandKeyValueData(s1)
        d2 = d_data_all[bundesland][-1]
        assert d2['Date'] == datestr
        # d2['Prozent COVID-19 pro Intensivbett'] = d1['Anteil COVID-19 Patienten/innen pro Intensivbett']
        # = COVID-19 Patienten / Betten gesamt
        d2['Int COVID-19 Patienten'] = d1['Anzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung']
        d_data_all[bundesland][-1] = d2
        1
    del myMatches, s1, bundesland, d1, d2


def add_DE_total():
    d_sums = {}
    global d_data_all
    for state, l_timeseries in d_data_all.items():
        for d in l_timeseries:
            if not d['Date'] in d_sums:
                d_sums[d['Date']] = {}
            for key, value in d.items():
                if key == 'Date':
                    continue
                if not key in d_sums[d['Date']]:
                    d_sums[d['Date']][key] = 0
                d_sums[d['Date']][key] += value
    # flatten dict
    l = []
    for date in sorted(d_sums.keys()):
        d = d_sums[date]
        d['Date'] = date
        l.append(d)
    d_data_all['DE Total'] = l
    1


def extract_latest():
    with open('data/de-divi/de-divi-latest.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
        csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
            'Code',
            'State',
            'Population',
            'Int Betten gesamt',
            'Betten pro 1000000',
            'Int Betten belegt',
            'Int Betten belegt Prozent',
            'Int COVID-19 Patienten',
            'Int Betten COVID-19 Prozent'
        ])
        csvwriter.writeheader()

        for state, l_timeseries in d_data_all.items():
            d = l_timeseries[-1]
            d2 = d
            if state != 'DE Total':
                d2['Code'] = d_states_map_name_code[state]
                d2['State'] = state
                d2['Population'] = d_states_ref[d2['Code']]['Population']
            else:
                d2['Code'] = 'DE'
                d2['State'] = 'Deutschland'
                d2['Population'] = 83149300
            d2['Betten pro 1000000'] = round(
                d2['Int Betten gesamt'] / d2['Population'] * 1000000, 0)
            covid = d['Int COVID-19 Patienten']
            belegt = d['Int Betten belegt']
            gesamt = d['Int Betten gesamt']
            d2['Int Betten belegt Prozent'] = round(100*belegt/gesamt, 1)
            d2['Int Betten COVID-19 Prozent'] = round(100*covid/gesamt, 1)
            csvwriter.writerow(d2)


def export_data():
    global d_data_all
    helper.write_json(filename+'.json',
                      d_data_all, sort_keys=False, indent=1)

    for state, l_timeseries in d_data_all.items():
        if state != 'DE Total':
            code = d_states_map_name_code[state]
            pop = d_states_ref[code]['Population']
        else:
            code = 'DE'
            pop = 83149300
        with open(f'data/de-divi/de-divi-{code}.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
            csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
                'Date',
                'Int Betten gesamt',
                'Betten pro 1000000',
                'Int Betten belegt',
                'Int Betten belegt Prozent',
                'Int COVID-19 Patienten',
                'Int Betten COVID-19 Prozent'
            ])
            csvwriter.writeheader()
            for d in l_timeseries:
                d2 = d
                gesamt = d['Int Betten gesamt']
                if not 'Int COVID-19 Patienten' in d2:
                    d2['Int COVID-19 Patienten'] = None
                    d2['Int Betten COVID-19 Prozent'] = None
                else:
                    covid = d['Int COVID-19 Patienten']
                    d2['Int Betten COVID-19 Prozent'] = round(
                        100*covid/gesamt, 1)
                d2['Betten pro 1000000'] = round(
                    d2['Int Betten gesamt'] / pop * 1000000, 0)
                belegt = d['Int Betten belegt']
                d2['Int Betten belegt Prozent'] = round(100*belegt/gesamt, 1)
                csvwriter.writerow(d2)


d_states_ref = helper.read_de_states_ref_data()

d_states_map_name_code = {}
for code, d in d_states_ref.items():
    d_states_map_name_code[d['State']] = code


fetch_betten()
fetch_covid()
add_DE_total()

extract_latest()

export_data()
