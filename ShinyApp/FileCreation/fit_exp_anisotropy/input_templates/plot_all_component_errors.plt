set nogrid
set key
set autoscale
set zeroaxis
set datafile missing "0.000000000000000E+000"
set terminal png size 1600, 1000
set output 'mon1_mon2_all_component_errors.png'

set multiplot;
set size 0.35, 0.5

set ylabel "Errors in Force Field Component (mH)"
set xlabel " "
set origin 0,0.5
set title "Electrostatic Errors" 
set key left
plot '<paste rank0_slater_total_energy_unconstrained.dat rank0_slater_electrostatics_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) title 'Rank0 Multipoles Slater' ,\
     '<paste rank2_slater_total_energy_unconstrained.dat rank2_slater_electrostatics_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) title 'Rank2 Multipoles Slater' ,\
     '<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_electrostatics_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) title 'Rank4 Multipoles Slater' ,x notitle

set ylabel " "
set xlabel " "
set origin 0.32,0.5
set title "Exchange Errors"
plot '<paste rank0_slater_total_energy_unconstrained.dat rank0_slater_exchange_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) notitle ,\
     '<paste rank2_slater_total_energy_unconstrained.dat rank2_slater_exchange_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) notitle ,\
     '<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_exchange_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) notitle ,x notitle

set ylabel " "
set xlabel " "
set origin 0.64,0.5
set title "Dispersion Errors"
plot '<paste rank0_slater_total_energy_unconstrained.dat rank0_slater_dispersion_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) notitle ,\
     '<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_dispersion_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) notitle ,\
     '<paste rank2_slater_total_energy_unconstrained.dat rank2_slater_dispersion_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3)*1000: 1/0) notitle ,x notitle

set ylabel "Force Field Fitted Errors (mH)"
set xlabel " "
set origin 0.0,0.0
set title "Induction + DHF Errors"
plot '<paste rank0_slater_total_energy_unconstrained.dat rank0_slater_induction_unconstrained.dat rank0_slater_dhf_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 <= 0 ? ($4-$3+$6-$5)*1000 : 1/0) notitle ,\
     '<paste rank2_slater_total_energy_unconstrained.dat rank2_slater_induction_unconstrained.dat rank2_slater_dhf_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 < 0 ? ($4-$3+$6-$5)*1000 : 1/0) notitle ,\
     '<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_induction_unconstrained.dat rank4_slater_dhf_unconstrained.dat' every ::1 u (($2-$1)*1000):($1 < 0 ? ($4-$3+$6-$5)*1000 : 1/0) notitle ,x notitle

set ylabel " "
set xlabel "Total Energy Errors (mH)"
set origin 0.32,0.0
set title "All Errors (vs. Total Energy)"
set xrange [:0]
## plot '<paste rank0_slater_total_energy_unconstrained.dat rank0_slater_dhf_unconstrained.dat' every ::1 u (($2-$1)*1000):(($4-$3)*1000) notitle ,\
##      '<paste rank2_slater_total_energy_unconstrained.dat rank2_slater_dhf_unconstrained.dat' every ::1 u (($2-$1)*1000):(($4-$3)*1000) notitle ,x notitle
plot '<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_exchange_unconstrained.dat' using ($1*1000):(($4-$3)*1000) every ::1 title 'Exchange Errors',\
'<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_electrostatics_unconstrained.dat' using ($1*1000):(($4-$3)*1000) every ::1 title 'Electrostatics Errors',\
'<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_induction_unconstrained.dat' using ($1*1000):(($4-$3)*1000) every ::1 title 'Induction Errors',\
'<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_dhf_unconstrained.dat' using ($1*1000):(($4-$3)*1000) every ::1 title 'Dhf Errors',\
'<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_dispersion_unconstrained.dat' using ($1*1000):(($4-$3)*1000) every ::1 title 'Dispersion Errors',\
'<paste rank4_slater_total_energy_unconstrained.dat rank4_slater_total_energy_unconstrained.dat' using ($1*1000):(($4-$3)*1000) every ::1 title 'Total Energy Errors',\
0

set ylabel " "
set xlabel " "
set autoscale
unset zeroaxis
set origin 0.64,0.0
set title "Total Attractive Energies (SAPT vs FF)"
binwidth=.1
bin(x,width)=width*floor(x/width)
plot 'rank0_slater_total_energy_unconstrained.dat' every ::1 u 1:($1 <= 0 ? $2: 1/0) notitle ,\
     'rank2_slater_total_energy_unconstrained.dat' every ::1 u 1:($1 <=0 ? $2: 1/0) notitle,\
     'rank4_slater_total_energy_unconstrained.dat' every ::1 u 1:($1 <=0 ? $2: 1/0) notitle, x title 'y=x',\
     x*0.9 lt 4 title '10% error bars', x*1.1 lt 4 notitle 

## set ylabel " "
## set xlabel " "
## set autoscale
## set origin 0.64,0.0
## set title "Total Errors in Attractive Energies"
## binwidth=.1
## bin(x,width)=width*floor(x/width)
## plot 'rank0_slater_total_energy_unconstrained.dat' every ::1 u (bin(($2-$1)*1000,binwidth)):($1 <= 0 ? 1.0: 0) smooth freq with boxes notitle ,\
##      'rank2_slater_total_energy_unconstrained.dat' every ::1 u (bin(($2-$1)*1000,binwidth)):($1 <=0 ? 1.0:0) smooth freq with boxes notitle


unset multiplot
