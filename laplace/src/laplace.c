#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    const float tol = 1.0e-3f * 1.0e-3f;
    const float exp_PI = exp(-M_PI);

    int n, m, iter, iter_max = 100;
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

    // Main loop: iterate until error <= tol a maximum of iter_max iterations
    iter = 0;
    while (error > tol && iter < iter_max) {
        // Compute new values using main matrix and writing into auxiliary matrix
        // Compute error = maximum of the square root of the absolute differences
        error = 0.0;
        for (int i = 1; i < n - 1; i++) {
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

        // if number of iterations is multiple of 10 then print error on the screen
        iter++;
        if (iter % 10 == 0) {
            printf("Iteration %i -> Error = %f\n", iter, sqrtf(error));
        }
    }

    free(A);
    free(Anew);
}
