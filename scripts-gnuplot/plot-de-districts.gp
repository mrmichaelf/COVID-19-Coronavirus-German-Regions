#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"
data = "../data/de-districts/de-districts-zero_cases_last_week.tsv"

set style data lines
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles

# set xlabel "Wochen"

set xdata time
set timefmt "%Y-%m-%d"
set xtics format "%d.%m."
set key off

set yrange [0:412]
set y2range [0:100]
set ytics nomirror
set y2tics (0, 20, 40, 60, 80, 100) nomirror format "%g%%"
unset grid
set grid xtics y2tics

set title "Anzahl der DE Landkreise ohne Neu-Infektion in 7 Tagen"

set output "../plots-gnuplot/de-districts/zero_cases_last_week.png"
plot data u 1:2 axis x1y1 with lines dt 1 

unset output