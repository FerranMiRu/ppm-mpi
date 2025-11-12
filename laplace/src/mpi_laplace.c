#include <math.h>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    const float tol = 1.0e-3f * 1.0e-3f;
    const float exp_PI = exp(-M_PI);

    int n, m, process_start_n, process_finish_n, iter, rank, size, iter_max = 100;
    float error, point_error;
    float *A, *Anew, *Atmp;

    error = 1.0;

    if (argc < 3) {
        printf(
            "ERROR: Provide the size of the matrix (N, M) as the first and second "
            "arguments\n");
        exit(1);
    }
    n = atoi(argv[1]);
    m = atoi(argv[2]);

    if ((A = malloc(sizeof(float) * n * m)) == NULL) {
        printf("Malloc of A failed!\n");
        exit(1);
    }
    if ((Anew = malloc(sizeof(float) * n * m)) == NULL) {
        printf("Malloc of Anew failed!\n");
        exit(1);
    }

    // get iter_max from command line at execution time
    if (argc >= 4) {
        iter_max = atoi(argv[3]);
    }

    // set all values in matrix as zero
    // set boundary conditions
    for (int i = 0; i < n; i++) {
        float calculation = sinf(i * M_PI / (n - 1));

        A[i * m + 0] = calculation;
        A[i * m + m - 1] = exp_PI * calculation;

        Anew[i * m + 0] = A[i * m + 0];
        Anew[i * m + m - 1] = A[i * m + m - 1];

        for (int j = 1; j < m - 1; j++) {
            A[i * m + j] = 0;
        }
    }

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    process_start_n = rank * n / size;
    process_finish_n = (rank + 1) * n / size;

    if (rank == 0)
        process_start_n++;
    else if (rank == size - 1)
        process_finish_n--;

    // Main loop: iterate until error <= tol a maximum of iter_max iterations
    iter = 0;
    while (error > tol && iter < iter_max) {
        // Compute new values using main matrix and writing into auxiliary matrix
        // Compute error = maximum of the square root of the absolute differences
        error = 0.0;

        for (int i = process_start_n; i < process_finish_n; i++) {
            for (int j = 1; j < m - 1; j++) {
                Anew[i * m + j] = (A[(i - 1) * m + j] + A[(i + 1) * m + j] + A[i * m + (j - 1)] +
                                   A[i * m + (j + 1)]) /
                                  4;

                point_error = fabsf(Anew[i * m + j] - A[i * m + j]);

                error = fmaxf(error, point_error);
            }
        }

        // Copy from auxiliary matrix to main matrix
        Atmp = A;
        A = Anew;
        Anew = Atmp;

        if (rank == 0) {
            MPI_Send(&A[(process_finish_n - 1) * m], m, MPI_FLOAT, 1, 0, MPI_COMM_WORLD);
        } else if (rank == size - 1) {
            MPI_Recv(&A[(process_start_n - 1) * m], m, MPI_FLOAT, rank - 1, MPI_ANY_TAG,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        } else {
            MPI_Recv(&A[(process_start_n - 1) * m], m, MPI_FLOAT, rank - 1, MPI_ANY_TAG,
                     MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Send(&A[(process_finish_n - 1) * m], m, MPI_FLOAT, rank + 1, 0, MPI_COMM_WORLD);
        }

        if (rank == 0) {
            MPI_Recv(&A[process_finish_n * m], m, MPI_FLOAT, 1, MPI_ANY_TAG, MPI_COMM_WORLD,
                     MPI_STATUS_IGNORE);
        } else if (rank == size - 1) {
            MPI_Send(&A[process_start_n * m], m, MPI_FLOAT, rank - 1, 0, MPI_COMM_WORLD);
        } else {
            MPI_Recv(&A[process_finish_n * m], m, MPI_FLOAT, rank + 1, MPI_ANY_TAG, MPI_COMM_WORLD,
                     MPI_STATUS_IGNORE);
            MPI_Send(&A[process_start_n * m], m, MPI_FLOAT, rank - 1, 0, MPI_COMM_WORLD);
        }

        MPI_Allreduce(&error, &error, 1, MPI_FLOAT, MPI_MAX, MPI_COMM_WORLD);

        // if number of iterations is multiple of 10 then print error on the screen
        iter++;
        if (iter % 10 == 0 && rank == 0) {
            printf("Iteration %i -> Error = %f\n", iter, sqrtf(error));
        }
    }

    MPI_Finalize();

    free(A);
    free(Anew);
}
