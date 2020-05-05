#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

# TODO: shall this go to de-states or to int/countries?

load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 3 linetype 7 dt "-" lw 2 linecolor rgb 'black' 




data = '../data/de-states/de-state-DE-total.tsv'
# data = '../data/int/country-DE.tsv'

date_last = system("tail -1 " . data . " | cut -f2")

set label 1 label1_text_right." based on RKI data of ".date_last
# set label 1 label1_text_right." based on JHU data of ".date_last


set xlabel "Weeks from now"
set xtics 1
set xtic add (date_last 0)




set ytics nomirror
set y2tics nomirror

set ylabel "Cases last week" offset 1,0 textcolor rgb 'blue' 
set y2label "Deaths last week" offset -1,0 textcolor rgb 'red' 

set ytics textcolor rgb 'blue' 
set y2tics textcolor rgb 'red' 

x_min = -7

set xrange [x_min:0]
# y_max=41000
mortality = 4.2/100

# mask_zero_values(x) = (x<=0)?1/0:x

set label 2 sprintf("scaling: %.2f%%", mortality*100.0) right front at graph 0.999, graph 0.95


set key width -3 bottom center

# How much are the deaths in Germany delayed?
set title "How much are the deaths in Germany delayed?"
set yrange [0:*]

output ='../plots-gnuplot/de-states/shift-deaths-to-match-cases_DE_last-week.png'
set output output
plot data u (column("Days_Past"))/7:(column("Cases_Last_Week")) t "Cases" ,\
     data u (column("Days_Past"))/7:(column("Deaths_Last_Week")) t "Deaths" axes x1y2, \
     data u (column("Days_Past")-14)/7:(column("Deaths_Last_Week")) t "Deaths shifted by 14 days" axes x1y2 with lines lc rgb "red"
unset output
# replot using correct y2 scale
y_max = GPVAL_Y_MAX
set yrange [0:y_max]
set y2range [0:y_max*mortality] 
set output output
replot
unset output


# cases last week per million
set ylabel "Cases last week per million" offset 1,0 textcolor rgb 'blue' 
set y2label "Deaths last week per million" offset -2,0 textcolor rgb 'red' 

set yrange [0:*]

output = '../plots-gnuplot/de-states/shift-deaths-to-match-cases_DE_last-week_per_million.png'
set output output
plot data u (column("Days_Past"))/7:(column("Cases_Last_Week_Per_Million")) t "Cases" ,\
     data u (column("Days_Past"))/7:(column("Deaths_Last_Week_Per_Million")) t "Deaths" axes x1y2, \
     data u (column("Days_Past")-14)/7:(column("Deaths_Last_Week_Per_Million")) t "Deaths shifted by 14 days" axes x1y2 with lines lc rgb "red"
unset output
# replot using correct y2 scale
y_max = GPVAL_Y_MAX
set yrange [0:y_max]
set y2range [0:y_max*mortality] 
set output output
replot
unset output


# Forecast
set key width 0

set xrange [x_min:2]

set title "Forecasting Deaths based on Cases"
data = '../data/de-states/de-state-DE-total.tsv'
# data = '../data/de-states/de-state-BY.tsv'
set yrange [0:*]
output = '../plots-gnuplot/de-states/forecasting-deaths-DE.png'
set output output
plot data u (column("Days_Past"))/7:(column("Cases_Last_Week_Per_Million")) t "Cases" ,\
     data u (column("Days_Past"))/7:(column("Deaths_Last_Week_Per_Million")) t "Deaths" axes x1y2, \
     data u (column("Days_Past")+14<0?1/0:column("Days_Past")+14)/7:(column("Cases_Last_Week_Per_Million")*mortality) t "Forecast" axes x1y2 with lines lc rgb "red"
unset output
# replot using correct y2 scale
y_max = GPVAL_Y_MAX
set yrange [0:y_max]
set y2range [0:y_max*mortality] 
set output output
replot
unset output