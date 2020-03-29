# core modules
import json
import urllib.request
# import csv
# import re
import datetime

# further modules
# fitting
import numpy as np
# curve-fit() function imported from scipy
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


# API Info: resultRecordCount: max 2000 -> multiple calls needed
# Covid19_RKI_Sums
# API Explorer
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0
# Daten
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=json&where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=Meldedatum%2C+IdBundesland%2C+IdLandkreis&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=

# Coronafälle_in_den_Bundesländern
# API Explorer
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0
# Daten
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Fallzahl%20desc&resultOffset=0&resultRecordCount=25&cacheHint=true

# Daten
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=json&where=(Bundesland%3D%27Baden-W%C3%BCrttemberg%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=ObjectId%2CSummeFall%2CMeldedatum&orderByFields=Meldedatum%20asc&resultOffset=0&resultRecordCount=2000&cacheHint=true


# Ref Data Landkreise
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=cases%20desc&outSR=102100&resultOffset=0&resultRecordCount=1000&cacheHint=true'

# urlbase = ''


d_ref_landkreise = {}


def fetch_json_as_dict_from_url(url: str) -> dict:
    filedata = urllib.request.urlopen(url)
    contents = filedata.read()
    d_json = json.loads(contents.decode('utf-8'))
    assert 'error' not in d_json, d_json['error']['details'][0] + "\n" + url
    return d_json


def fetch_json_as_dict_from_url_and_reduce_to_list(url: str) -> list:
    d_json = fetch_json_as_dict_from_url(url)
    l2 = d_json['features']
    l3 = [v['attributes'] for v in l2]
    return l3


def fetch_ref_landkreise() -> dict:
    """
    fetches ref-data for the German counties (Landkreise) via rest API from arcgis
    GUI
    1: https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_1/
    # /bca904a683844e7784141559b540dbc2
    2: https://npgeo-de.maps.arcgis.com/apps/opsdashboard/index.html
    Api Explorer
    https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0

    converts/flattens the retrieved json a bit and use the county name as key for the returred dict
    write the json to the file system, using utf-8 encoding
    returns the data as dict
    """
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

    d_landkreise = {}
    for d_landkreis in l3:
        lk_name = d_landkreis['RS']  # AGS = LK_ID ; county = LK_Name
        d = d_landkreis
        del d['RS']
        d_landkreise[lk_name] = d

    assert len(l3) == len(d_landkreise)

    with open('data/download-ref-de-counties.json', 'w', encoding='utf-8') as outfile:
        json.dump(d_landkreise, outfile, ensure_ascii=False)

    return d_landkreise


def get_lk_id_from_lk_name(lk_name: str) -> str:
    global d_ref_landkreise
    this_lk_id = None
    for lk_id in d_ref_landkreise.keys():
        if d_ref_landkreise[lk_id]['county'] == lk_name:
            this_lk_id = lk_id
    assert this_lk_id != None, "LK {lk_name} unknown"
    return this_lk_id


def fetch_lk_sums_time_series(lk_name: str):
    """
    Fetches all data from arcgis Covid19_RKI_Sums endpoint: Bundesland, Landkreis, etc.
    # API Explorer
    # https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0
    returns data as list, ordered by date
    """

    lk_id = get_lk_id_from_lk_name(lk_name)
    max_allowed_rows_to_fetch = 2000

    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query" + \
        "?f=json" + \
        "&where=(IdLandkreis='" + lk_id + "')" + \
        "&outFields=*" + \
        "&orderByFields=Meldedatum" + \
        "&resultRecordCount=" + str(max_allowed_rows_to_fetch) + \
        "&objectIds=&time=&resultType=none&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false" + \
        "&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&sqlFormat=none&token="

    l3 = fetch_json_as_dict_from_url_and_reduce_to_list(url)
    assert len(l3) < max_allowed_rows_to_fetch

    return l3

# helper - general


def convert_timestamp_in_ms_to_date_str(ts: int) -> str:
    """
    converts a ms timestand to date
    """
    d = datetime.datetime.fromtimestamp(ts/1000)
    # s = f"{d}"
    # 2020-03-29 01:00:00
    s = d.strftime("%Y-%m-%d")
    return s

# helper - specifiv


# def
# s = fetch_landkreise()
d_ref_landkreise = fetch_ref_landkreise()
# d_ref_landkreise[lk_id]['EWZ']    # = Einwohnerzahl: int
# d_ref_landkreise[lk_id]['county'] # zB 'SK Flensburg'
# d_ref_landkreise[lk_id]['BL']     # zB 'Schleswig-Holstein'
# d_ref_landkreise[lk_id]['BL_ID']  # zB '1'
# d_ref_landkreise[lk_id]['BEZ']    # zB 'Kreisfreie Stadt'
# d_ref_landkreise[lk_id]['last_update'] # zB '29.03.2020 00:00'


# for lk_id in d_ref_landkreise.keys():
#     print(
#         f"{lk_id}\t{d_ref_landkreise[lk_id]['county']}\t{d_ref_landkreise[lk_id]['EWZ']}")
# TODO: Bundeslandsummen


# Test function with coefficients as parameters
def fit_function(x, a, b):
    return a * np.exp(b * x)


def fetch_fit_and_plot_lk(lk_name: str):
    """
    fetches data for a german region
    fits the cases data
    plots a 4 week history as log plot
    1-day forcase
    TODO: format and re-structrue this dirty code
    """

    l_lk_time_series = fetch_lk_sums_time_series(lk_name)
    # 03353   LK Harburg      252776
    # 09562   SK Erlangen     111962
    # 09563   SK Fürth        127748
    # last_date = l_lk_time_series[-1]['Datenstand']
    # dt_last_date = datetime.datetime.fromisoformat(
    #     l_lk_time_series[-1]['Datenstand']  # 2020-03-29
    # )

    # ts_latest_date = l_lk_time_series[-1]['Meldedatum'] / 1000
    dt_latest_date = datetime.datetime.fromtimestamp(
        l_lk_time_series[-1]['Meldedatum'] / 1000)

    print(
        f"=== Zeitverlauf für {l_lk_time_series[-1]['Bundesland']}: {l_lk_time_series[-1]['Landkreis']}, vom {l_lk_time_series[-1]['Datenstand']} ===")

    # to ensure that each date is unique
    l_dates_processed = []

    # these will be used for plotting, and partly for fitting
    data_x = []
    data_y = []

    for entry in l_lk_time_series:
        # entry['IdBundesland']
        # entry['Bundesland']
        # entry['IdLandkreis']
        # entry['Landkreis']
        entry['SummeFall'] = int(entry['SummeFall'])
        entry['SummeTodesfall'] = int(entry['SummeTodesfall'])
        entry['AnzahlFall'] = int(entry['AnzahlFall'])
        entry['AnzahlTodesfall'] = int(entry['AnzahlTodesfall'])
        s_this_date = convert_timestamp_in_ms_to_date_str(entry['Meldedatum'])
        # dt_latest_date
        this_dt = datetime.datetime.fromtimestamp(entry['Meldedatum'] / 1000)
        # this_last_date
        i_days_past = (this_dt-dt_latest_date).days

        # data to fit
        data_x.append(i_days_past)
        data_y.append(entry['SummeFall'])

        assert s_this_date not in l_dates_processed
        l_dates_processed.append(s_this_date)
        print(
            f"{s_this_date}\t{i_days_past}\t{entry['SummeFall']}\t{entry['SummeTodesfall']}\t{entry['AnzahlFall']}\t{entry['AnzahlTodesfall']}")

    assert len(data_x) == len(data_y)

    # fit only the x range
    fit_range_x = (-6, 0)
    fit_range_y = (-np.inf, np.inf)
    # reduce the data on which we fit
    data_x_for_fit = []
    data_y_for_fit = []
    for i in range(len(data_x)):
        if data_x[i] >= fit_range_x[0] and data_x[i] <= fit_range_x[1] and data_y[i] >= fit_range_y[0] and data_y[i] <= fit_range_y[1]:
            data_x_for_fit.append(data_x[i])
            data_y_for_fit.append(data_y[i])

    # Do the fit
    p0 = [data_y[-1], 0.14]  # initial guess of parameters
    param, param_cov = curve_fit(fit_function, data_x_for_fit, data_y_for_fit, p0, bounds=(
        (0, -np.inf), (np.inf, np.inf)))

    print(f"Coefficients:\n{param}")
    print(f"Covariance of coefficients:\n{param_cov}")

    y_next_day = fit_function(1, param[0], param[1])
    y_next_day_delta = y_next_day - data_y[-1]
    factor_increase_next_day = y_next_day / data_y[-1]
    print("Tomorrow it could be: %d , that is a factor of %.3f" %
          (y_next_day, factor_increase_next_day))

    data_y_fitted = []
    for x in data_x_for_fit:
        y = fit_function(x, param[0], param[1])
        data_y_fitted.append(y)

    plt.title(f"Landkreis: {lk_name}\n%d new cases expected\nfactor:%.2f" %
              (y_next_day_delta, factor_increase_next_day))
    range_x = (-28, 1)
    plt.plot(data_x, data_y, 'o', color='red', label="data")
    plt.plot(data_x_for_fit, data_y_fitted, '--', color='blue', label="fit")
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
    fileout = f'plots-python/de-cases-region-fit-{lk_name}.png'.replace(
        " ", "_")
    plt.savefig(fileout)
    # plt.show()
    plt.clf()  # clear plot


fetch_fit_and_plot_lk('Region Hannover')
fetch_fit_and_plot_lk('SK Fürth')
fetch_fit_and_plot_lk('SK Erlangen')
fetch_fit_and_plot_lk('SK Hamburg')
fetch_fit_and_plot_lk('LK Harburg')


print(1)
