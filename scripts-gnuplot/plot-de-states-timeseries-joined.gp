# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set terminal pngcairo size 640,800


set title ""
# set xlabel "Datum"

# now lets compare several stats
set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
set format x '%d.%m'
set xdata time

# TODO:
# set term windows


set key top left at graph 0, graph 1

set colorsequence default
unset style # reset line styles/types to default


date_last = system("tail -1 '../data/de-states/de-states-BW.tsv' | cut -f2")
set label 1 label1_text_right." based on RKI data of ".date_last

title = "Zeitverlauf der Infektionen in den Bundesländern"
set title title
set ylabel "Infektionen"

set yrange [0:]
set output '../plots-gnuplot/cases-de-absolute.png'
plot \
  '../data/de-states/de-states-NW.tsv' using 2:3 title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-states-BY.tsv' using 2:3 title "Bayern" with lines lw 2, \
  '../data/de-states/de-states-BW.tsv' using 2:3 title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-states-NI.tsv' using 2:3 title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-states-HE.tsv' using 2:3 title "Hessen" with lines lw 2, \
  '../data/de-states/de-states-RP.tsv' using 2:3 title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-states-BE.tsv' using 2:3 title "Berlin" with lines lw 2, \
  '../data/de-states/de-states-HH.tsv' using 2:3 title "Hamburg" with lines lw 2, \
  '../data/de-states/de-states-SN.tsv' using 2:3 title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-states-SH.tsv' using 2:3 title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-states-BB.tsv' using 2:3 title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-states-TH.tsv' using 2:3 title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-states-ST.tsv' using 2:3 title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-states-SL.tsv' using 2:3 title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-states-MV.tsv' using 2:3 title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-states-HB.tsv' using 2:3 title "Bremen" with lines lw 2 dt "-", \

unset output
#  '../data/de-states/de-states-DE-total.tsv' using 2:3 title "Deutschland" with lines , \

set yrange [1:]
set logscale y

set title title ." - Logarithmische Skalierung"
set output '../plots-gnuplot/cases-de-absolute-log.png'
replot
unset output
unset logscale y


title = "Zeitverlauf der Infektionen in den Bundesländer pro 1 Mill Einwohner"
set title title
set ylabel "Infizierte pro 1 Millionen Einwohner"
set yrange [0:]
set output '../plots-gnuplot/cases-de-per-million.png'
plot \
  '../data/de-states/de-states-NW.tsv' using 2:7 title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-states-BY.tsv' using 2:7 title "Bayern" with lines lw 2, \
  '../data/de-states/de-states-BW.tsv' using 2:7 title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-states-NI.tsv' using 2:7 title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-states-HE.tsv' using 2:7 title "Hessen" with lines lw 2, \
  '../data/de-states/de-states-RP.tsv' using 2:7 title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-states-BE.tsv' using 2:7 title "Berlin" with lines lw 2, \
  '../data/de-states/de-states-HH.tsv' using 2:7 title "Hamburg" with lines lw 2, \
  '../data/de-states/de-states-SN.tsv' using 2:7 title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-states-SH.tsv' using 2:7 title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-states-BB.tsv' using 2:7 title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-states-TH.tsv' using 2:7 title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-states-ST.tsv' using 2:7 title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-states-SL.tsv' using 2:7 title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-states-MV.tsv' using 2:7 title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-states-HB.tsv' using 2:7 title "Bremen" with lines lw 2 dt "-", \

unset output
#  '../data/de-states/de-states-DE-total.tsv' using 2:3 title "Deutschland" with lines , \

set yrange [1:]
set logscale y
set title title ." - log. Skalierung"
set output '../plots-gnuplot/cases-de-per-million-log.png'
replot
unset output
unset logscale y







# set logscale y
# # set format y "10^{%L}"
# set title title ." - Logarithmische Skalierung"
# set output '../plots-gnuplot/cases-de-log.png'
# replot
# unset output
# unset logscale y
# unset xdata

# unset timefmt
# unset format
# unset xdata 