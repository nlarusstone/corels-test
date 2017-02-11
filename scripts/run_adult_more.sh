#!/bin/bash

#SBATCH -n 1                            #The number of cores
#SBATCH -N 1                            #Run on 1 node
#SBATCH --mem=256000                     

#SBATCH -t 12:00:00 #Indicate duration using HH:MM:SS
#SBATCH -p general #Based on your duration               

#SBATCH -o ./adult_more_out.txt
#SBATCH -e ./adult_more_err.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nlarusstone@college.harvard.edu

# --------------
# Fill this part out (and the specific fields above)
module load gcc/6.2.0-fasrc01
module load gmp
../src/bbcache -c 2 -p 1 -r 0.01 -n 2000000000 ../data/adult_R.out ../data/adult_R.label
