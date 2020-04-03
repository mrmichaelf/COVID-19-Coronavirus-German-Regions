#!/bin/bash

# dir_old=$PWD
# dir_of_this_script="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# cd dir_of_this_script

python fetch-int-country-data.py
python fetch-de-states-data.py
rm plots-gnuplot/*.png
cd scripts-gnuplot
gnuplot plot-de.gp
gnuplot plot-countries.gp
cd ..


wget -q -O index-online.html https://entorb.net/COVID-19-coronavirus/index.html 

echo Date DE-States: `tail -1 data/de-states/de-states-latest.tsv | cut -f5`
echo Date Int-Countries: `tail -1 data/countries-latest-selected.tsv | cut -f2`


# firefox index-online.html

echo "Check local html. Enter to continue with upoading, CTRG+C to cancel"
read ok

rsync -rvhu --delete --delete-excluded plots-gnuplot/*.png entorb@entorb.net:html/COVID-19-coronavirus/plots-gnuplot/
rsync -rvhu --delete --delete-excluded plots-excel/*.png entorb@entorb.net:html/COVID-19-coronavirus/plots-excel/

# git add .
# git commit -m "update 24.04."
# git push

# cd dir_old