"""
Task 3 - Parts-Based Design: Complete Machine Requirements Calculator
Calculates machine requirements for all 13 processes (A-M) based on Year +1 demand

Uses 2-shift operation: 4800 minutes/week per machine (2 shifts × 5 days × 8 hours × 60 min)
Target utilization: 99% for machine count calculation
"""

import csv
from pathlib import Path
from math import ceil

# Base directory setup
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "csv_outputs"

# Operating parameters
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
MINUTES_PER_SHIFT = HOURS_PER_SHIFT * 60  # 480 minutes
SHIFTS = 2
MINUTES_PER_WEEK = SHIFTS * DAYS_PER_WEEK * MINUTES_PER_SHIFT  # 4800 minutes/week
TARGET_UTILIZATION = 0.99

def load_weekly_product_demand():
    """Load Year +1 weekly product demand for A1, A2, A3, B1, B2"""
    with open(DATA_DIR / '+1 Year Product Demand.csv', 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    # Row 12, columns 2-6: Weekly demand
    products = ['A1', 'A2', 'A3', 'B1', 'B2']
    weekly_demand_values = [float(lines[12][i]) for i in range(2, 7)]
    
    weekly_demand = dict(zip(products, weekly_demand_values))
    
    print("=" * 80)
    print("WEEKLY PRODUCT DEMAND (Year +1)")
    print("=" * 80)
    for product, demand in weekly_demand.items():
        print(f"  {product}: {demand:,.2f} units/week")
    
    return weekly_demand

def load_bom():
    """Load Bill of Materials (BOM) - parts per product"""
    with open(DATA_DIR / '+1 Year Parts per Product.csv', 'r', encoding='utf-8') as f:
        lines = [line.strip().split(',') for line in f]
    
    bom = {}
    products = ['A1', 'A2', 'A3', 'B1', 'B2']
    
    # Starting from row 2 (index 2), parts P1-P20
    for i in range(2, 22):
        part_name = lines[i][1].strip()
        bom[part_name] = {}
        
        for j, product in enumerate(products):
            qty_str = lines[i][2+j].strip()
            if qty_str:
                bom[part_name][product] = int(float(qty_str))
    
    print("\n" + "=" * 80)
    print("BILL OF MATERIALS (BOM)")
    print("=" * 80)
    print(f"  Parts: P1 to P20")
    print(f"  Products: {products}")
    
    return bom

def load_process_sequences():
    """Load process sequences for each part from Parts Specs.csv"""
    with open(DATA_DIR / 'Parts Specs.csv', 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    process_sequences = {}
    
    # Rows 11-30 contain process sequences for P1-P20
    for i in range(11, 31):
        part_name = lines[i][1].strip() if lines[i][1] else None
        if part_name:
            sequence = []
            # Columns 2-8 contain Steps 1-7
            for j in range(2, 9):
                if j < len(lines[i]) and lines[i][j].strip():
                    sequence.append(lines[i][j].strip())
            process_sequences[part_name] = sequence
    
    print("\n" + "=" * 80)
    print("PROCESS SEQUENCES (Sample)")
    print("=" * 80)
    for part, seq in list(process_sequences.items())[:5]:
        print(f"  {part}: {' → '.join(seq)}")
    print("  ...")
    
    return process_sequences

def load_process_times():
    """Load process times (minutes) for each part at each step"""
    with open(DATA_DIR / 'Parts_Step_Time.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        lines = list(reader)
    
    process_times = {}
    
    for row in lines:
        part = row[0].strip()
        times = []
        for i in range(1, 8):  # Steps 1-7
            if i < len(row) and row[i].strip():
                times.append(float(row[i]))
            else:
                times.append(0)
        process_times[part] = times
    
    print("\n" + "=" * 80)
    print("PROCESS TIMES (Sample - minutes per unit)")
    print("=" * 80)
    for part, times in list(process_times.items())[:5]:
        non_zero_times = [t for t in times if t > 0]
        print(f"  {part}: {non_zero_times}")
    print("  ...")
    
    return process_times

def calculate_weekly_part_demand(weekly_product_demand, bom):
    """Calculate weekly demand for each part based on product demand and BOM"""
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
    
    print("\n" + "=" * 80)
    print("WEEKLY PART DEMAND")
    print("=" * 80)
    total_parts = sum(weekly_part_demand.values())
    for part, demand in weekly_part_demand.items():
        if demand > 0:
            print(f"  {part}: {demand:,.2f} units/week")
    print(f"  TOTAL: {total_parts:,.2f} units/week")
    
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
    
    return process_workload

def calculate_machines(process_workload):
    """
    Calculate required machines for each process
    
    Formula: machines = ceil((weekly_minutes) / (4800 * 0.99))
    
    Returns:
        dict: {process: machines_needed}
    """
    machines = {}
    
    print("\n" + "=" * 80)
    print("MACHINE REQUIREMENTS CALCULATION")
    print("=" * 80)
    print(f"2-Shift Operation: {MINUTES_PER_WEEK} minutes/week per machine")
    print(f"Target Utilization: {TARGET_UTILIZATION * 100:.0f}%")
    print(f"Available Time per Machine: {MINUTES_PER_WEEK * TARGET_UTILIZATION:.0f} minutes/week")
    print()
    
    total_machines = 0
    
    for process in sorted(process_workload.keys()):
        weekly_minutes = process_workload[process]
        
        # Calculate machines needed
        if weekly_minutes > 0:
            machines_needed = ceil(weekly_minutes / (MINUTES_PER_WEEK * TARGET_UTILIZATION))
            actual_utilization = (weekly_minutes / (machines_needed * MINUTES_PER_WEEK)) * 100
        else:
            machines_needed = 0
            actual_utilization = 0.0
        
        machines[process] = machines_needed
        total_machines += machines_needed
        
        print(f"Process {process}:")
        print(f"  Weekly Minutes: {weekly_minutes:,.2f}")
        print(f"  Machines Needed: {machines_needed}")
        print(f"  Actual Utilization: {actual_utilization:.1f}%")
        print()
    
    print("=" * 80)
    print(f"TOTAL MACHINES: {total_machines}")
    print("=" * 80)
    
    return machines, total_machines

def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("TASK 3 - PARTS-BASED DESIGN")
    print("COMPLETE MACHINE REQUIREMENTS CALCULATOR")
    print("=" * 80)
    
    # Load data
    weekly_product_demand = load_weekly_product_demand()
    bom = load_bom()
    process_sequences = load_process_sequences()
    process_times = load_process_times()
    
    # Calculate part demand
    weekly_part_demand = calculate_weekly_part_demand(weekly_product_demand, bom)
    
    # Calculate process workload
    process_workload = calculate_process_workload(weekly_part_demand, process_sequences, process_times)
    
    # Calculate machines
    machines, total_machines = calculate_machines(process_workload)
    
    # Summary
    print("\n" + "=" * 80)
    print("MACHINE COUNT SUMMARY")
    print("=" * 80)
    machine_list = []
    for process in 'ABCDEFGHIJKLM':
        count = machines.get(process, 0)
        machine_list.append(f"{process}={count}")
        print(f"  {process}: {count:3d} machines")
    
    print(f"\n  TOTAL: {total_machines} machines")
    print(f"  Summary: {', '.join(machine_list)}")
    print("=" * 80)

if __name__ == "__main__":
    main()
