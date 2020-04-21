#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/pomber/covid19

Data is enriched by calculated values and exported
"""


# Built-in/Generic Imports

import time
import urllib.request
import csv

# further modules
# process bar
from tqdm import tqdm

# my helper modules
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
file_cache = 'data/download-countries-timeseries.json'


def download_new_data():
    """
    downloads the data from the source to the cache dir
    """
    url = "https://pomber.github.io/covid19/timeseries.json"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(file_cache, mode='wb') as f:
        f.write(datatowrite)


def read_json_data() -> dict:
    """
    reads downloaded cached json file contents
    renames some country names according to ref database
    calls prepare_time_series
    adds _Per_Million fields
    NO LONGER exports as json file
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
    d_countries_to_rename['West Bank and Gaza'] = 'Palestinian Territory'
    d_countries_to_rename['Timor-Leste'] = 'Timor Leste'
    d_countries_to_rename['Holy See'] = 'Vatican'
    for country_name_old, country_name_new in d_countries_to_rename.items():
        d_json_downloaded[country_name_new] = d_json_downloaded[country_name_old]
        del d_json_downloaded[country_name_old]

    d_countries = {}
    # re-format date using my date_format(y,m,d) function
    for country in d_json_downloaded.keys():
        country_data = d_json_downloaded[country]
        l_time_series = []

        pop = read_population(country)
        if pop != None:
            pop_in_million = pop / 1000000
        else:
            pop_in_million = None

        for entry in country_data:
            d = {}
            # entry in country_data:
            s = entry['date']
            l = s.split("-")
            d['Date'] = helper.date_format(int(l[0]), int(l[1]), int(l[2]))
            d['Cases'] = int(entry['confirmed'])
            d['Deaths'] = int(entry['deaths'])
            l_time_series.append(d)

        l_time_series = helper.prepare_time_series(l_time_series)

        for i in range(len(l_time_series)):
            d = l_time_series[i]

            # _Per_Million
            d = helper.add_per_million(d, pop_in_million)

        d_countries[country] = l_time_series

    return d_countries


def read_ref_selected_countries() -> dict:
    """
    reads data for selected countries from tsv file and returns it as dict
    the population value of this field is no longer used, since I switche to using d_ref_country_database instead
    """
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
    write to data/int/countries-latest-all.tsv and data/int/countries-latest-all.json
    """
    l_for_export = []
    with open('data/int/countries-latest-all.tsv', mode='w', encoding='utf-8', newline='\n') as f:
        csvwriter = csv.writer(f, delimiter="\t")
        csvwriter.writerow(  # header row
            ('Country', 'Population', 'Date', 'Cases',
             'Deaths', 'Cases_Per_Million', 'Deaths_Per_Million', 'Cases_Last_Week_Per_Million', 'Deaths_Last_Week_Per_Million', 'Continent', 'Code')
        )
        for country in sorted(d_countries_timeseries.keys(), key=str.casefold):
            country_data = d_countries_timeseries[country]
            entry = country_data[-1]  # last entry (=>latest date)
            pop = read_population(country)

            d_for_export = entry
            d_for_export['Country'] = country
            d_for_export['Code'] = read_country_code(d_for_export['Country'])
            d_for_export['Continent'] = read_continent(d_for_export['Country'])
            d_for_export['Population'] = pop
            # d_for_export['Date'] = entry['Date']
            # d_for_export['Cases'] = entry['Cases']
            # d_for_export['Deaths'] = entry['Deaths']
            if d_for_export['Cases_Per_Million']:
                d_for_export['Cases_Per_Million'] = round(
                    entry['Cases_Per_Million'], 0)
            if d_for_export['Deaths_Per_Million']:
                d_for_export['Deaths_Per_Million'] = round(
                    entry['Deaths_Per_Million'], 0)
            if d_for_export['Cases_Last_Week_Per_Million']:
                d_for_export['Cases_Last_Week_Per_Million'] = round(
                    entry['Cases_Last_Week_Per_Million'], 0)
            if d_for_export['Deaths_Last_Week_Per_Million']:
                d_for_export['Deaths_Last_Week_Per_Million'] = round(
                    entry['Deaths_Last_Week_Per_Million'], 0)
            l_for_export.append(d_for_export)

            csvwriter.writerow(
                (
                    d_for_export['Country'], d_for_export['Population'], d_for_export['Date'],
                    d_for_export['Cases'], d_for_export['Deaths'],
                    d_for_export['Cases_Per_Million'], d_for_export['Deaths_Per_Million'],
                    d_for_export['Cases_Last_Week_Per_Million'], d_for_export[
                        'Deaths_Last_Week_Per_Million'], d_for_export['Continent'], d_for_export['Code']
                )
            )
            del d_for_export

    # JSON export
    helper.write_json(
        filename='data/int/countries-latest-all.json', d=l_for_export, sort_keys=False)

    # for selected countries write to separate file, for Gnuplot plotting
    with open('data/int/countries-latest-selected.tsv', mode='w', encoding='utf-8', newline='\n') as f:
        csvwriter = csv.writer(f, delimiter="\t")
        # TODO: change order: pop as no 3
        csvwriter.writerow(
            ('Country', 'Date',
             'Cases', 'Deaths',
             'Cases_Per_Million', 'Deaths_Per_Million',
             'Population'
             )
        )
        for country in sorted(d_selected_countries.keys(), key=str.casefold):
            country_data = d_countries_timeseries[country]
            entry = country_data[-1]  # last entry for this country
            csvwriter.writerow(
                (country, entry['Date'],
                 entry['Cases'], entry['Deaths'],
                 entry['Cases_Per_Million'], entry['Deaths_Per_Million'],
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
            print(
                f"{country}\t{entry['Cases']}\t{entry['Deaths']}\t{int(entry['Deaths_Per_Million'])}")


def fit_doubling_time():
    """
    fit time series for doubling time
    """
    global d_countries_timeseries
    global d_selected_countries
    for country in tqdm(d_countries_timeseries.keys()):
        # for country in d_selected_countries.keys():
        # print(country)
        # country_code = d_selected_countries[country]['Code']
        l_country_data = d_countries_timeseries[country]
        # pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        # for fits of doubling time
        data_t = []
        data_cases = []
        data_deaths = []

        for i in range(len(l_country_data)):
            entry = l_country_data[i]

            # for fits of doubling time
            data_t.append(entry['Days_Past'])
            data_cases.append(entry['Cases'])
            data_deaths.append(entry['Deaths'])

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
            entry['Cases_Doubling_Time'] = ""
            entry['Deaths_Doubling_Time'] = ""
            this_DaysPast = entry['Days_Past']
            if this_DaysPast in fit_series_res_cases:
                entry['Cases_Doubling_Time'] = fit_series_res_cases[this_DaysPast]
            if this_DaysPast in fit_series_res_deaths:
                entry['Deaths_Doubling_Time'] = fit_series_res_deaths[this_DaysPast]
            l_country_data[i] = entry

        if args["sleep"]:
            time.sleep(1)
        d_countries_timeseries[country] = l_country_data


def export_time_series_all_countries():
    for country in d_countries_timeseries.keys():
        # for country in d_selected_countries.keys():
        country_code = read_country_code(country)
        if not country_code:
            continue
        # country_code = d_selected_countries[country]['Code']
        l_country_data = d_countries_timeseries[country]
        #     pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        helper.write_json(
            f'data/int/country-{country_code}.json', l_country_data)

        with open(f'data/int/country-{country_code}.tsv', mode='w', encoding='utf-8', newline='\n') as f:
            csvwriter = csv.writer(f, delimiter="\t")
            csvwriter.writerow(  # header row
                ('Days_Past', 'Date',
                 'Cases', 'Deaths',
                 'Cases_New', 'Deaths_New',
                 'Cases_Per_Million', 'Deaths_Per_Million',
                 'Cases_New_Per_Million', 'Deaths_New_Per_Million',
                 'Cases_Doubling_Time', 'Deaths_Doubling_Time',
                 'Cases_Change_Factor', 'Deaths_Change_Factor',
                 'Days_Since_2nd_Death'
                 )
            )

            for entry in l_country_data:
                this_Cases_Doubling_Time = None
                this_Deaths_Doubling_Time = None
                if 'Cases_Doubling_Time' in entry:
                    this_Cases_Doubling_Time = entry['Cases_Doubling_Time']
                if 'Deaths_Doubling_Time' in entry:
                    this_Deaths_Doubling_Time = entry['Deaths_Doubling_Time']
                csvwriter.writerow(
                    (
                        entry['Days_Past'], entry['Date'],
                        entry['Cases'], entry['Deaths'],
                        entry['Cases_New'], entry['Deaths_New'],
                        entry['Cases_Per_Million'], entry['Deaths_Per_Million'],
                        entry['Cases_New_Per_Million'], entry['Deaths_New_Per_Million'],
                        this_Cases_Doubling_Time, this_Deaths_Doubling_Time,
                        entry['Cases_Change_Factor'], entry['Deaths_Change_Factor'],
                        entry['Days_Since_2nd_Death']
                    )
                )

    # export all to one file
    # helper.write_json('TODO.json', d_countries, sort_keys=True)


def get_ref_country_dict(country_name: str) -> dict:
    global d_ref_country_database
    d = {}
    if country_name == 'Congo (Brazzaville)':
        d = d_ref_country_database['Republic of the Congo']
    elif country_name == 'Congo (Kinshasa)':
        d = d_ref_country_database['Democratic Republic of the Congo']
    else:
        for ref_country_name in d_ref_country_database.keys():
            if country_name == ref_country_name:
                d = d_ref_country_database[country_name]
                break
    return d


def read_population(country_name: str, verbose: bool = False) -> int:
    pop = None
    d = get_ref_country_dict(country_name)
    if d != {}:
        pop = d['Population']

    if pop != None:
        pop = int(pop)
    if pop == 0:
        pop = None
    if verbose and pop == None:
        print(f"No Population found for {country_name}")
    return pop


def read_continent(country_name: str) -> str:
    continent = None
    d = get_ref_country_dict(country_name)
    if d != {}:
        continent = d['Continent']
    # move Turkey from Asia to Europe
    if country_name == 'Turkey':
        continent = 'EU'

    if continent != None:
        if continent == 'AF':
            continent = 'Africa'
        elif continent == 'AN':
            continent = 'Antarctica'
        elif continent == 'AS':
            continent = 'Asia'
        elif continent == 'EU':
            continent = 'Europe'
        elif continent == 'NA':
            continent = 'North America'
        elif continent == 'SA':
            continent = 'South America'
        elif continent == 'OC':
            continent = 'Oceania'
    return continent


def read_country_code(country_name: str) -> str:
    code = None
    d = get_ref_country_dict(country_name)
    if d != {}:
        code = d['ISO']
    return code


d_ref_country_database = helper.read_json_file(
    'data/ref_country_database.json')

d_selected_countries = read_ref_selected_countries()

if not helper.check_cache_file_available_and_recent(fname=file_cache, max_age=7200, verbose=True):
    download_new_data()

d_countries_timeseries = read_json_data()

check_for_further_interesting_countries()

fit_doubling_time()

extract_latest_date_data()

# deprecated: extract_latest_date_data_selected()


export_time_series_all_countries()

print(
    f"int: countries: latest date in DE set: {d_countries_timeseries['Germany'][-1]['Date']}")


# IDEAS

# DONE
# for selected countries write into csv: all 3 data per capita
# am I missing further intersting countries ?
# export time series for interesting countries to files
