"""
Task 3: Functional Layout - Capacity Requirements Analysis

Calculates equipment requirements for functional layout organization.
Functional layout groups similar processes together for efficiency.

This script:
1. Loads functional flow matrix data
2. Calculates process workloads from part-level data
3. Determines equipment requirements for functional organization
4. Generates capacity analysis reports

Author: Analysis Team
Date: November 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results" / "Task3" / "Functional"

# Operating parameters (same as Part and Fractal approaches)
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
MINUTES_PER_SHIFT = HOURS_PER_SHIFT * 60  # 480 minutes
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY  # 0.882 or 88.2%

def load_weekly_product_demand():
    """
    Load Year +1 weekly product demand for A1, A2, A3, B1, B2
    """
    df = pd.read_csv(DATA_DIR / '+1 Year Product Demand.csv', header=None)

    # Row 12, columns 2-6: Weekly demand
    products = ['A1', 'A2', 'A3', 'B1', 'B2']
    weekly_demand_values = df.iloc[12, 2:7].astype(float).tolist()

    weekly_demand = dict(zip(products, weekly_demand_values))

    print("Weekly Product Demand:")
    for product, demand in weekly_demand.items():
        print(f"  {product}: {demand:.2f} units/week")

    return weekly_demand

def load_bom():
    """
    Load Bill of Materials (BOM) - parts per product
    """
    # Read BOM file
    bom_lines = []
    with open(DATA_DIR / '+1 Year Parts per Product.csv', 'r', encoding='utf-8') as f:
        for line in f:
            bom_lines.append(line.strip().split(','))

    # Create BOM dictionary
    bom = {}
    products = ['A1', 'A2', 'A3', 'B1', 'B2']

    # Starting from row 2 (index 2), parts P1-P20
    for i in range(2, 22):
        part_name = bom_lines[i][1].strip()
        bom[part_name] = {}

        for j, product in enumerate(products):
            qty_str = bom_lines[i][2+j].strip()
            if qty_str:
                bom[part_name][product] = int(float(qty_str))

    print("\nBill of Materials (BOM) loaded:")
    print(f"  Parts: P1 to P20")
    print(f"  Products: {products}")

    return bom

def load_process_sequences():
    """
    Load process sequences for each part from Parts Specs.csv
    """
    df = pd.read_csv(DATA_DIR / 'Parts Specs.csv', header=None)

    process_sequences = {}

    # Rows 11-30 contain process sequences for P1-P20
    for i in range(11, 31):
        part_name = df.iloc[i, 1]
        if pd.notna(part_name):
            part_name = str(part_name).strip()
            sequence = []
            # Columns 2-8 contain Steps 1-7
            for j in range(2, 9):
                process = df.iloc[i, j]
                if pd.notna(process) and str(process).strip():
                    sequence.append(str(process).strip())
            process_sequences[part_name] = sequence

    print("\nProcess Sequences loaded:")
    for part, seq in list(process_sequences.items())[:3]:
        print(f"  {part}: {' → '.join(seq)}")
    print("  ...")

    return process_sequences

def load_process_times():
    """
    Load process times (minutes) for each part at each step
    """
    df = pd.read_csv(DATA_DIR / 'Parts_Step_Time.csv')

    process_times = {}

    for _, row in df.iterrows():
        part = row['Part']
        times = []
        for step in ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6', 'Step 7']:
            if pd.notna(row[step]):
                times.append(float(row[step]))
            else:
                times.append(0)
        process_times[part] = times

    print("\nProcess Times loaded (minutes per unit):")
    for part, times in list(process_times.items())[:3]:
        non_zero_times = [t for t in times if t > 0]
        print(f"  {part}: {non_zero_times}")
    print("  ...")

    return process_times

def calculate_weekly_part_demand(weekly_product_demand, bom):
    """
    Calculate weekly demand for each part based on product demand and BOM
    """
    weekly_part_demand = {}

    # Initialize all parts P1-P20
    for i in range(1, 21):
        part = f'P{i}'
        weekly_part_demand[part] = 0.0

    # Calculate demand for each part
    for part in weekly_part_demand.keys():
        total_demand = 0.0
        if part in bom:
            for product, qty_per_product in bom[part].items():
                if product in weekly_product_demand:
                    total_demand += weekly_product_demand[product] * qty_per_product
        weekly_part_demand[part] = total_demand

    print("\nWeekly Part Demand:")
    for part, demand in weekly_part_demand.items():
        if demand > 0:
            print(f"  {part}: {demand:.2f} units/week")

    return weekly_part_demand

def calculate_process_workload(weekly_part_demand, process_sequences, process_times):
    """
    Calculate total weekly minutes needed for each process (A-M) in functional layout

    Returns:
        dict: {process: total_minutes_per_week}
    """
    process_workload = {}

    # Initialize all processes A-M
    all_processes = list('ABCDEFGHIJKLM')
    for proc in all_processes:
        process_workload[proc] = 0.0

    # Detailed breakdown for verification
    process_breakdown = {proc: [] for proc in all_processes}

    # For each part
    for part in weekly_part_demand.keys():
        demand = weekly_part_demand[part]
        if demand == 0:
            continue

        if part not in process_sequences or part not in process_times:
            continue

        sequence = process_sequences[part]
        times = process_times[part]

        # For each step in the part's process sequence
        for step_idx, process in enumerate(sequence):
            if step_idx < len(times) and times[step_idx] > 0:
                time_per_unit = times[step_idx]
                total_minutes = demand * time_per_unit

                process_workload[process] += total_minutes
                process_breakdown[process].append({
                    'part': part,
                    'demand': demand,
                    'time_per_unit': time_per_unit,
                    'total_minutes': total_minutes
                })

    return process_workload, process_breakdown

def calculate_equipment_requirements(process_workload):
    """
    Calculate equipment requirements for functional layout

    Available capacity per week:
    - 1 shift: 5 days × 1 shift × 480 min × 88.2% = 2,116.8 min/week
    - 2 shifts: 5 days × 2 shifts × 480 min × 88.2% = 4,233.6 min/week
    """
    capacity_1_shift = DAYS_PER_WEEK * 1 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY
    capacity_2_shifts = DAYS_PER_WEEK * 2 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY

    equipment_reqs = []

    print("\n" + "="*80)
    print("FUNCTIONAL LAYOUT - EQUIPMENT REQUIREMENTS")
    print("="*80)
    print(f"Available capacity per equipment unit:")
    print(f"  1 shift/day:  {capacity_1_shift:.1f} minutes/week")
    print(f"  2 shifts/day: {capacity_2_shifts:.1f} minutes/week")
    print("\n" + "-"*80)

    for process in sorted(process_workload.keys()):
        workload = process_workload[process]

        if workload == 0:
            equipment_reqs.append({
                'Process': process,
                'Weekly_Minutes': 0,
                'Weekly_Hours': 0,
                'Equipment_1_Shift': 0,
                'Equipment_2_Shifts': 0,
                'Utilization_1_Shift': 0,
                'Utilization_2_Shifts': 0
            })
            continue

        # Calculate equipment needed
        equip_1_shift = np.ceil(workload / capacity_1_shift)
        equip_2_shifts = np.ceil(workload / capacity_2_shifts)

        # Calculate utilization
        util_1_shift = (workload / (equip_1_shift * capacity_1_shift)) * 100 if equip_1_shift > 0 else 0
        util_2_shifts = (workload / (equip_2_shifts * capacity_2_shifts)) * 100 if equip_2_shifts > 0 else 0

        equipment_reqs.append({
            'Process': process,
            'Weekly_Minutes': workload,
            'Weekly_Hours': workload / 60,
            'Equipment_1_Shift': int(equip_1_shift),
            'Equipment_2_Shifts': int(equip_2_shifts),
            'Utilization_1_Shift': util_1_shift,
            'Utilization_2_Shifts': util_2_shifts
        })

        print(f"Process {process}:")
        print(f"  Weekly workload: {workload:,.1f} minutes ({workload/60:.1f} hours)")
        print(f"  Equipment needed (1 shift):  {int(equip_1_shift)} units @ {util_1_shift:.1f}% utilization")
        print(f"  Equipment needed (2 shifts): {int(equip_2_shifts)} units @ {util_2_shifts:.1f}% utilization")
        print()

    return pd.DataFrame(equipment_reqs)

def analyze_functional_layout_efficiency(equipment_df, process_workload):
    """
    Analyze efficiency metrics specific to functional layout
    """
    print("\n" + "="*80)
    print("FUNCTIONAL LAYOUT EFFICIENCY ANALYSIS")
    print("="*80)

    # Calculate total equipment and utilization metrics
    total_equip_1shift = equipment_df['Equipment_1_Shift'].sum()
    total_equip_2shifts = equipment_df['Equipment_2_Shifts'].sum()

    active_processes = len(equipment_df[equipment_df['Equipment_2_Shifts'] > 0])
    total_workload = sum(process_workload.values())

    print(f"Active processes: {active_processes}/13")
    print(f"Total equipment (1 shift): {total_equip_1shift}")
    print(f"Total equipment (2 shifts): {total_equip_2shifts}")
    print(f"Total weekly workload: {total_workload:,.1f} minutes ({total_workload/60:,.1f} hours)")

    # Calculate average utilization for 2-shift scenario
    avg_utilization = equipment_df[equipment_df['Equipment_2_Shifts'] > 0]['Utilization_2_Shifts'].mean()
    print(f"Average equipment utilization (2 shifts): {avg_utilization:.1f}%")

    # Process grouping analysis (functional layout benefit)
    high_workload_processes = equipment_df[equipment_df['Weekly_Hours'] > 100]['Process'].tolist()
    print(f"High-workload processes (>100 hours/week): {high_workload_processes}")

    return {
        'total_equipment_1shift': total_equip_1shift,
        'total_equipment_2shifts': total_equip_2shifts,
        'active_processes': active_processes,
        'total_workload_hours': total_workload / 60,
        'average_utilization': avg_utilization,
        'high_workload_processes': high_workload_processes
    }

def main():
    """
    Main analysis for functional layout capacity requirements
    """
    print("="*80)
    print("TASK 3: FUNCTIONAL LAYOUT - CAPACITY REQUIREMENTS ANALYSIS")
    print("="*80)

    # Ensure output directory exists
    capacity_dir = RESULTS_DIR / "Capacity"
    capacity_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Load data
    print("\n1. Loading Data...")
    weekly_product_demand = load_weekly_product_demand()
    bom = load_bom()
    process_sequences = load_process_sequences()
    process_times = load_process_times()

    # Step 2: Calculate weekly part demand
    print("\n2. Calculating Weekly Part Demand...")
    weekly_part_demand = calculate_weekly_part_demand(weekly_product_demand, bom)

    # Step 3: Calculate process workload
    print("\n3. Calculating Process Workload...")
    process_workload, process_breakdown = calculate_process_workload(
        weekly_part_demand, process_sequences, process_times
    )

    # Step 4: Calculate equipment requirements
    print("\n4. Calculating Equipment Requirements...")
    equipment_df = calculate_equipment_requirements(process_workload)

    # Step 5: Analyze functional layout efficiency
    efficiency_metrics = analyze_functional_layout_efficiency(equipment_df, process_workload)

    # Step 6: Save all results
    print("\n5. Saving Results...")

    # Save equipment requirements
    output_file = capacity_dir / "Functional_Equipment_Requirements.csv"
    equipment_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # Save weekly part demand
    part_demand_df = pd.DataFrame([
        {'Part': part, 'Weekly_Demand': demand}
        for part, demand in weekly_part_demand.items()
    ])
    output_file = capacity_dir / "Functional_Weekly_Part_Demand.csv"
    part_demand_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # Save process workload breakdown
    breakdown_records = []
    for process, details in process_breakdown.items():
        for detail in details:
            breakdown_records.append({
                'Process': process,
                'Part': detail['part'],
                'Weekly_Part_Demand': detail['demand'],
                'Time_Per_Unit_Minutes': detail['time_per_unit'],
                'Total_Weekly_Minutes': detail['total_minutes']
            })

    breakdown_df = pd.DataFrame(breakdown_records)
    if not breakdown_df.empty:
        breakdown_df = breakdown_df.sort_values(['Process', 'Part'])
        output_file = capacity_dir / "Functional_Process_Workload_Breakdown.csv"
        breakdown_df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file}")

    # Save efficiency metrics
    efficiency_df = pd.DataFrame([efficiency_metrics])
    output_file = capacity_dir / "Functional_Layout_Efficiency_Metrics.csv"
    efficiency_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # Generate summary report
    print("\n6. Generating Summary Report...")
    summary_report = f"""
FUNCTIONAL LAYOUT CAPACITY ANALYSIS SUMMARY
{'='*50}

Operating Parameters:
- Days per week: {DAYS_PER_WEEK}
- Hours per shift: {HOURS_PER_SHIFT}
- Efficiency: {EFFICIENCY:.1%}
- Reliability: {RELIABILITY:.1%}
- Effective availability: {EFFECTIVE_AVAILABILITY:.1%}

Capacity Results (2-shift operation recommended):
- Active processes: {efficiency_metrics['active_processes']}/13
- Total equipment needed: {efficiency_metrics['total_equipment_2shifts']}
- Total weekly workload: {efficiency_metrics['total_workload_hours']:,.1f} hours
- Average utilization: {efficiency_metrics['average_utilization']:.1f}%

High-workload processes (>100 hours/week):
{', '.join(efficiency_metrics['high_workload_processes'])}

Equipment Requirements by Process:
"""

    for _, row in equipment_df.iterrows():
        if row['Equipment_2_Shifts'] > 0:
            summary_report += f"- Process {row['Process']}: {row['Equipment_2_Shifts']} units ({row['Utilization_2_Shifts']:.1f}% utilization)\n"

    # Save summary report
    output_file = capacity_dir / "Functional_Capacity_Summary_Report.txt"
    with open(output_file, 'w') as f:
        f.write(summary_report)
    print(f"  Saved: {output_file}")

    print("\n" + "="*80)
    print("FUNCTIONAL LAYOUT CAPACITY ANALYSIS COMPLETE!")
    print("="*80)
    print(f"All results saved to: {capacity_dir}")
    print("="*80)

if __name__ == "__main__":
    main()