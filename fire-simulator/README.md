# Fire Simulator MPI

## Problem Statement

In this lab assignment, we are going to focus on parallelizing the forest fire simulator using MPI.

This deliverable will be available, if, and only if, you've delivered before the first part (Laplace exercise).

The goal is to implement a basic parallel version of the simulator by exploiting the potential parallelism of work distribution in the sequential program using MPI. We present you (in the file attached to this deliverable) a basic assumptions and recommendations for developing this MPI program. The exercise is straightforward, use MPI to parallelize the code of the program as efficiently as possible, get and discuss the obtained results. What is the speed-up? How efficient is your solution in comparison to OpenMP version? What is the communication overhead? For answering some of these questions, you can obtain valuable data using TAU or MPI_Wtime() function for analyzing the execution of your program.
Each team must submit a report explaining the parallelization carried out, why this parallelization strategy has been used, the experimental study carried out (considering different number of processes and nodes and different tests) and the results obtained. Finally, a discussion on the results reached must be provided. You also must include your codes properly commented and documented.
The code must be included in .c file (or files) and the report in a PDF file. All files must be compressed in one zip file and delivered via Virtual Campus.
The maximum mark is 4.
