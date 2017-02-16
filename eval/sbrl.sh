#!/bin/bash

for i in `seq 0 9`;
do
    train_out=../data/CrossValidation/frisk_${i}_train.out
    train_label=../data/CrossValidation/frisk_${i}_train.label
    test_out=../data/CrossValidation/frisk_${i}_test.out
    test_label=../data/CrossValidation/frisk_${i}_test.label
    ./sbrlmod -t 3 -d 1 -S 0 $train_out $train_label $test_out $test_label
done
