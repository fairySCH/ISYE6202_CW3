"""
Combined Task 3 Analysis: Parts-Based Design with Detailed Capacity Requirements
Merges functionality from task3_parts_based_design.py and Part_Step_Capacity.py
Generates comprehensive analysis including process-level and part-step-level capacity requirements
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results" / "Task3" / "Part" / "Capacity"

# Operating parameters
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
    Calculate total weekly minutes needed for each process (A-M)

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
    Calculate equipment requirements for each process

    Available capacity per week:
    - 1 shift: 5 days × 1 shift × 480 min × 88.2% = 2,116.8 min/week
    - 2 shifts: 5 days × 2 shifts × 480 min × 88.2% = 4,233.6 min/week
    """
    capacity_1_shift = DAYS_PER_WEEK * 1 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY
    capacity_2_shifts = DAYS_PER_WEEK * 2 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY

    equipment_reqs = []

    print("\n" + "="*80)
    print("PROCESS WORKLOAD AND EQUIPMENT REQUIREMENTS")
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

def analyze_process_frequency(process_sequences, weekly_part_demand):
    """
    Analyze how many times each process occurs per week (based on part throughput)
    """
    process_frequency = {proc: 0 for proc in 'ABCDEFGHIJKLM'}

    for part, demand in weekly_part_demand.items():
        if demand == 0 or part not in process_sequences:
            continue

        sequence = process_sequences[part]
        for process in sequence:
            process_frequency[process] += demand

    print("\n" + "="*80)
    print("PROCESS FREQUENCY (Operations per Week)")
    print("="*80)

    for process in sorted(process_frequency.keys()):
        freq = process_frequency[process]
        if freq > 0:
            print(f"Process {process}: {freq:,.1f} operations/week")

    return process_frequency

def calculate_detailed_part_step_capacity(weekly_part_demand, process_sequences, process_times, shifts_per_day):
    """
    Calculate detailed capacity requirements at part-step-operation level
    Based on Part_Step_Capacity.py functionality
    """
    print(f"\n{'='*60}")
    print(f"DETAILED PART-STEP CAPACITY: {shifts_per_day} shift(s) per day")
    print(f"{'='*60}")

    hours_per_week = shifts_per_day * HOURS_PER_SHIFT * DAYS_PER_WEEK
    minutes_per_week_per_machine = hours_per_week * 60 * EFFECTIVE_AVAILABILITY

    print(f"Operating Schedule: {shifts_per_day} shift/day x {HOURS_PER_SHIFT} hours x {DAYS_PER_WEEK} days/week")
    print(f"Available: {hours_per_week} hours/week = {hours_per_week * 60} minutes/week per machine")
    print(f"Effective availability: {EFFECTIVE_AVAILABILITY:.1%}")
    print(f"Effective minutes per machine per week: {minutes_per_week_per_machine:.1f}")

    # Prepare data for CSV
    data = []
    for part in weekly_part_demand.keys():
        demand = weekly_part_demand[part]
        if demand == 0 or part not in process_sequences or part not in process_times:
            continue

        operations = process_sequences[part]
        times = process_times[part]

        for step_num, (operation, time_min) in enumerate(zip(operations, times), start=1):
            if time_min > 0:  # Only include steps with time requirements
                time_required_week = demand * time_min
                data.append({
                    'Part': part,
                    'Step': step_num,
                    'Operation': operation,
                    'Weekly_Demand_Units': demand,
                    'Time_Required_Min_Week': time_required_week
                })

    # Create DataFrame
    df = pd.DataFrame(data)

    if df.empty:
        print("No data to process for capacity calculations.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Calculate number of machines per part per operation (dedicated machines per part)
    # First, sum time required per part per operation
    part_operation_totals = df.groupby(['Part', 'Operation'])['Time_Required_Min_Week'].sum().reset_index()
    part_operation_totals['Number_of_Machines'] = np.ceil(part_operation_totals['Time_Required_Min_Week'] / minutes_per_week_per_machine)

    # Merge back to df
    df = df.merge(part_operation_totals[['Part', 'Operation', 'Number_of_Machines']], on=['Part', 'Operation'], how='left')

    # Save detailed CSV
    csv_filename = RESULTS_DIR / f'Part_Step_Process_Capacity_Requirements_{shifts_per_day}_shifts.csv'
    df.to_csv(csv_filename, index=False)
    print(f"CSV generated: {csv_filename}")

    # Create summary CSV with machines per part per step
    df['Step_Info'] = df['Operation'] + ': ' + df['Number_of_Machines'].astype(str)
    step_summary_df = df.pivot(index='Part', columns='Step', values='Step_Info').fillna('')
    step_summary_csv_filename = RESULTS_DIR / f'Part_Step_Machines_Summary_{shifts_per_day}_shifts.csv'
    step_summary_df.to_csv(step_summary_csv_filename)

    print(f"Step Summary CSV generated: {step_summary_csv_filename}")
    print(f"\nStep Summary for {shifts_per_day} shift(s):")
    print(step_summary_df.to_string())

    # Total machines per operation across all parts
    total_machines_per_operation = part_operation_totals.groupby('Operation')['Number_of_Machines'].sum().reset_index()
    total_machines_per_operation.rename(columns={'Number_of_Machines': 'Total_Machines_Across_Parts'}, inplace=True)

    print(f"\nTotal Machines Required per Operation (across all parts):")
    print(total_machines_per_operation.to_string(index=False))

    # Total machines per part
    total_machines_per_part = part_operation_totals.groupby('Part')['Number_of_Machines'].sum().reset_index()
    total_machines_per_part.rename(columns={'Number_of_Machines': 'Total_Machines_for_Part'}, inplace=True)
    print(f"\nTotal Machines Required per Part:")
    print(total_machines_per_part.to_string(index=False))

    return df, total_machines_per_operation, total_machines_per_part

def main():
    """
    Main analysis combining parts-based design and detailed capacity requirements
    """
    print("="*80)
    print("COMBINED TASK 3 ANALYSIS: PARTS-BASED DESIGN + DETAILED CAPACITY")
    print("="*80)

    # Ensure output directory exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

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

    # Step 4: Analyze process frequency
    process_frequency = analyze_process_frequency(process_sequences, weekly_part_demand)

    # Step 5: Calculate equipment requirements
    print("\n4. Calculating Equipment Requirements...")
    equipment_df = calculate_equipment_requirements(process_workload)

    # Step 6: Calculate detailed part-step capacity for both shift scenarios
    print("\n5. Calculating Detailed Part-Step Capacity Requirements...")

    # 1-shift scenario
    detailed_1shift, machines_op_1shift, machines_part_1shift = calculate_detailed_part_step_capacity(
        weekly_part_demand, process_sequences, process_times, 1
    )

    # 2-shift scenario
    detailed_2shift, machines_op_2shift, machines_part_2shift = calculate_detailed_part_step_capacity(
        weekly_part_demand, process_sequences, process_times, 2
    )

    # Step 7: Save all results
    print("\n6. Saving All Results...")

    # Save equipment requirements
    output_file = RESULTS_DIR / "Task3_Parts_Based_Equipment_Requirements.csv"
    equipment_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # Save weekly part demand
    part_demand_df = pd.DataFrame([
        {'Part': part, 'Weekly_Demand': demand}
        for part, demand in weekly_part_demand.items()
    ])
    output_file = RESULTS_DIR / "Task3_Weekly_Part_Demand.csv"
    part_demand_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # Save process frequency
    freq_df = pd.DataFrame([
        {'Process': proc, 'Operations_Per_Week': freq}
        for proc, freq in sorted(process_frequency.items())
    ])
    output_file = RESULTS_DIR / "Task3_Process_Frequency.csv"
    freq_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # Save detailed breakdown
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
        output_file = RESULTS_DIR / "Task3_Process_Workload_Breakdown.csv"
        breakdown_df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file}")

    # Save capacity comparison summaries
    if not machines_op_1shift.empty and not machines_op_2shift.empty:
        comparison_op = pd.merge(machines_op_1shift, machines_op_2shift, on='Operation', suffixes=('_1_shift', '_2_shifts'))
        output_file = RESULTS_DIR / "Capacity_Comparison_Operations.csv"
        comparison_op.to_csv(output_file, index=False)
        print(f"  Saved: {output_file}")

    if not machines_part_1shift.empty and not machines_part_2shift.empty:
        comparison_part = pd.merge(machines_part_1shift, machines_part_2shift, on='Part', suffixes=('_1_shift', '_2_shifts'))
        output_file = RESULTS_DIR / "Capacity_Comparison_Parts.csv"
        comparison_part.to_csv(output_file, index=False)
        print(f"  Saved: {output_file}")

    # Summary
    print("\n" + "="*80)
    print("COMPREHENSIVE SUMMARY")
    print("="*80)
    total_parts = sum(1 for d in weekly_part_demand.values() if d > 0)
    total_operations = sum(process_frequency.values())
    active_processes = sum(1 for w in process_workload.values() if w > 0)

    print(f"Active parts: {total_parts}/20")
    print(f"Active processes: {active_processes}/13")
    print(f"Total operations per week: {total_operations:,.1f}")

    print("\nEquipment Summary (2-shift operation recommended):")
    for _, row in equipment_df.iterrows():
        if row['Equipment_2_Shifts'] > 0:
            print(f"  Process {row['Process']}: {row['Equipment_2_Shifts']} units")

    print("\nCapacity Summary (2-shift scenario):")
    if not machines_op_2shift.empty:
        total_machines_2shift = machines_op_2shift['Total_Machines_Across_Parts'].sum()
        print(f"  Total machines across all operations: {total_machines_2shift}")

    print("\n" + "="*80)
    print("Analysis complete! All results saved to:")
    print(f"  {RESULTS_DIR}")
    print("="*80)

if __name__ == "__main__":
    main()