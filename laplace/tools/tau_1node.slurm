#!/bin/bash

#SBATCH --job-name=tau_1node
#SBATCH -N 1 # number of nodes
#SBATCH -n 12 # number of cores/processes
#SBATCH --exclusive
#SBATCH --partition=nodo.q
#SBATCH --output=data/output/tau_1node_%j.out

module load openmpi/4.1.1
module load tau/2.32.1

# Use the MPI TAU config
export TAU_MAKEFILE=/soft/tau-2.32.1/x86_64/lib/Makefile.tau-mpi
# Instrument user code via compiler
export TAU_OPTIONS='-optCompInst'
# Enable output
export TAU_PROFILE=1
export TAU_TRACE=1

# Create output directories
mkdir -p data/tau_results/1node_blocking_strong
mkdir -p data/tau_results/1node_blocking_weak
mkdir -p data/tau_results/1node_nonblocking_strong
mkdir -p data/tau_results/1node_nonblocking_weak

echo "=========================================="
echo "1 Node (12 processors) - TAU Profiling"
echo "=========================================="

# BLOCKING - STRONG SCALING (24000x24000, 100 iterations)
echo ""
echo "Running BLOCKING - Strong Scaling (24000x24000, 100 iter)"
cd data/tau_results/1node_blocking_strong
make -C ../../.. blocking_laplace_tau
cp ../../../blocking_laplace_tau .
mpirun -np 12 tau_exec -T mpi ./blocking_laplace_tau 24000 24000 100
tau_treemerge.pl
tau2slog2 tau.trc tau.edf -o tau.slog2
pprof > profile_summary.txt
cd ../../..

# BLOCKING - WEAK SCALING (2400x2400, 100 iterations - 200 rows per proc)
echo ""
echo "Running BLOCKING - Weak Scaling (2400x2400, 100 iter)"
cd data/tau_results/1node_blocking_weak
make -C ../../.. blocking_laplace_tau
cp ../../../blocking_laplace_tau .
mpirun -np 12 tau_exec -T mpi ./blocking_laplace_tau 2400 2400 100
tau_treemerge.pl
tau2slog2 tau.trc tau.edf -o tau.slog2
pprof > profile_summary.txt
cd ../../..

# NON-BLOCKING - STRONG SCALING (24000x24000, 100 iterations)
echo ""
echo "Running NON-BLOCKING - Strong Scaling (24000x24000, 100 iter)"
cd data/tau_results/1node_nonblocking_strong
make -C ../../.. non_blocking_laplace_tau
cp ../../../non_blocking_laplace_tau .
mpirun -np 12 tau_exec -T mpi ./non_blocking_laplace_tau 24000 24000 100
tau_treemerge.pl
tau2slog2 tau.trc tau.edf -o tau.slog2
pprof > profile_summary.txt
cd ../../..

# NON-BLOCKING - WEAK SCALING (2400x2400, 100 iterations - 200 rows per proc)
echo ""
echo "Running NON-BLOCKING - Weak Scaling (2400x2400, 100 iter)"
cd data/tau_results/1node_nonblocking_weak
make -C ../../.. non_blocking_laplace_tau
cp ../../../non_blocking_laplace_tau .
mpirun -np 12 tau_exec -T mpi ./non_blocking_laplace_tau 2400 2400 100
tau_treemerge.pl
tau2slog2 tau.trc tau.edf -o tau.slog2
pprof > profile_summary.txt
cd ../../..

echo ""
echo "=========================================="
echo "1 Node experiments completed!"
echo "=========================================="
