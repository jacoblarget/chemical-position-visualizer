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
/home/mvanvleet/research/working_directory/anisotropy/ff_fitting/heteroatomic_dimers_comparison2/anisotropy/final_fits/isotropic_fit_dispersion
scaledispisotropic_tag='scaledispisotropic'
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
    cp $isotropic_dir/$file/multipoles.dat $file/${isotropic_tag}_fit_exp_multipoles_unconstrained.dat
    cp $anisotropic_dir/$file/multipoles.dat $file/${anisotropic_tag}_fit_exp_multipoles_unconstrained.dat
    cp $fullisotropic_dir/$file/multipoles.dat $file/${fullisotropic_tag}_fit_exp_multipoles_unconstrained.dat
    cp $scaledispisotropic_dir/$file/multipoles.dat $file/${scaledispisotropic_tag}_fit_exp_multipoles_unconstrained.dat
    cp $scaledispanisotropic_dir/$file/multipoles.dat $file/${scaledispanisotropic_tag}_fit_exp_multipoles_unconstrained.dat

  done
  ((count++))
done
