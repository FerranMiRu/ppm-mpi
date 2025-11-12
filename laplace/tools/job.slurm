#!/bin/bash

#SBATCH --job-name=mpi-laplace
#SBATCH --output=data/output/execution-results.txt
#SBATCH -N 3
#SBATCH -n 3
#SBATCH --partition=nodo.q

module load openmpi

make
echo

mpirun -np 3 ./executables/mpi_laplace.exe 9 9

echo
make clean
