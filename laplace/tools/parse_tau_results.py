#!/usr/bin/env python3
"""
TAU Profile Parser for Laplace MPI Experiments

This script parses TAU profile_summary.txt files and extracts:
- Total execution time
- Communication time (MPI functions)
- Computation time (Total - Communication)

Generates 4 separate CSV files for easy plotting:
- blocking_strong.csv
- blocking_weak.csv
- nonblocking_strong.csv
- nonblocking_weak.csv

Usage:
    python3 parse_tau_results.py [data/tau_results]
"""

import csv
import os
import re
import sys
from pathlib import Path


def parse_time_value(time_str):
    """
    Parse a time value that may be in format:
    - "12,345" (milliseconds with comma)
    - "1:23.456" (minutes:seconds.milliseconds)
    - "1:23:45.678" (hours:minutes:seconds.milliseconds)

    Returns time in seconds as float.
    """
    time_str = time_str.strip()

    # Check if it contains a colon (time format)
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 2:
            # minutes:seconds.milliseconds
            minutes = int(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        elif len(parts) == 3:
            # hours:minutes:seconds.milliseconds
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
    else:
        # Regular number format (milliseconds)
        return float(time_str.replace(",", "")) / 1000.0

    return 0.0


def parse_tau_profile(profile_path):
    """
    Parse a TAU profile_summary.txt file and extract timing information
    from the FUNCTION SUMMARY (mean) section, and check for load imbalance
    across individual nodes.

    Returns a dictionary with:
    - total_time: Total execution time (from main)
    - mpi_times: Dictionary of MPI function times
    - comm_time: Total communication time
    - comp_time: Computation time (total - comm)
    - num_processes: Number of MPI processes
    """

    if not os.path.exists(profile_path):
        print(f"Warning: {profile_path} not found")
        return None

    with open(profile_path, "r") as f:
        content = f.read()

    results = {
        "total_time": 0.0,
        "mpi_times": {},
        "comm_time": 0.0,
        "comp_time": 0.0,
        "num_processes": 0,
    }

    # Extract number of processes
    process_matches = re.findall(r"NODE (\d+);CONTEXT", content)
    if process_matches:
        results["num_processes"] = len(set(process_matches))

    lines = content.split("\n")

    # MPI functions to track
    mpi_functions = [
        "MPI_Sendrecv()",
        "MPI_Send()",
        "MPI_Recv()",
        "MPI_Isend()",
        "MPI_Irecv()",
        "MPI_Wait()",
        "MPI_Waitall()",
        "MPI_Allreduce()",
        "MPI_Reduce()",
        "MPI_Barrier()",
        "MPI_Init()",
        "MPI_Finalize()",
        "MPI Collective Sync",
    ]

    # First, parse per-node data to check for load imbalance
    per_node_times = {}  # func_name -> [times across nodes]
    current_node = None
    in_node_section = False

    for i, line in enumerate(lines):
        # Detect node sections
        if re.match(r"NODE \d+;CONTEXT \d+;THREAD \d+:", line):
            current_node = line.strip()
            in_node_section = True
            continue

        # Stop at summary sections
        if "FUNCTION SUMMARY" in line:
            in_node_section = False
            current_node = None
            continue

        if not in_node_section or not current_node:
            continue

        # Skip header and separator lines
        if (
            not line.strip()
            or line.strip().startswith("-")
            or line.strip().startswith("%Time")
            or "msec" in line
        ):
            continue

        # Parse data lines
        parts = line.split()
        if len(parts) < 7:
            continue

        func_name = " ".join(parts[6:])

        # Track main function and MPI functions
        if func_name == "main" or any(mpi in func_name for mpi in mpi_functions):
            try:
                # parts[2] is Inclusive total msec
                time_val = parse_time_value(parts[2])
                if func_name not in per_node_times:
                    per_node_times[func_name] = []
                per_node_times[func_name].append((current_node, time_val))
            except (ValueError, IndexError):
                continue

    # Check for load imbalance (> 1 second difference)
    imbalance_threshold = 1.0  # seconds
    for func_name, times in per_node_times.items():
        if len(times) > 1:
            time_values = [t[1] for t in times]
            min_time = min(time_values)
            max_time = max(time_values)
            if max_time - min_time > imbalance_threshold:
                print(f"  ⚠ WARNING: Load imbalance detected for {func_name}")
                print(
                    f"    Min: {min_time:.3f}s, Max: {max_time:.3f}s, Diff: {max_time - min_time:.3f}s"
                )

    # Now parse the FUNCTION SUMMARY (mean) section for actual results
    in_mean_section = False
    for i, line in enumerate(lines):
        if "FUNCTION SUMMARY (mean):" in line:
            in_mean_section = True
            continue

        # Stop at next summary section or end
        if in_mean_section and (
            "FUNCTION SUMMARY" in line and "mean" not in line.lower()
        ):
            break

        if not in_mean_section:
            continue

        # Skip header lines and separator lines
        if (
            not line.strip()
            or line.strip().startswith("-")
            or line.strip().startswith("%Time")
            or "msec" in line
        ):
            continue

        # Parse data lines
        # Format: "%Time    Exclusive    Inclusive       #Call      #Subrs  Inclusive Name"
        #         "        msec   total msec                          usec/call"
        parts = line.split()
        if len(parts) < 7:
            continue

        # The function name is the last part(s)
        func_name = " ".join(parts[6:])

        # Find main function for total time
        if func_name == "main":
            try:
                # parts[2] is Inclusive total msec (could be in minutes:seconds format)
                results["total_time"] = parse_time_value(parts[2])
            except (ValueError, IndexError):
                print(f"  Warning: Could not parse main time from: {line}")
                continue

        # Check if this line contains an MPI function
        for mpi_func in mpi_functions:
            if func_name == mpi_func or func_name.startswith(mpi_func):
                try:
                    # parts[1] is Exclusive msec (could be in minutes:seconds format)
                    results["mpi_times"][mpi_func] = parse_time_value(parts[1])
                except (ValueError, IndexError):
                    print(f"  Warning: Could not parse MPI time from: {line}")
                break

    # Calculate total communication time
    # Exclude MPI_Init and MPI_Finalize as they're overhead, not communication
    results["comm_time"] = sum(
        time
        for func, time in results["mpi_times"].items()
        if func not in ["MPI_Init()", "MPI_Finalize()"]
    )

    # Calculate computation time
    results["comp_time"] = results["total_time"] - results["comm_time"]

    return results


def extract_config_from_path(path_str):
    """
    Extract configuration information from directory path.
    Example: '2nodes_blocking_strong' -> (2, 24, 'blocking', 'strong')
    """
    path_parts = Path(path_str).name.split("_")

    # Extract nodes
    nodes_str = path_parts[0]
    if "node" in nodes_str:
        nodes = int(nodes_str.replace("nodes", "").replace("node", ""))
    else:
        nodes = 0

    # Processors = nodes * 12
    processors = nodes * 12

    # Extract communication type (blocking/nonblocking)
    comm_type = path_parts[1] if len(path_parts) > 1 else "unknown"

    # Extract scaling type (strong/weak)
    scaling = path_parts[2] if len(path_parts) > 2 else "unknown"

    return nodes, processors, comm_type, scaling


def main():
    # Get base directory from command line or use default
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = "data/tau_results"

    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} not found")
        return

    # Collect all results
    all_results = []

    # Find all profile_summary.txt files
    for root, dirs, files in os.walk(base_dir):
        if "profile_summary.txt" in files:
            profile_path = os.path.join(root, "profile_summary.txt")
            print(f"\nParsing: {profile_path}")

            results = parse_tau_profile(profile_path)

            if results and results["total_time"] > 0:
                # Extract configuration from path
                nodes, processors, comm_type, scaling = extract_config_from_path(root)

                # Add configuration to results
                results["nodes"] = nodes
                results["processors"] = processors
                results["comm_type"] = comm_type
                results["scaling"] = scaling
                results["path"] = root

                all_results.append(results)

                # Print summary
                print(
                    f"  Config: {nodes} nodes, {processors} procs, {comm_type}, {scaling}"
                )
                print(f"  Total Time:         {results['total_time']:.3f} s")
                print(
                    f"  Communication Time: {results['comm_time']:.3f} s ({results['comm_time'] / results['total_time'] * 100:.1f}%)"
                )
                print(
                    f"  Computation Time:   {results['comp_time']:.3f} s ({results['comp_time'] / results['total_time'] * 100:.1f}%)"
                )
            else:
                print("  Warning: Could not parse timing data")

    # Sort results
    all_results.sort(key=lambda x: (x["scaling"], x["comm_type"], x["processors"]))

    # Generate 4 separate CSV files
    print("\n" + "=" * 80)
    print("Generating CSV files...")

    # Separate results by comm_type and scaling
    blocking_strong = [
        r
        for r in all_results
        if r["comm_type"] == "blocking" and r["scaling"] == "strong"
    ]
    blocking_weak = [
        r
        for r in all_results
        if r["comm_type"] == "blocking" and r["scaling"] == "weak"
    ]
    nonblocking_strong = [
        r
        for r in all_results
        if r["comm_type"] == "nonblocking" and r["scaling"] == "strong"
    ]
    nonblocking_weak = [
        r
        for r in all_results
        if r["comm_type"] == "nonblocking" and r["scaling"] == "weak"
    ]

    # Field names for CSVs
    fieldnames_strong = [
        "processors",
        "nodes",
        "total_time",
        "comm_time",
        "comp_time",
        "comm_percent",
        "speedup",
        "efficiency",
    ]

    fieldnames_weak = [
        "processors",
        "nodes",
        "total_time",
        "comm_time",
        "comp_time",
        "comm_percent",
        "efficiency",
    ]

    # 1. Blocking Strong Scaling
    if blocking_strong:
        csv_path = os.path.join(base_dir, "blocking_strong.csv")
        baseline = blocking_strong[0]  # First entry (12 processors)
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_strong)
            writer.writeheader()

            for result in blocking_strong:
                speedup = baseline["total_time"] / result["total_time"]
                efficiency = (
                    speedup / (result["processors"] / baseline["processors"])
                ) * 100

                writer.writerow(
                    {
                        "processors": result["processors"],
                        "nodes": result["nodes"],
                        "total_time": f"{result['total_time']:.4f}",
                        "comm_time": f"{result['comm_time']:.4f}",
                        "comp_time": f"{result['comp_time']:.4f}",
                        "comm_percent": f"{result['comm_time'] / result['total_time'] * 100:.2f}",
                        "speedup": f"{speedup:.2f}",
                        "efficiency": f"{efficiency:.2f}",
                    }
                )
        print(f"  Created: {csv_path}")

    # 2. Blocking Weak Scaling
    if blocking_weak:
        csv_path = os.path.join(base_dir, "blocking_weak.csv")
        baseline = blocking_weak[0]  # First entry (12 processors)
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_weak)
            writer.writeheader()

            for result in blocking_weak:
                efficiency = (baseline["total_time"] / result["total_time"]) * 100

                writer.writerow(
                    {
                        "processors": result["processors"],
                        "nodes": result["nodes"],
                        "total_time": f"{result['total_time']:.4f}",
                        "comm_time": f"{result['comm_time']:.4f}",
                        "comp_time": f"{result['comp_time']:.4f}",
                        "comm_percent": f"{result['comm_time'] / result['total_time'] * 100:.2f}",
                        "efficiency": f"{efficiency:.2f}",
                    }
                )
        print(f"  Created: {csv_path}")

    # 3. Non-Blocking Strong Scaling
    if nonblocking_strong:
        csv_path = os.path.join(base_dir, "nonblocking_strong.csv")
        baseline = nonblocking_strong[0]  # First entry (12 processors)
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_strong)
            writer.writeheader()

            for result in nonblocking_strong:
                speedup = baseline["total_time"] / result["total_time"]
                efficiency = (
                    speedup / (result["processors"] / baseline["processors"])
                ) * 100

                writer.writerow(
                    {
                        "processors": result["processors"],
                        "nodes": result["nodes"],
                        "total_time": f"{result['total_time']:.4f}",
                        "comm_time": f"{result['comm_time']:.4f}",
                        "comp_time": f"{result['comp_time']:.4f}",
                        "comm_percent": f"{result['comm_time'] / result['total_time'] * 100:.2f}",
                        "speedup": f"{speedup:.2f}",
                        "efficiency": f"{efficiency:.2f}",
                    }
                )
        print(f"  Created: {csv_path}")

    # 4. Non-Blocking Weak Scaling
    if nonblocking_weak:
        csv_path = os.path.join(base_dir, "nonblocking_weak.csv")
        baseline = nonblocking_weak[0]  # First entry (12 processors)
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_weak)
            writer.writeheader()

            for result in nonblocking_weak:
                efficiency = (baseline["total_time"] / result["total_time"]) * 100

                writer.writerow(
                    {
                        "processors": result["processors"],
                        "nodes": result["nodes"],
                        "total_time": f"{result['total_time']:.4f}",
                        "comm_time": f"{result['comm_time']:.4f}",
                        "comp_time": f"{result['comp_time']:.4f}",
                        "comm_percent": f"{result['comm_time'] / result['total_time'] * 100:.2f}",
                        "efficiency": f"{efficiency:.2f}",
                    }
                )
        print(f"  Created: {csv_path}")

    # Display comparison tables
    print("\n" + "=" * 80)
    print("STRONG SCALING COMPARISON")
    print("=" * 80)
    print(
        f"{'Procs':<8} {'Type':<12} {'Total (s)':<12} {'Comm (s)':<12} {'Comp (s)':<12} {'Comm %':<10} {'Speedup':<10} {'Eff %':<10}"
    )
    print("-" * 80)

    for result in blocking_strong + nonblocking_strong:
        if result in blocking_strong:
            baseline = blocking_strong[0]
        else:
            baseline = nonblocking_strong[0]

        speedup = baseline["total_time"] / result["total_time"]
        efficiency = (speedup / (result["processors"] / baseline["processors"])) * 100

        print(
            f"{result['processors']:<8} {result['comm_type']:<12} {result['total_time']:<12.4f} "
            f"{result['comm_time']:<12.4f} {result['comp_time']:<12.4f} "
            f"{result['comm_time'] / result['total_time'] * 100:<10.2f} "
            f"{speedup:<10.2f} {efficiency:<10.2f}"
        )

    print("\n" + "=" * 80)
    print("WEAK SCALING COMPARISON")
    print("=" * 80)
    print(
        f"{'Procs':<8} {'Type':<12} {'Total (s)':<12} {'Comm (s)':<12} {'Comp (s)':<12} {'Comm %':<10} {'Eff %':<10}"
    )
    print("-" * 80)

    for result in blocking_weak + nonblocking_weak:
        if result in blocking_weak:
            baseline = blocking_weak[0]
        else:
            baseline = nonblocking_weak[0]

        efficiency = (baseline["total_time"] / result["total_time"]) * 100

        print(
            f"{result['processors']:<8} {result['comm_type']:<12} {result['total_time']:<12.4f} "
            f"{result['comm_time']:<12.4f} {result['comp_time']:<12.4f} "
            f"{result['comm_time'] / result['total_time'] * 100:<10.2f} "
            f"{efficiency:<10.2f}"
        )

    print("\n" + "=" * 80)
    print(f"Parsed {len(all_results)} experiment results")
    print("CSV files created:")
    print("  - blocking_strong.csv")
    print("  - blocking_weak.csv")
    print("  - nonblocking_strong.csv")
    print("  - nonblocking_weak.csv")
    print("=" * 80)


if __name__ == "__main__":
    main()
