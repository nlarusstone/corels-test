#!/bin/bash

# ./ablation.sh compas 1000000000 none background
# ./ablation.sh compas 1000000000 identical serial
# etc.

args=("$@")
dataset=${args[0]}
n=${args[1]}
ablation=${args[2]}
mode=${args[3]}

if [ "$mode" = "background" ];
then
    background=&
elif [ "$mode" = "serial" ];
then
    background=
fi

for i in `seq 0 9`;
do
    bbcache=./../src/bbcache
    out=../data/CrossValidation/${dataset}_${i}_train.out
    label=../data/CrossValidation/${dataset}_${i}_train.label
    minor=../data/CrossValidation/${dataset}_${i}_train.minor
    if [ "$ablation" = "none" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 $out $label $minor $background
    elif [ "$ablation" = "priority" ];
    then
        $bbcache -n ${n} -b -r 0.005 -p 1 $out $label $minor $background
    elif [ "$ablation" = "support" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 -a 1 $out $label $minor $background
    elif [ "$ablation" = "pmap" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 $out $label $minor $background
    elif [ "$ablation" = "lookahead" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 -a 2 $out $label $minor $background
    elif [ "$ablation" = "identical" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 $out $label $background
    fi
done
