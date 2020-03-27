# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set terminal pngcairo size 640,800


set xlabel "Days since 2nd death reported"

# # now lets compare several stats
# set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
# set format x '%m-%d'
# set xdata time

# TODO:
# set term windows


set key top left at graph 0, graph 1

set colorsequence default
unset style # reset line styles/types to default


date_last = system("tail -1 '../data/country-DE.tsv' | cut -f2")
set label 1 label1_text_right." based on JHU data of ".date_last


last_x_AT = (system("tail -1 '../data/country-AT.tsv' | cut -f10") + 0)
last_y_AT = (system("tail -1 '../data/country-AT.tsv' | cut -f6") + 0)
set label 11 "AT" left at first last_x_AT , first last_y_AT

last_x_BE = (system("tail -1 '../data/country-BE.tsv' | cut -f10") + 0)
last_y_BE = (system("tail -1 '../data/country-BE.tsv' | cut -f6") + 0)
set label 12 "BE" left at first last_x_BE, first last_y_BE

last_x_CA = (system("tail -1 '../data/country-CA.tsv' | cut -f10") + 0)
last_y_CA = (system("tail -1 '../data/country-CA.tsv' | cut -f6") + 0)
set label 13 "CA" left at first last_x_CA, first last_y_CA

last_x_FR = (system("tail -1 '../data/country-FR.tsv' | cut -f10") + 0)
last_y_FR = (system("tail -1 '../data/country-FR.tsv' | cut -f6") + 0)
set label 14 "FR" left at first last_x_FR, first last_y_FR

last_x_DE = (system("tail -1 '../data/country-DE.tsv' | cut -f10") + 0)
last_y_DE = (system("tail -1 '../data/country-DE.tsv' | cut -f6") + 0)
set label 15 "DE" left at first last_x_DE, first last_y_DE

last_x_HU = (system("tail -1 '../data/country-HU.tsv' | cut -f10") + 0)
last_y_HU = (system("tail -1 '../data/country-HU.tsv' | cut -f6") + 0)
set label 16 "HU" left at first last_x_HU, first last_y_HU

last_x_IR = (system("tail -1 '../data/country-IR.tsv' | cut -f10") + 0)
last_y_IR = (system("tail -1 '../data/country-IR.tsv' | cut -f6") + 0)
set label 17 "IR" left at first last_x_IR, first last_y_IR

last_x_IT = (system("tail -1 '../data/country-IT.tsv' | cut -f10") + 0)
last_y_IT = (system("tail -1 '../data/country-IT.tsv' | cut -f6") + 0)
set label 18 "IT" left at first last_x_IT, first last_y_IT

last_x_JP = (system("tail -1 '../data/country-JP.tsv' | cut -f10") + 0)
last_y_JP = (system("tail -1 '../data/country-JP.tsv' | cut -f6") + 0)
set label 19 "JP" left at first last_x_JP, first last_y_JP

last_x_KR = (system("tail -1 '../data/country-KR.tsv' | cut -f10") + 0)
last_y_KR = (system("tail -1 '../data/country-KR.tsv' | cut -f6") + 0)
set label 20 "KR" left at first last_x_KR, first last_y_KR

last_x_NL = (system("tail -1 '../data/country-NL.tsv' | cut -f10") + 0)
last_y_NL = (system("tail -1 '../data/country-NL.tsv' | cut -f6") + 0)
set label 21 "NL" left at first last_x_NL, first last_y_NL

last_x_PT = (system("tail -1 '../data/country-PT.tsv' | cut -f10") + 0)
last_y_PT = (system("tail -1 '../data/country-PT.tsv' | cut -f6") + 0)
set label 22 "PT" left at first last_x_PT, first last_y_PT

last_x_ES = (system("tail -1 '../data/country-ES.tsv' | cut -f10") + 0)
last_y_ES = (system("tail -1 '../data/country-ES.tsv' | cut -f6") + 0)
set label 23 "ES" left at first last_x_ES, first last_y_ES

# last_x_SE = (system("tail -1 '../data/country-SE.tsv' | cut -f10") + 0)
# last_y_SE = (system("tail -1 '../data/country-SE.tsv' | cut -f6") + 0)
# set label "SE" left at first last_x_SE, first last_y_SE

last_x_CH = (system("tail -1 '../data/country-CH.tsv' | cut -f10") + 0)
last_y_CH = (system("tail -1 '../data/country-CH.tsv' | cut -f6") + 0)
set label 24 "CH" left at first last_x_CH, first last_y_CH

last_x_UK = (system("tail -1 '../data/country-UK.tsv' | cut -f10") + 0)
last_y_UK = (system("tail -1 '../data/country-UK.tsv' | cut -f6") + 0)
set label 25 "UK" left at first last_x_UK, first last_y_UK

last_x_US = (system("tail -1 '../data/country-US.tsv' | cut -f10") + 0)
last_y_US = (system("tail -1 '../data/country-US.tsv' | cut -f6") + 0)
set label 26 "US" left at first last_x_US, first last_y_US



title = "Death toll development - scaled per million population"
set title title
set ylabel "Deaths per Million Population"

set xrange [0:]
set yrange [:]
set output '../plots-gnuplot/countries-timeshifted-per-million.png'
plot \
  '../data/country-IT.tsv' using 10:6 title "Italy" with lines lw 2, \
  '../data/country-IR.tsv' using 10:6 title "Iran" with lines lw 2, \
  '../data/country-DE.tsv' using 10:6 title "Germany" with lines lw 2, \
  '../data/country-FR.tsv' using 10:6 title "France" with lines lw 2, \
  '../data/country-ES.tsv' using 10:6 title "Spain" with lines lw 2, \
  '../data/country-AT.tsv' using 10:6 title "Austria" with lines lw 2, \
  '../data/country-UK.tsv' using 10:6 title "United Kingdom" with lines lw 2, \
  '../data/country-US.tsv' using 10:6 title "US" with lines lw 2, \
  '../data/country-BE.tsv' using 10:6 title "Belgium" with lines lw 2 dt "-", \
  '../data/country-CA.tsv' using 10:6 title "Canada" with lines lw 2 dt "-", \
  '../data/country-HU.tsv' using 10:6 title "Hungary" with lines lw 2 dt "-", \
  '../data/country-NL.tsv' using 10:6 title "Netherlands" with lines lw 2 dt "-", \
  '../data/country-PT.tsv' using 10:6 title "Portugal" with lines lw 2 dt "-", \
  '../data/country-CH.tsv' using 10:6 title "Switzerland" with lines lw 2 dt "-", \
  '../data/country-JP.tsv' using 10:6 title "Japan" with lines lw 2 dt "-", \
  '../data/country-KR.tsv' using 10:6 title "Korea, South" with lines lw 2 dt "-",\

unset output
# '../data/country-CZ.tsv' using 10:6 title "Czechia" with lines lw 2 dt "-", \
# '../data/country-FI.tsv' using 10:6 title "# Finland" with lines lw 2 dt "-", \
  '../data/country-SE.tsv' using 10:6 title "Sweden" with lines lw 2 dt "-", \

set yrange [:]
set logscale y

title = "Death toll development - scaled per million population and log"
set title title
set output '../plots-gnuplot/countries-timeshifted-per-million-log.png'
replot
unset output
unset logscale y



last_x_AT = (system("tail -1 '../data/country-AT.tsv' | cut -f10") + 0)
last_y_AT = (system("tail -1 '../data/country-AT.tsv' | cut -f4") + 0)
set label 11 "AT" left at first last_x_AT , first last_y_AT

last_x_BE = (system("tail -1 '../data/country-BE.tsv' | cut -f10") + 0)
last_y_BE = (system("tail -1 '../data/country-BE.tsv' | cut -f4") + 0)
set label 12 "BE" left at first last_x_BE, first last_y_BE

last_x_CA = (system("tail -1 '../data/country-CA.tsv' | cut -f10") + 0)
last_y_CA = (system("tail -1 '../data/country-CA.tsv' | cut -f4") + 0)
set label 13 "CA" left at first last_x_CA, first last_y_CA

last_x_FR = (system("tail -1 '../data/country-FR.tsv' | cut -f10") + 0)
last_y_FR = (system("tail -1 '../data/country-FR.tsv' | cut -f4") + 0)
set label 14 "FR" left at first last_x_FR, first last_y_FR

last_x_DE = (system("tail -1 '../data/country-DE.tsv' | cut -f10") + 0)
last_y_DE = (system("tail -1 '../data/country-DE.tsv' | cut -f4") + 0)
set label 15 "DE" left at first last_x_DE, first last_y_DE

last_x_HU = (system("tail -1 '../data/country-HU.tsv' | cut -f10") + 0)
last_y_HU = (system("tail -1 '../data/country-HU.tsv' | cut -f4") + 0)
set label 16 "HU" left at first last_x_HU, first last_y_HU

last_x_IR = (system("tail -1 '../data/country-IR.tsv' | cut -f10") + 0)
last_y_IR = (system("tail -1 '../data/country-IR.tsv' | cut -f4") + 0)
set label 17 "IR" left at first last_x_IR, first last_y_IR

last_x_IT = (system("tail -1 '../data/country-IT.tsv' | cut -f10") + 0)
last_y_IT = (system("tail -1 '../data/country-IT.tsv' | cut -f4") + 0)
set label 18 "IT" left at first last_x_IT, first last_y_IT

last_x_JP = (system("tail -1 '../data/country-JP.tsv' | cut -f10") + 0)
last_y_JP = (system("tail -1 '../data/country-JP.tsv' | cut -f4") + 0)
set label 19 "JP" left at first last_x_JP, first last_y_JP

last_x_KR = (system("tail -1 '../data/country-KR.tsv' | cut -f10") + 0)
last_y_KR = (system("tail -1 '../data/country-KR.tsv' | cut -f4") + 0)
set label 20 "KR" left at first last_x_KR, first last_y_KR

last_x_NL = (system("tail -1 '../data/country-NL.tsv' | cut -f10") + 0)
last_y_NL = (system("tail -1 '../data/country-NL.tsv' | cut -f4") + 0)
set label 21 "NL" left at first last_x_NL, first last_y_NL

last_x_PT = (system("tail -1 '../data/country-PT.tsv' | cut -f10") + 0)
last_y_PT = (system("tail -1 '../data/country-PT.tsv' | cut -f4") + 0)
set label 22 "PT" left at first last_x_PT, first last_y_PT

last_x_ES = (system("tail -1 '../data/country-ES.tsv' | cut -f10") + 0)
last_y_ES = (system("tail -1 '../data/country-ES.tsv' | cut -f4") + 0)
set label 23 "ES" left at first last_x_ES, first last_y_ES

# last_x_SE = (system("tail -1 '../data/country-SE.tsv' | cut -f10") + 0)
# last_y_SE = (system("tail -1 '../data/country-SE.tsv' | cut -f4") + 0)
# set label "SE" left at first last_x_SE, first last_y_SE

last_x_CH = (system("tail -1 '../data/country-CH.tsv' | cut -f10") + 0)
last_y_CH = (system("tail -1 '../data/country-CH.tsv' | cut -f4") + 0)
set label 24 "CH" left at first last_x_CH, first last_y_CH

last_x_UK = (system("tail -1 '../data/country-UK.tsv' | cut -f10") + 0)
last_y_UK = (system("tail -1 '../data/country-UK.tsv' | cut -f4") + 0)
set label 25 "UK" left at first last_x_UK, first last_y_UK

last_x_US = (system("tail -1 '../data/country-US.tsv' | cut -f10") + 0)
last_y_US = (system("tail -1 '../data/country-US.tsv' | cut -f4") + 0)
set label 26 "US" left at first last_x_US, first last_y_US






title = "Death toll development after 2nd death"
set title title
set ylabel "Deaths"

set xrange [0:]
set yrange [:]
set output '../plots-gnuplot/countries-timeshifted-absolute.png'
plot \
  '../data/country-IT.tsv' using 10:4 title "Italy" with lines lw 2, \
  '../data/country-IR.tsv' using 10:4 title "Iran" with lines lw 2, \
  '../data/country-DE.tsv' using 10:4 title "Germany" with lines lw 2, \
  '../data/country-FR.tsv' using 10:4 title "France" with lines lw 2, \
  '../data/country-ES.tsv' using 10:4 title "Spain" with lines lw 2, \
  '../data/country-AT.tsv' using 10:4 title "Austria" with lines lw 2, \
  '../data/country-UK.tsv' using 10:4 title "United Kingdom" with lines lw 2, \
  '../data/country-US.tsv' using 10:4 title "US" with lines lw 2, \
  '../data/country-BE.tsv' using 10:4 title "Belgium" with lines lw 2 dt "-", \
  '../data/country-CA.tsv' using 10:4 title "Canada" with lines lw 2 dt "-", \
  '../data/country-HU.tsv' using 10:4 title "Hungary" with lines lw 2 dt "-", \
  '../data/country-NL.tsv' using 10:4 title "Netherlands" with lines lw 2 dt "-", \
  '../data/country-PT.tsv' using 10:4 title "Portugal" with lines lw 2 dt "-", \
  '../data/country-CH.tsv' using 10:4 title "Switzerland" with lines lw 2 dt "-", \
  '../data/country-JP.tsv' using 10:4 title "Japan" with lines lw 2 dt "-", \
  '../data/country-KR.tsv' using 10:4 title "Korea, South" with lines lw 2 dt "-",\

unset output
# '../data/country-CZ.tsv' using 10:4 title "Czechia" with lines lw 2 dt "-", \
# '../data/country-FI.tsv' using 10:4 title "# Finland" with lines lw 2 dt "-", \
  '../data/country-SE.tsv' using 10:4 title "Sweden" with lines lw 2 dt "-", \

set yrange [:]
set logscale y

set title title ." - log. scaled"
set output '../plots-gnuplot/countries-timeshifted-absolute-log.png'
replot
unset output
unset logscale y
