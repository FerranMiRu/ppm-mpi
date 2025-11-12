# Laplace MPI

## Problem Statement

In this lab assignment, we will focus on parallelizing the solution of the Laplace problem using MPI.

Previous to compiling mpi, it may require a run in terminal: module load openmpi.

You must use the SLURM queue to run more than one node. Check the guides on this course, and be aware of using too many nodes: Test 2, 3, or 4 nodes; what speedup do you achieve? Is it what you expect?

The goal is to implement a basic parallel version of the Laplace program by exploiting the potential parallelism of work distribution in the sequential program using MPI. We present you (in the file attached to this deliverable) a basic scheme (pseudo-code) and recommendations for developing this MPI program. The exercise is straightforward: use MPI to parallelize the program's code as efficiently as possible and get and discuss the obtained results. What is the speed-up? How efficient is your solution compared to the OpenMP version? What is the communication overhead? To answer some of these questions, you can obtain valuable data using the TAU or MPI_Wtime() function to analyze the execution of your program.
Each team must submit a report explaining the parallelization carried out, why this parallelization strategy has been used, the experimental study carried out (considering different numbers of processes and nodes and different matrix sizes), and the results obtained. Finally, a discussion of the results reached must be provided. You also must include your codes, which must be properly commented on and documented.
The code must be included in a .c file (or files), and the report in a PDF file. All files must be compressed into one zip file and delivered via Virtual Campus.

The maximum mark is 6.
