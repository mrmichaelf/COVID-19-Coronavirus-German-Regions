#!/bin/bash

rsync -rvhu --delete --delete-excluded --no-perms ../data/* entorb@entorb.net:html/COVID-19-coronavirus/data/
