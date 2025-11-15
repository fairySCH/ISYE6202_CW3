"""
task 4: functional layout - capacity requirements analysis (years 2-5)

calculates equipment requirements for functional layout organization across years 2-5.
functional layout groups similar processes together for efficiency.

this script:
1. loads demand data for each year (2-5)
2. calculates process workloads from part-level data per year
3. determines equipment requirements for functional organization per year
4. generates capacity analysis reports per year

author: machas^2 team
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results" / "task4" / "functional"

# Operating parameters (same as Part and Fractal approaches)
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
MINUTES_PER_SHIFT = HOURS_PER_SHIFT * 60  # 480 minutes
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY  # 0.882 or 88.2%

def load_weekly_product_demand(year):
    """
    Load weekly product demand for specified year (+2, +3, +4, +5)
    """
    df = pd.read_csv(DATA_DIR / '+2 to +5 Year Product Demand.csv', header=None)

    # Find the row with expected average weekly demand header
    header_row = None
    for i, (idx, row) in enumerate(df.iterrows()):
        if str(row[1]).strip() == 'Expected Average Weekly Demand for Each Product in the +2 to +5 Year Horizon':
            header_row = i + 1  # Data starts on next row
            break

    if header_row is None:
        raise ValueError("Could not find weekly demand header")

    year_label = f'+{year}'

    # find the row for the specific year
    data_row = None
    for i in range(header_row, len(df)):
        if str(df.iloc[i, 1]).strip() == year_label:
            data_row = i
            break

    if data_row is None:
        raise ValueError(f"Could not find weekly demand data for year {year_label}")

    # products: a1,a2,a3,b1,b2,a4,b3,b4 (columns 2-9, since column 0 is nan, 1 is year)
    products = ['A1', 'A2', 'A3', 'B1', 'B2', 'A4', 'B3', 'B4']
    weekly_demand_values = []
    for j in range(2, 10):  # Columns 2-9
        val = df.iloc[data_row, j]
        weekly_demand_values.append(float(val) if pd.notna(val) else 0.0)

    weekly_demand = dict(zip(products, weekly_demand_values))

    print(f"Year {year_label} Weekly Product Demand:")
    for product, demand in weekly_demand.items():
        print(f"  {product}: {demand:.2f} units/week")

    return weekly_demand

def load_bom():
    """
    Load Bill of Materials (BOM) - parts per product for years 2-5
    """
    df = pd.read_csv(DATA_DIR / '+2 to +5 Year Parts per Product.csv', header=None)

    # Create BOM dictionary
    bom = {}
    products = ['A1', 'A2', 'A3', 'B1', 'B2', 'A4', 'B3', 'B4']

    # Starting from row 2 (index 2), parts P1-P20
    for i in range(2, 22):
        part_name = df.iloc[i, 1]
        if pd.notna(part_name):
            part_name = str(part_name).strip()
            bom[part_name] = {}

            for j, product in enumerate(products):
                qty_str = str(df.iloc[i, 2+j]).strip() if pd.notna(df.iloc[i, 2+j]) else ''
                if qty_str and qty_str != '':
                    bom[part_name][product] = int(float(qty_str))

    print("\nBill of Materials (BOM) loaded for years 2-5:")
    print(f"  Parts: P1 to P20")
    print(f"  Products: {products}")

    return bom

def load_process_sequences():
    """
    Load process sequences for each part from Parts Specs.csv
    """
    df = pd.read_csv(DATA_DIR / 'Parts Specs.csv', header=None)

    process_sequences = {}

    # rows 11-30 contain process sequences for p1-p20
    for i in range(11, 31):
        part_name = df.iloc[i, 1]
        if pd.notna(part_name):
            part_name = str(part_name).strip()
            sequence = []
            # columns 2-8 contain steps 1-7
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

    # initialize all parts p1-p20
    for i in range(1, 21):
        part = f'P{i}'
        weekly_part_demand[part] = 0.0

    # calculate demand for each part
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

    # initialize all processes a-m
    all_processes = list('ABCDEFGHIJKLM')
    for proc in all_processes:
        process_workload[proc] = 0.0

    # detailed breakdown for verification
    process_breakdown = {proc: [] for proc in all_processes}

    # for each part
    for part in weekly_part_demand.keys():
        demand = weekly_part_demand[part]
        if demand == 0:
            continue

        if part not in process_sequences or part not in process_times:
            continue

        sequence = process_sequences[part]
        times = process_times[part]

        # for each step in the part's process sequence
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

def calculate_equipment_requirements(process_workload, year_label):
    """
    Calculate equipment requirements for functional layout
    """
    capacity_1_shift = DAYS_PER_WEEK * 1 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY
    capacity_2_shifts = DAYS_PER_WEEK * 2 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY

    equipment_reqs = []

    print(f"\n{'='*80}")
    print(f"FUNCTIONAL LAYOUT - EQUIPMENT REQUIREMENTS (Year {year_label})")
    print(f"{'='*80}")
    print(f"Available capacity per equipment unit:")
    print(f"  1 shift/day:  {capacity_1_shift:.1f} minutes/week")
    print(f"  2 shifts/day: {capacity_2_shifts:.1f} minutes/week")
    print(f"{'-'*80}")

    for process in sorted(process_workload.keys()):
        workload = process_workload[process]

        if workload == 0:
            equipment_reqs.append({
                'Year': year_label,
                'Process': process,
                'Weekly_Minutes': 0,
                'Weekly_Hours': 0,
                'Equipment_1_Shift': 0,
                'Equipment_2_Shifts': 0,
                'Utilization_1_Shift': 0,
                'Utilization_2_Shifts': 0
            })
            continue

        # calculate equipment needed
        equip_1_shift = np.ceil(workload / capacity_1_shift)
        equip_2_shifts = np.ceil(workload / capacity_2_shifts)

        # calculate utilization
        util_1_shift = (workload / (equip_1_shift * capacity_1_shift)) * 100 if equip_1_shift > 0 else 0
        util_2_shifts = (workload / (equip_2_shifts * capacity_2_shifts)) * 100 if equip_2_shifts > 0 else 0

        equipment_reqs.append({
            'Year': year_label,
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

def analyze_functional_layout_efficiency(equipment_df, process_workload, year_label):
    """
    Analyze efficiency metrics specific to functional layout
    """
    print(f"\n{'='*80}")
    print(f"FUNCTIONAL LAYOUT EFFICIENCY ANALYSIS (Year {year_label})")
    print(f"{'='*80}")

    # calculate total equipment and utilization metrics
    total_equip_1shift = equipment_df['Equipment_1_Shift'].sum()
    total_equip_2shifts = equipment_df['Equipment_2_Shifts'].sum()

    active_processes = len(equipment_df[equipment_df['Equipment_2_Shifts'] > 0])
    total_workload = sum(process_workload.values())

    print(f"Active processes: {active_processes}/13")
    print(f"Total equipment (1 shift): {total_equip_1shift}")
    print(f"Total equipment (2 shifts): {total_equip_2shifts}")
    print(f"Total weekly workload: {total_workload:,.1f} minutes ({total_workload/60:,.1f} hours)")

    # calculate average utilization for 2-shift scenario
    avg_utilization = equipment_df[equipment_df['Equipment_2_Shifts'] > 0]['Utilization_2_Shifts'].mean()
    print(f"Average equipment utilization (2 shifts): {avg_utilization:.1f}%")

    # process grouping analysis (functional layout benefit)
    high_workload_processes = equipment_df[equipment_df['Weekly_Hours'] > 100]['Process'].tolist()
    print(f"High-workload processes (>100 hours/week): {high_workload_processes}")

    return {
        'Year': year_label,
        'total_equipment_1shift': total_equip_1shift,
        'total_equipment_2shifts': total_equip_2shifts,
        'active_processes': active_processes,
        'total_workload_hours': total_workload / 60,
        'average_utilization': avg_utilization,
        'high_workload_processes': ', '.join(high_workload_processes)
    }

def main():
    """
    Main analysis for functional layout capacity requirements across years 2-5
    """
    print("="*80)
    print("TASK 4: FUNCTIONAL LAYOUT - CAPACITY REQUIREMENTS ANALYSIS (YEARS 2-5)")
    print("="*80)

    # ensure output directory exists
    capacity_dir = RESULTS_DIR / "Capacity"
    capacity_dir.mkdir(parents=True, exist_ok=True)

    # Load common data (same across years)
    print("\n1. Loading Common Data...")
    bom = load_bom()
    process_sequences = load_process_sequences()
    process_times = load_process_times()

    # initialize dataframes for aggregation
    all_equipment_reqs = []
    all_efficiency_metrics = []
    all_part_demands = []
    all_workload_breakdowns = []

    # process each year
    for year in [2, 3, 4, 5]:
        year_label = f"+{year}"
        print(f"\n{'='*60}")
        print(f"PROCESSING YEAR {year_label}")
        print(f"{'='*60}")

        # step 1: load year-specific demand
        print(f"\n1. Loading Demand Data for Year {year_label}...")
        weekly_product_demand = load_weekly_product_demand(year)

        # step 2: calculate weekly part demand
        print(f"\n2. Calculating Weekly Part Demand for Year {year_label}...")
        weekly_part_demand = calculate_weekly_part_demand(weekly_product_demand, bom)

        # step 3: calculate process workload
        print(f"\n3. Calculating Process Workload for Year {year_label}...")
        process_workload, process_breakdown = calculate_process_workload(
            weekly_part_demand, process_sequences, process_times
        )

        # step 4: calculate equipment requirements
        print(f"\n4. Calculating Equipment Requirements for Year {year_label}...")
        equipment_df = calculate_equipment_requirements(process_workload, year_label)

        # step 5: analyze functional layout efficiency
        efficiency_metrics = analyze_functional_layout_efficiency(equipment_df, process_workload, year_label)

        # collect data for aggregation
        all_equipment_reqs.append(equipment_df)
        all_efficiency_metrics.append(efficiency_metrics)

        # add year to part demand and workload breakdown
        part_demand_df = pd.DataFrame([
            {'Year': year_label, 'Part': part, 'Weekly_Demand': demand}
            for part, demand in weekly_part_demand.items()
        ])
        all_part_demands.append(part_demand_df)

        breakdown_records = []
        for process, details in process_breakdown.items():
            for detail in details:
                breakdown_records.append({
                    'Year': year_label,
                    'Process': process,
                    'Part': detail['part'],
                    'Weekly_Part_Demand': detail['demand'],
                    'Time_Per_Unit_Minutes': detail['time_per_unit'],
                    'Total_Weekly_Minutes': detail['total_minutes']
                })
        all_workload_breakdowns.extend(breakdown_records)

    # step 6: save all results
    print("\n5. Saving Results...")

    # save equipment requirements (all years)
    equipment_combined_df = pd.concat(all_equipment_reqs, ignore_index=True)
    output_file = capacity_dir / "Functional_Equipment_Requirements_All_Years.csv"
    equipment_combined_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # save efficiency metrics (all years)
    efficiency_df = pd.DataFrame(all_efficiency_metrics)
    output_file = capacity_dir / "Functional_Layout_Efficiency_Metrics_All_Years.csv"
    efficiency_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # save weekly part demand (all years)
    part_demand_combined_df = pd.concat(all_part_demands, ignore_index=True)
    output_file = capacity_dir / "Functional_Weekly_Part_Demand_All_Years.csv"
    part_demand_combined_df.to_csv(output_file, index=False)
    print(f"  Saved: {output_file}")

    # save process workload breakdown (all years)
    breakdown_df = pd.DataFrame(all_workload_breakdowns)
    if not breakdown_df.empty:
        breakdown_df = breakdown_df.sort_values(['Year', 'Process', 'Part'])
        output_file = capacity_dir / "Functional_Process_Workload_Breakdown_All_Years.csv"
        breakdown_df.to_csv(output_file, index=False)
        print(f"  Saved: {output_file}")

    # generate summary report
    print("\n6. Generating Summary Report...")
    summary_report = f"""
FUNCTIONAL LAYOUT CAPACITY ANALYSIS SUMMARY (YEARS 2-5)
{'='*60}

Operating Parameters:
- Days per week: {DAYS_PER_WEEK}
- Hours per shift: {HOURS_PER_SHIFT}
- Efficiency: {EFFICIENCY:.1%}
- Reliability: {RELIABILITY:.1%}
- Effective availability: {EFFECTIVE_AVAILABILITY:.1%}

Year-by-Year Capacity Results (2-shift operation recommended):
"""

    for _, row in efficiency_df.iterrows():
        summary_report += f"""
Year {row['Year']}:
- Active processes: {row['active_processes']}/13
- Total equipment needed: {row['total_equipment_2shifts']}
- Total weekly workload: {row['total_workload_hours']:,.1f} hours
- Average utilization: {row['average_utilization']:.1f}%
- High-workload processes (>100 hours/week): {row['high_workload_processes']}
"""

    # save summary report
    output_file = capacity_dir / "Functional_Capacity_Summary_Report_All_Years.txt"
    with open(output_file, 'w') as f:
        f.write(summary_report)
    print(f"  Saved: {output_file}")

    print("\n" + "="*80)
    print("FUNCTIONAL LAYOUT CAPACITY ANALYSIS COMPLETE (YEARS 2-5)!")
    print("="*80)
    print(f"All results saved to: {capacity_dir}")
    print("="*80)

if __name__ == "__main__":
    main()