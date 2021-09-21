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
    echo $mon1 $mon1
    display ${mon1}_$mon1/*comparison.png

  ((count++))
    
done
