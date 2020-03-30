# by Torben Menke
# https://entorb.net
# date 2020-03-22


load "header.gp"

set title ""
# set ylabel "Cases"
# set xlabel "Days since first data"
set ylabel "Infektionen"
set xlabel "Tage"
set xtics 7

set y2label "Verdopplungszeit (Tage)" tc ls 4 offset -2,0
set y2tics tc ls 4
set y2range [10:0]


# prepare data file for fit results
# write header line into fit output file
fit_data_file = "../data/de-states/de-states-cases-gnuplot-fit.tsv"
set print fit_data_file
print "# State\tShort\ta\tb\tCases\tDoubling time\tfactor t+1\tcases t+1\tfactor t+7\tcases t+7"
unset print

# text will be inserted later on
set label 2 "" right front at graph 0.98, graph 0.22
col = 3 ; col_name = 'Fälle' # infections
short_name = 'BW' ; long_name = "Baden-Württemberg" ; load "plot-de-states-fit-sub1.gp"
short_name = 'BY' ; long_name = "Bayern" ; load "plot-de-states-fit-sub1.gp"
short_name = 'BE' ; long_name = "Berlin" ; load "plot-de-states-fit-sub1.gp"
short_name = 'BB' ; long_name = "Brandenburg" ; load "plot-de-states-fit-sub1.gp"
short_name = 'HB' ; long_name = "Bremen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'HH' ; long_name = "Hamburg" ; load "plot-de-states-fit-sub1.gp"
short_name = 'HE' ; long_name = "Hessen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'MV' ; long_name = "Mecklenburg-Vorpommern" ; load "plot-de-states-fit-sub1.gp"
short_name = 'NI' ; long_name = "Niedersachsen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'NW' ; long_name = "Nordrhein-Westfalen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'RP' ; long_name = "Rheinland-Pfalz" ; load "plot-de-states-fit-sub1.gp"
short_name = 'SL' ; long_name = "Saarland" ; load "plot-de-states-fit-sub1.gp"
short_name = 'SN' ; long_name = "Sachsen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'ST' ; long_name = "Sachsen-Anhalt" ; load "plot-de-states-fit-sub1.gp"
short_name = 'SH' ; long_name = "Schleswig-Holstein" ; load "plot-de-states-fit-sub1.gp"
short_name = 'TH' ; long_name = "Thüringen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'DE-total' ; long_name = "Deutschland" ; load "plot-de-states-fit-sub1.gp"

# delete fit logfile
`rm fit.log`

unset label 2
unset label 3
unset xrange
unset yrange
unset xlabel
set xtics autofreq
set ytics mirror
unset y2tics
unset y2label


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
y_value_de = ( system("tail -1 " . fit_data_file . " | cut -f6") + 0)
set output '../plots-gnuplot/cases-de-fit-doubling-time.png'
plot fit_data_file u 6:xticlabels(1) with boxes ls 11, y_value_de with lines ls 12
unset output
set ytics format "%g%%" 
set title "Fitergebnis Zunahme Infektionen pro Tag"
set ylabel "Zunahme Infektionen pro Tag"
y_value_de = ( system("tail -1 " . fit_data_file . " | cut -f7") + 0)
y_value_de = (y_value_de-1)*100
set output '../plots-gnuplot/cases-de-fit-increase-1-day.png'
plot fit_data_file u (($7-1)*100):xticlabels(1) with boxes ls 11, y_value_de with lines ls 12
unset output
set ytics format "%g" 

# Plotting the latest number of infections per 1 Mill pop
set title "Infektionen pro 1 Millionen Einwohner"
set ylabel "Infektionen pro 1 Mill Einwohner"
data = '../data/de-states/de-states-latest.tsv'
y_value_de = ( system("tail -1 " . data . " | cut -f10") + 0)

set output '../plots-gnuplot/cases-de-states-latest-per-million.png'
plot data u 10:xticlabels(1) with boxes ls 11, y_value_de with lines ls 12
unset output

unset yrange
unset style
unset boxwidth
unset bmargin
unset xtics
unset ytics
