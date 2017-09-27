#!/bin/bash

## Writes out Cross-Validation accuracy/sparsity results for particular dataset (e.g. compas)
if [ "$#" -ne 4 ]; then
    printf "Usage: ./CompareSparsity.sh [dataset] [outputfile]"
    printf " [path to sbrlmod binary] [path to CV folder]\n"
    printf "e.g. ./CompareSparsity-ela.sh compas compas_sparsity-CORELS.csv ./sbrlmod ../data/CrossValidation\n"
    printf "e.g. ./CompareSparsity-ela.sh frisk frisk_sparsity-CORELS.csv ./sbrlmod ../data/CrossValidation\n"
    exit
fi

args=("$@")
dataset=${args[0]}
outf=${args[1]}
sbrl=${args[2]}
cv_dir=${args[3]}
printf 'Running Cross Validation folds for %s\n' "$dataset"

rm $outf

temp_f="random_file.txt"
# for i in `seq 0 9`;
# do
#     cv_fold=${dataset}_${i}
#     cv_fold_path=${cv_dir}/${cv_fold}
#     echo "\nCV fold: ${cv_fold}\n"
#     sbrl_run=$(printf '%s -t 3 -d 1 -S 0 %s_train.out %s_train.label %s_test.out %s_test.label' "$sbrl" "$cv_fold_path" "$cv_fold_path" "$cv_fold_path" "$cv_fold_path")
# 
#     echo "RUNNING CART, C4.5, RIPPER"
#     Rscript CompareSparsity.R $cv_fold $outf >> $temp_f 2>&1
# 
#     echo "RUNNING SBRL"
#     eval "$sbrl_run" >> $temp_f 2>&1
#     # super-hack; forgive me. Something quick for KDD deadline
#     sbrl_rules=$(cat $temp_f | grep -i "The best rulelist" | tr ":" "\n" | tail -n 1 | sed "s/ rules.*//g" | xargs)
#     sbrl_acc=$(cat $temp_f | tail -n 1 | sed "s/.*=//g" | xargs)
#     echo "$cv_fold,SBRL,0,0,0,$sbrl_acc,$sbrl_rules" >> $outf
# done

echo "\nRUNNING CORELS for all 10 folds of $dataset"
#echo "using regularization = {0.005, 0.01, 0.02} for compas"
echo "using regularization = {0.0025, 0.01, 0.04} for frisk"
#for R in 0.005 0.01 0.02; do
for R in 0.0025 0.01 0.04; do
    python eval_model.py $dataset --minor -c 2 -p 1 -r $R -n 100000000 --sparsity $outf >> $temp_f 2>&1
done

rm $temp_f

