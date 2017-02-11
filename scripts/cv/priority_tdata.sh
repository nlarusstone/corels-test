#!/bin/bash

#SBATCH -n 4                            #The number of cores
#SBATCH -N 1                            #Run on 1 node
#SBATCH --mem=256000                     

#SBATCH -t 6:00:00 #Indicate duration using HH:MM:SS
#SBATCH -p general #Based on your duration               

#SBATCH -o ./out/priority_tdata_out.txt
#SBATCH -e ./err/priority_tdata_err.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=nlarusstone@college.harvard.edu

# --------------
# Fill this part out (and the specific fields above)
cd ../../eval/
module load gcc/6.2.0-fasrc01
module load gmp
module load python/2.7.11-fasrc01
source activate bbcache
python eval_model.py tictactoe -n 1000000000 -r 0.001 -b -p 1
