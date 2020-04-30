#!/bin/bash

# fetch current index.html
wget -q -O index-online.html https://entorb.net/COVID-19-coronavirus/index.html 

# fetching and generating new data
python fetch-de-states-data.py
python fetch-de-divi-V2.py
python fetch-de-districts.py
python fetch-int-country-data.py

# IDEA: run in background processes via appending &


# plotting
rm plots-gnuplot/*/*.png
cd scripts-gnuplot
gnuplot all.gp
bash upload-to-entorb.sh
cd ..

# uploading data # (after plotting because gnuplot generates 2 data files as well)
cd data
bash upload-to-entorb.sh
cd ..

# reporting
echo Date Int-Countries: `tail -1 data/int/countries-latest-selected.tsv | cut -f2`
echo Date DE-States: `tail -1 data/de-states/de-states-latest.tsv | cut -f5`

echo "Check local html. Enter to close, CTRG+C to cancel"
read ok

# git add .
# git add data/*
# git add plot-gnuplot/*
# git commit -m "update"
# git push

# cd dir_old