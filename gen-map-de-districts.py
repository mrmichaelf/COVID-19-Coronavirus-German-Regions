#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Based on
# https://raw.githubusercontent.com/ythlev/covid-19/master/run.py
# by Chang Chia-huan

import os
import sys
import glob
import subprocess
# import argparse
# import pathlib
import json
# import csv
# import io
# import urllib.request
# import urllib.parse
import math
import statistics
# import datetime
import re
# my helper modules
import helper

unit = 1000000


def run_imagemagick_convert(l_imagemagick_parameters: list, wait_for_finish: bool = True):
    """
    wait_for_finish = False: the calling function needs to handle the returned process
    """
    # prepend 'convert'
    l_imagemagick_parameters.insert(0, 'convert')
    if os.name == 'posix':
        # print ('posix/Unix/Linux')
        1
    elif os.name == 'nt':
        # print ('Windows')
        # prepend 'magick
        l_imagemagick_parameters.insert(0, 'magick')
    else:
        print('unknown os')
        sys.exit(1)  # throws exception, use quit() to close silently

    process = subprocess.Popen(l_imagemagick_parameters,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    if wait_for_finish:
        stdout, stderr = process.communicate()
        if stdout != '':
            print(f'Out: {stdout}')
        if stderr != '':
            print(f'ERROR: {stderr}')
    return process


# https://www.w3schools.com/colors/colors_picker.asp
d_color_scales = {
    'template': [
        "#fee5d9", "#fcbba1", "#fc9272", "#fb6a4a", "#de2d26", "#a50f15"
    ],
    'blue': [
        '#e6e6ff',
        '#b3b3ff',
        '#8080ff',
        '#4d4dff',
        '#1a1aff',
        '#0000e6'
    ],
    'red':
    [
        '#ffe6e6',
        '#ffb3b3',
        '#ff8080',
        '#ff4d4d',
        '#ff1a1a',
        '#cc0000'
    ]
}

d_all_date_data = {}
l_month = []
count = 0
for f in glob.glob('data/de-districts/de-district_timeseries-*.json'):
    count += 1
    lk_id = int(re.search('^.*de-district_timeseries\-(\d+)\.json$', f).group(1))
    l = helper.read_json_file(f)
    for d in l:
        date = d['Date']
        thisMonth = date[0:7]
        # skip old data points
        if thisMonth in ('2020-01', '2020-02'):
            continue
        # add to list of months for later creations of 1 gif per month
        if count == 1:
            if thisMonth not in l_month:
                l_month.append(thisMonth)
        if not d['Date'] in d_all_date_data:
            d_all_date_data[d['Date']] = {}
        del d['Timestamp'], d['Date'], d['Days_Past'], d['Days_Since_2nd_Death']
        d_all_date_data[date][lk_id] = d
del f, d, l, count

# check if last date has as many values as the 2nd last, of not drop it
dates = sorted(d_all_date_data.keys())
if len(d_all_date_data[dates[-1]]) != len(d_all_date_data[dates[-2]]):
    print("WARNING: last date is incomplete, so removing it")
    del d_all_date_data[dates[-1]]
del dates


# property_to_plot = 'Deaths_Last_Week_Per_Million'
l_subprocesses = []
d_latest_svg_file = {}  # store the last generated file per property
for property_to_plot in ('Cases_Last_Week_Per_Million', 'Cases_Per_Million', 'DIVI_Intensivstationen_Covid_Prozent'):

    if property_to_plot == 'Cases_Last_Week_Per_Million':
        meta = {"colour": d_color_scales['blue']}
    elif property_to_plot == 'Cases_Per_Million':
        meta = {"colour": d_color_scales['red']}
    elif property_to_plot == 'DIVI_Intensivstationen_Covid_Prozent':
        meta = {"colour": d_color_scales['template']}

    values = []
    # collect all values for autoscaling
    # TODO filter here on selecten month as well?
    for date_str, l_districts in d_all_date_data.items():
        for lk_id, d in l_districts.items():
            values.append(d[property_to_plot])
    del d, l_districts, lk_id

    # generate color scale range
    q = statistics.quantiles(values, n=100, method="inclusive")
    step = math.sqrt(statistics.mean(values) - q[0]) / 3
    threshold = [0, 0, 0, 0, 0, 0]
    for i in range(1, 6):
        threshold[i] = math.pow(i * step, 2) + q[0]
    del q, step, i

    with open('maps/template_de-districts.svg', mode="r", newline="", encoding="utf-8") as file_in:
        # plot loop for each date
        # date_str = '2020-04-24'
        # l_districts = d_all_date_data[date_str]
        for date_str, l_districts in d_all_date_data.items():
            file_in.seek(0, 0)  # reset file pointer
            main = {}
            for lk_id, d in l_districts.items():
                area = lk_id
                pcapita = d[property_to_plot]
                main[area] = {'pcapita': pcapita}

            outfile = f'maps/out/de-districts/{property_to_plot}-{date_str}.svg'
            # overwrittin per date, until it holds the latest file
            d_latest_svg_file[property_to_plot] = outfile

            # skip svg generation if I have not cleaned up, for faster gif generation debugging
            if os.path.isfile(outfile):
                continue

            with open(outfile, mode="w", newline="", encoding="utf-8") as file_out:
                if threshold[5] >= 10000:
                    num = "{:_.0f}"
                elif threshold[1] >= 10:
                    num = "{:.0f}"
                else:
                    num = "{:.2f}"

                for row in file_in:
                    written = False
                    for area in main:
                        if row.find('id="{}"'.format(area)) > -1:
                            i = 0
                            while i < 5:
                                if main[area]["pcapita"] >= threshold[i + 1]:
                                    i += 1
                                else:
                                    break
                            file_out.write(row.replace('id="{}"'.format(
                                area), 'style="fill:{}"'.format(meta["colour"][i])))
                            written = True
                            break
                    if written == False:
                        if row.find('>Date') > -1:
                            file_out.write(row.replace(
                                'Date', date_str))
                        elif row.find('>level') > -1:
                            for i in range(6):
                                if row.find('level{}'.format(i)) > -1:
                                    if i == 0:
                                        file_out.write(row.replace('level{}'.format(
                                            i), "&lt; " + num.format(threshold[1]).replace("_", "&#8201;")))
                                    else:
                                        file_out.write(row.replace('level{}'.format(
                                            i), "≥ " + num.format(threshold[i]).replace("_", "&#8201;")))
                        elif row.find('<path fill="#') > -1:
                            s = row
                            for i in range(6):
                                s = s.replace(
                                    d_color_scales["template"][i], meta["colour"][i])
                            file_out.write(s)
                        # elif row.find('!!!TYPE!!!') > -1:
                        #     if property_to_plot == 'Cases_Last_Week_Per_Million':
                        #         file_out.write(row.replace(
                        #             '!!!TYPE!!!', 'Infizierte'))
                        #     elif property_to_plot == 'Deaths_Last_Week_Per_Million':
                        #         file_out.write(row.replace(
                        #             '!!!TYPE!!!', 'Verstorbene'))
                        else:
                            file_out.write(row)
        # break
    l_subprocesses = []
    # months are processed to gifs in parallel and later joined
    for month in l_month:
        # convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_Million-2020-03*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_Million-2020-03.gif
        l_imagemagick_parameters = [
            '-size', '480x', f'maps/out/de-districts/{property_to_plot}-{month}*.svg', '-resize', '480x', '-coalesce', '-fuzz', '2%', '+dither', '-layers', 'Optimize', f'maps/out/de-districts/{property_to_plot}-{month}.gif']
        process = run_imagemagick_convert(
            l_imagemagick_parameters, wait_for_finish=False)
        l_subprocesses.append(process)

    # wait for subprocesses to finish
    for process in l_subprocesses:
        stdout, stderr = process.communicate()
        if stdout != '':
            print(f'Out: {stdout}')
        if stderr != '':
            print(f'ERROR: {stderr}')

    outfile = f'maps/de-districts-{property_to_plot}.gif'

    # join monthly gifs
    l_imagemagick_parameters = [
        f'maps/out/de-districts/{property_to_plot}-*.gif', '-coalesce', '-fuzz', '2%', '+dither', '-layers', 'Optimize', outfile
    ]
    run_imagemagick_convert(l_imagemagick_parameters)

    # set delay of 0.25s for all frames
    l_imagemagick_parameters = [
        outfile, '-delay', '250x1000', outfile
    ]
    run_imagemagick_convert(l_imagemagick_parameters)

    # clone last frame and set longer delay time of 2s
    l_imagemagick_parameters = [
        outfile, '(', '-clone', '-1', '-set', 'delay', '2000x1000', ')', outfile
    ]
    run_imagemagick_convert(l_imagemagick_parameters)

    # # create copies with shorter and longer delay
    # # this does not work: all have the same speed :-(
    # delay_variants = (100, 250, 500)
    # for delay in delay_variants:
    #     outfileDelay = f'maps/de-districts-{property_to_plot}-{delay}.gif'
    #     run_imagemagick_convert([
    #         outfile, '-delay', f'{delay}x1000', outfileDelay
    #     ])
    #     run_imagemagick_convert([
    #         outfileDelay, '(', '-clone', '-1', '-set', 'delay', '2000x1000', ')', outfileDelay
    #     ])

    # generate a static image for the latest date
    l_imagemagick_parameters = [
        f'{d_latest_svg_file[property_to_plot]}', '-resize', '480x', '-coalesce', '-fuzz', '2%', '+dither', '-layers', 'Optimize', f'maps/de-districts-{property_to_plot}-latest.gif'
    ]
    run_imagemagick_convert(l_imagemagick_parameters)


# cleanup
for f in glob.glob('maps/out/de-districts/*.gif'):
    os.remove(f)
    pass

for f in glob.glob('maps/out/de-districts/*.svg'):
    os.remove(f)
    pass
