#!/bin/bash

## Prints out Cross-Validation results for particular dataset (e.g. compas)
if [ "$#" -ne 3 ]; then
    printf "Usage: ./<filename.sh> [dataset]"
    printf " [path to sbrlmod binary] [path to CV folder]\n"
    printf "e.g. ./<filename.sh> compas ./sbrlmod ../data/CrossValidation\n"
    exit
fi

args=("$@")
dataset=${args[0]}
sbrl=${args[1]}
cv_dir=${args[2]}

temp_f="random_file.txt"
rm $temp_f
echo "CV_fold,eta,lambda,num_rules,test_acc"
for i in `seq 0 9`;
do
    cv_fold=${dataset}_${i}
    cv_fold_path=${cv_dir}/${cv_fold}
    for e in `seq 1 5`;
    do
        for l in `seq 3 10`;
        do
            sbrl_run=$(printf '%s -t 3 -d 1 -e %s -l %s -i 10000 -S 0 %s_train.out %s_train.label %s_test.out %s_test.label' "$sbrl" "$e" "$l" "$cv_fold_path" "$cv_fold_path" "$cv_fold_path" "$cv_fold_path")
            eval "$sbrl_run" >> $temp_f 2>&1
            num_sbrl_rules=$(cat $temp_f | grep -i "The best rulelist" | tr ":" "\n" | tail -n 1 | sed "s/ rules.*//g" | xargs)
            sbrl_acc=$(cat $temp_f | tail -n 1 | sed "s/.*=//g" | xargs)
            echo "$cv_fold,$e,$l,$num_sbrl_rules,$sbrl_acc"
        done
    done
done
rm $temp_f
