#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/swildermann/COVID-19
"""


# Author and version info
__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__maintainer__ = __author__
# __copyright__ = "Copyright 2020, My Project"
# __credits__ = ["John", "Jim", "Jack"]
__license__ = "GPL"
__status__ = "Dev"
__version__ = "0.1"


# Built-in/Generic Imports

import urllib.request
import csv
import json

# from matplotlib import pyplot as plt

# my helper modules
import helper

download_file = 'data/download-de-federalstates-timeseries.csv'


def download_new_data():
    url = "https://covid19publicdata.blob.core.windows.net/rki/covid19-germany-federalstates.csv"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(download_file, mode='wb') as f:
        f.write(datatowrite)


def read_ref_data() -> dict:
    """
    read pop etc from ref table and returns it as dict of dict
    """
    d_states_ref = {}
    with open('data/ref_de-states.tsv', mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter="\t")
        for row in csv_reader:
            d = {}
            d['State'] = row['State']
            d['Population'] = int(row['Population'])
            d['Pop Density'] = float(row['Pop Density'])
            d_states_ref[row["Code"]] = d
    return d_states_ref


def read_csv_to_dict() -> dict:
    """
    read and convert the source csv file, containing: federalstate,infections,deaths,date,newinfections,newdeaths
    re-calc _New
    add _Per_Million
    add Fitted Doublication time
    """

    global d_states_ref
    # Preparations
    d_states_data = {'BW': [], 'BY': [], 'BE': [], 'BB': [], 'HB': [], 'HH': [], 'HE': [], 'MV': [
    ], 'NI': [], 'NW': [], 'RP': [], 'SL': [], 'SN': [], 'ST': [], 'SH': [], 'TH': []}
    # add German sum
    d_states_data['DE-total'] = []
    d_german_sums = {}  # date -> 'infections', 'deaths', 'new infections', 'new deaths'

    # data body
    with open(download_file, mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        for row in csv_reader:
            d = {}
            s = row['date']
            l = s.split("-")
            d['Date'] = helper.date_format(
                int(l[0]), int(l[1]), int(l[2]))
            d['Cases'] = int(row["infections"])
            d['Deaths'] = int(row["deaths"])

            if row["federalstate"] == 'Baden-Württemberg':
                d_states_data['BW'].append(d)
            elif row["federalstate"] == 'Bavaria':
                d_states_data['BY'].append(d)
            elif row["federalstate"] == 'Berlin':
                d_states_data['BE'].append(d)
            elif row["federalstate"] == 'Brandenburg':
                d_states_data['BB'].append(d)
            elif row["federalstate"] == 'Bremen':
                d_states_data['HB'].append(d)
            elif row["federalstate"] == 'Hamburg':
                d_states_data['HH'].append(d)
            elif row["federalstate"] == 'Hesse':
                d_states_data['HE'].append(d)
            elif row["federalstate"] == 'Lower Saxony':
                d_states_data['NI'].append(d)
            elif row["federalstate"] == 'North Rhine-Westphalia':
                d_states_data['NW'].append(d)
            elif row["federalstate"] == 'Mecklenburg-Western Pomerania':
                d_states_data['MV'].append(d)
            elif row["federalstate"] == 'Rhineland-Palatinate':
                d_states_data['RP'].append(d)
            elif row["federalstate"] == 'Saarland':
                d_states_data['SL'].append(d)
            elif row["federalstate"] == 'Saxony':
                d_states_data['SN'].append(d)
            elif row["federalstate"] == 'Saxony-Anhalt':
                d_states_data['ST'].append(d)
            elif row["federalstate"] == 'Schleswig-Holstein':
                d_states_data['SH'].append(d)
            elif row["federalstate"] == 'Thuringia':
                d_states_data['TH'].append(d)
            else:
                print("ERROR: unknown state")
                quit()

            # add to German sum
            if d['Date'] not in d_german_sums:
                d2 = {}
                d2['Cases'] = d['Cases']
                d2['Deaths'] = d['Deaths']
            else:
                d2 = d_german_sums[d['Date']]
                d2['Cases'] += d['Cases']
                d2['Deaths'] += d['Deaths']
            d_german_sums[d['Date']] = d2
            del d2

    # for German sum -> same dict
    for datum in d_german_sums.keys():
        d = d_german_sums[datum]
        d['Date'] = datum  # add date field
        d_states_data['DE-total'].append(d)
    del d_german_sums, d

    # check if DE sum of lastdate and per-last date has changed, if so: remove last date
    if d_states_data['DE-total'][-1]['Date'] == d_states_data['DE-total'][-2]['Date']:
        print("WARNING: DE cases sum is unchanged")
        for code in d_states_data:
            d_states_data[code].pop()

    for code in d_states_data.keys():
        l_state_data = d_states_data[code]

        # ensure sorting by date
        l_state_data = sorted(
            l_state_data, key=lambda x: x['Date'], reverse=False)

        # add days past and calc cases and deaths new
        DaysPast = 1-len(l_state_data)  # last date gets number 0
        last_confirmed = 0
        last_deaths = 0
        for i in range(len(l_state_data)):
            d = l_state_data[i]

            d['Days_Past'] = DaysPast
            # l_state_data[i] = d
            DaysPast += 1

            d['Cases_New'] = d['Cases'] - last_confirmed
            d['Deaths_New'] = d['Deaths'] - last_deaths
            last_confirmed = d['Cases']
            last_deaths = d['Deaths']

            # add per Million rows
            d = helper.add_per_million(d_states_ref, code, d)

        # fit cases data
        data = []
        for i in range(1, len(l_state_data)):
            # x= day , y = cases
            data.append(
                (
                    l_state_data[i]['Days_Past'],
                    l_state_data[i]['Cases']
                )
            )
        fit_series_res = helper.series_of_fits(
            data, fit_range=7, max_days_past=28)
        for i in range(0, len(l_state_data)):
            this_doublication_time = ""
            this_days_past = l_state_data[i]['Days_Past']
            if this_days_past in fit_series_res:
                this_doublication_time = fit_series_res[this_days_past]
            l_state_data[i]['Doublication_Time'] = this_doublication_time

        d_states_data[code] = l_state_data
    return d_states_data


def export_data(d_states_data: dict):
    # export JSON and CSV
    for code in d_states_data.keys():
        outfile = f'data/de-states/de-state-{code}.tsv'
        l_state_data = d_states_data[code]

        with open(f'data/de-states/de-state-{code}.json', mode='w', encoding='utf-8', newline='\n') as fh:
            json.dump(d_states_data, fh, ensure_ascii=False)

        with open(outfile, mode='w', encoding='utf-8', newline='\n') as fh:
            csvwriter = csv.writer(fh, delimiter='\t')
            csvwriter.writerow(
                (
                    '# Days_Past', 'Date',
                    'Cases', 'Deaths',
                    'Cases_New', 'Deaths_New',
                    'Cases_Per_Million', 'Deaths_Per_Million',
                    'Cases_New_Per_Million', 'Deaths_New_Per_Million',
                    'Doublication_Time'
                )
            )
            for entry in l_state_data:
                csvwriter.writerow(
                    (
                        entry['Days_Past'], entry['Date'],
                        entry['Cases'], entry['Deaths'],
                        entry['Cases_New'], entry['Deaths_New'],
                        entry['Cases_Per_Million'], entry['Deaths_Per_Million'],
                        entry['Cases_New_Per_Million'], entry['Deaths_New_Per_Million'],
                        entry['Doublication_Time']
                    )
                )


def export_latest_data(d_states_data: dict):
    d_states_latest = dict(d_states_ref)
    for code in d_states_latest.keys():
        assert code in d_states_data.keys()
        l_state = d_states_data[code]
        d_latest = l_state[-1]
        d_states_latest[code]['Date_Latest'] = d_latest['Date']
        for key in ('Cases', 'Deaths', 'Cases_New', 'Deaths_New', 'Cases_Per_Million', 'Deaths_Per_Million'):
            d_states_latest[code][key] = d_latest[key]
    with open('data/de-states/de-states-latest.tsv', mode='w', encoding='utf-8', newline='\n') as f:
        csvwriter = csv.writer(f, delimiter="\t")
        csvwriter.writerow(
            ('# State', 'Code', 'Population', 'Pop Density', 'Date', 'Cases', 'Deaths', 'Cases_New', 'Deaths_New',
             'Cases_Per_Million', 'Deaths_Per_Million')
        )
        for code in sorted(d_states_latest.keys()):
            d = d_states_latest[code]
            l = (d['State'], code, d['Population'], d['Pop Density'], d['Date_Latest'], d['Cases'], d['Deaths'],
                 d['Cases_New'], d['Deaths_New'], d['Cases_Per_Million'], d['Deaths_Per_Million'])
            if code == 'DE-total':  # DE as last row
                l_de = list(l)
                continue
            csvwriter.writerow(
                l
            )
        del d, l, code
        # add # to uncomment the DE total sum last line
        l_de[0] = '# Deutschland'
        csvwriter.writerow(l_de)


# def convert_csv_OLD():


#         d_states_data[code] = l_state
#         outfile = f'data/de-states/de-state-{code}.tsv'
#         with open(outfile, mode='w', encoding='utf-8', newline="\n") as f:
#             csvwriter = csv.writer(f, delimiter="\t")
#             csvwriter.writerows(d_states_data[code])
#         del l_state, day_num, code

#     # latest data into another file
#     assert len(d_states_data.keys()) == len(d_states_ref.keys())
#     for code in d_states_ref.keys():
#         assert code in d_states_data.keys()
#     del code

#     d_states_latest = dict(d_states_ref)


d_states_ref = read_ref_data()

# TODO
download_new_data()
d_states_data = read_csv_to_dict()
# convert_csv()

export_data(d_states_data)
export_latest_data(d_states_data)

# 1
