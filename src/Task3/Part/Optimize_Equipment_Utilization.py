"""
Optimize Part-Based Equipment Requirements for Higher Utilization
Goal: Target 85-95% utilization to match P1's efficiency
"""

import pandas as pd
import numpy as np

# Read current equipment requirements
equipment_df = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/Part_Based_Equipment_Requirements.csv'
)

# Read utilization matrix to understand per-part loading
utilization_df = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/Part_Operation_Utilization_Matrix_2_shifts.csv'
)

print("=" * 80)
print("EQUIPMENT UTILIZATION OPTIMIZATION ANALYSIS")
print("=" * 80)
print()

# Current state
print("CURRENT STATE (2 Shifts):")
print("-" * 80)
for idx, row in equipment_df.iterrows():
    if row['Process'] != 'TOTAL':
        process = row['Process']
        current_equip = int(row['Equipment_2_Shifts'])
        current_util = row['Utilization_2_Shifts']
        weekly_hours = row['Weekly_Hours']
        
        print(f"{process:8s}: {current_equip:3d} machines @ {current_util:5.1f}% util | {weekly_hours:8.1f} hrs/week")

print()
print("=" * 80)

# Define target utilization range
TARGET_MIN = 85.0  # Minimum acceptable utilization
TARGET_MAX = 95.0  # Maximum to leave some buffer

# Calculate optimized equipment counts
optimized_results = []

print("OPTIMIZATION RECOMMENDATIONS:")
print("-" * 80)
print()

for idx, row in equipment_df.iterrows():
    if row['Process'] == 'TOTAL':
        continue
    
    process = row['Process']
    weekly_hours = row['Weekly_Hours']
    current_equip = int(row['Equipment_2_Shifts'])
    current_util = row['Utilization_2_Shifts']
    
    # Available hours per machine per week (2 shifts, 8 hrs/shift, 5 days)
    hours_per_machine = 2 * 8 * 5  # 80 hours per week
    
    # Calculate optimal equipment count for target utilization
    # Formula: Equipment = Weekly_Hours / (Target_Util * Hours_Per_Machine)
    
    # Try to achieve 90% utilization (middle of target range)
    optimal_for_90 = weekly_hours / (0.90 * hours_per_machine)
    optimal_equip = int(np.ceil(optimal_for_90))
    
    # Calculate resulting utilization
    new_util = (weekly_hours / (optimal_equip * hours_per_machine)) * 100
    
    # If utilization is too high, add one more machine
    if new_util > TARGET_MAX:
        optimal_equip += 1
        new_util = (weekly_hours / (optimal_equip * hours_per_machine)) * 100
    
    # Calculate savings
    equipment_reduction = current_equip - optimal_equip
    util_increase = new_util - current_util
    
    optimized_results.append({
        'Process': process,
        'Current_Equipment': current_equip,
        'Current_Utilization_%': round(current_util, 1),
        'Optimized_Equipment': optimal_equip,
        'Optimized_Utilization_%': round(new_util, 1),
        'Equipment_Reduction': equipment_reduction,
        'Utilization_Increase_%': round(util_increase, 1),
        'Weekly_Hours': round(weekly_hours, 1)
    })
    
    # Print recommendations
    if equipment_reduction > 0:
        print(f"✓ {process:8s}: REDUCE {current_equip} → {optimal_equip} machines ({equipment_reduction:+d})")
        print(f"           Utilization: {current_util:5.1f}% → {new_util:5.1f}% ({util_increase:+5.1f}%)")
        print()
    elif equipment_reduction < 0:
        print(f"⚠ {process:8s}: INCREASE {current_equip} → {optimal_equip} machines ({equipment_reduction:+d})")
        print(f"           Utilization: {current_util:5.1f}% → {new_util:5.1f}% ({util_increase:+5.1f}%)")
        print()
    else:
        print(f"  {process:8s}: KEEP at {current_equip} machines (already optimal @ {current_util:5.1f}%)")
        print()

# Create summary DataFrame
optimized_df = pd.DataFrame(optimized_results)

# Calculate totals
total_current = optimized_df['Current_Equipment'].sum()
total_optimized = optimized_df['Optimized_Equipment'].sum()
total_reduction = total_current - total_optimized
total_weekly_hours = optimized_df['Weekly_Hours'].sum()

avg_current_util = (total_weekly_hours / (total_current * 80)) * 100
avg_optimized_util = (total_weekly_hours / (total_optimized * 80)) * 100

# Add totals row
totals = {
    'Process': 'TOTAL',
    'Current_Equipment': total_current,
    'Current_Utilization_%': round(avg_current_util, 1),
    'Optimized_Equipment': total_optimized,
    'Optimized_Utilization_%': round(avg_optimized_util, 1),
    'Equipment_Reduction': total_reduction,
    'Utilization_Increase_%': round(avg_optimized_util - avg_current_util, 1),
    'Weekly_Hours': round(total_weekly_hours, 1)
}

optimized_df = pd.concat([optimized_df, pd.DataFrame([totals])], ignore_index=True)

print()
print("=" * 80)
print("SUMMARY:")
print("-" * 80)
print(f"Total Equipment Reduction: {total_reduction} machines ({total_current} → {total_optimized})")
print(f"Overall Utilization: {avg_current_util:.1f}% → {avg_optimized_util:.1f}% ({avg_optimized_util - avg_current_util:+.1f}%)")
print()

# Estimate cost savings (using typical equipment costs)
equipment_costs = {
    'A': 400000, 'B': 400000, 'C': 400000, 'D': 400000,
    'E': 650000, 'F': 650000, 'G': 650000,
    'H': 800000, 'I': 800000, 'J': 800000,
    'K': 1000000, 'L': 1000000, 'M': 1000000
}

capital_savings = 0
for idx, row in optimized_df.iterrows():
    if row['Process'] != 'TOTAL' and row['Equipment_Reduction'] > 0:
        process = row['Process']
        reduction = row['Equipment_Reduction']
        cost_per_machine = equipment_costs[process]
        savings = reduction * cost_per_machine
        capital_savings += savings
        print(f"{process}: {reduction} × ${cost_per_machine:,} = ${savings:,}")

print()
print(f"TOTAL CAPITAL SAVINGS: ${capital_savings:,}")
print()

# Annual operating savings (assume $150/hr labor + overhead per machine)
hourly_operating_cost = 150  # $/hr
annual_hours = 2 * 8 * 5 * 52  # 2 shifts, 8 hrs, 5 days, 52 weeks = 4,160 hrs/year
annual_savings_per_machine = hourly_operating_cost * annual_hours

annual_operating_savings = total_reduction * annual_savings_per_machine
print(f"ANNUAL OPERATING SAVINGS: ${annual_operating_savings:,}")
print(f"  ({total_reduction} machines × ${annual_savings_per_machine:,}/machine/year)")
print()

# Save optimized results
output_path = 'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/OPTIMIZED_Equipment_Requirements.csv'
optimized_df.to_csv(output_path, index=False)
print(f"✓ Saved: {output_path}")
print()

# Create detailed comparison report
print("=" * 80)
print("DETAILED COMPARISON TABLE:")
print("-" * 80)
print()
print(optimized_df.to_string(index=False))
print()
print("=" * 80)

# Recalculate per-part utilization with optimized equipment
print()
print("RECALCULATING PER-PART UTILIZATION WITH OPTIMIZED EQUIPMENT...")
print()

# Create mapping of optimized equipment counts
optimized_counts = {}
for idx, row in optimized_df.iterrows():
    if row['Process'] != 'TOTAL':
        optimized_counts[row['Process']] = row['Optimized_Equipment']

# Read the original part-process time data
parts_step_time = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/data/csv_outputs/Parts_Step_Time.csv'
)

# Read demand data
demand_df = pd.read_csv(
    'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/Part_Based_Weekly_Part_Demand.csv'
)

# Calculate optimized utilization matrix
processes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
parts = [f'P{i}' for i in range(1, 21)]

optimized_utilization = pd.DataFrame(index=parts, columns=processes)
optimized_utilization.fillna(0.0, inplace=True)

for part in parts:
    weekly_demand = demand_df[demand_df['Part'] == part]['Weekly_Demand'].values[0]
    
    for process in processes:
        # Get process time for this part-process combination
        time_entry = parts_step_time[
            (parts_step_time['Part'] == part) & 
            (parts_step_time['Process'] == process)
        ]
        
        if len(time_entry) > 0:
            process_time = time_entry['Time_minutes'].values[0]
            weekly_minutes = weekly_demand * process_time
            
            # Get optimized equipment count
            num_machines = optimized_counts[process]
            available_minutes = num_machines * 80 * 60  # machines × 80 hrs/week × 60 min/hr
            
            utilization_pct = (weekly_minutes / available_minutes) * 100
            optimized_utilization.at[part, process] = round(utilization_pct, 1)

# Reset index to make Part a column
optimized_utilization.reset_index(inplace=True)
optimized_utilization.rename(columns={'index': 'Part'}, inplace=True)

# Save optimized utilization matrix
util_output_path = 'c:/Users/jatin/OneDrive/Desktop/Georgia Tech/Coursework/6202 Benoit/Case Work/Case Study 3/ISYE6202_CW3/results/Task3/Part/Capacity/OPTIMIZED_Utilization_Matrix_2_shifts.csv'
optimized_utilization.to_csv(util_output_path, index=False)
print(f"✓ Saved: {util_output_path}")
print()

print("=" * 80)
print("OPTIMIZATION COMPLETE!")
print("=" * 80)
