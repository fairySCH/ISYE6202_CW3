"""
Update Utilization Matrix with Optimized Equipment Counts
"""

import pandas as pd
import numpy as np

# Read optimized equipment counts
optimized_df = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/OPTIMIZED_Equipment_Requirements.csv'
)

# Read demand data
demand_df = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/Part_Based_Weekly_Part_Demand.csv'
)

# Read process-part matrix
process_part_matrix = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Part_Based_Process_Part_Matrix.csv',
    index_col=0
)

# Read parts step time data
parts_step_time_raw = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/data/csv_outputs/Parts_Step_Time.csv'
)

# Manual mapping of processes to steps (based on equipment specifications)
process_to_steps = {
    'A': [1],
    'B': [2],
    'C': [3],
    'D': [4],
    'E': [5],
    'F': [6],
    'G': [7],
    'H': [4],  # Alternative for step 4
    'I': [5],  # Alternative for step 5
    'J': [4],  # Alternative for step 4
    'K': [5],  # Alternative for step 5
    'L': [6],  # Alternative for step 6
    'M': [7]   # Alternative for step 7
}

print("=" * 80)
print("UPDATING UTILIZATION MATRIX WITH OPTIMIZED EQUIPMENT")
print("=" * 80)
print()

# Create optimized equipment lookup
optimized_counts = {}
for idx, row in optimized_df.iterrows():
    if row['Process'] != 'TOTAL':
        optimized_counts[row['Process']] = row['Optimized_Equipment']

print("Optimized Equipment Counts:")
for process, count in optimized_counts.items():
    print(f"  {process}: {count} machines")
print()

# Initialize utilization matrix
processes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
parts = [f'P{i}' for i in range(1, 21)]

optimized_utilization = pd.DataFrame(0.0, index=parts, columns=processes)

# Calculate utilization for each part-process combination
for part in parts:
    part_row = demand_df[demand_df['Part'] == part]
    if len(part_row) == 0:
        continue
    
    weekly_demand = part_row['Weekly_Demand'].values[0]
    
    # Get the time data for this part
    part_time_row = parts_step_time_raw[parts_step_time_raw['Part'] == part]
    if len(part_time_row) == 0:
        continue
    
    for process in processes:
        # Check if this part uses this process
        if process not in process_part_matrix.columns:
            continue
        
        uses_process = process_part_matrix.loc[part, process]
        if uses_process == 0:
            continue
        
        # Get the steps for this process
        if process not in process_to_steps:
            continue
        
        steps = process_to_steps[process]
        
        # Calculate total time for this part on this process
        total_time = 0
        for step_num in steps:
            step_col = f'Step {step_num}'
            if step_col in part_time_row.columns:
                step_time = part_time_row[step_col].values[0]
                if pd.notna(step_time):
                    total_time += step_time
        
        if total_time > 0:
            # Calculate weekly minutes needed
            weekly_minutes = weekly_demand * total_time
            
            # Get optimized equipment count
            num_machines = optimized_counts[process]
            
            # Available minutes per week (2 shifts, 8 hrs/shift, 5 days, 60 min/hr)
            available_minutes = num_machines * 2 * 8 * 5 * 60
            
            # Calculate utilization percentage
            utilization_pct = (weekly_minutes / available_minutes) * 100
            optimized_utilization.at[part, process] = round(utilization_pct, 1)

# Reset index to make Part a column
optimized_utilization.reset_index(inplace=True)
optimized_utilization.rename(columns={'index': 'Part'}, inplace=True)

# Save updated utilization matrix
output_path = 'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/OPTIMIZED_Utilization_Matrix_2_shifts.csv'
optimized_utilization.to_csv(output_path, index=False)

print(f"✓ Saved: {output_path}")
print()

# Display the updated matrix
print("=" * 80)
print("OPTIMIZED UTILIZATION MATRIX (2 Shifts):")
print("-" * 80)
print(optimized_utilization.to_string(index=False))
print()

# Calculate average utilization per process
print("=" * 80)
print("AVERAGE UTILIZATION BY PROCESS:")
print("-" * 80)

for process in processes:
    # Get all non-zero utilization values for this process
    util_values = optimized_utilization[process].values
    non_zero = [v for v in util_values if v > 0]
    
    if len(non_zero) > 0:
        avg_util = np.mean(non_zero)
        max_util = np.max(non_zero)
        min_util = np.min(non_zero)
        num_parts = len(non_zero)
        
        # Get equipment count
        equip_count = optimized_counts[process]
        
        # Calculate overall utilization (weighted by demand)
        total_minutes_needed = 0
        for part in parts:
            part_util = optimized_utilization[optimized_utilization['Part'] == part][process].values[0]
            if part_util > 0:
                # Calculate minutes from utilization
                available_minutes = equip_count * 2 * 8 * 5 * 60
                minutes_needed = (part_util / 100) * available_minutes
                total_minutes_needed += minutes_needed
        
        total_available = equip_count * 2 * 8 * 5 * 60
        overall_util = (total_minutes_needed / total_available) * 100
        
        print(f"{process:8s}: {equip_count:3d} machines | Overall: {overall_util:5.1f}% | Avg: {avg_util:5.1f}% | Range: {min_util:5.1f}%-{max_util:5.1f}% | {num_parts} parts")

print()

# Compare with original
print("=" * 80)
print("COMPARISON: ORIGINAL vs OPTIMIZED")
print("-" * 80)

original_df = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/Part_Based_Equipment_Requirements.csv'
)

print(f"{'Process':<8} {'Original':<9} {'Optimized':<10} {'Change':<8} {'Orig Util%':<11} {'Opt Util%':<10} {'Change'}")
print("-" * 80)

for idx, row in optimized_df.iterrows():
    if row['Process'] != 'TOTAL':
        process = row['Process']
        orig_row = original_df[original_df['Process'] == process]
        
        orig_equip = int(orig_row['Equipment_2_Shifts'].values[0])
        opt_equip = int(row['Optimized_Equipment'])
        equip_change = opt_equip - orig_equip
        
        orig_util = orig_row['Utilization_2_Shifts'].values[0]
        opt_util = row['Optimized_Utilization_%']
        util_change = opt_util - orig_util
        
        print(f"{process:<8} {orig_equip:3d} → {opt_equip:3d}  {equip_change:+3d}      {orig_util:5.1f}% → {opt_util:5.1f}%  {util_change:+5.1f}%")

print()
print("=" * 80)
print("OPTIMIZATION COMPLETE!")
print("=" * 80)
