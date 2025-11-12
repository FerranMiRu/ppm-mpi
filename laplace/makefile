CC = gcc
CFLAGS = -O3 -march=native
OMPFLAGS = -fopenmp
LDFLAGS = -lm

ALL_TARGETS = extinguishing.exe parallel_extinguishing.exe

all: $(ALL_TARGETS)

extinguishing.exe: src/extinguishing.c create_executables_dir
	$(CC) $(CFLAGS) -fno-inline $< -o executables/$@ $(LDFLAGS)

parallel_extinguishing.exe: src/parallel_extinguishing.c create_executables_dir
	$(CC) $(CFLAGS) $(OMPFLAGS) $< -o executables/$@ $(LDFLAGS)

create_executables_dir:
	mkdir -p executables

clean:
	find . -name ".DS_Store" -type f -delete
	rm -rf executables/
	rm -rf *.dSYM

help:
	@echo "Available targets:"
	@echo "  all                            - Compile all files (default)"
	@echo "  extinguishing.exe              - Compile extinguishing.c"
	@echo "  parallel_extinguishing.exe     - Compile parallel_extinguishing.c"
	@echo "  clean                          - Remove all compiled executables and debug symbols"
	@echo "  help                           - Show this help message"

.PHONY: all clean help create_executables_dir
