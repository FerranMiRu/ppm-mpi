#!/usr/bin/env python3
"""
TAU Results Plotting Script

Generates 5 plots from the CSV results:
1. Strong Scaling - Execution Time (blocking vs non-blocking)
2. Weak Scaling - Execution Time (blocking vs non-blocking)
3. Strong Scaling - Speedup
4. Strong Scaling - Efficiency
5. Weak Scaling - Efficiency

Usage:
    python3 tools/plot_results.py
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

# Set style for better-looking plots
plt.style.use("seaborn-v0_8-darkgrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.size"] = 11

# Define paths
DATA_DIR = "data/output"
OUTPUT_DIR = "data/output/images"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read CSV files
blocking_strong = pd.read_csv(os.path.join(DATA_DIR, "blocking_strong.csv"))
nonblocking_strong = pd.read_csv(os.path.join(DATA_DIR, "nonblocking_strong.csv"))
blocking_weak = pd.read_csv(os.path.join(DATA_DIR, "blocking_weak.csv"))
nonblocking_weak = pd.read_csv(os.path.join(DATA_DIR, "nonblocking_weak.csv"))

print("=" * 80)
print("Generating plots...")
print("=" * 80)

# ============================================================================
# Plot 1: Strong Scaling - Execution Time Comparison
# ============================================================================
plt.figure(figsize=(10, 6))

# Main lines - total time
plt.plot(
    blocking_strong["processors"],
    blocking_strong["total_time"],
    marker="o",
    linewidth=2.5,
    markersize=8,
    label="Blocking Total",
    color="C0",
)
plt.plot(
    nonblocking_strong["processors"],
    nonblocking_strong["total_time"],
    marker="s",
    linewidth=2.5,
    markersize=8,
    label="Non-Blocking Total",
    color="C1",
)

# Communication time (dashed, with alpha)
plt.plot(
    blocking_strong["processors"],
    blocking_strong["comm_time"],
    linestyle="--",
    linewidth=2,
    markersize=6,
    marker="o",
    alpha=0.6,
    label="Blocking Comm",
    color="C0",
)
plt.plot(
    nonblocking_strong["processors"],
    nonblocking_strong["comm_time"],
    linestyle="--",
    linewidth=2,
    markersize=6,
    marker="s",
    alpha=0.6,
    label="Non-Blocking Comm",
    color="C1",
)

# Computation time (dotted, with alpha)
plt.plot(
    blocking_strong["processors"],
    blocking_strong["comp_time"],
    linestyle=":",
    linewidth=2,
    markersize=6,
    marker="o",
    alpha=0.5,
    label="Blocking Comp",
    color="C0",
)
plt.plot(
    nonblocking_strong["processors"],
    nonblocking_strong["comp_time"],
    linestyle=":",
    linewidth=2,
    markersize=6,
    marker="s",
    alpha=0.5,
    label="Non-Blocking Comp",
    color="C1",
)

plt.xlabel("Number of Processors", fontsize=12, fontweight="bold")
plt.ylabel("Execution Time (seconds)", fontsize=12, fontweight="bold")
plt.title("Strong Scaling: Execution Time Comparison", fontsize=14, fontweight="bold")
plt.legend(fontsize=9, loc="best", ncol=2)
plt.grid(True, alpha=0.3)
plt.xticks(blocking_strong["processors"])

# Add annotations for total time only (to avoid clutter)
for i, row in blocking_strong.iterrows():
    plt.annotate(
        f"{row['total_time']:.1f}s",
        xy=(row["processors"], row["total_time"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=8,
        alpha=0.7,
    )

for i, row in nonblocking_strong.iterrows():
    plt.annotate(
        f"{row['total_time']:.1f}s",
        xy=(row["processors"], row["total_time"]),
        xytext=(0, -15),
        textcoords="offset points",
        ha="center",
        fontsize=8,
        alpha=0.7,
    )

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "1_strong_scaling_time.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✓ Created: {output_path}")
plt.close()

# ============================================================================
# Plot 2: Weak Scaling - Execution Time Comparison
# ============================================================================
plt.figure(figsize=(10, 6))

# Main lines - total time
plt.plot(
    blocking_weak["processors"],
    blocking_weak["total_time"],
    marker="o",
    linewidth=2.5,
    markersize=8,
    label="Blocking Total",
    color="C0",
)
plt.plot(
    nonblocking_weak["processors"],
    nonblocking_weak["total_time"],
    marker="s",
    linewidth=2.5,
    markersize=8,
    label="Non-Blocking Total",
    color="C1",
)

# Communication time (dashed, with alpha)
plt.plot(
    blocking_weak["processors"],
    blocking_weak["comm_time"],
    linestyle="--",
    linewidth=2,
    markersize=6,
    marker="o",
    alpha=0.6,
    label="Blocking Comm",
    color="C0",
)
plt.plot(
    nonblocking_weak["processors"],
    nonblocking_weak["comm_time"],
    linestyle="--",
    linewidth=2,
    markersize=6,
    marker="s",
    alpha=0.6,
    label="Non-Blocking Comm",
    color="C1",
)

# Computation time (dotted, with alpha)
plt.plot(
    blocking_weak["processors"],
    blocking_weak["comp_time"],
    linestyle=":",
    linewidth=2,
    markersize=6,
    marker="o",
    alpha=0.5,
    label="Blocking Comp",
    color="C0",
)
plt.plot(
    nonblocking_weak["processors"],
    nonblocking_weak["comp_time"],
    linestyle=":",
    linewidth=2,
    markersize=6,
    marker="s",
    alpha=0.5,
    label="Non-Blocking Comp",
    color="C1",
)

plt.xlabel("Number of Processors", fontsize=12, fontweight="bold")
plt.ylabel("Execution Time (seconds)", fontsize=12, fontweight="bold")
plt.title("Weak Scaling: Execution Time Comparison", fontsize=14, fontweight="bold")
plt.legend(fontsize=9, loc="best", ncol=2)
plt.grid(True, alpha=0.3)
plt.xticks(blocking_weak["processors"])

# Add annotations for total time only
for i, row in blocking_weak.iterrows():
    plt.annotate(
        f"{row['total_time']:.1f}s",
        xy=(row["processors"], row["total_time"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=8,
        alpha=0.7,
    )

for i, row in nonblocking_weak.iterrows():
    plt.annotate(
        f"{row['total_time']:.1f}s",
        xy=(row["processors"], row["total_time"]),
        xytext=(0, -15),
        textcoords="offset points",
        ha="center",
        fontsize=8,
        alpha=0.7,
    )

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "2_weak_scaling_time.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✓ Created: {output_path}")
plt.close()

# ============================================================================
# Plot 3: Strong Scaling - Speedup
# ============================================================================
plt.figure(figsize=(10, 6))

# Plot actual speedup
plt.plot(
    blocking_strong["processors"],
    blocking_strong["speedup"],
    marker="o",
    linewidth=2,
    markersize=8,
    label="Blocking MPI",
)
plt.plot(
    nonblocking_strong["processors"],
    nonblocking_strong["speedup"],
    marker="s",
    linewidth=2,
    markersize=8,
    label="Non-Blocking MPI",
)

# Plot ideal speedup (linear)
ideal_speedup = blocking_strong["processors"] / blocking_strong["processors"].iloc[0]
plt.plot(
    blocking_strong["processors"],
    ideal_speedup,
    linestyle="--",
    linewidth=2,
    color="black",
    alpha=0.5,
    label="Ideal Speedup",
)

plt.xlabel("Number of Processors", fontsize=12, fontweight="bold")
plt.ylabel("Speedup", fontsize=12, fontweight="bold")
plt.title("Strong Scaling: Speedup Comparison", fontsize=14, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(blocking_strong["processors"])

# Add annotations
for i, row in blocking_strong.iterrows():
    plt.annotate(
        f"{row['speedup']:.2f}×",
        xy=(row["processors"], row["speedup"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        alpha=0.7,
    )

for i, row in nonblocking_strong.iterrows():
    plt.annotate(
        f"{row['speedup']:.2f}×",
        xy=(row["processors"], row["speedup"]),
        xytext=(0, -15),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        alpha=0.7,
    )

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "3_strong_scaling_speedup.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✓ Created: {output_path}")
plt.close()

# ============================================================================
# Plot 4: Strong Scaling - Efficiency
# ============================================================================
plt.figure(figsize=(10, 6))

plt.plot(
    blocking_strong["processors"],
    blocking_strong["efficiency"],
    marker="o",
    linewidth=2,
    markersize=8,
    label="Blocking MPI",
)
plt.plot(
    nonblocking_strong["processors"],
    nonblocking_strong["efficiency"],
    marker="s",
    linewidth=2,
    markersize=8,
    label="Non-Blocking MPI",
)

# Add 100% efficiency reference line
plt.axhline(
    y=100, linestyle="--", linewidth=2, color="black", alpha=0.5, label="Ideal (100%)"
)

plt.xlabel("Number of Processors", fontsize=12, fontweight="bold")
plt.ylabel("Efficiency (%)", fontsize=12, fontweight="bold")
plt.title("Strong Scaling: Efficiency Comparison", fontsize=14, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(blocking_strong["processors"])
plt.ylim(0, 110)

# Add annotations
for i, row in blocking_strong.iterrows():
    plt.annotate(
        f"{row['efficiency']:.1f}%",
        xy=(row["processors"], row["efficiency"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        alpha=0.7,
    )

for i, row in nonblocking_strong.iterrows():
    plt.annotate(
        f"{row['efficiency']:.1f}%",
        xy=(row["processors"], row["efficiency"]),
        xytext=(0, -15),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        alpha=0.7,
    )

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "4_strong_scaling_efficiency.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✓ Created: {output_path}")
plt.close()

# ============================================================================
# Plot 5: Weak Scaling - Efficiency
# ============================================================================
plt.figure(figsize=(10, 6))

plt.plot(
    blocking_weak["processors"],
    blocking_weak["efficiency"],
    marker="o",
    linewidth=2,
    markersize=8,
    label="Blocking MPI",
)
plt.plot(
    nonblocking_weak["processors"],
    nonblocking_weak["efficiency"],
    marker="s",
    linewidth=2,
    markersize=8,
    label="Non-Blocking MPI",
)

# Add 100% efficiency reference line
plt.axhline(
    y=100, linestyle="--", linewidth=2, color="black", alpha=0.5, label="Ideal (100%)"
)

plt.xlabel("Number of Processors", fontsize=12, fontweight="bold")
plt.ylabel("Efficiency (%)", fontsize=12, fontweight="bold")
plt.title("Weak Scaling: Efficiency Comparison", fontsize=14, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xticks(blocking_weak["processors"])
plt.ylim(0, 110)

# Add annotations
for i, row in blocking_weak.iterrows():
    plt.annotate(
        f"{row['efficiency']:.1f}%",
        xy=(row["processors"], row["efficiency"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        alpha=0.7,
    )

for i, row in nonblocking_weak.iterrows():
    plt.annotate(
        f"{row['efficiency']:.1f}%",
        xy=(row["processors"], row["efficiency"]),
        xytext=(0, -15),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        alpha=0.7,
    )

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, "5_weak_scaling_efficiency.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✓ Created: {output_path}")
plt.close()

# ============================================================================
# Summary
# ============================================================================
print("=" * 80)
print("All plots generated successfully!")
print("=" * 80)
print("\nGenerated files:")
print("  1. 1_strong_scaling_time.png      - Strong scaling execution time")
print("  2. 2_weak_scaling_time.png        - Weak scaling execution time")
print("  3. 3_strong_scaling_speedup.png   - Strong scaling speedup")
print("  4. 4_strong_scaling_efficiency.png - Strong scaling efficiency")
print("  5. 5_weak_scaling_efficiency.png  - Weak scaling efficiency")
print("\nLocation: data/output/images/")
print("=" * 80)
