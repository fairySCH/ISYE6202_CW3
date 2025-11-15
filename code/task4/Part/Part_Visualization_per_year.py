# -*- coding: utf-8 -*-
"""
Task 4: Parts-Based Design — Per-Year Analysis with Visualizations
Reads aggregated per-year capacity CSVs and aggregated flow-matrix (all years),
then produces per-year dashboards and text reports.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------------- Configuration ----------------
BASE_DIR = Path(__file__).parent.parent.parent.parent  # project root
RESULTS_DIR = BASE_DIR / "results"

# Aggregated capacity inputs (with Year column)
CAPACITY_DIR = RESULTS_DIR / "task4" / "part" / "capacity"
CAPACITY_1 = CAPACITY_DIR / "Part_Step_Process_Capacity_Requirements_1_shifts.csv"
CAPACITY_2 = CAPACITY_DIR / "Part_Step_Process_Capacity_Requirements_2_shifts.csv"
PART_DEMAND = CAPACITY_DIR / "Weekly_Part_Demand.csv"  # Year, Part, Weekly_Demand

# Aggregated flow inputs (with Year column)
FLOW_DIR = RESULTS_DIR / "task4" / "part" / "flow_matrix"
FLOW_WIDE = FLOW_DIR / "Flow_Matrix_Wide_All_Years.csv"  # Year, Part, A_A..M_M

# Outputs
VIS_OUT_DIR = RESULTS_DIR / "task4" / "part" / "visualizations" / "per_year"
REP_OUT_DIR = RESULTS_DIR / "task4" / "part" / "reports" / "per_year"
VIS_OUT_DIR.mkdir(parents=True, exist_ok=True)
REP_OUT_DIR.mkdir(parents=True, exist_ok=True)

# Plot style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (20, 12)

# Constants used for workload/context (if needed)
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY
MINUTES_PER_MACHINE_1 = HOURS_PER_SHIFT * DAYS_PER_WEEK * 60 * EFFECTIVE_AVAILABILITY
MINUTES_PER_MACHINE_2 = 2 * HOURS_PER_SHIFT * DAYS_PER_WEEK * 60 * EFFECTIVE_AVAILABILITY

PROCESSES = list('ABCDEFGHIJKLM')
TRANSITION_COLS = [f"{a}_{b}" for a in PROCESSES for b in PROCESSES]

# ---------------- Helpers ----------------
def _require_file(path: Path, label: str):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file for {label}: {path}")

def _year_labels(df: pd.DataFrame) -> list:
    years = sorted(
        df['Year'].dropna().unique(),
        key=lambda s: (int(''.join([c for c in str(s) if c.isdigit()]) or 0), str(s))
    )
    return list(years)

def _build_total_flow_matrix_for_year(flow_wide_year: pd.DataFrame) -> pd.DataFrame:
    """
    Reconstruct a 13x13 total flow matrix for the year by summing transitions across all parts.
    """
    totals = flow_wide_year[TRANSITION_COLS].sum(axis=0) if not flow_wide_year.empty else pd.Series(0.0, index=TRANSITION_COLS)
    mat = pd.DataFrame(0.0, index=PROCESSES, columns=PROCESSES)
    for col, val in totals.items():
        a, b = col.split('_')
        mat.loc[a, b] = float(val)
    return mat

def _process_frequency_from_matrix(flow_mat: pd.DataFrame) -> pd.DataFrame:
    """
    Compute frequency proxy: in+out flows per process (row-sum + col-sum).
    """
    freq_series = flow_mat.sum(axis=1) + flow_mat.sum(axis=0)
    return pd.DataFrame({'Process': PROCESSES, 'Operations_Per_Week': [freq_series.get(p, 0.0) for p in PROCESSES]})

# ---------------- Per-Year Visualization ----------------
def create_visualizations_per_year():
    # --- Load inputs ---
    _require_file(CAPACITY_1, "capacity (1 shift)")
    _require_file(CAPACITY_2, "capacity (2 shifts)")
    _require_file(PART_DEMAND, "weekly part demand")
    _require_file(FLOW_WIDE, "flow matrix (wide, all years)")

    cap1 = pd.read_csv(CAPACITY_1)      # expects columns incl. Year, Operation, Number_of_Machines, Time_Required_Min_Week, Part, Step...
    cap2 = pd.read_csv(CAPACITY_2)
    part_demand_all = pd.read_csv(PART_DEMAND)   # Year, Part, Weekly_Demand
    flow_wide_all = pd.read_csv(FLOW_WIDE)       # Year, Part, A_A..M_M

    years = sorted(set(cap1['Year']).union(set(cap2['Year'])).union(set(part_demand_all['Year'])).union(set(flow_wide_all['Year'])),
                   key=lambda s: (int(''.join([c for c in str(s) if c.isdigit()]) or 0), str(s)))

    for year in years:
        year_mask1 = cap1['Year'] == year
        year_mask2 = cap2['Year'] == year
        cap1_y = cap1[year_mask1].copy()
        cap2_y = cap2[year_mask2].copy()
        pd_y = part_demand_all[part_demand_all['Year'] == year].copy()
        flow_y = flow_wide_all[flow_wide_all['Year'] == year].copy()

        # ----- Process capacity (group by operation) -----
        # NOTE: Summing Number_of_Machines at step-level will count duplicates for repeated operations in a routing;
        # this matches the original logic you used and keeps results consistent with prior dashboards.
        proc_cap_1 = cap1_y.groupby('Operation', as_index=False)['Number_of_Machines'].sum()
        proc_cap_2 = cap2_y.groupby('Operation', as_index=False)['Number_of_Machines'].sum()

        # Workload by operation (sum of Time_Required_Min_Week is shift-agnostic)
        # If that column is missing (older export), fall back to reverse from machines.
        if 'Time_Required_Min_Week' in cap2_y.columns:
            workload_ops = cap2_y.groupby('Operation', as_index=False)['Time_Required_Min_Week'].sum()
            workload_ops.rename(columns={'Time_Required_Min_Week': 'Weekly_Minutes'}, inplace=True)
        else:
            workload_ops = proc_cap_2.copy()
            workload_ops['Weekly_Minutes'] = workload_ops['Number_of_Machines'] * MINUTES_PER_MACHINE_2

        # Build equipment dataframe (1 vs 2 shifts)
        equip = pd.DataFrame({'Process': PROCESSES})

        proc_cap_1_ren = proc_cap_1.rename(
            columns={'Operation': 'Process', 'Number_of_Machines': 'Equipment_1_Shift'}
        )
        proc_cap_2_ren = proc_cap_2.rename(
            columns={'Operation': 'Process', 'Number_of_Machines': 'Equipment_2_Shifts'}
        )

        equip = (
            equip
            .merge(proc_cap_1_ren, on='Process', how='left')
            .merge(proc_cap_2_ren, on='Process', how='left')
        )

        equip['Equipment_1_Shift'] = equip['Equipment_1_Shift'].fillna(0).astype(int)
        equip['Equipment_2_Shifts'] = equip['Equipment_2_Shifts'].fillna(0).astype(int)


        # Workload (hours) per process for display
        wl = pd.DataFrame({'Process': PROCESSES}).merge(workload_ops.rename(columns={'Operation':'Process'}), on='Process', how='left')
        wl['Weekly_Minutes'] = wl['Weekly_Minutes'].fillna(0.0)
        wl['Weekly_Hours'] = wl['Weekly_Minutes'] / 60.0

        # ----- Flow matrix for this year -----
        total_flow_mat = _build_total_flow_matrix_for_year(flow_y)
        freq_df = _process_frequency_from_matrix(total_flow_mat)

        # ----- Part demand for this year -----
        part_demand_y = pd.DataFrame({'Part':[f'P{i}' for i in range(1,21)]}).merge(pd_y[['Part','Weekly_Demand']], on='Part', how='left')
        part_demand_y['Weekly_Demand'] = part_demand_y['Weekly_Demand'].fillna(0.0)

        # ----- Part capacity totals (2-shift) for this year -----
        # Sum machines per Part (again, consistent with your original approach)
        part_cap_2 = cap2_y.groupby('Part', as_index=False)['Number_of_Machines'].sum()

        # ===================== Build Figure =====================
        fig = plt.figure(figsize=(20, 12))
        fig.suptitle(f"Task 4 Parts-Based Analysis — {year}", fontsize=16, fontweight='bold')

        # 1) Equipment Requirements: 1 vs 2 shifts
        ax1 = plt.subplot(2, 3, 1)
        x = np.arange(len(PROCESSES))
        width = 0.38
        ax1.bar(x - width/2, equip['Equipment_1_Shift'], width, label='1 Shift/Day', alpha=0.85)
        ax1.bar(x + width/2, equip['Equipment_2_Shifts'], width, label='2 Shifts/Day', alpha=0.85)
        ax1.set_xlabel('Process', fontweight='bold')
        ax1.set_ylabel('Equipment Units Required', fontweight='bold')
        ax1.set_title('Equipment Requirements (1 vs 2 Shifts)', fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(PROCESSES)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

        # 2) Weekly Process Workload (hours)
        ax2 = plt.subplot(2, 3, 2)
        ax2.barh(wl['Process'], wl['Weekly_Hours'], alpha=0.9)
        ax2.set_xlabel('Weekly Hours', fontweight='bold')
        ax2.set_ylabel('Process', fontweight='bold')
        ax2.set_title('Weekly Workload by Process', fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)

        # 3) Flow volume per process (in+out), thousands
        ax3 = plt.subplot(2, 3, 3)
        flow_vol = (total_flow_mat.sum(axis=1) + total_flow_mat.sum(axis=0)).sort_values(ascending=True)
        if flow_vol.sum() > 0:
            ax3.barh(flow_vol.index, flow_vol.values / 1000.0, alpha=0.9)
            ax3.set_xlabel('Total Flow Volume (thousands)', fontweight='bold')
            ax3.set_ylabel('Process', fontweight='bold')
            ax3.set_title('Material Flow Volume (from flow matrix)', fontweight='bold')
            ax3.grid(axis='x', alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'No flow data', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Material Flow Volume', fontweight='bold')

        # 4) Weekly Part Demand (units)
        ax4 = plt.subplot(2, 3, 4)
        pd_sorted = part_demand_y.sort_values('Weekly_Demand', ascending=True)
        ax4.barh(pd_sorted['Part'], pd_sorted['Weekly_Demand'], alpha=0.9)
        ax4.set_xlabel('Units per Week', fontweight='bold')
        ax4.set_ylabel('Part', fontweight='bold')
        ax4.set_title('Weekly Part Demand', fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)

        # 5) Process Frequency (ops/week, thousands)
        ax5 = plt.subplot(2, 3, 5)
        freq_sorted = freq_df.sort_values('Operations_Per_Week', ascending=False)
        ax5.bar(freq_sorted['Process'], freq_sorted['Operations_Per_Week'] / 1000.0, alpha=0.9)
        ax5.set_xlabel('Process', fontweight='bold')
        ax5.set_ylabel('Operations per Week (thousands)', fontweight='bold')
        ax5.set_title('Process Frequency (from flow matrix)', fontweight='bold')
        ax5.grid(axis='y', alpha=0.3)

        # 6) Machine Requirements by Part (2-shift)
        ax6 = plt.subplot(2, 3, 6)
        pc_sorted = part_cap_2.sort_values('Number_of_Machines', ascending=True)
        ax6.barh(pc_sorted['Part'], pc_sorted['Number_of_Machines'], alpha=0.9)
        ax6.set_xlabel('Total Machines (2-shift)', fontweight='bold')
        ax6.set_ylabel('Part', fontweight='bold')
        ax6.set_title('Machine Requirements by Part (2-shift)', fontweight='bold')
        ax6.grid(axis='x', alpha=0.3)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Save figure
        year_sanitized = str(year).replace(' ', '_')
        fig_path = VIS_OUT_DIR / f"{year_sanitized}_Task4_Parts_Based_Analysis_Dashboard.png"
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"[{year}] Saved dashboard → {fig_path}")

# ---------------- Per-Year Summary Reports ----------------
def generate_summary_reports_per_year():
    _require_file(CAPACITY_1, "capacity (1 shift)")
    _require_file(CAPACITY_2, "capacity (2 shifts)")
    _require_file(PART_DEMAND, "weekly part demand")
    _require_file(FLOW_WIDE, "flow matrix (wide, all years)")

    cap1 = pd.read_csv(CAPACITY_1)
    cap2 = pd.read_csv(CAPACITY_2)
    part_demand_all = pd.read_csv(PART_DEMAND)
    flow_wide_all = pd.read_csv(FLOW_WIDE)

    years = sorted(set(cap1['Year']).union(set(cap2['Year'])).union(set(part_demand_all['Year'])).union(set(flow_wide_all['Year'])),
                   key=lambda s: (int(''.join([c for c in str(s) if c.isdigit()]) or 0), str(s)))

    for year in years:
        cap1_y = cap1[cap1['Year'] == year].copy()
        cap2_y = cap2[cap2['Year'] == year].copy()
        pd_y = part_demand_all[part_demand_all['Year'] == year].copy()
        flow_y = flow_wide_all[flow_wide_all['Year'] == year].copy()

        # Equipment totals (sum of machines across operations; consistent with earlier logic)
        proc_cap_1 = cap1_y.groupby('Operation', as_index=False)['Number_of_Machines'].sum()
        proc_cap_2 = cap2_y.groupby('Operation', as_index=False)['Number_of_Machines'].sum()
        total_equip_1 = int(proc_cap_1['Number_of_Machines'].sum())
        total_equip_2 = int(proc_cap_2['Number_of_Machines'].sum())

        # Top bottlenecks (2-shift)
        equip_df = pd.DataFrame({'Process': PROCESSES})
        equip_df = equip_df.merge(proc_cap_2.rename(columns={'Number_of_Machines':'Equipment_2_Shifts'}),
                                  left_on='Process', right_on='Operation', how='left')
        equip_df.drop(columns=['Operation'], inplace=True)
        equip_df['Equipment_2_Shifts'] = equip_df['Equipment_2_Shifts'].fillna(0).astype(int)
        bottlenecks = equip_df.nlargest(5, 'Equipment_2_Shifts')[['Process', 'Equipment_2_Shifts']]

        # Part demand (top 5)
        pd_y2 = pd.DataFrame({'Part':[f'P{i}' for i in range(1,21)]}).merge(pd_y[['Part','Weekly_Demand']], on='Part', how='left')
        pd_y2['Weekly_Demand'] = pd_y2['Weekly_Demand'].fillna(0.0)
        high_demand = pd_y2.nlargest(5, 'Weekly_Demand')[['Part','Weekly_Demand']]

        # Flow analytics
        total_flow_mat = _build_total_flow_matrix_for_year(flow_y)
        freq_df = _process_frequency_from_matrix(total_flow_mat)
        total_ops = freq_df['Operations_Per_Week'].sum()
        top_freq = freq_df.nlargest(3, 'Operations_Per_Week')
        total_flow_volume = float(total_flow_mat.values.sum())

        # Highest flow edges (top 3)
        pairs = []
        for i in PROCESSES:
            for j in PROCESSES:
                val = total_flow_mat.loc[i, j]
                if val > 0:
                    pairs.append((i, j, val))
        pairs.sort(key=lambda x: x[2], reverse=True)
        top_pairs = pairs[:3]

        # Build report
        rep = []
        rep.append("="*80)
        rep.append(f"TASK 4: PARTS-BASED DESIGN — CAPACITY & FLOW SUMMARY ({year})")
        rep.append("="*80)
        rep.append("")
        rep.append("KEY FINDINGS")
        rep.append("-"*80)
        rep.append("")
        rep.append("1) EQUIPMENT REQUIREMENTS")
        rep.append(f"   • 1-Shift: {total_equip_1} units")
        rep.append(f"   • 2-Shifts: {total_equip_2} units")
        if total_equip_1 > 0:
            rep.append(f"   • Savings with 2-shift: {total_equip_1 - total_equip_2} units "
                       f"({(1 - total_equip_2/total_equip_1)*100:.1f}% reduction)")
        rep.append("")
        rep.append("2) BOTTLENECK PROCESSES (Top 5 by equipment @ 2-shift):")
        for _, r in bottlenecks.iterrows():
            rep.append(f"   • Process {r['Process']}: {int(r['Equipment_2_Shifts'])} units")
        rep.append("")
        rep.append("3) HIGHEST DEMAND PARTS (Top 5):")
        for _, r in high_demand.iterrows():
            rep.append(f"   • {r['Part']}: {r['Weekly_Demand']:,.0f} units/week")
        rep.append("")
        rep.append("4) PROCESS FREQUENCY (from flow matrix):")
        rep.append(f"   • Total operations/week (in+out): {total_ops:,.0f}")
        rep.append("   • Most frequent processes:")
        for _, r in top_freq.iterrows():
            pct = (r['Operations_Per_Week']/total_ops*100) if total_ops > 0 else 0.0
            rep.append(f"     - {r['Process']}: {r['Operations_Per_Week']:,.0f} ops/wk ({pct:.1f}%)")
        rep.append("")
        rep.append("5) MATERIAL FLOW (from flow matrix):")
        rep.append(f"   • Total weekly flow volume (sum of all transitions): {total_flow_volume:,.0f} units")
        if top_pairs:
            rep.append("   • Highest flow process pairs:")
            for (a, b, v) in top_pairs:
                rep.append(f"     - {a} → {b}: {v:,.0f} units/week")

        year_sanitized = str(year).replace(' ', '_')
        out_path = REP_OUT_DIR / f"{year_sanitized}_Task4_Parts_Based_Summary_Report.txt"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rep))
        print(f"[{year}] Saved report → {out_path}")

# ---------------- Static Process-Part Matrix (unchanged; not year-dependent) ----------------
def create_process_matrix_static():
    """
    Create a static incidence matrix: which processes appear in each part's routing (1/0).
    This reads 'Parts Specs.csv' as in your original.
    """
    df = pd.read_csv(BASE_DIR / "data" / "csv_outputs" / 'Parts Specs.csv', header=None)

    process_sequences = {}
    for i in range(11, 31):
        part_name = df.iloc[i, 1]
        if pd.notna(part_name):
            part_name = str(part_name).strip()
            seq = []
            for j in range(2, 9):
                proc = df.iloc[i, j]
                if pd.notna(proc) and str(proc).strip():
                    seq.append(str(proc).strip())
            process_sequences[part_name] = seq

    parts = [f'P{i}' for i in range(1, 21)]
    mat = pd.DataFrame(0, index=parts, columns=PROCESSES)
    for part, seq in process_sequences.items():
        for p in seq:
            if p in PROCESSES:
                mat.loc[part, p] = 1

    mat.loc['TOTAL'] = mat.sum()
    mat['TOTAL'] = mat.sum(axis=1)

    out_csv = RESULTS_DIR / "task4" / "part" / "reports" / "Task4_Process_Part_Matrix.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    mat.to_csv(out_csv)
    print(f"Saved process-part incidence matrix → {out_csv}")
    return mat

# ---------------- Main ----------------
if __name__ == "__main__":
    print("Generating Task 4 Per-Year Analysis (with aggregated flow matrix)...\n")

    # Generate per-year reports
    generate_summary_reports_per_year()

    # Create static process-part matrix (routing incidence)
    create_process_matrix_static()

    # Generate per-year visualizations
    create_visualizations_per_year()

    print("\n" + "="*80)
    print("Task 4 Per-Year Analysis Complete!")
    print("="*80)
