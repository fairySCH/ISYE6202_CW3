"""
Quick Reference: Process Requirements Summary for Task 3
Run this to see a clean summary table
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(r"d:\Adarsh GATech Files\6335 Benoit SC1\CW3\ISYE6202_CW3")
RESULTS_DIR = BASE_DIR / "results"

# Load data
equipment_df = pd.read_csv(RESULTS_DIR / "Task3_Parts_Based_Equipment_Requirements.csv")
process_freq_df = pd.read_csv(RESULTS_DIR / "Task3_Process_Frequency.csv")

# Merge into summary table
summary = equipment_df.merge(process_freq_df, on='Process')

# Select and rename columns
summary = summary[['Process', 'Operations_Per_Week', 'Weekly_Hours', 
                   'Equipment_2_Shifts', 'Utilization_2_Shifts']]
summary.columns = ['Process', 'Operations/Week', 'Hours/Week', 
                   'Equipment (2-shift)', 'Utilization (%)']

# Format numbers
summary['Operations/Week'] = summary['Operations/Week'].apply(lambda x: f'{x:,.0f}')
summary['Hours/Week'] = summary['Hours/Week'].apply(lambda x: f'{x:.1f}')
summary['Equipment (2-shift)'] = summary['Equipment (2-shift)'].apply(lambda x: int(x))
summary['Utilization (%)'] = summary['Utilization (%)'].apply(lambda x: f'{x:.1f}%')

# Print formatted table
print("\n" + "="*90)
print("TASK 3: WEEKLY PROCESS REQUIREMENTS FOR PARTS-BASED DESIGN")
print("="*90)
print("\nOperating Schedule: 5 days/week, 2 shifts/day, 8 hours/shift")
print("Efficiency: 90%, Reliability: 98%, Effective Availability: 88.2%")
print("\n" + "-"*90)
print(summary.to_string(index=False))
print("-"*90)

# Summary stats
total_ops = process_freq_df['Operations_Per_Week'].sum()
total_equip = equipment_df['Equipment_2_Shifts'].sum()
total_hours = equipment_df['Weekly_Hours'].sum()
avg_util = equipment_df[equipment_df['Equipment_2_Shifts'] > 0]['Utilization_2_Shifts'].mean()

print(f"\nTOTAL OPERATIONS:       {total_ops:,.0f} per week")
print(f"TOTAL EQUIPMENT:        {int(total_equip)} units")
print(f"TOTAL WORKLOAD:         {total_hours:,.1f} hours/week")
print(f"AVERAGE UTILIZATION:    {avg_util:.1f}%")
print("="*90)

# Process groupings
print("\n" + "="*90)
print("RECOMMENDED PROCESS GROUPINGS FOR PARTS-BASED DESIGN")
print("="*90)

groups = {
    'A-B-C-D Group (Primary)': ['A', 'B', 'C', 'D'],
    'E-F-G Group (Secondary)': ['E', 'F', 'G'],
    'H-I-J Group (Finishing)': ['H', 'I', 'J'],
    'K-L-M Group (Light Ops)': ['K', 'L', 'M']
}

for group_name, processes in groups.items():
    group_data = equipment_df[equipment_df['Process'].isin(processes)]
    group_equip = group_data['Equipment_2_Shifts'].sum()
    group_hours = group_data['Weekly_Hours'].sum()
    group_util = group_data['Utilization_2_Shifts'].mean()
    
    print(f"\n{group_name}:")
    print(f"  Processes:  {', '.join(processes)}")
    print(f"  Equipment:  {int(group_equip)} units")
    print(f"  Hours/Week: {group_hours:,.1f}")
    print(f"  Avg Util:   {group_util:.1f}%")

print("\n" + "="*90)

# Top parts
part_demand_df = pd.read_csv(RESULTS_DIR / "Task3_Weekly_Part_Demand.csv")
top_parts = part_demand_df.nlargest(10, 'Weekly_Demand')

print("\nTOP 10 PARTS BY WEEKLY DEMAND:")
print("-"*50)
for i, (_, row) in enumerate(top_parts.iterrows(), 1):
    print(f"{i:2d}. {row['Part']}: {row['Weekly_Demand']:>10,.0f} units/week")
print("="*90)
