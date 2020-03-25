#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/pomber/covid19

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

download_file = 'data/download-countries-timeseries.json'


def download_new_data():
    url = "https://pomber.github.io/covid19/timeseries.json"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(download_file, 'wb') as f:
        f.write(datatowrite)


def date_format(y: int, m: int, d: int) -> str:
    # return "%02d.%02d.%04d" % (d, m, y)
    # TODO
    return "%04d-%02d-%02d" % (y, m, d)


def read_json_data() -> dict:
    "reads json file contents and returns it as a dict"
    with open(download_file, encoding='utf-8') as f:
        d = json.load(f)
    # re-format date using my date_format(y,m,d) function
    for country in d.keys():
        country_data = d[country]
        for i in range(len(country_data)):
            entry = country_data[i]
            # entry in country_data:
            date = entry['date']
            l = date.split("-")
            entry['date'] = date_format(int(l[0]), int(l[1]), int(l[2]))
            country_data[i] = entry
        d[country] = country_data
    return d


def read_ref_selected_countries() -> dict:
    "reads data for selected countries from tsv file and returns it as dict"
    d_countries = {}
    with open('data/ref_selected_countries.tsv', mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, dialect='excel', delimiter="\t")
        for row in csv_reader:
            if row["Country"][0] == '#':
                continue
            d = {}
            for key in ('Code',):
                d[key] = row[key]
            for key in ('Population',):
                d[key] = int(row[key])
            for key in ('Pop_Density', 'GDP_mon_capita'):
                d[key] = float(row[key])
            d_countries[row["Country"]] = d
    return d_countries


def extract_latest_date_data():
    """
    for all countries in json: extract latest entry
    writes to data/countries-latest-all.tsv
    """
    with open('data/countries-latest-all.tsv', 'w', newline="\n") as f:
        csvwriter = csv.writer(f, delimiter="\t")
        csvwriter.writerow(  # header row
            ('# Country', 'Date', 'Confirmed', 'Deaths')  # , 'Recovered'
        )
        for country in sorted(d_json_data.keys(), key=str.casefold):
            country_data = d_json_data[country]
            entry = country_data[-1]  # last entry (=>latest date)
            csvwriter.writerow(
                (country, entry['date'], entry['confirmed'],
                 entry['deaths'])  # , entry['recovered']
            )


def extract_latest_date_data_selected():
    """
    for my selected countries: extract latest of json and calculate per capita values
    writes to data/countries-latest-selected.tsv
    """
    with open('data/countries-latest-selected.tsv', 'w', newline="\n") as f:
        csvwriter = csv.writer(f, delimiter="\t")
        csvwriter.writerow(
            ('# Country', 'Date', 'Confirmed', 'Deaths',
             'Confirmed per Million', 'Deaths per Million')
            # , 'Recovered'
            # , 'Recovered per Million'
        )
        for country in sorted(d_selected_countries.keys(), key=str.casefold):
            country_data = d_json_data[country]
            entry = country_data[-1]  # last entry per
            pop_in_Mill = d_selected_countries[country]['Population'] / 1000000
            csvwriter.writerow(
                (country, entry['date'], entry['confirmed'],
                 entry['deaths'], "%.3f" % (entry['confirmed']/pop_in_Mill), "%.3f" % (entry['deaths']/pop_in_Mill))
                # entry['recovered'],
                # , "%.3f" % (entry['recovered']/pop_in_Mill)
            )


def check_for_further_interesting_countries():
    """
    checks if in the json date are contries with many deaths that are missing in my selection for close analysis
    """
    global d_json_data
    global d_selected_countries
    min_death = 10
    min_confirmed = 1000
    print("further interesting countries")
    print("Country\tConfirmed\tDeaths")
#    list_of_countries = sorted(d_json_data.keys(), key=str.casefold)
    for country in sorted(d_json_data.keys(), key=str.casefold):
        if country in d_selected_countries.keys():
            continue
        country_data = d_json_data[country]
        entry = country_data[-1]  # latest entry
        if entry['confirmed'] >= min_confirmed or entry['deaths'] >= min_death:
            print(f"{country}\t{entry['confirmed']}\t{entry['deaths']}")


def export_time_series_selected_countries():
    for country in d_selected_countries.keys():
        country_code = d_selected_countries[country]['Code']
        country_data = d_json_data[country]
        pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        with open(f'data/country-{country_code}.tsv', 'w', newline="\n") as f:
            csvwriter = csv.writer(f, delimiter="\t")
            csvwriter.writerow(  # header row
                ('# Day', 'Date', 'Confirmed', 'Deaths',
                 'Confirmed per Million', 'Deaths per Million',
                 'Confirmed Change', 'Deaths Change',
                 'Deaths Change Factor',
                 'Days since 2 Deaths'
                 )
            )
            i = 1-len(country_data)  # last date gets number 0
            last_confirmed = 0
            last_deaths = 0
            change_confirmed = ""
            change_deaths = ""
            change_deaths_factor = ""
            days_since_2_deaths = ""
            for entry in country_data:
                if entry['deaths'] >= 2:  # TODO: is 2 a good value?
                    if days_since_2_deaths == "":
                        days_since_2_deaths = 0
                    else:
                        days_since_2_deaths += 1
                if last_deaths >= 1:  # TODO: later increase to 10
                    change_confirmed = entry['confirmed'] - last_confirmed
                    change_deaths = entry['deaths'] - last_deaths
                    change_deaths_factor = "%.3f" % (
                        entry['deaths']/last_deaths)
                csvwriter.writerow(
                    (
                        i, entry['date'],
                        entry['confirmed'], entry['deaths'],
                        "%.3f" % (entry['confirmed']/pop_in_Mill), "%.3f" % (
                            entry['deaths']/pop_in_Mill),
                        change_confirmed, change_deaths,
                        change_deaths_factor,
                        days_since_2_deaths
                    )
                )
                last_confirmed = entry['confirmed']
                last_deaths = entry['deaths']
                i += 1


# TODO: uncomment once a day
# download_new_data()

d_selected_countries = read_ref_selected_countries()

d_json_data = read_json_data()

check_for_further_interesting_countries()

extract_latest_date_data()

extract_latest_date_data_selected()

export_time_series_selected_countries()

print("countries: latest date in DE set: " +
      d_json_data['Germany'][-1]['date'])


# IDEAS

# DONE
# for selected countries write into csv: all 3 data per capita
# am I missing further intersting countries ?
# export time series for interesting countries to files
