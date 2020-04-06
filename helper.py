"""
Helper functions collections
"""

import os.path
import time
import datetime

import json

import urllib.request

import math
import numpy as np
# curve-fit() function imported from scipy
from scipy.optimize import curve_fit


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
    T = time it takes for t doublication: f(t+T) = 2 x f(t)
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

    # Do the fit
    p0 = [data_y_for_fit[-1], 5.0]  # initial guess of parameters
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
        d = {}
        print(error)
    return d


def series_of_fits(data: list, fit_range: int = 7, max_days_past=14) -> list:
    """
    perform a series of fits: per day on data of 7 days back
    fit_range: fit over how many days
    max_days_past: how far in the past shall we go
    = (fitted in range [x-6, x])
    returns dict: day -> doublication_time
    """
    fit_series_res = {}
    for last_day_for_fit in range(0, -max_days_past, -1):
        d = fit_routine(
            data, (last_day_for_fit-fit_range, last_day_for_fit))
        # d is empty if fit fails
        if len(d) != 0:
            # douplication_time -> dict
            fit_series_res[last_day_for_fit] = round(d['fit_res'][1], 1)
    return fit_series_res
