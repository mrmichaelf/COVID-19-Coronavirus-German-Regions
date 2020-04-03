load "header.gp"

# set terminal pngcairo size 640,480 font 'Verdana,9'

# set datafile commentschars '#'
# # set datafile missing '#'
# set datafile separator "\t"


set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 3 linetype 7 dt 1 lw 2 linecolor rgb 'black' 


data_BW = '../data/de-divi/de-divi-BW.tsv'
data_BY = '../data/de-divi/de-divi-BY.tsv'
data_BE = '../data/de-divi/de-divi-BE.tsv'
data_BB = '../data/de-divi/de-divi-BB.tsv'
data_HB = '../data/de-divi/de-divi-HB.tsv'
data_HH = '../data/de-divi/de-divi-HH.tsv'
data_HE = '../data/de-divi/de-divi-HE.tsv'
data_MV = '../data/de-divi/de-divi-MV.tsv'
data_NI = '../data/de-divi/de-divi-NI.tsv'
data_NW = '../data/de-divi/de-divi-NW.tsv'
data_RP = '../data/de-divi/de-divi-RP.tsv'
data_SL = '../data/de-divi/de-divi-SL.tsv'
data_SN = '../data/de-divi/de-divi-SN.tsv'
data_ST = '../data/de-divi/de-divi-ST.tsv'
data_SH = '../data/de-divi/de-divi-SH.tsv'
data_TH = '../data/de-divi/de-divi-TH.tsv'

set yrange [0:100]

set timefmt '%Y-%m-%d'
set xdata time
set format x "%d.%m"


# set title "%A%"
# set output "../plots-gnuplot/de-divi/de-divi-%A%.png"
# plot data_%A% using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
# unset output


set title "BW"
set output "../plots-gnuplot/de-divi/de-divi-BW.png"
plot data_BW using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "BY"
set output "../plots-gnuplot/de-divi/de-divi-BY.png"
plot data_BY using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "BE"
set output "../plots-gnuplot/de-divi/de-divi-BE.png"
plot data_BE using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "BB"
set output "../plots-gnuplot/de-divi/de-divi-BB.png"
plot data_BB using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "HB"
set output "../plots-gnuplot/de-divi/de-divi-HB.png"
plot data_HB using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "HH"
set output "../plots-gnuplot/de-divi/de-divi-HH.png"
plot data_HH using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "HE"
set output "../plots-gnuplot/de-divi/de-divi-HE.png"
plot data_HE using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "MV"
set output "../plots-gnuplot/de-divi/de-divi-MV.png"
plot data_MV using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "NI"
set output "../plots-gnuplot/de-divi/de-divi-NI.png"
plot data_NI using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "NW"
set output "../plots-gnuplot/de-divi/de-divi-NW.png"
plot data_NW using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "RP"
set output "../plots-gnuplot/de-divi/de-divi-RP.png"
plot data_RP using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "SL"
set output "../plots-gnuplot/de-divi/de-divi-SL.png"
plot data_SL using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "SN"
set output "../plots-gnuplot/de-divi/de-divi-SN.png"
plot data_SN using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "ST"
set output "../plots-gnuplot/de-divi/de-divi-ST.png"
plot data_ST using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "SH"
set output "../plots-gnuplot/de-divi/de-divi-SH.png"
plot data_SH using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title "TH"
set output "../plots-gnuplot/de-divi/de-divi-TH.png"
plot data_TH using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output





# set style data histograms
# set style histogram rowstacked
# set boxwidth 1 relative
# set style fill solid 1.0 border -1

# set output "test-divi-BW.png"
# plot data_BW using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-BY.png"
# plot data_BY using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-BE.png"
# plot data_BE using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-BB.png"
# plot data_BB using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-HB.png"
# plot data_HB using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-HH.png"
# plot data_HH using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-HE.png"
# plot data_HE using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-MV.png"
# plot data_MV using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-NI.png"
# plot data_NI using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-NW.png"
# plot data_NW using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-RP.png"
# plot data_RP using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-SL.png"
# plot data_SL using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-SN.png"
# plot data_SN using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-ST.png"
# plot data_ST using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-SH.png"
# plot data_SH using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-TH.png"
# plot data_TH using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output