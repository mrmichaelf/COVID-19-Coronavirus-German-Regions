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



set title "How much are the deaths in Germany delayed?"
set xlabel "Days"
set ylabel "Doubling Time (Days)"
set xtics 7

data = '../data/de-states/de-state-DE-total.tsv'
# data = '../data/int/country-DE.tsv'



date_last = system("tail -1 " . data . " | cut -f2")

set label 1 label1_text_right." based on RKI data of ".date_last
# set label 1 label1_text_right." based on JHU data of ".date_last

set xtic add (date_last 0) 


#set key width -7 Left reverse

#set output '../plots-gnuplot/int/countries-shift-ddt-to-match-cdt.png'
#plot data u 1:11 t "Cases Doubling Time" ,\
     data u 1:12 t "Deaths Doubling Time" , \
     data u ($1-8):12 t "Deaths Doubling Time, shifted by 8 days" with lines
#unset output


set key width -3


# set yrange [100:1000000]
# set y2range [1:10000]
#set logscale y
#set logscale y2
set ytics nomirror
set y2tics nomirror
#set ylabel "Cases"
#set y2label "Deaths"
#set output '../plots-gnuplot/int/countries-shift-deaths-to-match-cases.png'
#plot data u (column("Days_Past")):(column("Cases")) t "Cases" ,\
#     data u (column("Days_Past")):(column("Deaths")) t "Deaths" axes x1y2, \
#     data u (column("Days_Past")-14):(column("Deaths")) t "Deaths, shifted by 14 days" axes x1y2 with lines
#unset output


set ylabel "Cases last week" offset 1,0
set y2label "Deaths last week" offset -2,0

set xrange [-56:0]
y_min=0
y_max=41000
mortality = 4.1/100
set yrange [y_min:y_max]
set y2range [y_min*mortality:y_max*mortality] 
# mortatility: 0.53% realistic? 

mask_zero_values(x) = (x<=0)?1/0:x

set label 2 sprintf("scaling: %.2f%%", mortality*100.0) left front at graph 0.04, graph 0.85

set output '../plots-gnuplot/int/shift-deaths-to-match-cases_DE_last-week.png'
plot data u (column("Days_Past")):(column("Cases_Last_Week")) t "Cases" ,\
     data u (column("Days_Past")):(column("Deaths_Last_Week")) t "Deaths" axes x1y2, \
     data u (column("Days_Past")-14):(column("Deaths_Last_Week")) t "Deaths shifted by 14 days" axes x1y2 with lines lc rgb "red"
unset output

