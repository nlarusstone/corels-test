#!/bin/bash

#SBATCH -n 8                            #The number of cores
#SBATCH -N 1                            #Run on 1 node
#SBATCH --mem=128000                     

#SBATCH -t 1:00:00 #Indicate duration using HH:MM:SS
#SBATCH -p serial_requeue #Based on your duration               

#SBATCH -o ./out/tdata_4_out.txt
#SBATCH -e ./err/tdata_4_err.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nlarusstone@college.harvard.edu

# --------------
# Fill this part out (and the specific fields above)
module load gcc/6.2.0-fasrc01
module load gmp
../src/bbcache -s -t 4 -p 0 -r 0.01 -n 1000000 ../data/tdata_R.out ../data/tdata_R.label
