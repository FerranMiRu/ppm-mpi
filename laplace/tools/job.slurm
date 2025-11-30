#!/bin/bash

#SBATCH -N 1  # nodes
#SBATCH -n 12  # processors
#SBATCH --exclusive
#SBATCH --distribution=cyclic
#SBATCH --partition=nodo.q
#SBATCH --job-name=mpi-laplace
#SBATCH --output=data/output/execution-results.txt

module load openmpi

make
echo

perf stat mpirun -np 12 ./executables/blocking_laplace.exe 4080 4080

echo

perf stat mpirun -np 12 ./executables/non_blocking_laplace.exe 4080 4080

echo
make clean
