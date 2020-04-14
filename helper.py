"""
Helper functions collections
"""

# Built-in/Generic Imports
import os.path
import time
import datetime
import argparse
import json
import urllib.request

# further modules
import math
import numpy as np
# curve-fit() function imported from scipy
from scipy.optimize import curve_fit


def read_json_file(filename: str):
    """
    returns list or dict
    """
    with open(filename, mode='r', encoding='utf-8') as fh:
        return json.load(fh)


def write_json(filename: str, d: dict, sort_keys: bool = False):
    with open(filename, mode='w', encoding='utf-8', newline='\n') as fh:
        json.dump(d, fh, ensure_ascii=False, sort_keys=sort_keys)


def read_command_line_parameters() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sleep", help="sleep 1 second after each item",
                        default=False, action="store_true")  # store_true -> Boolean Value
    return vars(parser.parse_args())


def convert_timestamp_to_date_str(ts: int) -> str:
    """
    converts a ms timestand to date string (without time)
    format: 2020-03-29
    """
    d = datetime.datetime.fromtimestamp(ts)
    # s = f"{d}"
    # 2020-03-29 01:00:00
    s = d.strftime("%Y-%m-%d")
    return s


def date_format(y: int, m: int, d: int) -> str:
    return "%04d-%02d-%02d" % (y, m, d)


def prepare_time_series(l_time_series: list) -> list:
    """
    assumes items in l_time_series are dicts haveing the following keys: Date, Cases, Deaths
    sorts l_time_series by Date
    if cases at last entry equals 2nd last entry, than remove last entry, as sometime the source has a problem.
    loops over l_time_series and calculates the 
      Days_Past
      _New values per item/day    
      _Last_Week
    """
    # some checks
    d = l_time_series[0]
    assert 'Date' in d
    assert 'Cases' in d
    assert 'Deaths' in d
    assert isinstance(d['Date'], str)
    assert isinstance(d['Cases'], int)
    assert isinstance(d['Deaths'], int)
    last_date = datetime.datetime.strptime(
        l_time_series[-1]['Date'], "%Y-%m-%d")

    # ensure sorting by date
    l_time_series = sorted(
        l_time_series, key=lambda x: x['Date'], reverse=False)

    # if lastdate and lastdate-1 have the same number of cases, than drop lastdate
    if l_time_series[-1]['Cases'] == l_time_series[-2]['Cases']:
        l_time_series.pop()

    # to ensure that each date is unique
    l_dates_processed = []

    last_cases = 0
    last_deaths = 0

    for i in range(len(l_time_series)):
        d = l_time_series[i]

        # ensure that each date is unique
        assert d['Date'] not in l_dates_processed
        l_dates_processed.append(d['Date'])

        this_date = datetime.datetime.strptime(d['Date'], "%Y-%m-%d")
        d['Days_Past'] = (this_date-last_date).days

        # _New since yesterday
        d['Cases_New'] = d['Cases'] - last_cases
        d['Deaths_New'] = d['Deaths'] - last_deaths
        last_cases = d['Cases']
        last_deaths = d['Deaths']

        # delta of _Last_Week = last 7 days
        d['Cases_Last_Week'] = 0
        d['Deaths_Last_Week'] = 0
        if i >= 7:
            d['Cases_Last_Week'] = d['Cases'] - l_time_series[i-7]['Cases']
            d['Deaths_Last_Week'] = d['Deaths'] - \
                l_time_series[i-7]['Deaths']

        l_time_series[i] = d

    return l_time_series


def add_per_million_via_lookup(d: dict, d_ref: dict, code: str) -> dict:
    pop_in_million = d_ref[code]['Population'] / 1000000
    return add_per_million(d=d, pop_in_million=pop_in_million)


def add_per_million(d: dict, pop_in_million: float) -> dict:
    for key in ('Cases', 'Deaths', 'Cases_New', 'Deaths_New', 'Cases_Last_Week', 'Deaths_Last_Week'):
        if pop_in_million:
            perMillion = round(d[key]/pop_in_million, 3)
        else:
            perMillion = 0  # if pop is unknown
        d[key+'_Per_Million'] = perMillion
    return d


def check_cache_file_available_and_recent(fname: str, max_age: int = 3600, verbose: bool = False) -> bool:
    b_cache_good = True
    if not os.path.exists(fname):
        if verbose:
            print(f"No Cache available: {fname}")
        b_cache_good = False
    if (b_cache_good and time.time() - os.path.getmtime(fname) > max_age):
        if verbose:
            print(f"Cache too old: {fname}")
        b_cache_good = False
    return b_cache_good


def fetch_json_as_dict_from_url(url: str) -> dict:
    filedata = urllib.request.urlopen(url)
    contents = filedata.read()
    d_json = json.loads(contents.decode('utf-8'))
    assert 'error' not in d_json, d_json['error']['details'][0] + "\n" + url
    return d_json


def extract_x_and_y_data(data: list) -> list:
    """
    data of (x,y) -> data_x, data_y
    """
    data_x = []
    data_y = []
    for pair in data:
        data_x.append(pair[0])
        data_y.append(pair[1])
    return data_x, data_y


def extract_data_according_to_fit_ranges(data: list, fit_range_x: list, fit_range_y: list):
    # reduce the data on which we fit
    data_x_for_fit = []
    data_y_for_fit = []
    for i in range(len(data)):
        if data[i][0] >= fit_range_x[0] and data[i][0] <= fit_range_x[1] and data[i][1] >= fit_range_y[0] and data[i][1] <= fit_range_y[1]:
            data_x_for_fit.append(data[i][0])
            data_y_for_fit.append(data[i][1])
    return (data_x_for_fit, data_y_for_fit)


# Fit function with coefficients as parameters
def fit_function_exp_growth(t, N0, T):
    """
    N0 = values at t = 0
    T = time it takes for t duplication: f(t+T) = 2 x f(t)
    """
    # previously b = ln(2)/T used, but this is better as T = doubling time is directy returned
    return N0 * np.exp(t * math.log(2)/T)


def fit_routine(data: list, fit_range_x: list = (-np.inf, np.inf), fit_range_y: list = (-np.inf, np.inf)) -> list:
    """
    data: list of x,y pairs
    """
    assert len(data) >= 2
    (data_x_for_fit, data_y_for_fit) = extract_data_according_to_fit_ranges(
        data, fit_range_x, fit_range_y)

    d = {}
    if len(data_x_for_fit) >= 3:
        # Do the fit
        p0 = [float(data_y_for_fit[-1]), 5.0]  # initial guess of parameters
        try:
            fit_res, fit_res_cov = curve_fit(
                fit_function_exp_growth,
                data_x_for_fit,
                data_y_for_fit,
                p0,
                bounds=(
                    (0, -np.inf), (np.inf, np.inf)
                )
            )
            # bounds: ( min of all parameters) , (max of all parameters) )

            y_next_day = fit_function_exp_growth(1, fit_res[0], fit_res[1])
            y_next_day_delta = y_next_day - data_y_for_fit[-1]
            factor_increase_next_day = ""
            if data_y_for_fit[-1] > 0:
                factor_increase_next_day = y_next_day / data_y_for_fit[-1]

            d = {
                'fit_set_x_range': fit_range_x,
                'fit_set_y_range': fit_range_y,
                'fit_used_x_range': (data_x_for_fit[0], data_x_for_fit[-1]),
                'fit_res': fit_res,
                'fit_res_cov': fit_res_cov,
                'y_at_x_max': data_y_for_fit[-1],
                'forcast_y_at_x+1': y_next_day,
                'forcast_y_delta_at_x+1': y_next_day_delta,
                'factor_increase_x+1': factor_increase_next_day
            }
        except (Exception, RuntimeError) as error:
            print(error)
    return d


def series_of_fits(data: list, fit_range: int = 7, max_days_past=14) -> list:
    """
    perform a series of fits: per day on data of 7 days back
    fit_range: fit over how many days
    max_days_past: how far in the past shall we go
    = (fitted in range [x-6, x])
    returns dict: day -> doubling_time
    """
    fit_series_res = {}
    # remove y=0 values until first non-null
    while len(data) > 0 and data[0][1] == 0:
        data.pop(0)
    if len(data) >= 3:
        for last_day_for_fit in range(0, -max_days_past, -1):
            d = fit_routine(
                data, (last_day_for_fit-fit_range, last_day_for_fit))
            # d is empty if fit fails
            if len(d) != 0:
                # douplication_time -> dict
                fit_series_res[last_day_for_fit] = round(d['fit_res'][1], 1)
    return fit_series_res
