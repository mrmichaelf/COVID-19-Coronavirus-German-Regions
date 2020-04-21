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


date_last = system("tail -1 '../data/de-states/de-state-BW.tsv' | cut -f2")
set label 1 label1_text_right." based on RKI data of ".date_last

title = "Zeitverlauf der Infektionen in den Bundesländern"
set title title
set ylabel "Infektionen"


set yrange [0:]
set output '../plots-gnuplot/de-states/cases-de-absolute.png'
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Cases")) title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Cases")) title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Cases")) title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Cases")) title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Cases")) title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Cases")) title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Cases")) title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Cases")) title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Cases")) title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Cases")) title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Cases")) title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Cases")) title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Cases")) title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Cases")) title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Cases")) title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Cases")) title "Bremen" with lines lw 2 dt "-", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases")) title "Deutschland" with lines , \

set yrange [1:]
set logscale y

set title title ." - Logarithmische Skalierung"
set output '../plots-gnuplot/de-states/cases-de-absolute-log.png'
replot
unset output
unset logscale y


title = "Zeitverlauf der Infektionen in den Bundesländer pro 1 Mill Einwohner"
set title title
set ylabel "Infizierte pro 1 Millionen Einwohner"
set yrange [0:]
set output '../plots-gnuplot/de-states/cases-de-per-million.png'
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Deutschland" with lines lw 4 dt 1, \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases")) title "Deutschland" with lines , \

set yrange [1:]
set logscale y
set title title ." - log. Skalierung"
set output '../plots-gnuplot/de-states/cases-de-per-million-log.png'
replot
unset output
unset logscale y



title = "Zeitverlauf der täglichen Neu-Infektionen in den Bundesländer pro 1 Mill Einwohner"
set title title
set ylabel "Täglich neu Infizierte pro 1 Millionen Einwohner"
set yrange [0:]
set output '../plots-gnuplot/de-states/cases-de-new-per-million.png'
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Deutschland" with lines lw 4 dt 1, \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases")) title "Deutschland" with lines , \

set yrange [1:]
set logscale y
set title title ." - log. Skalierung"
set output '../plots-gnuplot/de-states/cases-de-new-per-million-log.png'
replot
unset output
unset logscale y



