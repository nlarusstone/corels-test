#!/bin/bash

#SBATCH -n 1                            #The number of cores
#SBATCH -N 1                            #Run on 1 node
#SBATCH --mem=256000                     

#SBATCH -t 4:00:00 #Indicate duration using HH:MM:SS
#SBATCH -p general #Based on your duration               

#SBATCH -o ./out/lookahead_compas_%a_out.txt
#SBATCH -e ./err/lookahead_compas_%a_err.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nlarusstone@college.harvard.edu

# --------------
# Fill this part out (and the specific fields above)
#export $SLURM_ARRAY_TASK_ID 0
OUT=../data/CrossValidation/compas_"$SLURM_ARRAY_TASK_ID"_train.out
LABEL=../data/CrossValidation/compas_"$SLURM_ARRAY_TASK_ID"_train.label
MINOR=../data/CrossValidation/compas_"$SLURM_ARRAY_TASK_ID"_train.minor
cd ../../src/
module load gcc/6.2.0-fasrc01
module load gmp
#module load python/2.7.11-fasrc01
#source activate bbcache
eval ./bbcache -c 2 -n 1000000000 -p 1 -r 0.005 -a 2 "$OUT" "$LABEL" "$MINOR"
#python eval_model.py --minor compas -n 1000000000 -r 0.005 -c 1 -p 1
