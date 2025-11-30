# Laplace MPI

## Problem Statement

In this lab assignment, we will focus on parallelizing the solution of the Laplace problem using MPI.

Previous to compiling mpi, it may require a run in terminal: module load openmpi.

You must use the SLURM queue to run more than one node. Check the guides on this course, and be
aware of using too many nodes: Test 2, 3, or 4 nodes; what speedup do you achieve? Is it what you
expect?

The goal is to implement a basic parallel version of the Laplace program by exploiting the potential
parallelism of work distribution in the sequential program using MPI. We present you (in the file
attached to this deliverable) a basic scheme (pseudo-code) and recommendations for developing this
MPI program. The exercise is straightforward: use MPI to parallelize the program's code as
efficiently as possible and get and discuss the obtained results. What is the speed-up? How
efficient is your solution compared to the OpenMP version? What is the communication overhead? To
answer some of these questions, you can obtain valuable data using the TAU or MPI_Wtime() function
to analyze the execution of your program.
Each team must submit a report explaining the parallelization carried out, why this parallelization
strategy has been used, the experimental study carried out (considering different numbers of
processes and nodes and different matrix sizes), and the results obtained. Finally, a discussion of
the results reached must be provided. You also must include your codes, which must be properly
commented on and documented.
The code must be included in a .c file (or files), and the report in a PDF file. All files must be
compressed into one zip file and delivered via Virtual Campus.

The maximum mark is 6.

### OpenMP Results

Parallel time 12 threads : 0.4101 seconds

### OpenMPI Results

Blocking time: 3.3192 seconds
Non-Blocking time: 3.5428 seconds

## Experiments

For all dimensions try weak and strong scaling.

Dimensions:

- Blocking vs Non-blocking communication
- MPI process mapping fill-node-first vs round-robin

## Real Output

MATRIX 9 x 9
Iteration 10 -> Error = 0.127748
Iteration 20 -> Error = 0.075729
Iteration 30 -> Error = 0.050112
Iteration 40 -> Error = 0.033732
Iteration 50 -> Error = 0.022705
Iteration 60 -> Error = 0.015282
Iteration 70 -> Error = 0.010286
Iteration 80 -> Error = 0.006925
Iteration 90 -> Error = 0.004660
Iteration 100 -> Error = 0.003134

MATRIX 4080 x 4080
Iteration 10 -> Error = 0.155006
Iteration 20 -> Error = 0.110024
Iteration 30 -> Error = 0.089901
Iteration 40 -> Error = 0.077374
Iteration 50 -> Error = 0.069623
Iteration 60 -> Error = 0.063285
Iteration 70 -> Error = 0.058825
Iteration 80 -> Error = 0.054945
Iteration 90 -> Error = 0.051831
Iteration 100 -> Error = 0.049207
