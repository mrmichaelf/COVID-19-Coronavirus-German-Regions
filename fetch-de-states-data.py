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

from matplotlib import pyplot as plt

# my helper modules
import helper

download_file = 'data/download-de-federalstates-timeseries.csv'


def download_new_data():
    url = "https://covid19publicdata.blob.core.windows.net/rki/covid19-germany-federalstates.csv"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(download_file, 'wb') as f:
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


def date_format(y: int, m: int, d: int) -> str:
    # return "%02d.%02d.%04d" % (d, m, y)
    # besser, weil sortierbar
    return "%04d-%02d-%02d" % (y, m, d)


def helper_add_per_millions(state_code: str, l: list) -> list:
    global d_states_ref
    pop_in_million = d_states_ref[state_code]['Population'] / 1000000
    for i in range(1, 5):
        l.append(round(l[i]/pop_in_million, 3))
    return l


def convert_csv():
    """
    read and convert the source csv file: federalstate,infections,deaths,date,newinfections,newdeaths
    out: one file per state: 'date', 'infections', 'deaths', 'new infections', 'new deaths'
    """

    global d_states_ref
    # Preparations
    d_states_data = {'BW': [], 'BY': [], 'BE': [], 'BB': [], 'HB': [], 'HH': [], 'HE': [], 'MV': [
    ], 'NI': [], 'NW': [], 'RP': [], 'SL': [], 'SN': [], 'ST': [], 'SH': [], 'TH': []}
    # add German sum
    d_states_data['DE-total'] = []
    d_german_sums = {}  # date -> 'infections', 'deaths', 'new infections', 'new deaths'

    # header row
    for code in d_states_data.keys():
        # d_states_data is a dict of lists, first item is the header
        d_states_data[code] = [['# day', 'date',
                                'infections', 'deaths', 'new infections', 'new deaths',
                                'infections per million', 'deaths per million', 'new infections per million', 'new deaths per million',
                                'fitted_infection_doublication_time_last_7_days'
                                ]]

    # data body
    with open(download_file, mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        for row in csv_reader:
            # not needed as date already is in yyyy-mm-dd format
            # l = row["date"].split('-')
            # l = [int(v) for v in l]
            # datum = date_format(*l)

            this_infections = int(row["infections"])
            this_deaths = int(row["deaths"])
            if row["newinfections"] != "":
                this_newinfections = int(row["newinfections"])
            else:
                this_newinfections = 0
            if row["newdeaths"] != "":
                this_newdeaths = int(row["newdeaths"])
            else:
                this_newdeaths = 0

            l = [row["date"],
                 this_infections,
                 this_deaths,
                 this_newinfections,
                 this_newdeaths
                 ]

            if row["federalstate"] == 'Baden-Württemberg':
                d_states_data['BW'].append(helper_add_per_millions('BW', l))
            elif row["federalstate"] == 'Bavaria':
                d_states_data['BY'].append(helper_add_per_millions('BY', l))
            elif row["federalstate"] == 'Berlin':
                d_states_data['BE'].append(helper_add_per_millions('BE', l))
            elif row["federalstate"] == 'Brandenburg':
                d_states_data['BB'].append(helper_add_per_millions('BB', l))
            elif row["federalstate"] == 'Bremen':
                d_states_data['HB'].append(helper_add_per_millions('HB', l))
            elif row["federalstate"] == 'Hamburg':
                d_states_data['HH'].append(helper_add_per_millions('HH', l))
            elif row["federalstate"] == 'Hesse':
                d_states_data['HE'].append(helper_add_per_millions('HE', l))
            elif row["federalstate"] == 'Lower Saxony':
                d_states_data['NI'].append(helper_add_per_millions('NI', l))
            elif row["federalstate"] == 'North Rhine-Westphalia':
                d_states_data['NW'].append(helper_add_per_millions('NW', l))
            elif row["federalstate"] == 'Mecklenburg-Western Pomerania':
                d_states_data['MV'].append(helper_add_per_millions('MV', l))
            elif row["federalstate"] == 'Rhineland-Palatinate':
                d_states_data['RP'].append(helper_add_per_millions('RP', l))
            elif row["federalstate"] == 'Saarland':
                d_states_data['SL'].append(helper_add_per_millions('SL', l))
            elif row["federalstate"] == 'Saxony':
                d_states_data['SN'].append(helper_add_per_millions('SN', l))
            elif row["federalstate"] == 'Saxony-Anhalt':
                d_states_data['ST'].append(helper_add_per_millions('ST', l))
            elif row["federalstate"] == 'Schleswig-Holstein':
                d_states_data['SH'].append(helper_add_per_millions('SH', l))
            elif row["federalstate"] == 'Thuringia':
                d_states_data['TH'].append(helper_add_per_millions('TH', l))
            else:
                print("ERROR: unknown state")
                quit()
            del l

            # add to German sum

            if row["date"] not in d_german_sums:
                d_german_sums[row["date"]] = [this_infections,
                                              this_deaths, this_newinfections, this_newdeaths]
            else:
                l2 = d_german_sums[row["date"]]
                l2[0] += this_infections
                l2[1] += this_deaths
                l2[2] += this_newinfections
                l2[3] += this_newdeaths
                d_german_sums[row["date"]] = list(l2)
                del l2

    # for German sum: add per Million rows
    for datum in d_german_sums.keys():
        l2 = d_german_sums[datum]
        l3 = [datum, *l2]
        d_states_data['DE-total'].append(
            helper_add_per_millions('DE-total', l3))
    del l2, l3

    # write to export files
    for code in d_states_data.keys():
        # ensure sorting by date
        l_state = d_states_data[code]
        l_state = sorted(l_state, key=lambda x: x[0], reverse=False)

        # add counter of days
        day_num = 2-len(l_state)
        for i in range(1, len(l_state)):
            l_state[i].insert(0, day_num)
            day_num += 1

        # fit cases data
        data = []
        for i in range(1, len(l_state)):
            data.append((l_state[i][0], l_state[i][2]))  # x= day , y = cases

        # perform a series of fits: per day on data of 7 days back
        # pairs of (day, doublication_time) (fitted in range [x-6, x])
        fit_series_res = {}
        for last_day_for_fit in range(0, -14, -1):
            d = helper.fit_routine(
                data, (last_day_for_fit-6, last_day_for_fit))
            douplication_time = d['fit_res'][1]
            fit_series_res[last_day_for_fit] = douplication_time
        # add to export data
        for i in range(1, len(l_state)):
            this_doublication_time = ""
            this_days_past = l_state[i][0]
            if this_days_past in fit_series_res:
                this_doublication_time = "%.3f" % (
                    fit_series_res[this_days_past])
            l_state[i].append(this_doublication_time)

        # d = fit_routine(data, (-6, 0))
        # douplication_time = d['fit_res'[1]]
        # print(douplication_time)

        d_states_data[code] = l_state
        outfile = f'data/de-states/de-state-{code}.tsv'
        with open(outfile, 'w', newline="\n", encoding='utf-8') as f:
            csvwriter = csv.writer(f, delimiter="\t")
            csvwriter.writerows(d_states_data[code])
        del l_state, day_num, code

    # latest data into another file
    assert len(d_states_data.keys()) == len(d_states_ref.keys())
    for code in d_states_ref.keys():
        assert code in d_states_data.keys()
    del code

    d_states_latest = dict(d_states_ref)

    for code in d_states_latest.keys():
        assert code in d_states_data.keys()
        l_state = d_states_data[code]
        l_latest = l_state[-1]
        d_states_latest[code]['Latest Date'] = l_latest[1]
        d_states_latest[code]['Infections'] = l_latest[2]
        d_states_latest[code]['Deaths'] = l_latest[3]
        d_states_latest[code]['New Infections'] = l_latest[4]
        d_states_latest[code]['New Deaths'] = l_latest[5]
        d_states_latest[code]['Infections per Million'] = l_latest[6]
        d_states_latest[code]['Deaths per Million'] = l_latest[7]
    with open('data/de-states/de-states-latest.tsv', 'w', newline="\n", encoding='utf-8') as f:
        csvwriter = csv.writer(f, delimiter="\t")
        csvwriter.writerow(
            ('# State', 'Code', 'Population', 'Pop Density', 'Date', 'Infections', 'Deaths', 'New Infections', 'New Deaths',
             'Infections per Million', 'Deaths per Million')
        )
        for code in sorted(d_states_latest.keys()):
            d = d_states_latest[code]
            l = (d['State'], code, d['Population'], d['Pop Density'], d['Latest Date'], d['Infections'], d['Deaths'],
                 d['New Infections'], d['New Deaths'], "%.3f" % (d['Infections per Million']), "%.3f" % (d['Deaths per Million']))
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


d_states_ref = read_ref_data()

# TODO
download_new_data()

convert_csv()

1
