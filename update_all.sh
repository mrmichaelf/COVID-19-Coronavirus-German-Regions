#!/bin/bash
echo === git pull
git pull

echo === fetching index.html -> index-online.html
wget -q -O index-online.html https://entorb.net/COVID-19-coronavirus/index.html 

echo === fetching and generating new data
python3 fetch-de-states-data.py
python3 fetch-de-divi-V2.py
python3 fetch-de-districts.py
python3 fetch-int-country-data.py

# IDEA: run in background processes via appending '&'. Problem 1: how to know when ready for plotting? Problem 2: Errors are no longer displayed at the terminal


echo === plotting
rm plots-gnuplot/*/*.png
cd scripts-gnuplot
gnuplot all.gp
bash upload-to-entorb.sh
cd ..

echo  === uploading data
# (after plotting because gnuplot generates 2 data files as well)
cd data
bash upload-to-entorb.sh
cd ..

echo  === date of data
echo Date Int-Countries: `tail -1 data/int/countries-latest-selected.tsv | cut -f2`
echo Date DE-States: `tail -1 data/de-states/de-states-latest.tsv | cut -f5`

echo === Check local html. Enter to close, CTRG+C to cancel
read ok

echo  === git: add and commit
git add data/*
git commit -m "update"
git push
