#!/bin/bash

rsync -rvhu --delete --delete-excluded --no-perms index.html entorb@entorb.net:html/COVID-19-coronavirus/
rsync -rvhu --delete --delete-excluded --no-perms eCharts/myHelper.js entorb@entorb.net:html/COVID-19-coronavirus/eCharts/
