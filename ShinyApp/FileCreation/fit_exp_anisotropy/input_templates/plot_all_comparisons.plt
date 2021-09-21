set nogrid
set key
set autoscale
set datafile missing "0.000000000000000E+000"
set terminal png size 1600, 1000
set output 'mon1_mon2_all_comparisons.png'

set multiplot;
set size 0.35, 0.5

set ylabel "Force Field Fitted Energy (mH)"
set xlabel " "
set origin 0,0.5
set title "Electrostatic Energy" 
set key left
plot 'saptff_noslater_electrostatics_unconstrained.dat' every ::1 u ($1*1000):($2*1000) title 'SAPTFF (Unconstrained Fits)' ,\
     'saptff_noslater_electrostatics_constrained.dat' every ::1 u ($1*1000):($2*1000) title 'SAPTFF (Constrained Fits)',\
     'isa_density_exponents_slater_electrostatics_unconstrained.dat' every ::1 u ($1*1000):($2*1000) title 'ISA-FF (Unconstrained Fits)' ,\
     'isa_density_exponents_slater_electrostatics_constrained.dat' every ::1 u ($1*1000):($2*1000) title 'ISA-FF (Constrained Fits)' ,x notitle

set ylabel " "
set xlabel " "
set origin 0.32,0.5
set title "Exchange Energy"
plot 'saptff_noslater_exchange_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'saptff_noslater_exchange_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_exchange_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_exchange_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,x notitle

set ylabel " "
set xlabel " "
set origin 0.64,0.5
set title "Dispersion Energy"
plot 'saptff_noslater_dispersion_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'saptff_noslater_dispersion_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_dispersion_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_dispersion_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,x notitle

set ylabel " "
set xlabel "SAPT Energy (mH)"
set origin 0.32,0.0
set title "Dhf Energy"
plot 'saptff_noslater_dhf_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'saptff_noslater_dhf_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_dhf_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_dhf_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,x notitle

set ylabel " "
set xlabel " "
set origin 0.64,0.0
set title "Total Energy"
plot 'saptff_noslater_total_energy_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'saptff_noslater_total_energy_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_total_energy_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_total_energy_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,x notitle

set ylabel "Force Field Fitted Energy (mH)"
set xlabel " "
set origin 0.0,0.0
set title "Induction Energy"
plot 'saptff_noslater_induction_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'saptff_noslater_induction_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_induction_unconstrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,\
     'isa_density_exponents_slater_induction_constrained.dat' every ::1 u ($1*1000):($2*1000) notitle ,x notitle

unset multiplot
