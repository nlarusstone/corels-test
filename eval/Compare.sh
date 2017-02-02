#!/bin/bash

## Prints out Cross-Validation results for particular dataset (e.g. compas)
## Assumes that data files are in 'data/CrossValidation'
if [ "$#" -ne 4 ]; then
    printf "Usage: ./Compare.sh [dataset]"
    printf " [path to bbrl binary] [path to sbrlmod binary] [path to CV folder]\n"
    printf "e.g. ./Compare.sh compas ./bbcache ./sbrlmod ../data/CrossValidation\n"
    exit
fi

args=("$@")
dataset=${args[0]}
bbrl=${args[1]}
sbrl=${args[2]}
cv_dir=${args[3]}
printf 'Running Cross Validation folds for %s\n' "$dataset"

temp_f="random_file.txt"
for i in `seq 0 9`;
do
    cv_fold=${dataset}_${i}
    cv_fold_path=${cv_dir}/${cv_fold}
    echo "\nCV fold: ${cv_fold}\n"
    sbrl_run=$(printf '%s -t 3 -d 1 %s_train.out %s_train.label %s_test.out %s_test.label' "$sbrl" "$cv_fold_path" "$cv_fold_path" "$cv_fold_path" "$cv_fold_path")
    echo "RUNNING SBRL"
    eval "$sbrl_run" >> $temp_f 2>&1
    echo $(tail -n 1 $temp_f)
    echo "RUNNING GLM, SVM, Adaboost, CART, C4.5, RF, RIPPER"
    Rscript Compare.R $cv_fold >> $temp_f 2>&1
    echo $(tail -n 1 $temp_f)
done

echo "\nRUNNING BBRL for all 10 folds of $dataset"
rm $temp_f
python eval_model.py $dataset --parallel -n 100000 -r 0.01 -c 1 -p 1 >> $temp_f 2>&1
echo $(tail -n 1 $temp_f)

rm $temp_f

