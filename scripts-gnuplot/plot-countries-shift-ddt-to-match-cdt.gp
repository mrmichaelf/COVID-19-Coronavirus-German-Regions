# by Torben Menke
# https://entorb.net
# date 2020-03-22


# TODO: shall this go to de-states or to int/countries?

load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 3 linetype 7 dt "-" lw 2 linecolor rgb 'black' 



set title "How much are the deaths delayed?"
set xlabel "Days"
set ylabel "Doublication Time (Days)"
set xtics 7

data = '../data/de-states/de-state-DE-total.tsv'
# data = '../data/int/country-DE.tsv'



date_last = system("tail -1 " . data . " | cut -f2")

set label 1 label1_text_right." based on RKI data of ".date_last
# set label 1 label1_text_right." based on JHU data of ".date_last

set xtic add (date_last 0) 

#set xrange [-35:0]

set key width -7 Left reverse

set output '../plots-gnuplot/int/countries-shift-ddt-to-match-cdt.png'
plot data u 1:11 t "Cases Doublication Time" ,\
     data u 1:12 t "Deaths Doublication Time" , \
     data u ($1-8):12 t "Deaths Doublication Time, shifted by 8 days" with lines
unset output


set key width -4

set yrange [100:1000000]
set y2range [1:10000]
set logscale y
set logscale y2
set ylabel "Cases"
set y2label "Deaths"
set ytics nomirror
set y2tics nomirror
set output '../plots-gnuplot/int/countries-shift-deaths-to-match-cases.png'
plot data u 1:3 t "Cases" ,\
     data u 1:4 t "Deaths" axes x1y2, \
     data u ($1-8):4 t "Deaths, shifted by 8 days" axes x1y2 with lines
unset output

