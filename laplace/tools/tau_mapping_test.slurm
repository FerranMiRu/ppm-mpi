#!/bin/bash

#SBATCH --job-name=tau_mapping_test
#SBATCH -N 4 # number of nodes
#SBATCH -n 48 # number of cores/processes
#SBATCH --exclusive
#SBATCH --partition=nodo.q
#SBATCH --output=logs/tau_mapping_test_%j.out

# TAU Mapping Test: Default vs Round-Robin
# Tests impact of MPI process mapping on communication overhead
# Configuration: 4 nodes, 48 processors, 24000x24000 matrix, blocking

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
mkdir -p data/tau_results/mapping_default
mkdir -p data/tau_results/mapping_roundrobin

# Problem size
SIZE=24000
ITERATIONS=100

echo "========================================================================"
echo "TAU MPI MAPPING TEST"
echo "Configuration: 4 nodes, 48 processors"
echo "Problem size: ${SIZE}x${SIZE}, Iterations: ${ITERATIONS}"
echo "========================================================================"

# Test 1: Default mapping (fill nodes sequentially)
echo ""
echo "Test 1: Default Mapping (fill nodes sequentially)"
echo "------------------------------------------------------------------------"
cd data/tau_results/mapping_default
make -C ../../.. blocking_laplace_tau
cp ../../../blocking_laplace_tau .

mpirun --bind-to core -np 48 tau_exec -T mpi ./blocking_laplace_tau ${SIZE} ${SIZE} ${ITERATIONS}

# Generate profile summary
tau_treemerge.pl
tau2slog2 tau.trc tau.edf -o tau.slog2
pprof >profile_summary.txt

echo "Default mapping results saved to: data/tau_results/mapping_default/"
cd ../../..

# Test 2: Round-robin mapping (distribute across nodes)
echo ""
echo "Test 2: Round-Robin Mapping (distribute across nodes)"
echo "------------------------------------------------------------------------"
cd data/tau_results/mapping_roundrobin
make -C ../../.. blocking_laplace_tau
cp ../../../blocking_laplace_tau .

mpirun --map-by node --bind-to core -np 48 tau_exec -T mpi ./blocking_laplace_tau ${SIZE} ${SIZE} ${ITERATIONS}

# Generate profile summary
tau_treemerge.pl
tau2slog2 tau.trc tau.edf -o tau.slog2
pprof >profile_summary.txt

echo "Round-robin mapping results saved to: data/tau_results/mapping_roundrobin/"
cd ../../..

echo ""
echo "========================================================================"
echo "MAPPING TEST COMPLETE"
echo "========================================================================"
echo "Results can be parsed with:"
echo "  python3 tools/parse_tau_results.py data/tau_results"
echo ""
echo "To compare results manually:"
echo "  grep 'main' data/tau_results/mapping_*/profile_summary.txt"
echo "========================================================================"
