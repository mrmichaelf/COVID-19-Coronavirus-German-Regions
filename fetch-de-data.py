#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/swildermann/COVID-19

"""

import json
import urllib.request
import csv

# Built-in/Generic Imports

# Author and version info
__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__maintainer__ = __author__
# __copyright__ = "Copyright 2020, My Project"
# __credits__ = ["John", "Jim", "Jack"]
__license__ = "GPL"
__status__ = "Dev"
__version__ = "0.1"


download_file = 'data/download-de-federalstates-timeseries.csv'


def download_new_data():
    url = "https://covid19publicdata.blob.core.windows.net/rki/covid19-germany-federalstates.csv"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(download_file, 'wb') as f:
        f.write(datatowrite)


def date_format(y: int, m: int, d: int) -> str:
    # return "%02d.%02d.%04d" % (d, m, y)
    # besser, weil sortierbar
    return "%04d-%02d-%02d" % (y, m, d)


# IDEA:
# def translate_name_to_german(name:str) -> str:
#     d =
#     Baden-Württemberg
# # Bavaria
# # Berlin
# # Brandenburg
# # Bremen
# # Hamburg
# # Hesse
# # Lower Saxony
# # Mecklenburg-Western Pomerania
# # North Rhine-Westphalia
# # Rhineland-Palatinate
# # Saarland
# # Saxony
# # Saxony-Anhalt
# # Schleswig-Holstein
# # Thuringia


def convert_csv():
    """
    read and convert the source csv file: federalstate,infections,deaths,date,newinfections,newdeaths
    out: one file per state: 'date', 'infections', 'deaths', 'new infections', 'new deaths'
    """
    d = {'BW': [], 'BY': [], 'BE': [], 'BB': [], 'HB': [], 'HH': [], 'HE': [], 'MV': [
    ], 'NI': [], 'NW': [], 'RP': [], 'SL': [], 'SN': [], 'ST': [], 'SH': [], 'TH': []}
    # add German sum
    d['DE-total'] = []

    d_german_sums = {}  # date -> 'infections', 'deaths', 'new infections', 'new deaths'
    for key in d.keys():
        d[key] = [['# date', 'infections', 'deaths', 'new infections', 'new deaths']]
    with open(download_file, mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        for row in csv_reader:
            # not needed as date already is in yyyy-mm-dd format
            # l = row["date"].split('-')
            # l = [int(v) for v in l]
            # datum = date_format(*l)
            l = [row["date"], row["infections"], row["deaths"],
                 row["newinfections"], row["newdeaths"]]
            if row["federalstate"] == 'Baden-Württemberg':
                d['BW'].append(l)
            if row["federalstate"] == 'Bavaria':
                d['BY'].append(l)
            if row["federalstate"] == 'Berlin':
                d['BE'].append(l)
            if row["federalstate"] == 'Brandenburg':
                d['BB'].append(l)
            if row["federalstate"] == 'Bremen':
                d['HB'].append(l)
            if row["federalstate"] == 'Hamburg':
                d['HH'].append(l)
            if row["federalstate"] == 'Hesse':
                d['HE'].append(l)
            if row["federalstate"] == 'Lower Saxony':
                d['NI'].append(l)
            if row["federalstate"] == 'North Rhine-Westphalia':
                d['NW'].append(l)
            if row["federalstate"] == 'Mecklenburg-Western Pomerania':
                d['MV'].append(l)
            if row["federalstate"] == 'Rhineland-Palatinate':
                d['RP'].append(l)
            if row["federalstate"] == 'Saarland':
                d['SL'].append(l)
            if row["federalstate"] == 'Saxony':
                d['SN'].append(l)
            if row["federalstate"] == 'Saxony-Anhalt':
                d['ST'].append(l)
            if row["federalstate"] == 'Schleswig-Holstein':
                d['SH'].append(l)
            if row["federalstate"] == 'Thuringia':
                d['TH'].append(l)

            # add to German sum
            this_infections = int(row["infections"])
            this_deaths = int(row["deaths"])
            # set "" values 0
            this_newinfections = 0
            if row["newinfections"] != "":
                this_newinfections = int(row["newinfections"])
            this_newdeaths = 0
            if row["newdeaths"] != "":
                this_newdeaths = int(row["newdeaths"])

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
    for key in d_german_sums.keys():
        l3 = [key, *d_german_sums[key]]
        d['DE-total'].append(list(l3))
    for key in d.keys():
        # ensure sorting by date
        l = d[key]
        l = sorted(l, key=lambda x: x[0], reverse=False)
        d[key] = l
        outfile = f'data/cases-de-V2-{key}.tsv'
        with open(outfile, 'w') as f:
            csvwriter = csv.writer(f, delimiter="\t")
            csvwriter.writerows(d[key])


# download_new_data()
convert_csv()

1
1
