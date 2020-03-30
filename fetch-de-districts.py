#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data of German region provided by

GUI: https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_0/

f=json or f=html

resultRecordCount: max=2000 -> multiple calls needed


Endpoint: RKI_Landkreisdaten
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0




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
import os.path
import time
import datetime
import json
import urllib.request
import csv
# import re

# further modules
# fitting
import numpy as np
# curve-fit() function imported from scipy
from scipy.optimize import curve_fit
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
    name = f"{d_ref_landkreise[lk_id]['GEN']} ({d_ref_landkreise[lk_id]['BEZ']})"
    return name


# def get_lk_id_from_lk_name(lk_name: str) -> str:
#     global d_ref_landkreise
#     this_lk_id = None
#     for lk_id in d_ref_landkreise.keys():
#         if d_ref_landkreise[lk_id]['county'] == lk_name:
#             this_lk_id = lk_id
#     assert this_lk_id != None, "LK {lk_name} unknown"
#     return this_lk_id

def helper_check_cache_file_available_and_recent(fname: str, max_age: int) -> bool:
    b_cache_good = True
    if not os.path.exists(fname):
        print("No Cache available")
        b_cache_good = False
    if (b_cache_good == True and time.time() - os.path.getmtime(fname) > max_age):
        print("Cache too old")
        b_cache_good = False
    return b_cache_good


def convert_timestamp_in_ms_to_date_str(ts: int) -> str:
    """
    converts a ms timestand to date
    """
    d = datetime.datetime.fromtimestamp(ts/1000)
    # s = f"{d}"
    # 2020-03-29 01:00:00
    s = d.strftime("%Y-%m-%d")
    return s


def fetch_json_as_dict_from_url(url: str) -> dict:
    filedata = urllib.request.urlopen(url)
    contents = filedata.read()
    d_json = json.loads(contents.decode('utf-8'))
    assert 'error' not in d_json, d_json['error']['details'][0] + "\n" + url
    return d_json


def fetch_json_as_dict_from_url_and_reduce_to_list(url: str) -> list:
    """
    This removed some of the returned structur
    """
    d_json = fetch_json_as_dict_from_url(url)
    l2 = d_json['features']
    l3 = [v['attributes'] for v in l2]
    return l3


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
    write the json to the file system, using utf-8 encoding
    returns the data as dict, using lk_id as key
    """
    file_cache = "data/download-ref-de-districts.json"

    if readFromCache == True:
        readFromCache = helper_check_cache_file_available_and_recent(
            file_cache, 3600)

    d_landkreise = {}
    if readFromCache == True:  # read from cache
        with open(file_cache, encoding='utf-8') as json_file:
            d_landkreise = json.load(json_file)
    elif readFromCache == False:  # fetch and write to cache
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

        l3 = fetch_json_as_dict_from_url_and_reduce_to_list(url)

        # convert list to dict, using lk_id as key
        for d_landkreis in l3:
            lk_id = d_landkreis['RS']  # RS = LK_ID ; county = LK_Name
            assert "012345".isdecimal() == True
            d = d_landkreis
            del d['RS']
            d_landkreise[lk_id] = d

        assert len(l3) == len(d_landkreise)

        with open('data/download-ref-de-districts.json', 'w', encoding='utf-8') as outfile:
            json.dump(d_landkreise, outfile, ensure_ascii=False)

    return d_landkreise


def fetch_lk_sums_time_series(lk_id: str, readFromCache: bool = True) -> list:
    """
    Fetches all data from arcgis Covid19_RKI_Sums endpoint: Bundesland, Landkreis, etc.
    # API Explorer
    # https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0

    readFromCache=True -> not calling the API, but returning cached data
    readFromCache=False -> calling the API, and writing cache to filesystem

    returns data as list, ordered by date
    """
    dir_cache = 'data/de-districts/cache'
    file_cache = f"{dir_cache}/distict_timeseries-{lk_id}.json"

    if readFromCache == True:
        readFromCache = helper_check_cache_file_available_and_recent(
            file_cache, 3600)

    l3 = []
    if readFromCache == True:  # read from cache
        with open(file_cache, encoding='utf-8') as json_file:
            l3 = json.load(json_file)

    elif readFromCache == False:  # fetch and write to cache
        # lk_id = get_lk_id_from_lk_name(lk_name)
        # lk_name = get_lk_name_from_lk_id(lk_id)
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

        l3 = fetch_json_as_dict_from_url_and_reduce_to_list(url)
        assert len(l3) < max_allowed_rows_to_fetch

        # add days past counter for plotting
        # to ensure that each date is unique
        l_dates_processed = []
        dt_latest_date = datetime.datetime.fromtimestamp(
            l3[-1]['Meldedatum'] / 1000)

        for i in range(len(l3)):
            entry = l3[i]
            # entry['IdBundesland']
            # entry['Bundesland']
            # entry['IdLandkreis']
            # entry['Landkreis']
            # covert to int
            entry['SummeFall'] = int(entry['SummeFall'])
            entry['SummeTodesfall'] = int(entry['SummeTodesfall'])
            entry['AnzahlFall'] = int(entry['AnzahlFall'])
            entry['AnzahlTodesfall'] = int(entry['AnzahlTodesfall'])
            s_this_date = convert_timestamp_in_ms_to_date_str(
                entry['Meldedatum'])
            # to ensure that each date is unique
            assert s_this_date not in l_dates_processed
            l_dates_processed.append(s_this_date)
            this_dt = datetime.datetime.fromtimestamp(
                entry['Meldedatum'] / 1000)
            # this_last_date
            i_days_past = (this_dt-dt_latest_date).days
            entry['DaysPast'] = i_days_past
            l3[i] = entry

        with open(file_cache, 'w', encoding='utf-8') as outfile:
            json.dump(l3, outfile, ensure_ascii=False)

    return l3


# Test function with coefficients as parameters
def fit_function(x, a, b):
    # TODO: replace b by b = ln(2)/T ; with T = doubling time
    return a * np.exp(b * x)


def fit_routine(data: list, fit_range_x: list = (-np.inf, np.inf), fit_range_y: list = (-np.inf, np.inf)) -> list:
    """
    data list of x,y pairs
    """
    assert len(data) >= 2
    (data_x_for_fit, data_y_for_fit) = helper.extract_data_according_to_fit_ranges(
        data, fit_range_x, fit_range_y)

    # Do the fit
    p0 = [data_y_for_fit[-1], 0.14]  # initial guess of parameters
    param, param_cov = curve_fit(fit_function, data_x_for_fit, data_y_for_fit, p0, bounds=(
        (0, -np.inf), (np.inf, np.inf)))

    y_next_day = fit_function(1, param[0], param[1])
    y_next_day_delta = y_next_day - data_y_for_fit[-1]
    factor_increase_next_day = y_next_day / data_y_for_fit[-1]

    d = {
        'fit_x_range': fit_range_x,
        'fit_y_range': fit_range_y,
        'fit_res_a': param[0],
        'fit_res_b': param[1],
        'value_at_last_day': data_y_for_fit[-1],
        'forcast_for_next_day': y_next_day_delta,
        'factor_increase_next_day': factor_increase_next_day
    }

    return d


def plot_lk_fit(lk_id: str, data: list, d_fit_results: dict):
    """
    plots a 4 week history as log plot
    1-day forcase
    TODO: format and re-structrue this dirty code
    """

    lk_name = get_lk_name_from_lk_id(lk_id)

    dt_latest_date = datetime.datetime.fromtimestamp(
        l_lk_time_series[-1]['Meldedatum'] / 1000)

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

    fit_range_x = d_fit_results['fit_x_range']
    fit_range_y = d_fit_results['fit_y_range']

    (data_x_for_fit, data_y_for_fit) = helper.extract_data_according_to_fit_ranges(
        data, fit_range_x, fit_range_y)

    fit_res_a = d_fit_results['fit_res_a']
    fit_res_b = d_fit_results['fit_res_b']
    data_y_fitted = []
    for x in data_x_for_fit:
        y = fit_function(x, fit_res_a, fit_res_b)
        data_y_fitted.append(y)

    plt.title(f"{lk_name}\n%d new cases expected\nfactor:%.2f" %
              (d_fit_results['forcast_for_next_day'], d_fit_results['factor_increase_next_day']))
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


d_ref_landkreise = fetch_ref_landkreise(readFromCache=True)
# d_ref_landkreise[lk_id]['EWZ']    # = Einwohnerzahl: int
# d_ref_landkreise[lk_id]['county'] # zB 'SK Flensburg'
# d_ref_landkreise[lk_id]['BL']     # zB 'Schleswig-Holstein'
# d_ref_landkreise[lk_id]['BL_ID']  # zB '1'
# d_ref_landkreise[lk_id]['BEZ']    # zB 'Kreisfreie Stadt'
# d_ref_landkreise[lk_id]['last_update'] # zB '29.03.2020 00:00'

# TODO: sort by Bundesland, Landkreis


d_fit_results_for_json_export = {}

# Fit Cases für alle LK
for lk_id in d_ref_landkreise.keys():
    lk_name = get_lk_name_from_lk_id(lk_id)
    print(lk_name)

    # 03353   LK Harburg      252776
    # 09562   SK Erlangen     111962
    # 09563   SK Fürth        127748

    data = []
    l_lk_time_series = fetch_lk_sums_time_series(lk_id, readFromCache=True)
    for entry in l_lk_time_series:
        # choose columns to fit
        data.append((entry['DaysPast'], entry['SummeFall']))

    d_fit_results = fit_routine(data, fit_range_x=(-6, 0))

    # TODO: add fit range, as needed for plot
    d = {
        'Bundesland': d_ref_landkreise[lk_id]['BL'],  # Bundesland
        'Landkreis': lk_name,
        'LK_Einwohner': d_ref_landkreise[lk_id]['EWZ'],  # Einwohner
        'fit_res_a': "%.3f" % (d_fit_results['fit_res_a']),
        'fit_res_b': "%.3f" % (d_fit_results['fit_res_b']),
        'Faelle_heute': d_fit_results['value_at_last_day'],
        'Faelle_morgen': "%d" % (d_fit_results['forcast_for_next_day']),
        'Faelle_Faktor_f_morgen': "%.3f" % (d_fit_results['factor_increase_next_day'])
    }

    d_fit_results_for_json_export[lk_id] = d

    plot_lk_fit(lk_id, data, d_fit_results)
    break

# Export fit data as CSV
with open('data/de-districs-cases-fit-data.tsv', 'w', encoding='utf-8', newline="\n") as f:
    csvwriter = csv.writer(f, delimiter="\t")
    csvwriter.writerow(  # header row
        (
            'Bundesland',
            'Landkreis',
            'Population',
            'cases_today',
            'cases_tomorrow',
            'cases_factor_tomorrow'
        )
    )

    for lk_id in d_fit_results_for_json_export.keys():
        lk_name = get_lk_name_from_lk_id(lk_id)
        csvwriter.writerow(
            (
                d_fit_results_for_json_export[lk_id]['Bundesland'],
                d_fit_results_for_json_export[lk_id]['Landkreis'],
                d_fit_results_for_json_export[lk_id]['LK_Einwohner'],
                d_fit_results_for_json_export[lk_id]['Faelle_heute'],
                d_fit_results_for_json_export[lk_id]['Faelle_morgen'],
                d_fit_results_for_json_export[lk_id]['Faelle_Faktor_f_morgen'],
            )
        )

# Export fit data as JSON
with open('data/de-districs-cases-fit-data.json', 'w', encoding='utf-8') as outfile:
    json.dump(d_fit_results_for_json_export, outfile, ensure_ascii=False)


# TODO: Bundeslandsummen


print(1)