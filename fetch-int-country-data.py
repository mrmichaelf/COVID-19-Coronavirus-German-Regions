#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/pomber/covid19


"""


# Built-in/Generic Imports

import time
import json
import urllib.request
import csv


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

args = helper.read_command_line_parameters()
file_cache = 'cache/int/countries-timeseries.json'
file_all_timeseries = 'data/download-countries-timeseries.json'


def download_new_data():
    """
    downloads the data from the source to the cache dir
    """
    # TODO: caching
    url = "https://pomber.github.io/covid19/timeseries.json"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(file_cache, mode='wb') as f:
        f.write(datatowrite)

def read_json_data() -> dict:
    """
    reads downloaded cached json file contents
    renames some country names according to ref database
    adds _Per_Million fields
    exports as json file
    returns as a dict
    """
    d_json_downloaded = helper.read_json_file(file_cache)
    
    # rename some countries
    d_countries_to_rename = {}
    d_countries_to_rename['US'] = 'United States'
    d_countries_to_rename['Korea, South'] = 'South Korea'
    d_countries_to_rename['Taiwan*'] = 'Taiwan'
    d_countries_to_rename['Burma'] = 'Myanmar'
    d_countries_to_rename['Cote d\'Ivoire'] = 'Ivory Coast'
    for country_name in d_json_downloaded.keys():
        if country_name in d_countries_to_rename:
            d_json_downloaded[d_countries_to_rename[country_name]] = d_json_downloaded[country_name]
            del d_json_downloaded[country_name]

    d_countries = {}
    # re-format date using my date_format(y,m,d) function
    for country in d_json_downloaded.keys():
        country_data = d_json_downloaded[country]
        l_time_series = []

        pop = fetch_population(country)

        for entry in country_data:
            d = {}
            # entry in country_data:
            s = entry['date']
            l = s.split("-")
            d['Date'] = helper.date_format(int(l[0]), int(l[1]), int(l[2]))
            d['Cases'] = int(entry['confirmed'])
            d['Deaths'] = int(entry['deaths'])
            d['Cases_Per_Million'] = None
            d['Deaths_Per_Million'] = None
            if pop != None:
                d['Cases_Per_Million'] = round(d['Cases'] / pop * 1000000,3)
                d['Deaths_Per_Million'] = round(d['Deaths'] / pop * 1000000,3)
            l_time_series.append(d)

        # ensure sorting by date
        l_time_series = sorted(
            l_time_series, key=lambda x: x['Date'], reverse=False)

        d_countries[country] = l_time_series

    # export to file
    helper.write_json(file_all_timeseries, d_countries, sort_keys=True)
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
            ('# Country', 'Population', 'Date', 'Cases', 'Deaths', 'Cases_Per_Million', 'Deaths_Per_Million')
        )
        for country in sorted(d_countries_timeseries.keys(), key=str.casefold):
            country_data = d_countries_timeseries[country]
            entry = country_data[-1]  # last entry (=>latest date)
            pop = fetch_population(country)

            csvwriter.writerow(
                (
                country, pop, entry['Date'], 
                entry['Cases'], entry['Deaths'],
                entry['Cases_Per_Million'], entry['Deaths_Per_Million']
                 )
            )


def extract_latest_date_data_selected():
    """
    TODO: this is now the same as extract_latest_date_data()
    for my selected countries: extract latest of json and calculate per capita values
    writes to data/countries-latest-selected.tsv
    """
    with open('data/int/countries-latest-selected.tsv', mode='w', encoding='utf-8', newline='\n') as f:
        csvwriter = csv.writer(f, delimiter="\t")
        # TODO: change order: pop as no 3
        csvwriter.writerow(
            ('# Country', 'Date',
             'Confirmed', 'Deaths',
             'Confirmed per Million', 'Deaths per Million',
             'Population'
             )
        )
        for country in sorted(d_selected_countries.keys(), key=str.casefold):
            country_data = d_countries_timeseries[country]
            entry = country_data[-1]  # last entry for this country
            pop_in_Mill = d_selected_countries[country]['Population'] / 1000000
            csvwriter.writerow(
                (country, entry['Date'], 
                entry['Cases'], entry['Deaths'], 
                "%.3f" % (entry['Cases']/pop_in_Mill), "%.3f" % (entry['Deaths']/pop_in_Mill),
                d_selected_countries[country]['Population'])
            )


def check_for_further_interesting_countries():
    """
    checks if in the json data are countries with many deaths that are missing in my selection for closer analysis
    """
    global d_countries_timeseries
    global d_selected_countries
    min_death = 10
    min_confirmed = 1000
    min_death_per_million = 100
    print("further interesting countries")
    print("Country\tConfirmed\tDeaths\tDeathsPerMillion")
#    list_of_countries = sorted(d_countries_timeseries.keys(), key=str.casefold)
    for country in sorted(d_countries_timeseries.keys(), key=str.casefold):
        if country in d_selected_countries.keys():
            continue
        l_country_data = d_countries_timeseries[country]
        entry = l_country_data[-1]  # latest entry
        # if entry['Cases'] >= min_confirmed or entry['Deaths'] >= min_death:
        if entry['Deaths_Per_Million'] and entry['Deaths_Per_Million'] >= min_death_per_million:
            print(f"{country}\t{entry['Cases']}\t{entry['Deaths']}\t{int(entry['Deaths_Per_Million'])}")

            
def enrich_data_by_calculated_fields():
    global d_countries_timeseries
    global d_selected_countries
    for country in d_selected_countries.keys():
        # print(country)
        # country_code = d_selected_countries[country]['Code']
        l_country_data = d_countries_timeseries[country]
        # pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        # initial values
        last_cases = 0
        last_deaths = 0
        days_since_2_deaths = 0
        # for fits of doubling time
        data_t = []
        data_cases = []
        data_deaths = []

        DaysPast = 1-len(l_country_data)  # last date gets number 0
        last_cases = 0
        last_deaths = 0

        for i in range(len(l_country_data)):
            entry = l_country_data[i]

            entry['Days_Past'] = DaysPast
            data_t.append(entry['Days_Past'])
            DaysPast += 1

            # for fits of doubling time
            data_cases.append(entry['Cases'])
            data_deaths.append(entry['Deaths'])

            # days_since_2_deaths
            entry['Days_Since_2_Deaths'] = ""
            if entry['Deaths'] >= 2:  # TODO: is 2 a good value?
                entry['Days_Since_2_Deaths'] = days_since_2_deaths
                days_since_2_deaths += 1

            entry['Cases_New'] = entry['Cases'] - last_cases
            entry['Deaths_New'] = entry['Deaths'] - last_deaths

            entry['Cases_Change_Factor'] = ""
            if last_cases >= 100:
                entry['Cases_Change_Factor'] = round(
                    entry['Cases']/last_cases, 3)
            entry['Deaths_Change_Factor'] = ""
            if last_deaths >= 10:
                entry['Deaths_Change_Factor'] = round(
                    entry['Deaths']/last_deaths, 3)

            last_cases = entry['Cases']
            last_deaths = entry['Deaths']

            # add per Million rows
            entry = helper.add_per_million(
                d_selected_countries, country, entry)

            l_country_data[i] = entry

        # fit the doubling time each day
        data = list(zip(data_t, data_cases))
        fit_series_res_cases = helper.series_of_fits(
            data, fit_range=7, max_days_past=28)
        data = list(zip(data_t, data_deaths))
        fit_series_res_deaths = helper.series_of_fits(
            data, fit_range=7, max_days_past=28)

        for i in range(len(l_country_data)):
            entry = l_country_data[i]
            this_cases_doubling_time = ""
            this_deaths_doubling_time = ""
            this_DaysPast = entry['Days_Past']
            if this_DaysPast in fit_series_res_cases:
                this_cases_doubling_time = fit_series_res_cases[this_DaysPast]
            if this_DaysPast in fit_series_res_deaths:
                this_deaths_doubling_time = fit_series_res_deaths[this_DaysPast]
            entry['Cases_Doubling_Time'] = this_cases_doubling_time
            entry['Deaths_Doubling_Time'] = this_deaths_doubling_time
            l_country_data[i] = entry

        if args["sleep"]:
            time.sleep(1)


def export_time_series_selected_countries():
    for country in d_selected_countries.keys():
        country_code = d_selected_countries[country]['Code']
        l_country_data = d_countries_timeseries[country]
        #     pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        helper.write_json(f'data/int/country-{country_code}.json', l_country_data)

        with open(f'data/int/country-{country_code}.tsv', mode='w', encoding='utf-8', newline='\n') as f:
            csvwriter = csv.writer(f, delimiter="\t")
            csvwriter.writerow(  # header row
                ('# Day', 'Date',
                 'Cases', 'Deaths',
                 'Cases_New', 'Deaths_New',
                 'Cases_Per_Million', 'Deaths_Per_Million',
                 'Cases_New_Per_Million', 'Deaths_New_Per_Million',
                 'Cases_Doubling_Time', 'Deaths_Doubling_Time',
                 'Cases_Change_Factor', 'Deaths_Change_Factor',
                 'Days_Since_2_Deaths'
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
                        entry['Cases_Doubling_Time'], entry['Deaths_Doubling_Time'],
                        entry['Cases_Change_Factor'], entry['Deaths_Change_Factor'],
                        entry['Days_Since_2_Deaths']
                    )
                )



def test():
    d_ref_country_database = helper.read_json_file('data/ref_country_database.json')

    d_country_covid_time_series = helper.read_json_file('data/download-countries-timeseries.json')

    for country_name in d_country_covid_time_series.keys():
        pop = None
        # TODO: do this mapping in other file?
        if country_name == 'Congo (Brazzaville)':
            pop = d_ref_country_database['Republic of the Congo']['Population']
        if country_name == 'Congo (Kinshasa)':
            pop = d_ref_country_database['Democratic Republic of the Congo']['Population']

        if pop == None:
            for ref_country_name in d_ref_country_database.keys():
                if country_name == ref_country_name:
                    pop = d_ref_country_database[country_name]['Population']

        if pop == None:
            print (f"not found: {country_name}")

def fetch_population(country_name:str, verbose:bool=False) -> int:
    global d_ref_country_database
    pop = None
    if country_name == 'Congo (Brazzaville)':
        pop = d_ref_country_database['Republic of the Congo']['Population']
    if country_name == 'Congo (Kinshasa)':
        pop = d_ref_country_database['Democratic Republic of the Congo']['Population']

    if pop == None:
        for ref_country_name in d_ref_country_database.keys():
            if country_name == ref_country_name:
                pop = d_ref_country_database[country_name]['Population']
    if pop != None: pop = int(pop)
    if pop == 0: pop = None
    if verbose and pop == None : 
        print (f"No Population found for {country_name}")
    return pop



d_ref_country_database = helper.read_json_file('data/ref_country_database.json')

if not helper.check_cache_file_available_and_recent(fname=file_cache, max_age=7200, verbose=True) :
    download_new_data()

d_selected_countries = read_ref_selected_countries()

d_countries_timeseries = read_json_data()



check_for_further_interesting_countries()

extract_latest_date_data()

extract_latest_date_data_selected()

enrich_data_by_calculated_fields()

export_time_series_selected_countries()

print(
    f"int: countries: latest date in DE set: {d_countries_timeseries['Germany'][-1]['Date']}")


# IDEAS

# DONE
# for selected countries write into csv: all 3 data per capita
# am I missing further intersting countries ?
# export time series for interesting countries to files
