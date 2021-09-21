set key right
set title 'Errors in FF for mon1_mon2'
set xlabel 'SAPT(PBE0) Total Energy (mH)'
set ylabel 'Errors in FF Energy Components (mH)'

## set y2label 'Energy (mH)'
## set y2tics
## set y2range [:0.2]
set xrange[:0]
set terminal unknown

plot '<paste saptff_noslater_total_energy_unconstrained.dat saptff_noslater_electrostatics_unconstrained.dat' using 1:(($3-$4)*1000) every ::1 title 'DMA Electrostatics Errors'
replot '<paste isa_density_exponents_slater_total_energy_unconstrained.dat isa_density_exponents_slater_electrostatics_unconstrained.dat' using 1:(($3-$4)*1000) every ::1 title 'ISA Electrostatics Errors'
replot 0

set terminal png size 1000,1000 giant
set output 'all_errors.png'
replot
