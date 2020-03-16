# by Torben Menke
# https://entorb.net
# date 2020-03-12


# set terminal png noenhanced large size 640,480
set terminal pngcairo size 640,480 font 'Verdana,9'
# set terminal svg size 640,480 fname 'Verdana, Helvetica, Arial, sans-serif' rounded dashed

set datafile commentschars '#'
# set datafile missing '#'
set datafile separator "\t"

data = '../data/cases-de.csv'

set encoding utf8

set grid xtics ytics
set xtics mirror
set ytics mirror 


set title "Titel"
# set ylabel "Cases"
# set xlabel "Days since first data"
set ylabel "Infektionen"
set xlabel "Tage seit erstem Datenpunkt (28.02.20)"


set key top left box

# FOR SOME STRANGE REASON THIS IS NOT WORKING, So fitting againt number column insteays since first datanot working: Singular matrix
# set timefmt '%d.%m.%Y %H:%M'
# set xdata time
# x0 = 1582884000 # unix time of 28.02.20 10:00
# f(x)=a * exp(b * (x-x0))
# fit f(x) data using 2:col via a, b


# doubling time
# 2 * a = a * exp (b * t) 
# ln 2  = b * t
# -> t = ln (2) / b

set fit quiet

#set key off
# font ",20" 
print ("Doubling time")
# write header line into fit output file
fit_data_file = "../data/cases-de-gnuplot-fit.csv"
set print fit_data_file
print "# Region\tShort\ta\tb\tCases\tDoubling time\tfactor t+1\tcases t+1\tfactor t+7\tcases t+7"
unset print

# fetch data from last row of data
x_max = ( system("tail -1 " . data . " | cut -f1") + 0 )
date_last = system("tail -1 " . data . " | cut -f2")

# text will be inserted later on
set label 1 "by Torben (https://entorb.net) based on RKI data of ".date_last rotate by 90 center at screen 0.985, screen 0.5
set label 2 "" right front at graph 0.98, graph 0.22

short_name = 'BW' ; col = 4; long_name = "Baden-Württemberg"
load "plot-sub1.gp"

short_name = 'BY' ; col = 5; long_name = "Bayern"
load "plot-sub1.gp"

short_name = 'BE' ; col = 6; long_name = "Berlin"
load "plot-sub1.gp"

short_name = 'BB' ; col = 7; long_name = "Brandenburg"
load "plot-sub1.gp"

short_name = 'HB' ; col = 8; long_name = "Bremen"
load "plot-sub1.gp"

short_name = 'HH' ; col = 9; long_name = "Hamburg"
load "plot-sub1.gp"

short_name = 'HE' ; col = 10; long_name = "Hessen"
load "plot-sub1.gp"

short_name = 'MV' ; col = 11; long_name = "Mecklenburg-Vorpommern"
load "plot-sub1.gp"

short_name = 'NI' ; col = 12; long_name = "Niedersachsen"
load "plot-sub1.gp"

short_name = 'NW' ; col = 13; long_name = "Nordrhein-Westfalen"
load "plot-sub1.gp"

short_name = 'RP' ; col = 14; long_name = "Rheinland-Pfalz"
load "plot-sub1.gp"

short_name = 'SL' ; col = 15; long_name = "Saarland"
load "plot-sub1.gp"

short_name = 'SN' ; col = 16; long_name = "Sachsen"
load "plot-sub1.gp"

short_name = 'ST' ; col = 17; long_name = "Sachsen-Anhalt"
load "plot-sub1.gp"

short_name = 'SH' ; col = 18; long_name = "Schleswig-Holstein"
load "plot-sub1.gp"

short_name = 'TH' ; col = 19; long_name = "Thüringen"
load "plot-sub1.gp"

short_name = 'DE-total' ; col = 20; long_name = "Deutschland"
load "plot-sub1.gp"

unset label 2
unset label 3

# delete fit logfile
`rm fit.log`
unset xrange
unset xlabel

# now lets compare several stats
set timefmt '%d.%m.%Y %H:%M'
set format x '%d.%m'
set xdata time

# set key on
title = "Vergleich ausgewählter Regionen"
set title title
set output '../plots-gnuplot/cases-de-comparison.png'
plot \
 data using 2:20 title "DE total" with linespoints \
,data using 2:4 title "BW" with linespoints \
,data using 2:5 title "BY" with linespoints \
,data using 2:12 title "NS" with linespoints \
,data using 2:13 title "NW" with linespoints \

unset output

set logscale y
# set format y "10^{%L}"
set title title ." - Logarithmische Skalierung"
set output '../plots-gnuplot/cases-de-comparison-log.png'
replot
unset output
unset logscale y
unset xdata

# let's plot the fit data as boxes
set title "Fitergebnis Verdopplungszeit (Tage)"
set ylabel "Verdopplungszeit (Tage)"
set xtics rotate by 60 offset 1,0 right
set ytics format "%.1f" 
set bmargin 10.5
set style fill solid 0.5 border 0
set boxwidth 0.75 relative
set key off
set yrange [0:]
set output '../plots-gnuplot/cases-de-fit-doubling-time.png'
plot fit_data_file u 6:xticlabels(1) with boxes linecolor rgb "red"
unset output
set ytics format "%g%%" 
set title "Fitergebnis Zunahme Infektionen pro Tag"
set ylabel "Zunahme Infektionen pro Tag"
set output '../plots-gnuplot/cases-de-fit-increase-1-day.png'
plot fit_data_file u (($7-1)*100):xticlabels(1) with boxes linecolor rgb "red"
unset output


unset yrange
unset style
unset boxwidth
unset bmargin
unset xtics
unset ytics
