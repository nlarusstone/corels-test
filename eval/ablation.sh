#!/bin/bash

# ./ablation.sh compas 1000000000 none 0.005
# ./ablation.sh compas 1000000000 identical 0.005
# ./ablation.sh weapon 1000000000 none 0.01
# etc.

args=("$@")
dataset=${args[0]}
n=${args[1]}
ablation=${args[2]}
r=${args[3]}

for i in `seq 0 9`;
do
    bbcache=./../src/bbcache
    out=../data/CrossValidation/${dataset}_${i}_train.out
    label=../data/CrossValidation/${dataset}_${i}_train.label
    minor=../data/CrossValidation/${dataset}_${i}_train.minor
    if [ "$ablation" = "none" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 $out $label $minor &
    elif [ "$ablation" = "priority" ];
    then
        $bbcache -n ${n} -b -r $r -p 1 $out $label $minor &
    elif [ "$ablation" = "support" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 -a 1 $out $label $minor &
    elif [ "$ablation" = "pmap" ];
    then
        $bbcache -n ${n} -c 2 -r $r $out $label $minor &
    elif [ "$ablation" = "lookahead" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 -a 2 $out $label $minor &
    elif [ "$ablation" = "identical" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 $out $label
    fi
done
