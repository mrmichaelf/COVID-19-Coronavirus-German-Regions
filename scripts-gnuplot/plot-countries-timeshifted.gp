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


last_x_AT = (system("tail -1 '../data/int/country-AT.tsv' | cut -f15") + 0)
last_y_AT_pm = (system("tail -1 '../data/int/country-AT.tsv' | cut -f8") + 0)
last_y_absolute_AT = (system("tail -1 '../data/int/country-AT.tsv' | cut -f4") + 0)
last_y_new_per_million_AT = (system("tail -1 '../data/int/country-AT.tsv' | cut -f10") + 0)

last_x_BE = (system("tail -1 '../data/int/country-BE.tsv' | cut -f15") + 0)
last_y_BE_pm = (system("tail -1 '../data/int/country-BE.tsv' | cut -f8") + 0)
last_y_absolute_BE = (system("tail -1 '../data/int/country-BE.tsv' | cut -f4") + 0)
last_y_new_per_million_BE = (system("tail -1 '../data/int/country-BE.tsv' | cut -f10") + 0)

last_x_CA = (system("tail -1 '../data/int/country-CA.tsv' | cut -f15") + 0)
last_y_CA_pm = (system("tail -1 '../data/int/country-CA.tsv' | cut -f8") + 0)
last_y_absolute_CA = (system("tail -1 '../data/int/country-CA.tsv' | cut -f4") + 0)
last_y_new_per_million_CA = (system("tail -1 '../data/int/country-CA.tsv' | cut -f10") + 0)

last_x_FR = (system("tail -1 '../data/int/country-FR.tsv' | cut -f15") + 0)
last_y_FR_pm = (system("tail -1 '../data/int/country-FR.tsv' | cut -f8") + 0)
last_y_absolute_FR = (system("tail -1 '../data/int/country-FR.tsv' | cut -f4") + 0)
last_y_new_per_million_FR = (system("tail -1 '../data/int/country-FR.tsv' | cut -f10") + 0)

last_x_DE = (system("tail -1 '../data/int/country-DE.tsv' | cut -f15") + 0)
last_y_DE_pm = (system("tail -1 '../data/int/country-DE.tsv' | cut -f8") + 0)
last_y_absolute_DE = (system("tail -1 '../data/int/country-DE.tsv' | cut -f4") + 0)
last_y_new_per_million_DE = (system("tail -1 '../data/int/country-DE.tsv' | cut -f10") + 0)

last_x_HU = (system("tail -1 '../data/int/country-HU.tsv' | cut -f15") + 0)
last_y_HU_pm = (system("tail -1 '../data/int/country-HU.tsv' | cut -f8") + 0)
last_y_absolute_HU = (system("tail -1 '../data/int/country-HU.tsv' | cut -f4") + 0)
last_y_new_per_million_HU = (system("tail -1 '../data/int/country-HU.tsv' | cut -f10") + 0)

last_x_IR = (system("tail -1 '../data/int/country-IR.tsv' | cut -f15") + 0)
last_y_IR_pm = (system("tail -1 '../data/int/country-IR.tsv' | cut -f8") + 0)
last_y_absolute_IR = (system("tail -1 '../data/int/country-IR.tsv' | cut -f4") + 0)
last_y_new_per_million_IR = (system("tail -1 '../data/int/country-IR.tsv' | cut -f10") + 0)

last_x_IT = (system("tail -1 '../data/int/country-IT.tsv' | cut -f15") + 0)
last_y_IT_pm = (system("tail -1 '../data/int/country-IT.tsv' | cut -f8") + 0)
last_y_absolute_IT = (system("tail -1 '../data/int/country-IT.tsv' | cut -f4") + 0)
last_y_new_per_million_IT = (system("tail -1 '../data/int/country-IT.tsv' | cut -f10") + 0)

last_x_JP = (system("tail -1 '../data/int/country-JP.tsv' | cut -f15") + 0)
last_y_JP_pm = (system("tail -1 '../data/int/country-JP.tsv' | cut -f8") + 0)
last_y_absolute_JP = (system("tail -1 '../data/int/country-JP.tsv' | cut -f4") + 0)
last_y_new_per_million_JP = (system("tail -1 '../data/int/country-JP.tsv' | cut -f10") + 0)

last_x_KR = (system("tail -1 '../data/int/country-KR.tsv' | cut -f15") + 0)
last_y_KR_pm = (system("tail -1 '../data/int/country-KR.tsv' | cut -f8") + 0)
last_y_absolute_KR = (system("tail -1 '../data/int/country-KR.tsv' | cut -f4") + 0)
last_y_new_per_million_KR = (system("tail -1 '../data/int/country-KR.tsv' | cut -f10") + 0)

last_x_NL = (system("tail -1 '../data/int/country-NL.tsv' | cut -f15") + 0)
last_y_NL_pm = (system("tail -1 '../data/int/country-NL.tsv' | cut -f8") + 0)
last_y_absolute_NL = (system("tail -1 '../data/int/country-NL.tsv' | cut -f4") + 0)
last_y_new_per_million_NL = (system("tail -1 '../data/int/country-NL.tsv' | cut -f10") + 0)

last_x_PT = (system("tail -1 '../data/int/country-PT.tsv' | cut -f15") + 0)
last_y_PT_pm = (system("tail -1 '../data/int/country-PT.tsv' | cut -f8") + 0)
last_y_absolute_PT = (system("tail -1 '../data/int/country-PT.tsv' | cut -f4") + 0)
last_y_new_per_million_PT = (system("tail -1 '../data/int/country-PT.tsv' | cut -f10") + 0)

last_x_ES = (system("tail -1 '../data/int/country-ES.tsv' | cut -f15") + 0)
last_y_ES_pm = (system("tail -1 '../data/int/country-ES.tsv' | cut -f8") + 0)
last_y_absolute_ES = (system("tail -1 '../data/int/country-ES.tsv' | cut -f4") + 0)
last_y_new_per_million_ES = (system("tail -1 '../data/int/country-ES.tsv' | cut -f10") + 0)

last_x_CH = (system("tail -1 '../data/int/country-CH.tsv' | cut -f15") + 0)
last_y_CH_pm = (system("tail -1 '../data/int/country-CH.tsv' | cut -f8") + 0)
last_y_absolute_CH = (system("tail -1 '../data/int/country-CH.tsv' | cut -f4") + 0)
last_y_new_per_million_CH = (system("tail -1 '../data/int/country-CH.tsv' | cut -f10") + 0)

last_x_UK = (system("tail -1 '../data/int/country-GB.tsv' | cut -f15") + 0)
last_y_UK_pm = (system("tail -1 '../data/int/country-GB.tsv' | cut -f8") + 0)
last_y_absolute_UK = (system("tail -1 '../data/int/country-GB.tsv' | cut -f4") + 0)
last_y_new_per_million_UK = (system("tail -1 '../data/int/country-GB.tsv' | cut -f10") + 0)

last_x_US = (system("tail -1 '../data/int/country-US.tsv' | cut -f15") + 0)
last_y_US_pm = (system("tail -1 '../data/int/country-US.tsv' | cut -f8") + 0)
last_y_absolute_US = (system("tail -1 '../data/int/country-US.tsv' | cut -f4") + 0)
last_y_new_per_million_US = (system("tail -1 '../data/int/country-US.tsv' | cut -f10") + 0)

last_x_SE = (system("tail -1 '../data/int/country-SE.tsv' | cut -f15") + 0)
last_y_SE_pm = (system("tail -1 '../data/int/country-SE.tsv' | cut -f8") + 0)
last_y_absolute_SE = (system("tail -1 '../data/int/country-SE.tsv' | cut -f4") + 0)
last_y_new_per_million_SE = (system("tail -1 '../data/int/country-SE.tsv' | cut -f10") + 0)





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
set label 27 "SE" left at first last_x_SE/7.0 , first last_y_absolute_SE


set xrange [0:]
set yrange [0:]
set output '../plots-gnuplot/int/countries-timeshifted-absolute.png'
plot \
  '../data/int/country-IT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Austria" with lines lw 2, \
  '../data/int/country-GB.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-JP.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-SE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths")) title "Sweden" with lines lw 2 dt ".",\

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


set label 11 "AT" left at first last_x_AT/7.0 , first last_y_AT_pm
set label 12 "BE" left at first last_x_BE/7.0 , first last_y_BE_pm
set label 13 "CA" left at first last_x_CA/7.0 , first last_y_CA_pm
set label 14 "FR" left at first last_x_FR/7.0 , first last_y_FR_pm
set label 15 "DE" left at first last_x_DE/7.0 , first last_y_DE_pm
set label 16 "HU" left at first last_x_HU/7.0 , first last_y_HU_pm
set label 17 "IR" left at first last_x_IR/7.0 , first last_y_IR_pm
set label 18 "IT" left at first last_x_IT/7.0 , first last_y_IT_pm
set label 19 "JP" left at first last_x_JP/7.0 , first last_y_JP_pm
set label 20 "KR" left at first last_x_KR/7.0 , first last_y_KR_pm
set label 21 "NL" left at first last_x_NL/7.0 , first last_y_NL_pm
set label 22 "PT" left at first last_x_PT/7.0 , first last_y_PT_pm
set label 23 "ES" left at first last_x_ES/7.0 , first last_y_ES_pm
set label 24 "CH" left at first last_x_CH/7.0 , first last_y_CH_pm
set label 25 "UK" left at first last_x_UK/7.0 , first last_y_UK_pm
set label 26 "US" left at first last_x_US/7.0 , first last_y_US_pm
set label 27 "SE" left at first last_x_SE/7.0 , first last_y_SE_pm





output = '../plots-gnuplot/int/countries-timeshifted-per-million.png'
set xrange [0:]
# TODO:
# set yrange [0:2000]
set yrange [0:]
set output output
plot \
  '../data/int/country-IT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Austria" with lines lw 2, \
  '../data/int/country-GB.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-JP.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-SE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_Per_Million")) title "Sweden" with lines lw 2 dt ".", \

unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output output
replot
unset output

# TODO
# set yrange [1:2000]
set yrange [1:]
set logscale y
set logscale y2
title = "Death toll development - scaled per million population and log"
set title title
output = '../plots-gnuplot/int/countries-timeshifted-per-million-log.png'
set output = output
replot
unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output output
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
set label 27 "SE" left at first last_x_SE/7.0 , first last_y_new_per_million_SE


unset y2tics
set y2tics add ("US 9/11" 9,"1,5%% pop die\na year\nper day" 1000000.0*0.015/365)
set y2tics add ("US cancer\nper day" 1857.0/365)



set xrange [0:]
set yrange [0:]
output = '../plots-gnuplot/int/countries-timeshifted-new_deaths-per-million.png'
set output output
plot \
  '../data/int/country-IT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Austria" with lines lw 2, \
  '../data/int/country-GB.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-JP.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-SE.tsv' using (column("Days_Since_2nd_Death")/7):(column("Deaths_New_Per_Million")) smooth bezier title "Sweden" with lines lw 2 dt ".",\

unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output output
replot
unset output


# Log plot
set y2tics add ("US guns\nper day" 44.0/365, "US traffic \nor flu\nper day" 104.0/365, "US drugs\nper day" 205.0/365 , "US cancer\nper day" 1857.0/365)

set yrange [0.01:]
set logscale y
set logscale y2
set title title ." - log. scaled"
output= '../plots-gnuplot/int/countries-timeshifted-new_deaths-per-million-log.png'
set output output
replot
unset output
# replot to set y2range accordingly to yrange
set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output output
replot
unset output

unset logscale y


set xtics autofreq