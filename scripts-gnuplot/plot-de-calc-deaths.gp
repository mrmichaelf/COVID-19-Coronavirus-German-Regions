# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 3 linetype 7 dt 1 lw 2 linecolor rgb 'black' 

# fit
set style line 11 linetype 7 dt "-" lw 2 linecolor rgb 'black' 


set title "Abschätzung der Dunkelziffer der Infektionen\nAnnahme: Sterben nach 2 Wochen mit Wahrscheinlichkeit von 1%"
# set ylabel "Cases"
# set xlabel "Days since first data"
set ylabel "Infektionen"
set xlabel "Tage"
set xtics 7

data = '../data/de-states/de-state-DE-total.tsv'


f(x)=N0 * exp(x * log(2)/T)
N0 = 10000.0
b = 5.0

# use only last 7 days for fit at require the number to be at least 2
set xrange [-21.1:-13.9]


fit f(x) data using ($1-14):($4*100) via N0, T
b = log(2)/T

# delete fit logfile
`rm fit.log`

# set timefmt '%Y-%m-%d'
# set xdata time
# set format x "%d.%m"

date_last = system("tail -1 " . data . " | cut -f2")
cases_last = ( system("tail -1 " . data . " | cut -f3") + 0)

set xtic add (date_last 0) 

set label 2 \
 sprintf("Fit Ergebnisse\nVerdopplungszeit: %.1f Tage\nDunkelziffer Infizierte heute: %d\nProzent der DE-Bevölkerung: %.1f%%", T, f(0) , f(0) / 83019200 * 100) \
 right front at graph 0.98, graph 0.22

 # , y_last * exp(b * 1), (exp(b * 7)-1)*100, y_last * exp(b * 7) )\

set logscale y
set xrange [-35:0]
set output '../plots-gnuplot/de-states/calc-cases-from-deaths-DE-total.png'
plot data using ($1-14):($4*100) title "geschätze Infizierte" with linespoints ls 1 ,\
     data using ($1):($3) title "positiv getestete Infizierte" with linespoints ls 2 ,\
     (x<=-14.0)?1/0:f(x) notitle with lines ls 1 dt "-"

unset output
