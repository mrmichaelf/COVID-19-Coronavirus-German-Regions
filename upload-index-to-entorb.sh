#!/bin/bash

rsync -rvhu --delete --delete-excluded --no-perms index-reset.html entorb@entorb.net:html/COVID-19-coronavirus/
rsync -rvhu --delete --delete-excluded --no-perms eCharts/myHelper-reset.js entorb@entorb.net:html/COVID-19-coronavirus/eCharts/

rsync -rvhu --delete --delete-excluded --no-perms index.html entorb@entorb.net:html/COVID-19-coronavirus/
rsync -rvhu --delete --delete-excluded --no-perms eCharts/myHelper.js entorb@entorb.net:html/COVID-19-coronavirus/eCharts/


rsync -rvhu --delete --delete-excluded --no-perms index-nav*.html entorb@entorb.net:html/COVID-19-coronavirus/

