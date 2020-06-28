#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import re
import requests  # for read_url_or_cachefile


# my helper modules
import helper


url = 'https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table'
cachefile = 'cache/de-divi/list-csv-page-1.html'
payload = {"filter_order_Dir": "DESC",
           "filter_order": "tbl.ordering",
           "start": 0}
# "cid[]": "0", "category_id": "54", "task": "", "8ba87835776d29f4e379a261512319f1": "1"


cont = helper.read_url_or_cachefile(
    url=url, cachefile=cachefile, request_type='post', payload=payload, cache_max_age=900, verbose=True)


# extract link of from <a href="/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-28-12-15/download"

def extractLinkList(cont: str) -> list:
    myPattern = '<a href="(/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-[^"]+/download)"'
    myRegExp = re.compile(myPattern)
    myMatches = myRegExp.findall(cont)
    return myMatches


l_csv_urls = extractLinkList(cont=cont)

# reduce list to the 5 latest files
while len(l_csv_urls) > 5:
    l_csv_urls.pop()

d_csvs_to_fetch = {}

# loop over urls to replaces outdated files by latest file per day
# '/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-25-12-15/download'
# '/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-25-12-15-2/download'
for url in l_csv_urls:
    url = f"https://www.divi.de{url}"
    filename = re.search(
        '/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-(\d{4}\-\d{2}\-\d{2})[^/]+/download$', url).group(1)
    d_csvs_to_fetch[filename] = url
del l_csv_urls

for filename, url in d_csvs_to_fetch.items():
    cachefile = f"data/de-divi/csv/{filename}.csv"
    cont = helper.read_url_or_cachefile(
        url=url, cachefile=cachefile, request_type='get', payload={}, cache_max_age=900, verbose=True)


pass
