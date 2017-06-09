#!/bin/bash

# ./sbrl.sh compas > compas_sparsity-sbrl-eta=15-lambda=5.txt
# ./sbrl.sh frisk > frisk_sparsity-sbrl-eta=15-lambda=5.txt

args=("$@")
dataset=${args[0]}

for i in `seq 0 9`;
do
    train_out=../data/CrossValidation/${dataset}_${i}_train.out
    train_label=../data/CrossValidation/${dataset}_${i}_train.label
    test_out=../data/CrossValidation/${dataset}_${i}_test.out
    test_label=../data/CrossValidation/${dataset}_${i}_test.label
    ./sbrlmod -t 3 -d 1 -e 15 -l 5 -i 10000 -S 0 $train_out $train_label $test_out $test_label
done
