#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/pomber/covid19


"""
# TODO: add 7 day fit of doublication time


import json
import urllib.request
import csv

# Built-in/Generic Imports

import helper

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
    # TODO: caching
    url = "https://pomber.github.io/covid19/timeseries.json"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(download_file, mode='wb') as f:
        f.write(datatowrite)


def read_json_data() -> dict:
    "reads json file contents and returns it as a dict"
    with open(download_file, mode='r', encoding='utf-8') as f:
        d_json_downloaded = json.load(f)
    d_countries = {}
    # re-format date using my date_format(y,m,d) function
    for country in d_json_downloaded.keys():
        country_data = d_json_downloaded[country]
        l_time_series = []
        for entry in country_data:
            d = {}
            # entry in country_data:
            s = entry['date']
            l = s.split("-")
            d['Date'] = helper.date_format(int(l[0]), int(l[1]), int(l[2]))
            d['Cases'] = int(entry['confirmed'])
            d['Deaths'] = int(entry['deaths'])
            l_time_series.append(d)

        d_countries[country] = l_time_series
    return d_countries


def read_ref_selected_countries() -> dict:
    "reads data for selected countries from tsv file and returns it as dict"
    d_selected_countries = {}
    with open('data/ref_selected_countries.tsv', mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, dialect='excel', delimiter="\t")
        for row in csv_reader:
            # skip commented lines
            if row["Country"][0] == '#':
                continue
            d = {}
            for key in ('Code',):
                d[key] = row[key]
            for key in ('Population',):
                d[key] = int(row[key])
            for key in ('Pop_Density', 'GDP_mon_capita'):
                d[key] = float(row[key])
            d_selected_countries[row["Country"]] = d
    return d_selected_countries


def extract_latest_date_data():
    """
    for all countries in json: extract latest entry
    write to data/countries-latest-all.tsv
    """
    with open('data/int/countries-latest-all.tsv', mode='w', encoding='utf-8', newline='\n') as f:
        csvwriter = csv.writer(f, delimiter="\t")
        csvwriter.writerow(  # header row
            ('# Country', 'Date', 'Confirmed', 'Deaths')  # , 'Recovered'
        )
        for country in sorted(d_json_data.keys(), key=str.casefold):
            country_data = d_json_data[country]
            entry = country_data[-1]  # last entry (=>latest date)
            csvwriter.writerow(
                (country, entry['Date'], entry['Cases'],
                 entry['Deaths'])  # , entry['recovered']
            )


def extract_latest_date_data_selected():
    """
    for my selected countries: extract latest of json and calculate per capita values
    writes to data/countries-latest-selected.tsv
    """
    with open('data/int/countries-latest-selected.tsv', mode='w', encoding='utf-8', newline='\n') as f:
        csvwriter = csv.writer(f, delimiter="\t")
        csvwriter.writerow(
            ('# Country', 'Date',
             'Confirmed', 'Deaths',
             'Confirmed per Million', 'Deaths per Million')
        )
        for country in sorted(d_selected_countries.keys(), key=str.casefold):
            country_data = d_json_data[country]
            entry = country_data[-1]  # last entry of this country
            pop_in_Mill = d_selected_countries[country]['Population'] / 1000000
            csvwriter.writerow(
                (country, entry['Date'], entry['Cases'],
                 entry['Deaths'], "%.3f" % (entry['Cases']/pop_in_Mill), "%.3f" % (entry['Deaths']/pop_in_Mill))
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
        l_country_data = d_json_data[country]
        entry = l_country_data[-1]  # latest entry
        if entry['Cases'] >= min_confirmed or entry['Deaths'] >= min_death:
            print(f"{country}\t{entry['Cases']}\t{entry['Deaths']}")


def enrich_data_by_calculated_fields():
    global d_json_data
    global d_selected_countries
    for country in d_selected_countries.keys():
        # print(country)
        country_code = d_selected_countries[country]['Code']
        l_country_data = d_json_data[country]
        pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        # initial values
        last_confirmed = 0
        last_deaths = 0
        days_since_2_deaths = 0
        # for fits of doublication time
        data_t = []
        data_cases = []
        data_deaths = []

        DaysPast = 1-len(l_country_data)  # last date gets number 0
        last_confirmed = 0
        last_deaths = 0

        for i in range(len(l_country_data)):
            entry = l_country_data[i]

            entry['Days_Past'] = DaysPast
            data_t.append(entry['Days_Past'])
            DaysPast += 1

            # for fits of doublication time
            data_cases.append(entry['Cases'])
            data_deaths.append(entry['Deaths'])

            # days_since_2_deaths
            entry['Days_Since_2_Deaths'] = ""
            if entry['Deaths'] >= 2:  # TODO: is 2 a good value?
                entry['Days_Since_2_Deaths'] = days_since_2_deaths
                days_since_2_deaths += 1

            entry['Cases_New'] = entry['Cases'] - last_confirmed
            entry['Deaths_New'] = entry['Deaths'] - last_deaths

            entry['change_deaths_factor'] = ""
            if last_deaths >= 1:
                entry['change_deaths_factor'] = round(
                    entry['Deaths']/last_deaths, 3)

            last_confirmed = entry['Cases']
            last_deaths = entry['Deaths']

            # add per Million rows
            entry = helper.add_per_million(
                d_selected_countries, country, entry)

            l_country_data[i] = entry

        # fit the doublication time each day
        data = list(zip(data_t, data_deaths))
        fit_series_res = helper.series_of_fits(
            data, fit_range=7, max_days_past=28)

        for i in range(len(l_country_data)):
            entry = l_country_data[i]
            this_doublication_time = ""
            this_DaysPast = entry['Days_Past']
            if this_DaysPast in fit_series_res:
                this_doublication_time = fit_series_res[this_DaysPast]
            entry['Doublication_Time'] = this_doublication_time
            l_country_data[i] = entry


def export_time_series_selected_countries():
    for country in d_selected_countries.keys():
        country_code = d_selected_countries[country]['Code']
        l_country_data = d_json_data[country]
        #     pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        with open(f'data/int/country-{country_code}.json', mode='w', encoding='utf-8', newline='\n') as fh:
            json.dump(l_country_data, fh, ensure_ascii=False)

        with open(f'data/int/country-{country_code}.tsv', mode='w', encoding='utf-8', newline='\n') as f:
            csvwriter = csv.writer(f, delimiter="\t")
            csvwriter.writerow(  # header row
                ('# Day', 'Date',
                 'Cases', 'Deaths',
                 'Cases_New', 'Deaths_New',
                 'Cases_Per_Million', 'Deaths_Per_Million',
                 'Cases_New_Per_Million', 'Deaths_New_Per_Million',
                 'Deaths Doublication Time',
                 'Days since 2 Deaths',
                 'Deaths Change Factor'
                 )
            )
            for entry in l_country_data:
                csvwriter.writerow(
                    (
                        entry['Days_Past'], entry['Date'],
                        entry['Cases'], entry['Deaths'],
                        entry['Cases_New'], entry['Deaths_New'],
                        entry['Cases_Per_Million'], entry['Deaths_Per_Million'],
                        entry['Cases_New_Per_Million'], entry['Deaths_New_Per_Million'],
                        entry['Doublication_Time'],
                        entry['Days_Since_2_Deaths'],
                        entry['change_deaths_factor']
                    )
                )


# TODO: uncomment once a day
# download_new_data()

d_selected_countries = read_ref_selected_countries()

d_json_data = read_json_data()

check_for_further_interesting_countries()

extract_latest_date_data()

extract_latest_date_data_selected()

enrich_data_by_calculated_fields()

export_time_series_selected_countries()

print(
    f"int: countries: latest date in DE set: {d_json_data['Germany'][-1]['Date']}")


# IDEAS

# DONE
# for selected countries write into csv: all 3 data per capita
# am I missing further intersting countries ?
# export time series for interesting countries to files
