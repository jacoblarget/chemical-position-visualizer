#!/bin/bash
plot_command='python ../plot_compare_sapt_components.py'
#/home/mvanvleet/templates/figure_templates/plot_compare_sapt_components.py
isotropic_tag='isotropic_'
anisotropic_tag='anisotropic_'
fullanisotropic_tag='ohnanisotropic_'

all_prefix='fit_exp_'
all_suffix='_constrained.dat'

## # Get all atomnames
names=input_templates/atomtypes/*xyz

count=0
for mon1 in $names
do
    molecules[$count]=$(basename ${mon1%.xyz})
    ((count++))
done

echo ${molecules[*]}

count=0
homedir=`pwd`
## for dir in *[^ysth]
## do
for mon1 in ${molecules[*]}
do
  for mon2 in ${molecules[*]:$count}
  do 
    dir=${mon1}_${mon2}
    echo $dir
    cd $dir
    $plot_command -p $anisotropic_tag$all_prefix $isotropic_tag$all_prefix -s $all_suffix $all_suffix 
    mv sapt_comparison.png ${dir}_sapt_comparison.png
    cd $homedir

  done
  ((count++))
done
