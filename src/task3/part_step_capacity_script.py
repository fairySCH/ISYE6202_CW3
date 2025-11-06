# Script to create a detailed breakdown of parts, steps, operations, and capacity requirements to fulfill weekly demand
# Calculates for both 1-shift and 2-shift scenarios

import pandas as pd
import numpy as np

# Load weekly demand from Task1 results
task1_df = pd.read_csv('../results/Task1_Demand_Fulfillment_Capacity_Plan.csv')
weekly_demand = dict(zip(task1_df['Part'], task1_df['Weekly_Demand_Units']))

# Process operations from Parts Specs
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

# Process times from Parts_Step_Time
process_times = {
    'P1':  [2.5, 1.0, 2.5, 0.5, 2.5, 1.25, 2.5],
    'P2':  [1.25, 0.5, 2.5, 1.0, 2.5],
    'P3':  [1.75, 3.0, 0.75, 1.5, 2.5],
    'P4':  [1.0, 2.0, 3.0, 0.25, 1.25],
    'P5':  [1.5, 0.75, 3.5, 1.75],
    'P6':  [0.75, 1.25, 0.5, 3.0, 1.0, 1.25, 2.75],
    'P7':  [1.0, 1.5, 0.75, 3.5, 1.25, 2.0],
    'P8':  [1.25, 2.0, 0.5, 1.0],
    'P9':  [1.75, 0.75, 1.25, 0.5, 1.25, 3.0],
    'P10': [1.5, 1.75, 1.25, 2.0],
    'P11': [1.25, 0.5, 1.25, 0.25, 0.75],
    'P12': [1.0, 0.5, 1.0, 1.25, 2.25],
    'P13': [1.25, 1.25, 0.5, 1.0, 0.25, 2.0, 1.25],
    'P14': [1.0, 1.5, 0.5, 1.75],
    'P15': [0.75, 0.5, 1.25, 2.5, 2.5],
    'P16': [1.25, 5.0, 1.25, 2.5],
    'P17': [0.75, 3.0, 3.5],
    'P18': [0.75, 1.25, 0.5, 3.75],
    'P19': [2.25, 2.5, 2.0, 3.75],
    'P20': [2.0, 0.75, 3.0],
}

# Common parameters
HOURS_PER_SHIFT = 8
DAYS_PER_WEEK = 5
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY

def calculate_for_shifts(shifts_per_day):
    # Parameters
    HOURS_PER_SHIFT = 8
    DAYS_PER_WEEK = 5
    EFFICIENCY = 0.90
    RELIABILITY = 0.98
    EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY
    
    print(f"\n{'='*60}")
    print(f"SHIFT SCENARIO: {shifts_per_day} shift(s) per day")
    print(f"{'='*60}")
    
    hours_per_week = shifts_per_day * HOURS_PER_SHIFT * DAYS_PER_WEEK
    minutes_per_week_per_machine = hours_per_week * 60 * EFFECTIVE_AVAILABILITY

    print(f"Operating Schedule: {shifts_per_day} shift/day x {HOURS_PER_SHIFT} hours x {DAYS_PER_WEEK} days/week")
    print(f"Available: {hours_per_week} hours/week = {hours_per_week * 60} minutes/week per machine")
    print(f"Effective availability: {EFFECTIVE_AVAILABILITY:.1%}")
    print(f"Effective minutes per machine per week: {minutes_per_week_per_machine:.1f}")

    # Prepare data for CSV
    data = []
    for part in process_operations:
        operations = process_operations[part]
        times = process_times[part]
        demand = weekly_demand[part]
        
        for step_num, (operation, time_min) in enumerate(zip(operations, times), start=1):
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

    # Calculate number of machines per part per operation (dedicated machines per part)
    # First, sum time required per part per operation
    part_operation_totals = df.groupby(['Part', 'Operation'])['Time_Required_Min_Week'].sum().reset_index()
    part_operation_totals['Number_of_Machines'] = np.ceil(part_operation_totals['Time_Required_Min_Week'] / minutes_per_week_per_machine)

    # Merge back to df
    df = df.merge(part_operation_totals[['Part', 'Operation', 'Number_of_Machines']], on=['Part', 'Operation'], how='left')

    # Save to CSV
    csv_filename = f'../results/Part_Step_Process_Capacity_Requirements_{shifts_per_day}_shifts.csv'
    df.to_csv(csv_filename, index=False)

    print(f"CSV generated: {csv_filename}")
    
    # Create summary CSV with machines per part per step
    df['Step_Info'] = df['Operation'] + ': ' + df['Number_of_Machines'].astype(str)
    step_summary_df = df.pivot(index='Part', columns='Step', values='Step_Info').fillna('')
    step_summary_csv_filename = f'../results/Part_Step_Machines_Summary_{shifts_per_day}_shifts.csv'
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
    
    return total_machines_per_operation

# Run for both scenarios
results_1_shift = calculate_for_shifts(1)
results_2_shifts = calculate_for_shifts(2)

print(f"\n{'='*80}")
print("SUMMARY COMPARISON")
print(f"{'='*80}")
comparison = pd.merge(results_1_shift, results_2_shifts, on='Operation', suffixes=('_1_shift', '_2_shifts'))
print("Machine Comparison:")
print(comparison.to_string(index=False))