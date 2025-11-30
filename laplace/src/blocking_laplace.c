#include <math.h>
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    const float tol = 1.0e-3f * 1.0e-3f;
    const float exp_PI = exp(-M_PI);

    int n, m, process_n, rank_n_step, iter, rank, size, iter_max = 100, i, j, p, row_index;
    float error, point_error, calculation;
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

    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    rank_n_step = n / size;

    if (rank == 0 || rank == size - 1) {
        process_n = rank_n_step + 1;
    } else {
        process_n = rank_n_step + 2;
    }

    if ((A = malloc(sizeof(float) * process_n * m)) == NULL) {
        printf("Malloc of A failed!\n");
        exit(1);
    }
    if ((Anew = malloc(sizeof(float) * process_n * m)) == NULL) {
        printf("Malloc of Anew failed!\n");
        exit(1);
    }

    // get iter_max from command line at execution time
    if (argc >= 4) {
        iter_max = atoi(argv[3]);
    }

    // set all values in matrix as zero
    // set boundary conditions
    for (i = 0; i < process_n; i++) {
        row_index = i + rank * rank_n_step;

        if (rank != 0) row_index -= 1;

        calculation = sinf(row_index * M_PI / (n - 1));

        A[i * m + 0] = calculation;
        A[i * m + m - 1] = exp_PI * calculation;

        Anew[i * m + 0] = A[i * m + 0];
        Anew[i * m + m - 1] = A[i * m + m - 1];

        for (j = 1; j < m - 1; j++) {
            A[i * m + j] = 0;
            Anew[i * m + j] = 0;
        }
    }

    // Main loop: iterate until error <= tol a maximum of iter_max iterations
    iter = 0;
    while (error > tol && iter < iter_max) {
        // Compute new values using main matrix and writing into auxiliary matrix
        // Compute error = maximum of the square root of the absolute differences
        error = 0.0;

        for (i = 1; i < process_n - 1; i++) {
            for (j = 1; j < m - 1; j++) {
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

        if (rank > 0) {
            MPI_Sendrecv(&A[m], m, MPI_FLOAT, rank - 1, rank, &A[0], m, MPI_FLOAT, rank - 1,
                         rank - 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
        if (rank < size - 1) {
            MPI_Sendrecv(&A[(process_n - 2) * m], m, MPI_FLOAT, rank + 1, rank,
                         &A[(process_n - 1) * m], m, MPI_FLOAT, rank + 1, rank + 1, MPI_COMM_WORLD,
                         MPI_STATUS_IGNORE);
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
