#!/bin/bash

# dir_old=$PWD
# dir_of_this_script="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# cd dir_of_this_script


wget -q -O index-online.html https://entorb.net/COVID-19-coronavirus/index.html 

python fetch-int-country-data.py
echo Date Int-Countries: `tail -1 data/int/countries-latest-selected.tsv | cut -f2`

echo "shall we continue?"
read ok

rsync -rvhu --delete --delete-excluded data/* entorb@entorb.net:html/COVID-19-coronavirus/data/
rsync -rvhu --delete --delete-excluded plots-gnuplot/* entorb@entorb.net:html/COVID-19-coronavirus/plots-gnuplot/

rm plots-gnuplot/int/*.png
cd scripts-gnuplot
gnuplot plot-countries.gp
cd ..


python fetch-de-states-data.py
echo Date DE-States: `tail -1 data/de-states/de-states-latest.tsv | cut -f5`
echo "shall we continue?"
read ok

rsync -rvhu --delete --delete-excluded data/* entorb@entorb.net:html/COVID-19-coronavirus/data/

rm plots-gnuplot/de-states/*.png
cd scripts-gnuplot
gnuplot plot-de.gp
cd ..

# firefox index-online.html

echo "Check local html. Enter to continue with upoading, CTRG+C to cancel"
read ok


# python fetch-de-districts.py
# python fetch-de-divi.py

rsync -rvhu --delete --delete-excluded plots-gnuplot/* entorb@entorb.net:html/COVID-19-coronavirus/plots-gnuplot/
# rsync -rvhu --delete --delete-excluded plots-excel/* entorb@entorb.net:html/COVID-19-coronavirus/plots-excel/

rsync -rvhu results-de-districts.html entorb@entorb.net:html/COVID-19-coronavirus/results-de-districts.html

# git add .
# git commit -m "update 24.04."
# git push

# cd dir_old