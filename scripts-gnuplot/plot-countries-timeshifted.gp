# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set terminal pngcairo size 800,800


# # now lets compare several stats
# set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
# set format x '%m-%d'
# set xdata time

# TODO:
# set term windows


set key top left at graph 0, graph 1

set colorsequence default
unset style # reset line styles/types to default



set xtics 1
set xlabel "Weeks since 2nd death reported"

# set lmargin 10

date_last = system("tail -1 '../data/int/country-DE.tsv' | cut -f2")
set label 1 label1_text_right." based on JHU data of ".date_last


last_x_AT = (system("tail -1 '../data/int/country-AT.tsv' | cut -f10") + 0)
last_y_AT = (system("tail -1 '../data/int/country-AT.tsv' | cut -f6") + 0)
last_y_absolute_AT = (system("tail -1 '../data/int/country-AT.tsv' | cut -f4") + 0)
last_y_new_per_million_AT = (system("tail -1 '../data/int/country-AT.tsv' | cut -f13") + 0)

last_x_BE = (system("tail -1 '../data/int/country-BE.tsv' | cut -f10") + 0)
last_y_BE = (system("tail -1 '../data/int/country-BE.tsv' | cut -f6") + 0)
last_y_absolute_BE = (system("tail -1 '../data/int/country-BE.tsv' | cut -f4") + 0)
last_y_new_per_million_BE = (system("tail -1 '../data/int/country-BE.tsv' | cut -f13") + 0)

last_x_CA = (system("tail -1 '../data/int/country-CA.tsv' | cut -f10") + 0)
last_y_CA = (system("tail -1 '../data/int/country-CA.tsv' | cut -f6") + 0)
last_y_absolute_CA = (system("tail -1 '../data/int/country-CA.tsv' | cut -f4") + 0)
last_y_new_per_million_CA = (system("tail -1 '../data/int/country-CA.tsv' | cut -f13") + 0)

last_x_FR = (system("tail -1 '../data/int/country-FR.tsv' | cut -f10") + 0)
last_y_FR = (system("tail -1 '../data/int/country-FR.tsv' | cut -f6") + 0)
last_y_absolute_FR = (system("tail -1 '../data/int/country-FR.tsv' | cut -f4") + 0)
last_y_new_per_million_FR = (system("tail -1 '../data/int/country-FR.tsv' | cut -f13") + 0)

last_x_DE = (system("tail -1 '../data/int/country-DE.tsv' | cut -f10") + 0)
last_y_DE = (system("tail -1 '../data/int/country-DE.tsv' | cut -f6") + 0)
last_y_absolute_DE = (system("tail -1 '../data/int/country-DE.tsv' | cut -f4") + 0)
last_y_new_per_million_DE = (system("tail -1 '../data/int/country-DE.tsv' | cut -f13") + 0)

last_x_HU = (system("tail -1 '../data/int/country-HU.tsv' | cut -f10") + 0)
last_y_HU = (system("tail -1 '../data/int/country-HU.tsv' | cut -f6") + 0)
last_y_absolute_HU = (system("tail -1 '../data/int/country-HU.tsv' | cut -f4") + 0)
last_y_new_per_million_HU = (system("tail -1 '../data/int/country-HU.tsv' | cut -f13") + 0)

last_x_IR = (system("tail -1 '../data/int/country-IR.tsv' | cut -f10") + 0)
last_y_IR = (system("tail -1 '../data/int/country-IR.tsv' | cut -f6") + 0)
last_y_absolute_IR = (system("tail -1 '../data/int/country-IR.tsv' | cut -f4") + 0)
last_y_new_per_million_IR = (system("tail -1 '../data/int/country-IR.tsv' | cut -f13") + 0)

last_x_IT = (system("tail -1 '../data/int/country-IT.tsv' | cut -f10") + 0)
last_y_IT = (system("tail -1 '../data/int/country-IT.tsv' | cut -f6") + 0)
last_y_absolute_IT = (system("tail -1 '../data/int/country-IT.tsv' | cut -f4") + 0)
last_y_new_per_million_IT = (system("tail -1 '../data/int/country-IT.tsv' | cut -f13") + 0)

last_x_JP = (system("tail -1 '../data/int/country-JP.tsv' | cut -f10") + 0)
last_y_JP = (system("tail -1 '../data/int/country-JP.tsv' | cut -f6") + 0)
last_y_absolute_JP = (system("tail -1 '../data/int/country-JP.tsv' | cut -f4") + 0)
last_y_new_per_million_JP = (system("tail -1 '../data/int/country-JP.tsv' | cut -f13") + 0)

last_x_KR = (system("tail -1 '../data/int/country-KR.tsv' | cut -f10") + 0)
last_y_KR = (system("tail -1 '../data/int/country-KR.tsv' | cut -f6") + 0)
last_y_absolute_KR = (system("tail -1 '../data/int/country-KR.tsv' | cut -f4") + 0)
last_y_new_per_million_KR = (system("tail -1 '../data/int/country-KR.tsv' | cut -f13") + 0)

last_x_NL = (system("tail -1 '../data/int/country-NL.tsv' | cut -f10") + 0)
last_y_NL = (system("tail -1 '../data/int/country-NL.tsv' | cut -f6") + 0)
last_y_absolute_NL = (system("tail -1 '../data/int/country-NL.tsv' | cut -f4") + 0)
last_y_new_per_million_NL = (system("tail -1 '../data/int/country-NL.tsv' | cut -f13") + 0)

last_x_PT = (system("tail -1 '../data/int/country-PT.tsv' | cut -f10") + 0)
last_y_PT = (system("tail -1 '../data/int/country-PT.tsv' | cut -f6") + 0)
last_y_absolute_PT = (system("tail -1 '../data/int/country-PT.tsv' | cut -f4") + 0)
last_y_new_per_million_PT = (system("tail -1 '../data/int/country-PT.tsv' | cut -f13") + 0)

last_x_ES = (system("tail -1 '../data/int/country-ES.tsv' | cut -f10") + 0)
last_y_ES = (system("tail -1 '../data/int/country-ES.tsv' | cut -f6") + 0)
last_y_absolute_ES = (system("tail -1 '../data/int/country-ES.tsv' | cut -f4") + 0)
last_y_new_per_million_ES = (system("tail -1 '../data/int/country-ES.tsv' | cut -f13") + 0)

last_x_CH = (system("tail -1 '../data/int/country-CH.tsv' | cut -f10") + 0)
last_y_CH = (system("tail -1 '../data/int/country-CH.tsv' | cut -f6") + 0)
last_y_absolute_CH = (system("tail -1 '../data/int/country-CH.tsv' | cut -f4") + 0)
last_y_new_per_million_CH = (system("tail -1 '../data/int/country-CH.tsv' | cut -f13") + 0)

last_x_UK = (system("tail -1 '../data/int/country-UK.tsv' | cut -f10") + 0)
last_y_UK = (system("tail -1 '../data/int/country-UK.tsv' | cut -f6") + 0)
last_y_absolute_UK = (system("tail -1 '../data/int/country-UK.tsv' | cut -f4") + 0)
last_y_new_per_million_UK = (system("tail -1 '../data/int/country-UK.tsv' | cut -f13") + 0)

last_x_US = (system("tail -1 '../data/int/country-US.tsv' | cut -f10") + 0)
last_y_US = (system("tail -1 '../data/int/country-US.tsv' | cut -f6") + 0)
last_y_absolute_US = (system("tail -1 '../data/int/country-US.tsv' | cut -f4") + 0)
last_y_new_per_million_US = (system("tail -1 '../data/int/country-US.tsv' | cut -f13") + 0)

last_x_SE = (system("tail -1 '../data/int/country-SE.tsv' | cut -f10") + 0)
last_y_SE = (system("tail -1 '../data/int/country-SE.tsv' | cut -f6") + 0)
last_y_absolute_SE = (system("tail -1 '../data/int/country-SE.tsv' | cut -f4") + 0)
last_y_new_per_million_SE = (system("tail -1 '../data/int/country-SE.tsv' | cut -f13") + 0)





title = "Death toll development after 2nd death"
set title title
set ylabel "Deaths"


set label 11 "AT" left at first last_x_AT/7.0 , first last_y_absolute_AT
set label 12 "BE" left at first last_x_BE/7.0 , first last_y_absolute_BE
set label 13 "CA" left at first last_x_CA/7.0 , first last_y_absolute_CA
set label 14 "FR" left at first last_x_FR/7.0 , first last_y_absolute_FR
set label 15 "DE" left at first last_x_DE/7.0 , first last_y_absolute_DE
set label 16 "HU" left at first last_x_HU/7.0 , first last_y_absolute_HU
set label 17 "IR" left at first last_x_IR/7.0 , first last_y_absolute_IR
set label 18 "IT" left at first last_x_IT/7.0 , first last_y_absolute_IT
set label 19 "JP" left at first last_x_JP/7.0 , first last_y_absolute_JP
set label 20 "KR" left at first last_x_KR/7.0 , first last_y_absolute_KR
set label 21 "NL" left at first last_x_NL/7.0 , first last_y_absolute_NL
set label 22 "PT" left at first last_x_PT/7.0 , first last_y_absolute_PT
set label 23 "ES" left at first last_x_ES/7.0 , first last_y_absolute_ES
set label 24 "CH" left at first last_x_CH/7.0 , first last_y_absolute_CH
set label 25 "UK" left at first last_x_UK/7.0 , first last_y_absolute_UK
set label 26 "US" left at first last_x_US/7.0 , first last_y_absolute_US

set label 26 "SE" left at first last_x_SE/7.0 , first last_y_absolute_SE


set xrange [0:]
set yrange [0:]
set output '../plots-gnuplot/int/countries-timeshifted-absolute.png'
plot \
  '../data/int/country-IT.tsv' using ($10/7):4 title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using ($10/7):4 title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using ($10/7):4 title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using ($10/7):4 title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using ($10/7):4 title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using ($10/7):4 title "Austria" with lines lw 2, \
  '../data/int/country-UK.tsv' using ($10/7):4 title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using ($10/7):4 title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using ($10/7):4 title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using ($10/7):4 title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using ($10/7):4 title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using ($10/7):4 title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using ($10/7):4 title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using ($10/7):4 title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-JP.tsv' using ($10/7):4 title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using ($10/7):4 title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-SE.tsv' using ($10/7):4 title "Sweden" with lines lw 2 dt ".",\

unset output

set yrange [1:]
set logscale y
set title title ." - log. scaled"
set output '../plots-gnuplot/int/countries-timeshifted-absolute-log.png'
replot
unset output
unset logscale y



# for per million plots I now try adding y2 tics
set ytics nomirror

# same scale on y and y2 axis (not working for log axis :-()
# set link y2

set y2tics ("US 9/11" 9, "US guns\n2017" 44, "US traffic 2018\nand\nflu 2018/19" 104, "US drugs\n2018" 205 , "US cancer\n2018" 1857)

set rmargin 15

title = "Death toll development - scaled per million population"
set title title
set ylabel "Deaths per Million Population"


set label 11 "AT" left at first last_x_AT/7.0 , first last_y_AT
set label 12 "BE" left at first last_x_BE/7.0 , first last_y_BE
set label 13 "CA" left at first last_x_CA/7.0 , first last_y_CA
set label 14 "FR" left at first last_x_FR/7.0 , first last_y_FR
set label 15 "DE" left at first last_x_DE/7.0 , first last_y_DE
set label 16 "HU" left at first last_x_HU/7.0 , first last_y_HU
set label 17 "IR" left at first last_x_IR/7.0 , first last_y_IR
set label 18 "IT" left at first last_x_IT/7.0 , first last_y_IT
set label 19 "JP" left at first last_x_JP/7.0 , first last_y_JP
set label 20 "KR" left at first last_x_KR/7.0 , first last_y_KR
set label 21 "NL" left at first last_x_NL/7.0 , first last_y_NL
set label 22 "PT" left at first last_x_PT/7.0 , first last_y_PT
set label 23 "ES" left at first last_x_ES/7.0 , first last_y_ES
set label 24 "CH" left at first last_x_CH/7.0 , first last_y_CH
set label 25 "UK" left at first last_x_UK/7.0 , first last_y_UK
set label 26 "US" left at first last_x_US/7.0 , first last_y_US
set label 26 "SE" left at first last_x_SE/7.0 , first last_y_SE






set xrange [0:]
# TODO:
# set yrange [0:2000]
set yrange [0:]
set output '../plots-gnuplot/int/countries-timeshifted-per-million.png'
plot \
  '../data/int/country-IT.tsv' using ($10/7):6 title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using ($10/7):6 title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using ($10/7):6 title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using ($10/7):6 title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using ($10/7):6 title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using ($10/7):6 title "Austria" with lines lw 2, \
  '../data/int/country-UK.tsv' using ($10/7):6 title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using ($10/7):6 title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using ($10/7):6 title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using ($10/7):6 title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using ($10/7):6 title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using ($10/7):6 title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using ($10/7):6 title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using ($10/7):6 title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using ($10/7):6 title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-JP.tsv' using ($10/7):6 title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-SE.tsv' using ($10/7):6 title "Sweden" with lines lw 2 dt ".", \

unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output '../plots-gnuplot/int/countries-timeshifted-per-million.png'
replot
unset output

# TODO
# set yrange [1:2000]
set yrange [1:]
set logscale y
set logscale y2
title = "Death toll development - scaled per million population and log"
set title title
set output '../plots-gnuplot/int/countries-timeshifted-per-million-log.png'
replot
unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output '../plots-gnuplot/int/countries-timeshifted-per-million-log.png'
replot
unset output


unset logscale y
unset logscale y2







title = "Daily new deaths per million after 2nd death"
set title title
set ylabel "Daily new deaths per million"


set label 11 "AT" left at first last_x_AT/7.0 , first last_y_new_per_million_AT
set label 12 "BE" left at first last_x_BE/7.0 , first last_y_new_per_million_BE
set label 13 "CA" left at first last_x_CA/7.0 , first last_y_new_per_million_CA
set label 14 "FR" left at first last_x_FR/7.0 , first last_y_new_per_million_FR
set label 15 "DE" left at first last_x_DE/7.0 , first last_y_new_per_million_DE
set label 16 "HU" left at first last_x_HU/7.0 , first last_y_new_per_million_HU
set label 17 "IR" left at first last_x_IR/7.0 , first last_y_new_per_million_IR
set label 18 "IT" left at first last_x_IT/7.0 , first last_y_new_per_million_IT
set label 19 "JP" left at first last_x_JP/7.0 , first last_y_new_per_million_JP
set label 20 "KR" left at first last_x_KR/7.0 , first last_y_new_per_million_KR
set label 21 "NL" left at first last_x_NL/7.0 , first last_y_new_per_million_NL
set label 22 "PT" left at first last_x_PT/7.0 , first last_y_new_per_million_PT
set label 23 "ES" left at first last_x_ES/7.0 , first last_y_new_per_million_ES
set label 24 "CH" left at first last_x_CH/7.0 , first last_y_new_per_million_CH
set label 25 "UK" left at first last_x_UK/7.0 , first last_y_new_per_million_UK
set label 26 "US" left at first last_x_US/7.0 , first last_y_new_per_million_US
set label 26 "SE" left at first last_x_SE/7.0 , first last_y_new_per_million_SE


unset y2tics
set y2tics add ("US 9/11" 9,"1,5%% pop die\nper year" 1000000.0*0.015/365)


set xrange [0:]
set yrange [0:]
set output '../plots-gnuplot/int/countries-timeshifted-new_deaths-per-million.png'
plot \
  '../data/int/country-IT.tsv' using ($10/7):13 smooth bezier title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using ($10/7):13 smooth bezier title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using ($10/7):13 smooth bezier title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using ($10/7):13 smooth bezier title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using ($10/7):13 smooth bezier title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using ($10/7):13 smooth bezier title "Austria" with lines lw 2, \
  '../data/int/country-UK.tsv' using ($10/7):13 smooth bezier title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using ($10/7):13 smooth bezier title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using ($10/7):13 smooth bezier title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using ($10/7):13 smooth bezier title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using ($10/7):13 smooth bezier title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using ($10/7):13 smooth bezier title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using ($10/7):13 smooth bezier title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using ($10/7):13 smooth bezier title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-JP.tsv' using ($10/7):13 smooth bezier title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using ($10/7):13 smooth bezier title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-SE.tsv' using ($10/7):13 smooth bezier title "Sweden" with lines lw 2 dt ".",\

unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output '../plots-gnuplot/int/countries-timeshifted-new_deaths-per-million.png'
replot
unset output

set yrange [0.01:]
set logscale y
set logscale y2
set title title ." - log. scaled"
set output '../plots-gnuplot/int/countries-timeshifted-new_deaths-per-million-log.png'
replot
unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output '../plots-gnuplot/int/countries-timeshifted-new_deaths-per-million-log.png'
replot
unset output

unset logscale y


set xtics autofreq