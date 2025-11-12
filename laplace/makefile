CC = mpicc
# CFLAGS = -O3 -march=native
CFLAGS =
MPIFLAGS = -lmpi
LDFLAGS = -lm

ALL_TARGETS = laplace.exe mpi_laplace.exe

all: $(ALL_TARGETS)

laplace.exe: src/laplace.c create_executables_dir
	$(CC) $(CFLAGS) $< -o executables/$@ $(LDFLAGS)

mpi_laplace.exe: src/mpi_laplace.c create_executables_dir
	$(CC) $(CFLAGS) $< -o executables/$@ $(LDFLAGS) $(MPIFLAGS)

create_executables_dir:
	mkdir -p executables

clean:
	find . -name ".DS_Store" -type f -delete
	rm -rf executables/
	rm -rf *.dSYM

.PHONY: all clean create_executables_dir
