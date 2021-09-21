set key right
set title 'Dispersion FF Quality for mon1_mon2'
set xlabel 'SAPT(PBE0) Dispersion Energy (mH)'
set ylabel 'FF Dispersion Energy (mH)'

set ytics nomirror
## set y2label 'Energy (mH)'
## set y2tics
set xrange [-2.0:0.001]
set yrange [-2.0:0.001]
set terminal unknown

plot 'scaled_exponents_slater_dispersion_unconstrained.dat' using ($1*1000):($2*1000) every ::1 title 'Unconstrained Fit of Dimer Pair w/ Slater functional form' axes x1y1
replot 'scaled_exponents_noslater_dispersion_unconstrained.dat' using ($1*1000):($2*1000) every ::1 title 'Unconstrained Fit of Dimer Pair w/o Slater functional form' axes x1y1
replot 'slater_dispersion_unconstrained.dat' using ($1*1000):($2*1000) every ::1 title 'Exponents Constrained Fit of Dimer Pair w/ Slater functional form' axes x1y1
replot 'noslater_dispersion_unconstrained.dat' using ($1*1000):($2*1000) every ::1 title 'Exponents Constrained Fit of Dimer Pair w/o Slater functional form' axes x1y1
replot x


set terminal png size 1000,1000 giant
set output 'dispersion_comparison.png'
replot
