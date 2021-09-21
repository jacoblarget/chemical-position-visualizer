set key right
set title 'Exchange FF Quality for mon1_mon2'
set xlabel 'SAPT(PBE0) Exchange Energy (mH)'
set ylabel 'FF Exchange Energy (mH)'

set ytics nomirror
## set y2label 'Energy (mH)'
## set y2tics
## set y2range [:0.2]
set terminal unknown
set logscale xy

plot 'line_average_isa_slater_exchange_unconstrained.dat' every ::1 u ($1*1000):($2*1000) title 'Line Averaged ISA Exponent',\
     'longrange_abs_cutoff_isa_slater_exchange_unconstrained.dat' every ::1 u ($1*1000):($2*1000) title 'Long-ranged points RMSE minimization',\
     'allrange_abs_cutoff_isa_slater_exchange_unconstrained.dat' every ::1 u ($1*1000):($2*1000) title 'All-ranged points RMSE minimization',\
     'vdw_rel_cutoff_isa_slater_exchange_unconstrained.dat' every ::1 u ($1*1000):($2*1000) title '0.8-1.2vdw radius RMSE minimization',x notitle


set terminal png size 1000,1000 giant
set output 'exchange_comparison.png'
replot
