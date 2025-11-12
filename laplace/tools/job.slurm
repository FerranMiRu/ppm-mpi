#!/bin/bash

#SBATCH --job-name=parallel-fire-simulator-job
#SBATCH --output=data/output/execution-results.txt
#SBATCH -N 1
#SBATCH -n 12
#SBATCH --partition=aolin.q

module add gcc/13.2.1
export OMP_NUM_THREADS=12

make

for file_name in test1 test2 test3 test4; do
    echo "#################### $file_name ####################"
    echo
    # echo "========= EXTINGUISHING ========="
    # perf stat ./executables/extinguishing.exe -f data/input/$file_name
    # echo

    echo "========= PARALLEL EXTINGUISHING ========="
    perf stat ./executables/parallel_extinguishing.exe -f data/input/$file_name
    echo
    echo
done

make clean
