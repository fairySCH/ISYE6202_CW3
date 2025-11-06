# -*- coding: utf-8 -*-
"""
Per-year flow matrices aggregated into single CSVs (all years).
Creates:
  - ../results/task4/part/flow_matrix/Flow_Edges_All_Years.csv
  - ../results/task4/part/flow_matrix/Flow_Matrix_Wide_All_Years.csv
"""

import os
import pandas as pd
from pathlib import Path

# ---------------- Utilities ----------------
def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

# ---------------- Config ----------------
BASE_DIR = Path(__file__).parent.parent.parent.parent  # project root
RESULTS_DIR = BASE_DIR / "results"

# Output directory (single place, no per-year subfolders)
OUT_DIR = RESULTS_DIR / "task4" / "part" / "flow_matrix"
ensure_dir(str(OUT_DIR))

# ---------------- Load multi-year demand ----------------
# Try both spellings just in case (Fulfilment vs Fulfillment)
task4_load = r"results\task4\Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv"
df_all = None

df_all = pd.read_csv(task4_load)

if df_all is None:
    raise FileNotFoundError(
        f"Could not find Task4 multi-year CSV. Tried"
    )

# Order years like 'Year 1', 'Year 2', ...
years = sorted(
    df_all['Year'].unique(),
    key=lambda s: (int(''.join(ch for ch in str(s) if ch.isdigit()) or 0), str(s))
)

# ---------------- Routings ----------------
process_operations = {
    'P1': ['B', 'A', 'B', 'C', 'D', 'I', 'J'],
    'P2': ['A', 'C', 'D', 'H', 'J'],
    'P3': ['B', 'D', 'C', 'I', 'J'],
    'P4': ['A', 'B', 'D', 'G', 'H'],
    'P5': ['B', 'C', 'D', 'I'],
    'P6': ['A', 'B', 'C', 'D', 'H', 'I', 'J'],
    'P7': ['E', 'F', 'C', 'D', 'I', 'J'],
    'P8': ['E', 'H', 'J', 'I'],
    'P9': ['F', 'G', 'E', 'G', 'I', 'J'],
    'P10': ['E', 'F', 'I', 'J'],
    'P11': ['E', 'G', 'E', 'G', 'I'],
    'P12': ['E', 'G', 'F', 'I', 'J'],
    'P13': ['E', 'F', 'G', 'F', 'G', 'H', 'I'],
    'P14': ['E', 'F', 'G', 'H'],
    'P15': ['E', 'G', 'F', 'H', 'J'],
    'P16': ['F', 'H', 'I', 'J'],
    'P17': ['K', 'L', 'M'],
    'P18': ['K', 'L', 'K', 'M'],
    'P19': ['L', 'M', 'L', 'M'],
    'P20': ['L', 'K', 'M']
}
processes = list('ABCDEFGHIJKLM')  # all processes
all_transition_cols = [f"{a}_{b}" for a in processes for b in processes]

# ---------------- Accumulators for aggregated outputs ----------------
edges_rows = []   # tidy: Year, Part, From, To, Flow
wide_rows = []    # wide: Year, Part, A_A, A_B, ..., M_M

# ---------------- Build matrices for each Year × Part ----------------
for year in years:
    df_y = df_all[df_all['Year'] == year].copy()

    # Weekly demand dict for this year (default 0 if a part is missing)
    weekly_demand_year = {f'P{i}': 0.0 for i in range(1, 21)}
    weekly_demand_year.update(
        dict(zip(df_y['Part'].astype(str), df_y['Weekly_Demand_Units'].astype(float)))
    )

    for part, ops in process_operations.items():
        demand = float(weekly_demand_year.get(part, 0.0))

        # Initialize a 13x13 zero matrix (as a dict for speed/clarity)
        mat = {f"{a}_{b}": 0.0 for a in processes for b in processes}

        # Fill transitions present in the routing
        for i in range(len(ops) - 1):
            a = ops[i]
            b = ops[i + 1]
            key = f"{a}_{b}"
            mat[key] += demand

            # Also add to tidy edges (sparse; include zeros only if you want full trace)
            edges_rows.append({
                'Year': year,
                'Part': part,
                'From': a,
                'To': b,
                'Flow': demand
            })

        # Append wide row (Year, Part, then all 169 transitions)
        wide_row = {'Year': year, 'Part': part}
        wide_row.update(mat)
        wide_rows.append(wide_row)

# ---------------- Write aggregated CSVs ----------------
edges_df = pd.DataFrame(edges_rows)
# Keep only nonzero flows to reduce size (comment out the next line to keep zeros too)
edges_df = edges_df[edges_df['Flow'] != 0.0]
edges_df.sort_values(['Year', 'Part', 'From', 'To'], inplace=True)
edges_df.to_csv(OUT_DIR / "Flow_Edges_All_Years.csv", index=False)

wide_df = pd.DataFrame(wide_rows)
# Ensure all transition columns exist even if some never appear for some parts/years
for col in all_transition_cols:
    if col not in wide_df.columns:
        wide_df[col] = 0.0
wide_df = wide_df[['Year', 'Part'] + all_transition_cols]
wide_df.sort_values(['Year', 'Part'], inplace=True)
wide_df.to_csv(OUT_DIR / "Flow_Matrix_Wide_All_Years.csv", index=False)

print("Done. Aggregated flow files written to:", OUT_DIR.resolve())
