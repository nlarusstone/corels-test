#!/bin/bash

#SBATCH -n 1                            #The number of cores should match the '--threads' parameter of subjunc
#SBATCH -N 1                            #Run on 1 node
#SBATCH --mem=256000                     

#SBATCH -t 16:00:00 #Indicate duration using HH:MM:SS
#SBATCH -p general #Based on your duration               

#SBATCH -o ./compas_out_2.txt
#SBATCH -e ./compas_err.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nlarusstone@college.harvard.edu

# --------------
# Fill this part out (and the specific fields above)
module load gcc/6.2.0-fasrc01
module load gmp
../src/bbcache -c 2 -n 500000000 -p 1 -r 0.001 ../data/compas.out ../data/compas.label
