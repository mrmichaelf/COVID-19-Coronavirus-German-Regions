# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set terminal pngcairo size 640,800


set title ""
set ylabel "Deaths per Million Population"
set xlabel "Days since 2nd death"

# # now lets compare several stats
# set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
# set format x '%m-%d'
# set xdata time

# TODO:
set term windows


set key top left at graph 0, graph 1

set colorsequence default
unset style # reset line styles/types to default


date_last = system("tail -1 '../data/country-DE.tsv' | cut -f2")
set label 1 label1_text_right." based on JHU data of ".date_last


last_x_IT = (system("tail -1 '../data/country-IT.tsv' | cut -f10") + 0)
last_y_IT = (system("tail -1 '../data/country-IT.tsv' | cut -f6") + 0)
set label 21 "IT" left at first last_x_IT, first last_y_IT

title = "How did the death toll develop in selected countries?"
set title title

#set xrange [0:]
#set yrange [0:]
set output '../plots-gnuplot/countries-timeshifted-per-Million.png'
plot \
  '../data/country-IT.tsv' using 10:6 title "Italy" with lines lw 2, \
  '../data/country-IR.tsv' using 10:6 title "Iran" with lines lw 2, \
  '../data/country-DE.tsv' using 10:6 title "Germany" with lines lw 2, \
  '../data/country-FR.tsv' using 10:6 title "France" with lines lw 2, \
  '../data/country-ES.tsv' using 10:6 title "Spain" with lines lw 2, \
  '../data/country-AT.tsv' using 10:6 title "Austria" with lines lw 2, \
  '../data/country-JP.tsv' using 10:6 title "Japan" with lines lw 2, \
  '../data/country-KR.tsv' using 10:6 title "Korea, South" with lines lw 2,\
  '../data/country-BE.tsv' using 10:6 title "Belgium" with lines lw 2 dt "-", \
  '../data/country-CA.tsv' using 10:6 title "Canada" with lines lw 2 dt "-", \
  '../data/country-HU.tsv' using 10:6 title "Hungary" with lines lw 2 dt "-", \
  '../data/country-NL.tsv' using 10:6 title "Netherlands" with lines lw 2 dt "-", \
  '../data/country-PT.tsv' using 10:6 title "Portugal" with lines lw 2 dt "-", \
  '../data/country-CH.tsv' using 10:6 title "Switzerland" with lines lw 2 dt "-", \
  '../data/country-UK.tsv' using 10:6 title "United Kingdom" with lines lw 2 dt "-", \
  '../data/country-US.tsv' using 10:6 title "US" with lines lw 2 dt "-", \

unset output
# '../data/country-CZ.tsv' using 10:6 title "Czechia" with lines lw 2 dt "-", \
# '../data/country-FI.tsv' using 10:6 title "# Finland" with lines lw 2 dt "-", \
  '../data/country-SE.tsv' using 10:6 title "Sweden" with lines lw 2 dt "-", \

set yrange [:]
set logscale y

set title title ." - Logarithmische Skalierung"
set output '../plots-gnuplot/countries-timeshifted-per-Million-log.png'
replot
unset output
unset logscale y


# title = "Zeitverlauf der Infektionen in den Bundesländer pro 1 Mill Einwohner"
# set title title
# set yrange [0:]
# set output '../plots-gnuplot/cases-de-per-million.png'
# plot \
#   '../data/de-state-NW.tsv' using 2:7 title "Nordrhein-Westfalen" with lines lw 2, \
#   '../data/de-state-BY.tsv' using 2:7 title "Bayern" with lines lw 2, \
#   '../data/de-state-BW.tsv' using 2:7 title "Baden-Württemberg" with lines lw 2, \
#   '../data/de-state-NI.tsv' using 2:7 title "Niedersachsen" with lines lw 2, \
#   '../data/de-state-HE.tsv' using 2:7 title "Hessen" with lines lw 2, \
#   '../data/de-state-RP.tsv' using 2:7 title "Rheinland-Pfalz" with lines lw 2, \
#   '../data/de-state-BE.tsv' using 2:7 title "Berlin" with lines lw 2, \
#   '../data/de-state-HH.tsv' using 2:7 title "Hamburg" with lines lw 2, \
#   '../data/de-state-SN.tsv' using 2:7 title "Sachsen" with lines lw 2 dt "-", \
#   '../data/de-state-SH.tsv' using 2:7 title "Schleswig-Holstein" with lines lw 2 dt "-", \
#   '../data/de-state-BB.tsv' using 2:7 title "Brandenburg" with lines lw 2 dt "-", \
#   '../data/de-state-TH.tsv' using 2:7 title "Thüringen" with lines lw 2 dt "-", \
#   '../data/de-state-ST.tsv' using 2:7 title "Sachsen-Anhalt" with lines lw 2 dt "-", \
#   '../data/de-state-SL.tsv' using 2:7 title "Saarland" with lines lw 2 dt "-", \
#   '../data/de-state-MV.tsv' using 2:7 title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
#   '../data/de-state-HB.tsv' using 2:7 title "Bremen" with lines lw 2 dt "-", \

# unset output
# #  '../data/de-state-DE-total.tsv' using 2:3 title "Deutschland" with lines , \

# set yrange [1:]
# set logscale y
# set title title ." - log. Skalierung"
# set output '../plots-gnuplot/cases-de-per-million-log.png'
# replot
# unset output
# unset logscale y


