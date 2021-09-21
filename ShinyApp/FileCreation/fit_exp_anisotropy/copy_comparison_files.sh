#!/bin/bash

## line_average_isa_dir=/home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison/unique_atomtypes_individual_fits/rank2/isa_charges
## line_average_isa_tag='line_average_isa'
isotropic_dir=\
/home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/final_fits/isotropic
isotropic_tag='isotropic'
anisotropic_dir=\
/home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/final_fits/anisotropic
anisotropic_tag='anisotropic'
#fullisotropic_dir=~/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/isotropic
#fullisotropic_dir=~/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/rank2_allatoms_rank2_anisotropy
fullisotropic_dir=\
/home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/final_fits/isotropic_l0_multipoles
fullisotropic_tag='fullisotropic'
scaledispisotropic_dir=\
/home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/final_fits/isotropic_l0_multipoles_fit_dispersion
scaledispisotropic_tag='scaledispfullisotropic'
## scaledispisotropic_dir=\
## /home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/final_fits/isotropic_fit_dispersion
## scaledispisotropic_tag='scaledispisotropic'
scaledispanisotropic_dir=\
/home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/final_fits/anisotropic_fit_dispersion
scaledispanisotropic_tag='scaledispanisotropic'

# Get all atomnames
names=input_templates/atomtypes/*xyz

count=0
for mon1 in $names
do
    molecules[$count]=$(basename ${mon1%.xyz})
    ((count++))
done

echo ${molecules[*]}

count=0
for mon1 in ${molecules[*]}
do
  for mon2 in ${molecules[*]:$count}
  do 
    file=${mon1}_${mon2}
    mkdir -p $file
    cp $isotropic_dir/$file/fit_exp_coeffs_unconstrained.out $file/${isotropic_tag}_fit_exp_coeffs_unconstrained.out
    cp $anisotropic_dir/$file/fit_exp_coeffs_unconstrained.out $file/${anisotropic_tag}_fit_exp_coeffs_unconstrained.out
    cp $fullisotropic_dir/$file/fit_exp_coeffs_unconstrained.out $file/${fullisotropic_tag}_fit_exp_coeffs_unconstrained.out
    cp $scaledispisotropic_dir/$file/fit_exp_coeffs_unconstrained.out $file/${scaledispisotropic_tag}_fit_exp_coeffs_unconstrained.out
    cp $scaledispanisotropic_dir/$file/fit_exp_coeffs_unconstrained.out $file/${scaledispanisotropic_tag}_fit_exp_coeffs_unconstrained.out
    cp $isotropic_dir/$file/fit_exp_coeffs_constrained.out $file/${isotropic_tag}_fit_exp_coeffs_constrained.out
    cp $anisotropic_dir/$file/fit_exp_coeffs_constrained.out $file/${anisotropic_tag}_fit_exp_coeffs_constrained.out
    cp $fullisotropic_dir/$file/fit_exp_coeffs_constrained.out $file/${fullisotropic_tag}_fit_exp_coeffs_constrained.out
    cp $scaledispisotropic_dir/$file/fit_exp_coeffs_constrained.out $file/${scaledispisotropic_tag}_fit_exp_coeffs_constrained.out
    cp $scaledispanisotropic_dir/$file/fit_exp_coeffs_constrained.out $file/${scaledispanisotropic_tag}_fit_exp_coeffs_constrained.out
    #cp $kt50_dir/$file/fit_exp_coeffs_unconstrained.out $file/${kt50_tag}_fit_exp_coeffs_unconstrained.out

    cp $isotropic_dir/$file/fit_exp_exchange_unconstrained.dat $file/${isotropic_tag}_fit_exp_exchange_unconstrained.dat
    cp $anisotropic_dir/$file/fit_exp_exchange_unconstrained.dat $file/${anisotropic_tag}_fit_exp_exchange_unconstrained.dat
    cp $fullisotropic_dir/$file/fit_exp_exchange_unconstrained.dat $file/${fullisotropic_tag}_fit_exp_exchange_unconstrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_exchange_unconstrained.dat $file/${scaledispisotropic_tag}_fit_exp_exchange_unconstrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_exchange_unconstrained.dat $file/${scaledispanisotropic_tag}_fit_exp_exchange_unconstrained.dat
    cp $isotropic_dir/$file/fit_exp_exchange_constrained.dat $file/${isotropic_tag}_fit_exp_exchange_constrained.dat
    cp $anisotropic_dir/$file/fit_exp_exchange_constrained.dat $file/${anisotropic_tag}_fit_exp_exchange_constrained.dat
    cp $fullisotropic_dir/$file/fit_exp_exchange_constrained.dat $file/${fullisotropic_tag}_fit_exp_exchange_constrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_exchange_constrained.dat $file/${scaledispisotropic_tag}_fit_exp_exchange_constrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_exchange_constrained.dat $file/${scaledispanisotropic_tag}_fit_exp_exchange_constrained.dat
    #cp $kt50_dir/$file/fit_exp_exchange_unconstrained.dat $file/${kt50_tag}_fit_exp_exchange_unconstrained.dat

    cp $isotropic_dir/$file/fit_exp_electrostatics_unconstrained.dat $file/${isotropic_tag}_fit_exp_electrostatics_unconstrained.dat
    cp $anisotropic_dir/$file/fit_exp_electrostatics_unconstrained.dat $file/${anisotropic_tag}_fit_exp_electrostatics_unconstrained.dat
    cp $fullisotropic_dir/$file/fit_exp_electrostatics_unconstrained.dat $file/${fullisotropic_tag}_fit_exp_electrostatics_unconstrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_electrostatics_unconstrained.dat $file/${scaledispisotropic_tag}_fit_exp_electrostatics_unconstrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_electrostatics_unconstrained.dat $file/${scaledispanisotropic_tag}_fit_exp_electrostatics_unconstrained.dat
    cp $isotropic_dir/$file/fit_exp_electrostatics_constrained.dat $file/${isotropic_tag}_fit_exp_electrostatics_constrained.dat
    cp $anisotropic_dir/$file/fit_exp_electrostatics_constrained.dat $file/${anisotropic_tag}_fit_exp_electrostatics_constrained.dat
    cp $fullisotropic_dir/$file/fit_exp_electrostatics_constrained.dat $file/${fullisotropic_tag}_fit_exp_electrostatics_constrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_electrostatics_constrained.dat $file/${scaledispisotropic_tag}_fit_exp_electrostatics_constrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_electrostatics_constrained.dat $file/${scaledispanisotropic_tag}_fit_exp_electrostatics_constrained.dat
    #cp $kt50_dir/$file/fit_exp_electrostatics_unconstrained.dat $file/${kt50_tag}_fit_exp_electrostatics_unconstrained.dat

    cp $isotropic_dir/$file/fit_exp_induction_unconstrained.dat $file/${isotropic_tag}_fit_exp_induction_unconstrained.dat
    cp $anisotropic_dir/$file/fit_exp_induction_unconstrained.dat $file/${anisotropic_tag}_fit_exp_induction_unconstrained.dat
    cp $fullisotropic_dir/$file/fit_exp_induction_unconstrained.dat $file/${fullisotropic_tag}_fit_exp_induction_unconstrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_induction_unconstrained.dat $file/${scaledispisotropic_tag}_fit_exp_induction_unconstrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_induction_unconstrained.dat $file/${scaledispanisotropic_tag}_fit_exp_induction_unconstrained.dat
    cp $isotropic_dir/$file/fit_exp_induction_constrained.dat $file/${isotropic_tag}_fit_exp_induction_constrained.dat
    cp $anisotropic_dir/$file/fit_exp_induction_constrained.dat $file/${anisotropic_tag}_fit_exp_induction_constrained.dat
    cp $fullisotropic_dir/$file/fit_exp_induction_constrained.dat $file/${fullisotropic_tag}_fit_exp_induction_constrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_induction_constrained.dat $file/${scaledispisotropic_tag}_fit_exp_induction_constrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_induction_constrained.dat $file/${scaledispanisotropic_tag}_fit_exp_induction_constrained.dat
    #cp $kt50_dir/$file/fit_exp_induction_unconstrained.dat $file/${kt50_tag}_fit_exp_induction_unconstrained.dat

    cp $isotropic_dir/$file/fit_exp_dhf_unconstrained.dat $file/${isotropic_tag}_fit_exp_dhf_unconstrained.dat
    cp $anisotropic_dir/$file/fit_exp_dhf_unconstrained.dat $file/${anisotropic_tag}_fit_exp_dhf_unconstrained.dat
    cp $fullisotropic_dir/$file/fit_exp_dhf_unconstrained.dat $file/${fullisotropic_tag}_fit_exp_dhf_unconstrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_dhf_unconstrained.dat $file/${scaledispisotropic_tag}_fit_exp_dhf_unconstrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_dhf_unconstrained.dat $file/${scaledispanisotropic_tag}_fit_exp_dhf_unconstrained.dat
    cp $isotropic_dir/$file/fit_exp_dhf_constrained.dat $file/${isotropic_tag}_fit_exp_dhf_constrained.dat
    cp $anisotropic_dir/$file/fit_exp_dhf_constrained.dat $file/${anisotropic_tag}_fit_exp_dhf_constrained.dat
    cp $fullisotropic_dir/$file/fit_exp_dhf_constrained.dat $file/${fullisotropic_tag}_fit_exp_dhf_constrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_dhf_constrained.dat $file/${scaledispisotropic_tag}_fit_exp_dhf_constrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_dhf_constrained.dat $file/${scaledispanisotropic_tag}_fit_exp_dhf_constrained.dat
    #cp $kt50_dir/$file/fit_exp_dhf_unconstrained.dat $file/${kt50_tag}_fit_exp_dhf_unconstrained.dat

    cp $isotropic_dir/$file/fit_exp_dispersion_unconstrained.dat $file/${isotropic_tag}_fit_exp_dispersion_unconstrained.dat
    cp $anisotropic_dir/$file/fit_exp_dispersion_unconstrained.dat $file/${anisotropic_tag}_fit_exp_dispersion_unconstrained.dat
    cp $fullisotropic_dir/$file/fit_exp_dispersion_unconstrained.dat $file/${fullisotropic_tag}_fit_exp_dispersion_unconstrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_dispersion_unconstrained.dat $file/${scaledispisotropic_tag}_fit_exp_dispersion_unconstrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_dispersion_unconstrained.dat $file/${scaledispanisotropic_tag}_fit_exp_dispersion_unconstrained.dat
    cp $isotropic_dir/$file/fit_exp_dispersion_constrained.dat $file/${isotropic_tag}_fit_exp_dispersion_constrained.dat
    cp $anisotropic_dir/$file/fit_exp_dispersion_constrained.dat $file/${anisotropic_tag}_fit_exp_dispersion_constrained.dat
    cp $fullisotropic_dir/$file/fit_exp_dispersion_constrained.dat $file/${fullisotropic_tag}_fit_exp_dispersion_constrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_dispersion_constrained.dat $file/${scaledispisotropic_tag}_fit_exp_dispersion_constrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_dispersion_constrained.dat $file/${scaledispanisotropic_tag}_fit_exp_dispersion_constrained.dat
    #cp $kt50_dir/$file/fit_exp_dispersion_unconstrained.dat $file/${kt50_tag}_fit_exp_dispersion_unconstrained.dat

    cp $isotropic_dir/$file/fit_exp_total_energy_unconstrained.dat $file/${isotropic_tag}_fit_exp_total_energy_unconstrained.dat
    cp $anisotropic_dir/$file/fit_exp_total_energy_unconstrained.dat $file/${anisotropic_tag}_fit_exp_total_energy_unconstrained.dat
    cp $fullisotropic_dir/$file/fit_exp_total_energy_unconstrained.dat $file/${fullisotropic_tag}_fit_exp_total_energy_unconstrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_total_energy_unconstrained.dat $file/${scaledispisotropic_tag}_fit_exp_total_energy_unconstrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_total_energy_unconstrained.dat $file/${scaledispanisotropic_tag}_fit_exp_total_energy_unconstrained.dat
    cp $isotropic_dir/$file/fit_exp_total_energy_constrained.dat $file/${isotropic_tag}_fit_exp_total_energy_constrained.dat
    cp $anisotropic_dir/$file/fit_exp_total_energy_constrained.dat $file/${anisotropic_tag}_fit_exp_total_energy_constrained.dat
    cp $fullisotropic_dir/$file/fit_exp_total_energy_constrained.dat $file/${fullisotropic_tag}_fit_exp_total_energy_constrained.dat
    cp $scaledispisotropic_dir/$file/fit_exp_total_energy_constrained.dat $file/${scaledispisotropic_tag}_fit_exp_total_energy_constrained.dat
    cp $scaledispanisotropic_dir/$file/fit_exp_total_energy_constrained.dat $file/${scaledispanisotropic_tag}_fit_exp_total_energy_constrained.dat
    #cp $kt50_dir/$file/fit_exp_total_energy_unconstrained.dat $file/${kt50_tag}_fit_exp_total_energy_unconstrained.dat

  done
  ((count++))
done
