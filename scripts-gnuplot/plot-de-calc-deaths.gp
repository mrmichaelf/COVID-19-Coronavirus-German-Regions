# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 3 linetype 7 dt 1 lw 2 linecolor rgb 'black' 



set title "Abschätzung der Dunkelziffer der Infektionen\nAnnahme: Sterben nach 2 Wochen mit Wahrscheinlichkeit von 1%"
# set ylabel "Cases"
# set xlabel "Days since first data"
set ylabel "Infektionen"
set xlabel "Tage"
set xtics 7

# set timefmt '%Y-%m-%d'
# set xdata time
# set format x "%d.%m"


set logscale y
set xrange [-35:0]
data = '../data/de-states/de-state-DE-total.tsv'
set output '../plots-gnuplot/de-states/calc-cases-from-deaths-DE-total.png'
plot data using ($1-14):($4*100) title "geschätze Infizierte" with linespoints ls 1 ,\
     data using ($1):($3) title "positiv getestete Infizierte" with linespoints ls 2 ,\

unset output
