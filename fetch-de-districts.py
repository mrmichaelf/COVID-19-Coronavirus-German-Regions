#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data of German discticts (Landkreise) provided by

GUI: https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_0/



Endpoint: RKI_Landkreisdaten
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0

f=json or f=html

resultRecordCount: max=2000 -> multiple calls needed



Endpoint: Covid19_RKI_Sums
API-Doc: https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0
API-Test: https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=html&where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=
Examples
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=json&where=(Bundesland%3D%27Baden-W%C3%BCrttemberg%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=ObjectId%2CSummeFall%2CMeldedatum&orderByFields=Meldedatum%20asc&resultOffset=0&resultRecordCount=2000&cacheHint=true
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=json&where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=Meldedatum%2C+IdBundesland%2C+IdLandkreis&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=

# Report of cases and deaths per Bundesland using sum
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=html&where=IdBundesland%3D%2702%27&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=true&orderByFields=Bundesland%2C+Meldedatum+asc&groupByFieldsForStatistics=Bundesland%2C+Meldedatum&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeFall%22%2C%22outStatisticFieldName%22%3A%22SumSummeFall%22%7D%2C%0D%0A%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeTodesfall%22%2C%22outStatisticFieldName%22%3A%22SumSummeTodesfall%22%7D%5D&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=

List of Bundesländer and lastest number of cases/deaths, not time series
Endpoint: Coronafälle_in_den_Bundesländern
-> BL_mit_EW_und_Faellen
API-Doc
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0
API-Test
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Fallzahl%20desc&resultOffset=0&resultRecordCount=25&cacheHint=true

Example
Man / Woman & Age Distribution
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f=html&where=(Geschlecht%3C%3E%27unbekannt%27%20AND%20Altersgruppe%3C%3E%27unbekannt%27%20AND%20NeuerFall%20IN(0%2C%201))%20AND%20(Bundesland%3D%27Nordrhein-Westfalen%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Altersgruppe%2CGeschlecht&orderByFields=Altersgruppe%20asc&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22AnzahlFall%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&cacheHint=true


Endpoint: RKI_COVID19
API-Doc
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0
API-Test
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=Meldedatum&groupByFieldsForStatistics=&outStatistics=%0D%0A&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=html&token=

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
import datetime
import json
import csv
# import re

# further modules
# fitting
import numpy as np
# curve-fit() function imported from scipy
# from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


# my helper modules
import helper


# urlbase = ''

# here I store the fetched ref_data_from
d_ref_landkreise = {}


# small helpers

def get_lk_name_from_lk_id(lk_id: str) -> str:
    global d_ref_landkreise
    # name = d_ref_landkreise[lk_id]['county']
    name = f"{d_ref_landkreise[lk_id]['LK_Name']} ({d_ref_landkreise[lk_id]['LK_Typ']})"
    return name


# def get_lk_id_from_lk_name(lk_name: str) -> str:
#     global d_ref_landkreise
#     this_lk_id = None
#     for lk_id in d_ref_landkreise.keys():
#         if d_ref_landkreise[lk_id]['county'] == lk_name:
#             this_lk_id = lk_id
#     assert this_lk_id != None, "LK {lk_name} unknown"
#     return this_lk_id


def fetch_json_as_dict_from_url_and_reduce_to_list(url: str) -> list:
    """
    removes some of the returned structur
    """
    d_json = helper.fetch_json_as_dict_from_url(url)
    l2 = d_json['features']
    l3 = [v['attributes'] for v in l2]
    return l3


def helper_read_from_cache_or_fetch_from_url(url: str, file_cache: str, readFromCache: bool = True):
    """
    readFromCache=True -> not calling the API, but returning cached data
    readFromCache=False -> calling the API, and writing cache to filesystem
    """
    if readFromCache:
        readFromCache = helper.check_cache_file_available_and_recent(
            fname=file_cache, max_age=7200, verbose=True)

    json_cont = []
    if readFromCache == True:  # read from cache
        with open(file_cache, mode='r', encoding='utf-8') as json_file:
            json_cont = json.load(json_file)
    elif readFromCache == False:  # fetch and write to cache
        json_cont = fetch_json_as_dict_from_url_and_reduce_to_list(url)
        with open(file_cache, mode='w', encoding='utf-8', newline='\n') as fh:
            json.dump(json_cont, fh, ensure_ascii=False)

    return json_cont


def fetch_ref_landkreise(readFromCache: bool = True) -> dict:
    """
    fetches ref-data for the German districts (Landkreise) via rest API from arcgis
    GUI
    1: https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_1/
    # /bca904a683844e7784141559b540dbc2
    2: https://npgeo-de.maps.arcgis.com/apps/opsdashboard/index.html
    Api Explorer
    https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0

    converts/flattens the retrieved json a bit and use the district ID lk_id as key for the returred dict
    write the json to cache folder in file system, using utf-8 encoding

    returns the data as list of dicts
    """
    file_cache = "cache/de-districts/de-districts.json"

    max_allowed_rows_to_fetch = 2000
    url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?f=json' +\
        '&where=1%3D1' +\
        '&outFields=*' +\
        '&orderByFields=BL_ID%2C+AGS' +\
        "&resultRecordCount=" + str(max_allowed_rows_to_fetch) + \
        '&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false' +\
        '&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false' +\
        '&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=' +\
        '&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&token='

    l_landkreise = helper_read_from_cache_or_fetch_from_url(
        url=url, file_cache=file_cache, readFromCache=readFromCache)

    return l_landkreise


def BL_code_from_BL_ID(bl_id: str) -> str:
    """
    converts BL IDs to Codes: 01 -> SH
    """
    d = {
        '1': 'SH',
        '2': 'HH',
        '3': 'NI',
        '4': 'HB',
        '5': 'NW',
        '6': 'HE',
        '7': 'RP',
        '8': 'BW',
        '9': 'BY',
        '10': 'SL',
        '11': 'BE',
        '12': 'BB',
        '13': 'MV',
        '14': 'SN',
        '15': 'ST',
        '16': 'TH'
    }
    return d[bl_id]


def prepare_ref_landkreise() -> dict:
    file_out = 'data/de-districts/ref-de-districts.json'
    l_landkreise = fetch_ref_landkreise(readFromCache=True)
    d_landkreise = {}

    # convert list to dict, using lk_id as key
    for d_this_landkreis in l_landkreise:
        lk_id = d_this_landkreis['RS']  # RS = LK_ID ; county = LK_Name

        assert type(lk_id) == str
        assert lk_id.isdecimal() == True

        d = {}
        d['Population'] = d_this_landkreis['EWZ']
        assert type(d['Population']) == int
        d['BL_Name'] = d_this_landkreis['BL']
        d['BL_Code'] = BL_code_from_BL_ID(d_this_landkreis['BL_ID'])
        d['LK_Name'] = d_this_landkreis['GEN']
        d['LK_Typ'] = d_this_landkreis['BEZ']
        d_landkreise[lk_id] = d
    with open(file_out, mode='w', encoding='utf-8', newline='\n') as fh:
        json.dump(d_landkreise, fh, ensure_ascii=False)

    del d_this_landkreis

    # assure we did not loose any
    assert len(l_landkreise) == len(d_landkreise)

    gen_mapping_BL2LK_json(d_landkreise)

    return d_landkreise


def gen_mapping_BL2LK_json(d_landkreise: dict):
    d_bundeslaender = {}
    for lk_id in d_landkreise.keys():
        lk = d_landkreise[lk_id]
        if lk['BL_Code'] not in d_bundeslaender.keys():
            d = {}
            l_lk_ids = []
            l_lk_ids.append((lk_id, lk['LK_Name']))
            d['BL_Name'] = lk['BL_Name']
            d['LK_IDs'] = l_lk_ids

            d_bundeslaender[lk['BL_Code']] = d
        else:
            d_bundeslaender[lk['BL_Code']]['LK_IDs'].append(
                (lk_id, lk['LK_Name']))

    with open('data/de-districts/mapping_bundesland_landkreis.json', mode='w', encoding='utf-8', newline='\n') as fh:
        json.dump(d_bundeslaender, fh, ensure_ascii=False)

    1


def fetch_landkreis_time_series(lk_id: str, readFromCache: bool = True) -> list:
    """
    Fetches all data from arcgis Covid19_RKI_Sums endpoint: Bundesland, Landkreis, etc.
    # API Explorer
    # https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0

    readFromCache=True -> not calling the API, but returning cached data
    readFromCache=False -> calling the API, and writing cache to filesystem

    returns data as list, ordered by date
    """
    file_cache = f"cache/de-districts/distict_timeseries-{lk_id}.json"

    max_allowed_rows_to_fetch = 2000

    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query" + \
        "?f=json" + \
        "&where=(IdLandkreis='" + lk_id + "')" + \
        "&outFields=Meldedatum%2CSummeFall%2C+SummeTodesfall%2C+AnzahlFall%2C+AnzahlTodesfall" \
        "&orderByFields=Meldedatum" + \
        "&resultRecordCount=" + str(max_allowed_rows_to_fetch) + \
        "&objectIds=&time=&resultType=none&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false" + \
        "&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&sqlFormat=none&token="
    # get more stuff
    # "&outFields=*" + \

    l_time_series = helper_read_from_cache_or_fetch_from_url(
        url=url, file_cache=file_cache, readFromCache=readFromCache)

    assert len(l_time_series) < max_allowed_rows_to_fetch
    return l_time_series


def prepare_lk_time_series(lk_id: str) -> list:
    """
    convert and add fields of time series list
    returns list
    writes to filesystem
    """
    file_out = f'data/de-districts/de-distict_timeseries-{lk_id}.json'
    l_time_series_fetched = fetch_landkreis_time_series(
        lk_id=lk_id, readFromCache=True)

    l_time_series = []

    # add days past counter for plotting
    # to ensure that each date is unique
    l_dates_processed = []
    dt_latest_date = datetime.datetime.fromtimestamp(
        l_time_series_fetched[-1]['Meldedatum'] / 1000)

    # add and convert some data fields
    data_t = []
    data_cases = []
    data_deaths = []
    last_cases = 0
    last_deaths = 0

    # if lastdate and lastdate-1 have the same number of cases, than drop lastdate
    if l_time_series_fetched[-1]['SummeFall'] == l_time_series_fetched[-2]['SummeFall']:
        l_time_series_fetched.pop()
    # entry = one data point
    for entry in l_time_series_fetched:
        d = {}

        # covert to int
        d['Cases'] = int(entry['SummeFall'])
        d['Deaths'] = int(entry['SummeTodesfall'])
        # d['Cases_New'] = int(entry['AnzahlFall'])
        # d['Deaths_New'] = int(entry['AnzahlTodesfall'])
        d['Cases_New'] = d['Cases'] - last_cases
        d['Deaths_New'] = d['Deaths'] - last_deaths

        d = helper.add_per_million(d_ref_landkreise, lk_id, d)

        last_cases = d['Cases']
        last_deaths = d['Deaths']

        # Rename 'Meldedatum' (ms) -> Timestamp (s)
        d['Timestamp'] = int(entry['Meldedatum'] / 1000)

        # add Date
        d['Date'] = helper.convert_timestamp_to_date_str(
            d['Timestamp'])
        # ensure that each date is unique
        assert d['Date'] not in l_dates_processed
        l_dates_processed.append(d['Date'])

        # add DaysPast
        this_dt = datetime.datetime.fromtimestamp(
            d['Timestamp'])
        i_days_past = (this_dt-dt_latest_date).days
        d['Days_Past'] = i_days_past
        l_time_series.append(d)

        data_t.append(d['Days_Past'])
        data_cases.append(d['Cases'])
        data_deaths.append(d['Deaths'])

    # perform fit for last 7 days to obtain doublication time
    data = list(zip(data_t, data_cases))
    fit_series_res = helper.series_of_fits(
        data, fit_range=7, max_days_past=14)

    for i in range(len(l_time_series)):
        entry = l_time_series[i]
        this_doublication_time = ""
        this_days_past = entry['Days_Past']
        if this_days_past in fit_series_res:
            this_doublication_time = fit_series_res[this_days_past]
        entry['Doublication_Time'] = this_doublication_time
        l_time_series[i] = entry

    with open(file_out, mode='w', encoding='utf-8', newline='\n') as fh:
        json.dump(l_time_series, fh, ensure_ascii=False)

    return l_time_series


def plot_lk_fit(lk_id: str, data: list, d_fit_results: dict):
    """
    plots a 4 week history as log plot
    1-day forcase
    TODO: format and re-structrue this dirty code
    """

    lk_name = get_lk_name_from_lk_id(lk_id)

    dt_latest_date = datetime.datetime.fromtimestamp(
        l_lk_time_series[-1]['Timestamp'])

    # print(
    #     f"=== Zeitverlauf für {l_lk_time_series[-1]['Bundesland']}: {l_lk_time_series[-1]['Landkreis']}, vom {l_lk_time_series[-1]['Datenstand']} ===")

    # these will be used for plotting, and partly for fitting

    # print(
    #     f"{s_this_date}\t{i_days_past}\t{entry['SummeFall']}\t{entry['SummeTodesfall']}\t{entry['AnzahlFall']}\t{entry['AnzahlTodesfall']}")

    # print(f"Coefficients:\n{param}")
    # print(f"Covariance of coefficients:\n{param_cov}")

    # print("Tomorrow it could be: %d , that is a factor of %.3f" %
    #   (y_next_day, factor_increase_next_day))

    #
    (data_x, data_y) = helper.extract_x_and_y_data(data)

    fit_range_x = d_fit_results['fit_set_x_range']
    fit_range_y = d_fit_results['fit_set_y_range']

    (data_x_for_fit, data_y_for_fit) = helper.extract_data_according_to_fit_ranges(
        data, fit_range_x, fit_range_y)

    data_y_fitted = []
    for x in data_x_for_fit:
        y = helper.fit_function_exp_growth(x, *d_fit_results['fit_res'])
        data_y_fitted.append(y)

    plt.title(f"{lk_name}\n%d new cases expected\nfactor:%.2f" %
              (d_fit_results['forcast_y_at_x+1'], d_fit_results['factor_increase_x+1']))
    range_x = (-28, 1)
    plt.plot(data_x, data_y, 'o', color='red', label="data")
    plt.plot(data_x_for_fit, data_y_fitted,
             '--', color='blue', label="fit")
    plt.legend()
    plt.grid()
    # plt.xticks(np.arange(min(data_x), 0, 7.0))
    axes = plt.gca()
    axes.tick_params(direction='in', bottom=True,
                     top=True, left=True, right=True)
    plt.yscale('log')
    x_ticks = np.arange(range_x[0], range_x[1], 7)
    axes.set_xlim([range_x[0], range_x[1]])
    plt.xticks(x_ticks)

    # axes.set_ylim([ymin,ymax])
    fileout = f'plots-python/de-cases-fit-region-{lk_id}.png'
    # .replace(" ", "_")
    plt.savefig(fileout)
    # plt.show()
    plt.clf()  # clear plot

    # fetch_fit_and_plot_lk('SK Fürth')
    # fetch_fit_and_plot_lk('SK Erlangen')
    # fetch_fit_and_plot_lk('SK Hamburg')
    # fetch_fit_and_plot_lk('LK Harburg')


d_ref_landkreise = prepare_ref_landkreise()


# fetch_ref_landkreise(readFromCache=True)

# d_ref_landkreise[lk_id]['EWZ']    # = Einwohnerzahl: int
# d_ref_landkreise[lk_id]['county'] # zB 'SK Flensburg'
# d_ref_landkreise[lk_id]['BL']     # zB 'Schleswig-Holstein'
# d_ref_landkreise[lk_id]['BL_ID']  # zB '1'
# d_ref_landkreise[lk_id]['BEZ']    # zB 'Kreisfreie Stadt'
# d_ref_landkreise[lk_id]['last_update'] # zB '29.03.2020 00:00'

# TODO: sort by Bundesland, Landkreis


d_results_for_json_export = {}

# Fit Cases für alle LK
# 16068 machte Probleme

# l2 = ('16068',)
for lk_id in d_ref_landkreise.keys():
    lk_name = get_lk_name_from_lk_id(lk_id)
    print(f"{lk_id} {lk_name}")

    # 03353   LK Harburg      252776
    # 09562   SK Erlangen     111962
    # 09563   SK Fürth        127748

    data = []
    l_lk_time_series = prepare_lk_time_series(lk_id)
    # l_lk_time_series = fetch_landkreis_time_series(lk_id, readFromCache=True)
    for entry in l_lk_time_series:
        # choose columns for fitting
        data.append((entry['Days_Past'], entry['Cases']))

    last_entry = l_lk_time_series[-1]
    last_deaths = last_entry['Deaths']

    d_fit_results = helper.fit_routine(data, fit_range_x=(-6, 0))

    # TODO: add fit range, as needed for plot
    d = {
        'Bundesland': d_ref_landkreise[lk_id]['BL_Name'],  # Bundesland
        'Landkreis': lk_name,
        'LK_Einwohner': d_ref_landkreise[lk_id]['Population'],  # Einwohner
        'fit_res_N0': round(d_fit_results['fit_res'][0], 3),
        'fit_res_T': round(d_fit_results['fit_res'][1], 3),
        'fit_used_x_range': d_fit_results['fit_used_x_range'],
        'Cases': last_entry['Cases'],
        'Cases_Per_Million': last_entry['Cases_Per_Million'],
        'Deaths': last_entry['Deaths'],
        'Deaths_Per_Million': last_entry['Deaths_Per_Million'],
        'Cases_Forecast_Tomorrow': round(d_fit_results['forcast_y_at_x+1'], 3),
        'Cases_Forecast_Tomorrow_Factor': round(d_fit_results['factor_increase_x+1'], 3)
    }

    d_results_for_json_export[lk_id] = d

    # TODO:
    # plot_lk_fit(lk_id, data, d_fit_results)
    # break


# Export fit data as JSON
with open('data/de-districts/de-districts-results.json', mode='w', encoding='utf-8', newline='\n') as fh:
    json.dump(d_results_for_json_export, fh, ensure_ascii=False)

# Export fit data as CSV + HTML
with open('data/de-districts/de-districts-results.tsv', mode='w', encoding='utf-8', newline='\n') as fh_csv:
    csvwriter = csv.writer(fh_csv, delimiter="\t")
    with open('results-de-districts.html', mode='w', encoding='utf-8', newline='\n') as fh_html:

        l = (
            'Landkreis',
            'Bundesland',
            'Einwohner',
            'Fälle',
            'Tode',
            'Fälle pro 1 Millionen Einwohner',
            'Tote pro 1 Millionen Einwohner',
            'Prognose Fälle Morgen (%)'
        )

        csvwriter.writerow(l)

        fh_html.write("""<!doctype html>
<html lang="de">
<head>
    <meta charset="utf-8">
    
<style>
    #myInput {
      background-image: url('/css/searchicon.png');      /* Add a search icon to input */
      background-position: 10px 12px;      /* Position the search icon */
      background-repeat: no-repeat;      /* Do not repeat the icon image */
      width: 400px;
      font-size: 16px;      /* Increase font-size */
      padding: 12px 20px 12px 10px;      /* Add some padding */
      border: 1px solid #ddd;       /* Add a grey border */
      margin-bottom: 12px;       /* Add some space below the input */
    }

#myTable {
  border-collapse: collapse; /* Collapse borders */
  width: 100%; /* Full-width */
  border: 1px solid #ddd; /* Add a grey border */
  font-size: 18px; /* Increase font-size */
}

#myTable th, #myTable td {
  text-align: left; /* Left-align text */
  padding: 12px; /* Add padding */
}

#myTable tr {
  /* Add a bottom border to all table rows */
  border-bottom: 1px solid #ddd;
}

#myTable tr.header, #myTable tr:hover {
  /* Add a grey background color to the table header and on hover */
  background-color: #f1f1f1;
}
</style>

<script>
    function mySortFunction() {
        // Declare variables
        var input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("myInput");
        filter = input.value.toUpperCase();
        table = document.getElementById("myTable");
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
</script>
</head>

<body>
<p>
<a href="index.html">zurück zur Auswertung</a>
</p>
<h1>Landkreisprognose</h1>
<p>Basierend auf Daten des
<a href="https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_0/" target="_blank">Robert Koch-Institut COVID-19-Dashboards</a>
</p>
    <input type="text" id="myInput" onkeyup="mySortFunction()" placeholder="Landkreissuche">
    <table id="myTable">        
        """)
        fh_html.write('<tr><th>')
        fh_html.write('</th><th>'.join(l))
        # fh_html.write(f'<th>{l[0]}</th>')
        # fh_html.write(f'<th>{l[1]}</th>')
        # fh_html.write(f'<th>{l[2]}</th>')
        # fh_html.write(f'<th>{l[3]}</th>')
        # fh_html.write(f'<th>{l[4]}</th>')
        # fh_html.write(f'<th>{l[5]}</th>')
        # fh_html.write(f'<th>{l[6]}</th>')
        # fh_html.write(f'<th>{l[7]}</th>')
        # fh_html.write(f'<th>{l[8]}</th>')
        fh_html.write('</th></tr>\n')

        for lk_id in d_results_for_json_export.keys():
            l = (
                d_results_for_json_export[lk_id]['Landkreis'],
                d_results_for_json_export[lk_id]['Bundesland'],
                d_results_for_json_export[lk_id]['LK_Einwohner'],
                d_results_for_json_export[lk_id]['Cases'],
                d_results_for_json_export[lk_id]['Deaths'],
                int(round(d_results_for_json_export[lk_id]
                          ['Cases_Per_Million'], 0)),
                int(round(
                    d_results_for_json_export[lk_id]['Deaths_Per_Million'], 0)),
                round(
                    100 * (d_results_for_json_export[lk_id]['Cases_Forecast_Tomorrow_Factor'] - 1), 1)
            )
            l = [str(v) for v in l]

            csvwriter.writerow(l)
            fh_html.write('<tr><td>')
            fh_html.write('</td><td>'.join(l))
            fh_html.write('</td></tr>\n')

        fh_html.write('</table>\n')
        fh_html.write('</body>\n')
        fh_html.write('</html>\n')

# Export fit data as HTML

# TODO: Bundeslandsummen


print(1)
