# Laplace MPI Experiments - Tools Guide

## Quick Start

```bash
# 1. Submit all experiments
./tools/submit_all_tau_jobs.sh

# 2. Monitor jobs
squeue -u $USER

# 3. Parse results (after completion)
python3 tools/parse_tau_results.py
```

Results will be in `data/tau_results/`:

- `blocking_strong.csv`
- `blocking_weak.csv`
- `nonblocking_strong.csv`
- `nonblocking_weak.csv`

---

## Experiments Overview

**20 total experiments** comparing blocking vs non-blocking MPI communication:

| Nodes | Procs | Strong Scaling | Weak Scaling  |
| ----- | ----- | -------------- | ------------- |
| 1     | 12    | 24000 x 24000  | 2400 x 2400   |
| 2     | 24    | 24000 x 24000  | 4800 x 4800   |
| 4     | 48    | 24000 x 24000  | 9600 x 9600   |
| 8     | 96    | 24000 x 24000  | 19200 x 19200 |
| 10    | 120   | 24000 x 24000  | 24000 x 24000 |

Each configuration runs 4 tests: blocking/non-blocking × strong/weak

---

## Files

### SLURM Scripts (in `tools/`)

- `tau_1node.slurm` through `tau_10nodes.slurm` - Individual experiments
- `submit_all_tau_jobs.sh` - Submit all at once

### Helper Scripts

- `parse_tau_results.py` - Extract timing data from TAU profiles
- `makefile` - Includes TAU compilation targets with optimization flags

### Source Code (in `src/`)

- `blocking_laplace.c` - Uses `MPI_Sendrecv`
- `non_blocking_laplace.c` - Uses `MPI_Isend/Irecv/Waitall`

---

## Commands Reference

### Job Management

```bash
# Submit
sbatch tools/tau_1node.slurm          # Individual job
./tools/submit_all_tau_jobs.sh        # All jobs

# Monitor
squeue -u $USER                       # Your jobs
squeue                                # All jobs
scontrol show job <jobid>             # Job details

# Cancel
scancel <jobid>                       # Specific job
scancel -u $USER                      # All your jobs
```

### Check Results

```bash
# SLURM output
cat data/output/tau_1node_*.out
tail -f data/output/tau_1node_*.out   # Follow in real-time

# List experiments
ls -la data/tau_results/

# Quick check
grep "main" data/tau_results/1node_blocking_strong/profile_summary.txt
```

### Parse Results

```bash
# Run parser
python3 tools/parse_tau_results.py

# View CSVs
cat data/tau_results/blocking_strong.csv
cat data/tau_results/nonblocking_weak.csv
```

---

## Understanding Results

### CSV Columns

**Strong Scaling Files:**

- `processors` - Number of MPI processes
- `nodes` - Number of cluster nodes
- `total_time` - Total execution time (seconds)
- `comm_time` - Communication time (MPI calls)
- `comp_time` - Computation time
- `comm_percent` - Communication as % of total
- `speedup` - Speedup vs 12-processor baseline
- `efficiency` - Parallel efficiency %

**Weak Scaling Files:**

- Same as strong, but `efficiency` = T(12)/T(p) × 100%

### Key Metrics

**From profile_summary.txt:**

- Total time = Inclusive time of `main()`
- Comm time = Sum of MPI function times (Sendrecv/Isend/Irecv/Wait/Allreduce)
- Comp time = Total - Comm

**Calculated:**

- Speedup = T(baseline) / T(current)
- Efficiency = (Speedup / Ideal_Speedup) × 100%
- Comm % = (Comm_Time / Total_Time) × 100%

---

## For Your Report

### Graphs to Create

1. **Strong Scaling Speedup** - Line graph: processors vs speedup (compare to ideal)
2. **Strong Scaling Efficiency** - Line graph: processors vs efficiency %
3. **Weak Scaling Efficiency** - Line graph: should stay near 100%
4. **Communication Overhead** - Stacked bar: computation + communication time
5. **Communication %** - Line graph: how it grows with scale

### Discussion Points

- How does speedup compare to ideal?
- Is non-blocking better than blocking? By how much?
- What's the communication overhead trend?
- Weak scaling: does time stay constant?
- Compare to OpenMP results (from README)

---

## File Structure

```
laplace/
├── tools/
│   ├── tau_*.slurm                    # SLURM job scripts
│   ├── submit_all_tau_jobs.sh         # Submit helper
│   └── parse_tau_results.py           # Parse TAU output
├── src/
│   ├── blocking_laplace.c             # Blocking version
│   └── non_blocking_laplace.c         # Non-blocking version
├── data/
│   ├── output/                        # SLURM logs
│   └── tau_results/                   # TAU profiles + CSVs
│       ├── 1node_blocking_strong/
│       ├── 1node_blocking_weak/
│       ├── ... (20 directories)
│       ├── blocking_strong.csv        # Results
│       ├── blocking_weak.csv
│       ├── nonblocking_strong.csv
│       └── nonblocking_weak.csv
└── makefile                           # Includes TAU targets
```

---

## Troubleshooting

| Problem            | Solution                                            |
| ------------------ | --------------------------------------------------- |
| Job stuck in queue | Check `sinfo`, wait or resubmit                     |
| Job fails          | Check `data/output/tau_*.out` for errors            |
| No TAU files       | Verify modules loaded in SLURM script               |
| Parser shows zeros | Check `profile_summary.txt` exists and has data     |
| Out of memory      | Reduce problem size in SLURM script                 |
| Compilation fails  | Ensure TAU modules loaded: `module load tau/2.32.1` |

---

## TAU Compilation

The makefile includes TAU targets with optimization flags (`-O3 -march=native`):

```bash
make blocking_laplace_tau       # Compile blocking version with TAU
make non_blocking_laplace_tau   # Compile non-blocking version with TAU
```

SLURM scripts automatically use these makefile targets.

---

## Tips

- Submit jobs during off-peak hours for faster queue times
- Test one job first before submitting all 5
- Back up CSV files - they're your final results
- Check that all 20 experiment directories exist before parsing
- Use the parser output tables for quick validation

---

## Timeline

- Job submission: 1 min
- Queue wait: 5-60 min (varies by cluster load)
- Execution: 30-90 min (jobs may run in parallel)
- Parse results: 1 min
- Total: ~1-2 hours

---

## Need Help?

- SLURM docs: `man sbatch`, `man squeue`
- TAU docs: `man tau_exec`
- Check SLURM output files for error messages
- Verify modules: `module list`
- Test with smaller problem sizes first
