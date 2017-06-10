#!/bin/bash

## Prints out Cross-Validation results for particular dataset (e.g. compas)
if [ "$#" -ne 2 ]; then
    printf "e.g. ./c45.sh frisk ../data/CrossValidation\n"
    exit
fi

args=("$@")
dataset=${args[0]}
cv_dir=${args[1]}
printf 'Running Cross Validation folds for %s\n' "$dataset"

temp_f="random_file.txt"
for i in `seq 0 9`;
do
    cv_fold=${dataset}_${i}
    cv_fold_path=${cv_dir}/${cv_fold}
    echo "\nCV fold: ${cv_fold}\n"
    Rscript c45.R $cv_fold >> $temp_f 2>&1
    echo $(tail -n 1 $temp_f)
done
