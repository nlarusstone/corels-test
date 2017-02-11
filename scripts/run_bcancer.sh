#!/bin/bash

#SBATCH -n 1                            #The number of cores
#SBATCH -N 1                            #Run on 1 node
#SBATCH --mem=256000                     

#SBATCH -t 24:00:00 #Indicate duration using HH:MM:SS
#SBATCH -p general #Based on your duration               

#SBATCH -o ./bcancer_out.txt
#SBATCH -e ./bcancer_err.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nlarusstone@college.harvard.edu

# --------------
# Fill this part out (and the specific fields above)
module load gcc/6.2.0-fasrc01
module load gmp
../src/bbcache -c 1 -p 1 -r 0.01 -n 1000000000 ../data/bcancer.out ../data/bcancer.label
