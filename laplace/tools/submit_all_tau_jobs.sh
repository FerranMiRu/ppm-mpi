#!/bin/bash

# Helper script to submit all TAU profiling jobs
# This will queue all experiments for blocking vs non-blocking comparison
# with both strong and weak scaling tests

echo "=========================================="
echo "Submitting TAU Profiling Jobs"
echo "=========================================="
echo ""

# Make sure output directories exist
mkdir -p data/output
mkdir -p data/tau_results

echo "Submitting 1 node (12 processors) job..."
sbatch tools/tau_1node.slurm
echo ""

echo "Submitting 2 nodes (24 processors) job..."
sbatch tools/tau_2nodes.slurm
echo ""

echo "Submitting 4 nodes (48 processors) job..."
sbatch tools/tau_4nodes.slurm
echo ""

echo "Submitting 8 nodes (96 processors) job..."
sbatch tools/tau_8nodes.slurm
echo ""

echo "Submitting 10 nodes (120 processors) job..."
sbatch tools/tau_10nodes.slurm
echo ""

echo "=========================================="
echo "All jobs submitted!"
echo "=========================================="
echo ""
echo "Check job status with: squeue -u \$USER"
echo "Cancel all jobs with: scancel -u \$USER"
echo ""
echo "Results will be saved in:"
echo "  - data/output/tau_*nodes_*.out (SLURM output)"
echo "  - data/tau_results/*/ (TAU profiles and traces)"
echo ""
