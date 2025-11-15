# -*- coding: utf-8 -*-
"""
Combined Task 3 (aggregated across all years) — PARTS-BASED + DETAILED CAPACITY
Reads ../results/Task4_Demand_Fulfilment_Capacity_Plan_by_year.csv,
computes requirements for each year, and writes single CSVs (with a Year column)
to ../results/task4/part/capacity/
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path

# ---------- Utils ----------
def ensure_dir(path: str):
    """Create directory if it doesn't exist (parents included)."""
    os.makedirs(path, exist_ok=True)

# =========================
# Technical data files configuration
# =========================
BASE_DIR = Path(__file__).parent.parent.parent.parent  # project root
DATA_DIR = BASE_DIR / "data" / "csv_outputs"

# =========================
# Operating parameters
# =========================
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
MINUTES_PER_SHIFT = HOURS_PER_SHIFT * 60  # 480
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY  # 0.882

# =========================
# Load routings and step times
# =========================
def load_process_sequences():
    """Load the operation sequences (A..M) per part from 'Parts Specs.csv'."""
    df = pd.read_csv(DATA_DIR / 'Parts Specs.csv', header=None)
    process_sequences = {}
    # Rows 11-30: P1..P20 ; columns 2-8: Steps 1..7
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
    return process_sequences

def load_process_times():
    """Load step times (min/unit) per part from 'Parts_Step_Time.csv'."""
    df = pd.read_csv(DATA_DIR / 'Parts_Step_Time.csv')
    process_times = {}
    for _, row in df.iterrows():
        part = row['Part']
        times = []
        for step in ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6', 'Step 7']:
            val = row.get(step, np.nan)
            times.append(float(val) if pd.notna(val) else 0.0)
        process_times[part] = times
    return process_times

# =========================
# Calculations
# =========================
def calculate_process_workload(weekly_part_demand, process_sequences, process_times):
    """Total weekly workload (min/week) per process A..M + detailed breakdown."""
    all_processes = list('ABCDEFGHIJKLM')
    process_workload = {p: 0.0 for p in all_processes}
    process_breakdown = {p: [] for p in all_processes}

    for part, demand in weekly_part_demand.items():
        if demand <= 0 or part not in process_sequences or part not in process_times:
            continue
        seq = process_sequences[part]
        times = process_times[part]
        for step_idx, proc in enumerate(seq):
            if step_idx < len(times) and times[step_idx] > 0:
                tpu = times[step_idx]
                total_min = demand * tpu
                process_workload[proc] += total_min
                process_breakdown[proc].append({
                    'part': part,
                    'demand': demand,
                    'time_per_unit': tpu,
                    'total_minutes': total_min
                })
    return process_workload, process_breakdown

def calculate_equipment_requirements(process_workload):
    """Equipment requirements per process (1 shift / 2 shifts) with utilization."""
    cap_1 = DAYS_PER_WEEK * 1 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY
    cap_2 = DAYS_PER_WEEK * 2 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY
    rows = []
    for process in sorted(process_workload.keys()):
        wl = process_workload[process]
        if wl <= 0:
            rows.append({
                'Process': process,
                'Weekly_Minutes': 0,
                'Weekly_Hours': 0,
                'Equipment_1_Shift': 0,
                'Equipment_2_Shifts': 0,
                'Utilization_1_Shift': 0.0,
                'Utilization_2_Shifts': 0.0
            })
            continue
        eq1 = int(np.ceil(wl / cap_1))
        eq2 = int(np.ceil(wl / cap_2))
        util1 = (wl / (eq1 * cap_1)) * 100 if eq1 > 0 else 0.0
        util2 = (wl / (eq2 * cap_2)) * 100 if eq2 > 0 else 0.0
        rows.append({
            'Process': process,
            'Weekly_Minutes': wl,
            'Weekly_Hours': wl / 60.0,
            'Equipment_1_Shift': eq1,
            'Equipment_2_Shifts': eq2,
            'Utilization_1_Shift': util1,
            'Utilization_2_Shifts': util2
        })
    return pd.DataFrame(rows)

def analyze_process_frequency(process_sequences, weekly_part_demand):
    """How often each operation appears per week (based on part throughput)."""
    freq = {p: 0.0 for p in 'ABCDEFGHIJKLM'}
    for part, demand in weekly_part_demand.items():
        if demand <= 0 or part not in process_sequences:
            continue
        for proc in process_sequences[part]:
            freq[proc] += demand
    return freq

def calculate_detailed_part_step_capacity(year_label, weekly_part_demand, process_sequences, process_times, shifts_per_day):
    """
    Detailed capacity at part-step-operation level (machines dedicated per part/operation).
    This computes and returns 4 DataFrames (no disk IO here):
      - df_detail (Year, Part, Step, Operation, Weekly_Demand_Units, Time_Required_Min_Week, Number_of_Machines)
      - total_by_op (Year, Operation, Total_Machines_Across_Parts)
      - total_by_part (Year, Part, Total_Machines_for_Part)
      - step_summary (Year, Part, Step_1..Step_7) with 'Operation: machines' values
    """
    hours_per_week = shifts_per_day * HOURS_PER_SHIFT * DAYS_PER_WEEK
    minutes_per_week_per_machine = hours_per_week * 60 * EFFECTIVE_AVAILABILITY

    rows = []
    for part, demand in weekly_part_demand.items():
        if demand <= 0 or part not in process_sequences or part not in process_times:
            continue
        ops = process_sequences[part]
        tms = process_times[part]
        for step_num, (op, tmin) in enumerate(zip(ops, tms), start=1):
            if tmin > 0:
                rows.append({
                    'Year': year_label,
                    'Part': part,
                    'Step': step_num,
                    'Operation': op,
                    'Weekly_Demand_Units': float(demand),
                    'Time_Required_Min_Week': float(demand) * float(tmin)
                })
    df = pd.DataFrame(rows)
    if df.empty:
        return (df,
                pd.DataFrame(columns=['Year', 'Operation', 'Total_Machines_Across_Parts']),
                pd.DataFrame(columns=['Year', 'Part', 'Total_Machines_for_Part']),
                pd.DataFrame(columns=['Year', 'Part']))  # empty step summary

    # Machines dedicated per (Part, Operation)
    part_op = (df.groupby(['Year', 'Part', 'Operation'], as_index=False)
                 ['Time_Required_Min_Week'].sum())
    part_op['Number_of_Machines'] = np.ceil(part_op['Time_Required_Min_Week'] / minutes_per_week_per_machine)

    # Join back into detail
    df = df.merge(part_op[['Year', 'Part', 'Operation', 'Number_of_Machines']],
                  on=['Year', 'Part', 'Operation'], how='left')

    # Totals
    total_by_op = (part_op.groupby(['Year', 'Operation'], as_index=False)
                   ['Number_of_Machines'].sum()
                   .rename(columns={'Number_of_Machines': 'Total_Machines_Across_Parts'}))

    total_by_part = (part_op.groupby(['Year', 'Part'], as_index=False)
                     ['Number_of_Machines'].sum()
                     .rename(columns={'Number_of_Machines': 'Total_Machines_for_Part'}))

    # Step summary (Year, Part, Step_1..Step_7)
    tmp = df.copy()
    tmp['Step_Info'] = tmp['Operation'] + ': ' + tmp['Number_of_Machines'].astype(int).astype(str)
    step_summary = (tmp.pivot_table(index=['Year', 'Part'], columns='Step', values='Step_Info', aggfunc='first')
                      .fillna(''))
    # Rename numeric columns 1..7 -> Step_1..Step_7
    step_summary.columns = [f"Step_{int(c)}" for c in step_summary.columns]
    step_summary = step_summary.reset_index()

    return df, total_by_op, total_by_part, step_summary

# =========================
# Main program (aggregated)
# =========================
def main():
    print("="*80)
    print("COMBINED TASK 3 (AGGREGATED) — all years in each CSV")
    print("="*80)

    # Load routings / times
    process_sequences = load_process_sequences()
    process_times = load_process_times()

    # Read multi-year input
    year_plan_csv = r"results\task4\Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv"
    df_all = pd.read_csv(year_plan_csv)

    # Order labels like 'Year 1', 'Year 2', ...
    years = sorted(
        df_all['Year'].unique(),
        key=lambda s: (int(''.join([c for c in str(s) if c.isdigit()]) or 0), str(s))
    )

    # Single output directory (no per-year subfolders)
    out_dir = os.path.join('results', 'task4', 'part', 'capacity')
    ensure_dir(out_dir)
    out_path = Path(out_dir)
    print(f"Aggregated outputs → {out_path.resolve()}")

    # Accumulators
    equip_all = []
    weekly_part_demand_all = []
    freq_all = []
    breakdown_all = []

    detail_1_all = []
    op_1_all = []
    part_1_all = []
    step_1_all = []

    detail_2_all = []
    op_2_all = []
    part_2_all = []
    step_2_all = []

    # Per-year loop (append rows with Year column)
    for year in years:
        df_y = df_all[df_all['Year'] == year].copy()

        # Weekly demand per part (P1..P20)
        weekly_part_demand = {f'P{i}': 0.0 for i in range(1, 21)}
        weekly_part_demand.update(
            dict(zip(df_y['Part'].astype(str), df_y['Weekly_Demand_Units'].astype(float)))
        )

        # Process workload & breakdown
        process_workload, process_breakdown = calculate_process_workload(
            weekly_part_demand, process_sequences, process_times
        )

        # Equipment (process-level)
        equip_df = calculate_equipment_requirements(process_workload)
        equip_df.insert(0, 'Year', year)
        equip_all.append(equip_df)

        # Part demand & frequency
        weekly_part_demand_all.extend([{'Year': year, 'Part': p, 'Weekly_Demand': d}
                                       for p, d in weekly_part_demand.items()])
        freq = analyze_process_frequency(process_sequences, weekly_part_demand)
        freq_all.extend([{'Year': year, 'Process': k, 'Operations_Per_Week': v}
                         for k, v in sorted(freq.items())])

        # Detailed breakdown (for traceability)
        for proc, details in process_breakdown.items():
            for d in details:
                breakdown_all.append({
                    'Year': year,
                    'Process': proc,
                    'Part': d['part'],
                    'Weekly_Part_Demand': d['demand'],
                    'Time_Per_Unit_Minutes': d['time_per_unit'],
                    'Total_Weekly_Minutes': d['total_minutes']
                })

        # Part-step detail (1 and 2 shifts) — only compute and collect
        det1, op1, part1, step1 = calculate_detailed_part_step_capacity(
            year, weekly_part_demand, process_sequences, process_times, shifts_per_day=1
        )
        det2, op2, part2, step2 = calculate_detailed_part_step_capacity(
            year, weekly_part_demand, process_sequences, process_times, shifts_per_day=2
        )

        detail_1_all.append(det1)
        op_1_all.append(op1)
        part_1_all.append(part1)
        step_1_all.append(step1)

        detail_2_all.append(det2)
        op_2_all.append(op2)
        part_2_all.append(part2)
        step_2_all.append(step2)

    # ---------- Concatenate & write single CSVs ----------
    # Equipment
    pd.concat(equip_all, ignore_index=True).to_csv(out_path / "Parts_Based_Equipment_Requirements.csv", index=False)

    # Part demand / frequency / breakdown
    pd.DataFrame(weekly_part_demand_all).to_csv(out_path / "Weekly_Part_Demand.csv", index=False)
    pd.DataFrame(freq_all).to_csv(out_path / "Process_Frequency.csv", index=False)
    if breakdown_all:
        pd.DataFrame(breakdown_all).sort_values(['Year', 'Process', 'Part']).to_csv(
            out_path / "Process_Workload_Breakdown.csv", index=False
        )

    # Part-step details + summaries + comparisons
    # 1 shift
    if detail_1_all:
        pd.concat(detail_1_all, ignore_index=True).to_csv(
            out_path / "Part_Step_Process_Capacity_Requirements_1_shifts.csv", index=False
        )
        pd.concat(step_1_all, ignore_index=True).sort_values(['Year', 'Part']).to_csv(
            out_path / "Part_Step_Machines_Summary_1_shifts.csv", index=False
        )
        op1_all = pd.concat(op_1_all, ignore_index=True)
        part1_all = pd.concat(part_1_all, ignore_index=True)
    else:
        op1_all = pd.DataFrame(columns=['Year', 'Operation', 'Total_Machines_Across_Parts'])
        part1_all = pd.DataFrame(columns=['Year', 'Part', 'Total_Machines_for_Part'])

    # 2 shifts
    if detail_2_all:
        pd.concat(detail_2_all, ignore_index=True).to_csv(
            out_path / "Part_Step_Process_Capacity_Requirements_2_shifts.csv", index=False
        )
        pd.concat(step_2_all, ignore_index=True).sort_values(['Year', 'Part']).to_csv(
            out_path / "Part_Step_Machines_Summary_2_shifts.csv", index=False
        )
        op2_all = pd.concat(op_2_all, ignore_index=True)
        part2_all = pd.concat(part_2_all, ignore_index=True)
    else:
        op2_all = pd.DataFrame(columns=['Year', 'Operation', 'Total_Machines_Across_Parts'])
        part2_all = pd.DataFrame(columns=['Year', 'Part', 'Total_Machines_for_Part'])

    # Comparisons (merge on Year + key)
    if not op1_all.empty and not op2_all.empty:
        comp_op = pd.merge(op1_all, op2_all, on=['Year', 'Operation'],
                           suffixes=('_1_shift', '_2_shifts'))
        comp_op.to_csv(out_path / "Capacity_Comparison_Operations.csv", index=False)

    if not part1_all.empty and not part2_all.empty:
        comp_part = pd.merge(part1_all, part2_all, on=['Year', 'Part'],
                             suffixes=('_1_shift', '_2_shifts'))
        comp_part.to_csv(out_path / "Capacity_Comparison_Parts.csv", index=False)

    print("\nDone. All aggregated files (all years) are in:")
    print(out_path.resolve())

if __name__ == "__main__":
    main()
