#!/bin/bash

## Writes out Cross-Validation accuracy/sparsity results for particular dataset (e.g. compas)
if [ "$#" -ne 3 ]; then
    printf "Usage: ./CompareSparsity.sh [dataset] [outputfile] [datadir]"
    printf "e.g. ./Compare.sh compas compas_sparsity.csv ../data/CrossValidation\n"
    exit
fi

args=("$@")
dataset=${args[0]}
outf=${args[1]}
cv_dir=${args[2]}
printf 'Running Cross Validation folds for %s\n' "$dataset"

rm $outf

temp_f="random_file.txt"
for i in `seq 0 9`;
do
    cv_fold=${dataset}_${i}
    cv_fold_path=${cv_dir}/${cv_fold}
    echo "\nCV fold: ${cv_fold}\n"
    echo "RUNNING C4.5"
    Rscript CompareSparsity.R $cv_fold $outf >> $temp_f 2>&1
done
