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


def convert_csv():
    """
    read and convert the source csv file: federalstate,infections,deaths,date,newinfections,newdeaths
    out: one file per state: 'date', 'infections', 'deaths', 'new infections', 'new deaths'
    """
    d_states_data = {'BW': [], 'BY': [], 'BE': [], 'BB': [], 'HB': [], 'HH': [], 'HE': [], 'MV': [
    ], 'NI': [], 'NW': [], 'RP': [], 'SL': [], 'SN': [], 'ST': [], 'SH': [], 'TH': []}
    # add German sum
    d_states_data['DE-total'] = []

    d_german_sums = {}  # date -> 'infections', 'deaths', 'new infections', 'new deaths'
    for code in d_states_data.keys():
        d_states_data[code] = [['#', 'date', 'infections',
                                'deaths', 'new infections', 'new deaths']]
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
                d_states_data['BW'].append(l)
            if row["federalstate"] == 'Bavaria':
                d_states_data['BY'].append(l)
            if row["federalstate"] == 'Berlin':
                d_states_data['BE'].append(l)
            if row["federalstate"] == 'Brandenburg':
                d_states_data['BB'].append(l)
            if row["federalstate"] == 'Bremen':
                d_states_data['HB'].append(l)
            if row["federalstate"] == 'Hamburg':
                d_states_data['HH'].append(l)
            if row["federalstate"] == 'Hesse':
                d_states_data['HE'].append(l)
            if row["federalstate"] == 'Lower Saxony':
                d_states_data['NI'].append(l)
            if row["federalstate"] == 'North Rhine-Westphalia':
                d_states_data['NW'].append(l)
            if row["federalstate"] == 'Mecklenburg-Western Pomerania':
                d_states_data['MV'].append(l)
            if row["federalstate"] == 'Rhineland-Palatinate':
                d_states_data['RP'].append(l)
            if row["federalstate"] == 'Saarland':
                d_states_data['SL'].append(l)
            if row["federalstate"] == 'Saxony':
                d_states_data['SN'].append(l)
            if row["federalstate"] == 'Saxony-Anhalt':
                d_states_data['ST'].append(l)
            if row["federalstate"] == 'Schleswig-Holstein':
                d_states_data['SH'].append(l)
            if row["federalstate"] == 'Thuringia':
                d_states_data['TH'].append(l)

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
    for code in d_german_sums.keys():
        l3 = [code, *d_german_sums[code]]
        d_states_data['DE-total'].append(list(l3))

    for code in d_states_data.keys():
        # ensure sorting by date
        l_state = d_states_data[code]
        l_state = sorted(l_state, key=lambda x: x[0], reverse=False)

        # add counter of days
        day_num = 2-len(l_state)
        for i in range(1, len(l_state)):
            l_state[i].insert(0, day_num)
            day_num += 1

        d_states_data[code] = l_state
        outfile = f'data/de-state-{code}.tsv'
        with open(outfile, 'w') as f:
            csvwriter = csv.writer(f, delimiter="\t")
            csvwriter.writerows(d_states_data[code])

    # now let's extract the latest data and scale by pop
    d_states_ref = {}
    with open('data/ref_de-states.tsv', mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter="\t")
        for row in csv_reader:
            d = {}
            d['State'] = row['State']
            d['Population'] = int(row['Population'])
            d['Pop Density'] = float(row['Pop Density'])
            d_states_ref[row["Code"]] = d

    assert len(d_states_data.keys()) == len(d_states_ref.keys())
    for code in d_states_ref:
        assert code in d_states_data.keys()

    d_states_latest = dict(d_states_ref)

    for code in d_states_latest.keys():
        assert code in d_states_data.keys()
        l_state = d_states_data[code]
        l_latest = l_state[-1]
        d_states_latest[code]['Latest Date'] = l_latest[1]
        d_states_latest[code]['Infections'] = int(l_latest[2])
        d_states_latest[code]['Deaths'] = int(l_latest[3])
        d_states_latest[code]['New Infections'] = int(l_latest[4])
        d_states_latest[code]['New Deaths'] = int(l_latest[5])
        d_states_latest[code]['Infections per Million'] = d_states_latest[code]['Infections'] / \
            d_states_latest[code]['Population'] * 1000000
        d_states_latest[code]['Deaths per Million'] = d_states_latest[code]['Deaths'] / \
            d_states_latest[code]['Population'] * 1000000
    with open('data/de-states-latest.tsv', 'w') as f:
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
        l_de[0] = '# Deutschland'
        csvwriter.writerow(
            l_de
        )

#         1


# def extract_latest_date_and_scale_by_pop():
#     """
#     extract latest of json and calculate per capita values
#     writes to data/countries-latest-selected.tsv
#     """
#     with open('data/countries-latest-selected.tsv', 'w') as f:
#         csvwriter = csv.writer(f, delimiter="\t")
#         csvwriter.writerow(
#             ('# Country', 'Date', 'Confirmed', 'Deaths', 'Recovered',
#              'Confirmed per Million', 'Deaths per Million', 'Recovered per Million')
#         )
#         for country in sorted(d_selected_countries.keys(), key=str.casefold):
#             country_data = d_json_data[country]
#             entry = country_data[-1]  # last entry per
#             pop_in_Mill = d_selected_countries[country]['Population'] / 1000000
#             csvwriter.writerow(
#                 (country, entry['date'], entry['confirmed'],
#                  entry['deaths'], entry['recovered'], "%.3f" % (entry['confirmed']/pop_in_Mill), "%.3f" % (entry['deaths']/pop_in_Mill), "%.3f" % (entry['recovered']/pop_in_Mill))
#             )


download_new_data()
convert_csv()

1
1
