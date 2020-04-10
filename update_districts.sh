#!/bin/bash

python fetch-de-districts.py
rsync -rvhu --delete --delete-excluded data/* entorb@entorb.net:html/COVID-19-coronavirus/data/
