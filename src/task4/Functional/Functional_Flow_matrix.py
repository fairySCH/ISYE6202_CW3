# -*- coding: utf-8 -*-
"""
aggregate functional flow matrices per year.

inputs (it will try in this order):
  1) ../results/task4/part/flow_matrix/Flow_Matrix_Wide_All_Years.csv
     (wide table with columns Year, Part, A_A..M_M)
  2) ../results/task4/part/flow_matrix/per_year/<Year_>/P*_Flow_Matrix.csv

outputs:
  ../results/task4/functional/per_year/<Year_>_Functional_Flow_Matrix.csv
  ../results/task4/functional/per_year/<Year_>_Flow_Matrix_Summary.csv
  ../results/task4/functional/AllYears_Flow_Matrix_Summary.csv   (stack of all per-year summaries)

author: machas^2 team
"""

import os
import pandas as pd
from pathlib import Path

# ---------------- config ----------------
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent.parent  # adjust if your repo depth differs

PROCESSES = list("ABCDEFGHIJKLM")
TRANSITION_COLS = [f"{a}_{b}" for a in PROCESSES for b in PROCESSES]

# input candidates
FLOW_WIDE = project_root / 'results' / 'task4' / 'part' / 'flow_matrix' / 'Flow_Matrix_Wide_All_Years.csv'
PER_YEAR_DIR = project_root / 'results' / 'task4' / 'part' / 'flow_matrix' / 'per_year'

# outputs
OUT_BASE = project_root / 'results' / 'task4' / 'functional'
OUT_PER_YEAR = OUT_BASE / 'per_year'
OUT_PER_YEAR.mkdir(parents=True, exist_ok=True)

# ---------------- helpers ----------------
def year_sort_key(y):
    y = str(y)
    num = ''.join(ch for ch in y if ch.isdigit())
    return (int(num) if num else 0, y)

def empty_matrix():
    return pd.DataFrame(0.0, index=PROCESSES, columns=PROCESSES, dtype=float)

def save_year_outputs(year_label: str, flow_mat: pd.DataFrame):
    """Save per-year functional matrix and per-year summary."""
    ytag = str(year_label).replace(' ', '_')
    # matrix
    mat_path = OUT_PER_YEAR / f"{ytag}_Functional_Flow_Matrix.csv"
    flow_mat.to_csv(mat_path)

    # summary (total in/out per process)
    total_in = flow_mat.sum(axis=0)   # incoming to each process
    total_out = flow_mat.sum(axis=1)  # outgoing from each process
    summary_df = pd.DataFrame({
        'Year': year_label,
        'Process': PROCESSES,
        'Total_In_Flow': [total_in.get(p, 0.0) for p in PROCESSES],
        'Total_Out_Flow': [total_out.get(p, 0.0) for p in PROCESSES],
    })
    sum_path = OUT_PER_YEAR / f"{ytag}_Flow_Matrix_Summary.csv"
    summary_df.to_csv(sum_path, index=False)
    print(f"[{year_label}] Saved matrix → {mat_path}")
    print(f"[{year_label}] Saved summary → {sum_path}")
    return summary_df

# ---------------- strategy a: wide all-years file ----------------
if FLOW_WIDE.exists():
    df = pd.read_csv(FLOW_WIDE)
    # Keep only transition columns that actually exist
    trans_cols = [c for c in TRANSITION_COLS if c in df.columns]
    if not trans_cols:
        raise ValueError(f"No transition columns found in {FLOW_WIDE}")

    years = sorted(df['Year'].dropna().unique(), key=year_sort_key)
    all_years_summary = []

    for year in years:
        df_y = df[df['Year'] == year]
        totals = df_y[trans_cols].sum(axis=0) if not df_y.empty else pd.Series(0.0, index=trans_cols)

        # Rebuild 13x13 matrix
        mat = empty_matrix()
        for col, val in totals.items():
            a, b = col.split('_', 1)
            if a in PROCESSES and b in PROCESSES:
                mat.loc[a, b] = float(val)

        summary_df = save_year_outputs(year, mat)
        all_years_summary.append(summary_df)

    # Write all-years stacked summary
    if all_years_summary:
        pd.concat(all_years_summary, ignore_index=True).sort_values(['Year', 'Process']).to_csv(
            OUT_BASE / 'AllYears_Flow_Matrix_Summary.csv', index=False
        )
        print("Saved all-years stacked summary →", (OUT_BASE / 'AllYears_Flow_Matrix_Summary.csv').resolve())

# ---------------- strategy b: per-year folders of part matrices ----------------
elif PER_YEAR_DIR.exists():
    years_dirs = sorted([p for p in PER_YEAR_DIR.iterdir() if p.is_dir()], key=lambda p: year_sort_key(p.name.replace('_', ' ')))
    if not years_dirs:
        raise FileNotFoundError(f"No year subfolders found in {PER_YEAR_DIR}")

    all_years_summary = []

    for ydir in years_dirs:
        year_label = ydir.name.replace('_', ' ')  # e.g., "Year_1" -> "Year 1"
        mat = empty_matrix()

        # Sum all part flow matrices in this year folder
        for fn in os.listdir(ydir):
            if fn.endswith('_Flow_Matrix.csv'):
                fpath = ydir / fn
                try:
                    part_mat = pd.read_csv(fpath, index_col=0)
                    # Align to ensure same order/shape
                    part_mat = part_mat.reindex(index=PROCESSES, columns=PROCESSES, fill_value=0.0)
                    mat += part_mat
                except Exception as e:
                    print(f"Warning: skipping {fpath} due to error: {e}")

        summary_df = save_year_outputs(year_label, mat)
        all_years_summary.append(summary_df)

    if all_years_summary:
        pd.concat(all_years_summary, ignore_index=True).sort_values(['Year', 'Process']).to_csv(
            OUT_BASE / 'AllYears_Flow_Matrix_Summary.csv', index=False
        )
        print("Saved all-years stacked summary →", (OUT_BASE / 'AllYears_Flow_Matrix_Summary.csv').resolve())

# ---------------- fallback: old single-folder task3 layout (not per-year) ----------------
else:
    raise FileNotFoundError(
        "No per-year flow data found.\n"
        f"Tried:\n  - {FLOW_WIDE}\n  - {PER_YEAR_DIR}\n"
        "Generate per-year flow matrices (or the wide all-years file) and rerun."
    )
