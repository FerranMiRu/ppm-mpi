CC = mpicc
CFLAGS = -O3 -march=native
MPIFLAGS = -lmpi
LDFLAGS = -lm
TAU_CC = tau_cc.sh
TAU_CFLAGS = -O3 -march=native

ALL_TARGETS = laplace.exe blocking_laplace.exe non_blocking_laplace.exe

all: $(ALL_TARGETS)

laplace.exe: src/laplace.c create_executables_dir
	gcc $(CFLAGS) $< -o executables/$@ $(LDFLAGS)

blocking_laplace.exe: src/blocking_laplace.c create_executables_dir
	$(CC) $(CFLAGS) $< -o executables/$@ $(LDFLAGS) $(MPIFLAGS)

non_blocking_laplace.exe: src/non_blocking_laplace.c create_executables_dir
	$(CC) $(CFLAGS) $< -o executables/$@ $(LDFLAGS) $(MPIFLAGS)

blocking_laplace_tau: src/blocking_laplace.c
	$(TAU_CC) $(TAU_CFLAGS) $< -o $@ $(LDFLAGS) -lstdc++

non_blocking_laplace_tau: src/non_blocking_laplace.c
	$(TAU_CC) $(TAU_CFLAGS) $< -o $@ $(LDFLAGS) -lstdc++

create_executables_dir:
	mkdir -p executables

clean:
	find . -name ".DS_Store" -type f -delete
	rm -rf executables/
	rm -rf *.dSYM
	rm -f blocking_laplace_tau non_blocking_laplace_tau

.PHONY: all clean create_executables_dir
