"""
Extract Flow Distance Breakdown for All Parts
Creates a CSV with step-by-step distance details
"""

import pandas as pd
import re

# Read the detailed report
report_path = r"c:\Users\jatin\OneDrive\Desktop\Georgia Tech\Coursework\6202 Benoit\Case Work\Case Study 3\ISYE6202_CW3\results\Task3\Part\Capacity\Part_Based_All_Parts_Detailed_Report.txt"

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Store all flow data
flow_breakdown_data = []

current_part = None
step_num = 0
in_flow_section = False

for line in lines:
    # Detect part header
    if '- DETAILED METRICS' in line:
        part_match = re.search(r'(P\d+)', line)
        if part_match:
            current_part = part_match.group(1)
            step_num = 0
            in_flow_section = False
    
    # Detect flow section
    if 'FLOW DISTANCE CALCULATION:' in line:
        in_flow_section = True
        continue
    
    # Exit flow section
    if in_flow_section and 'MACHINE USAGE BY PROCESS:' in line:
        in_flow_section = False
        continue
    
    # Parse flow distance lines
    if in_flow_section and current_part and '→' in line and 'center' in line:
        # Pattern: "B center (19.0, 37.0) → A center (51.0, 25.0) = 34.18 ft"
        match = re.search(r'(\S+)\s+center\s+\(([\d.]+),\s+([\d.]+)\)\s+→\s+(\S+)\s+center\s+\(([\d.]+),\s+([\d.]+)\)\s+=\s+([\d.]+)\s+ft', line)
        if match:
            step_num += 1
            from_area = match.group(1)
            from_x = float(match.group(2))
            from_y = float(match.group(3))
            to_area = match.group(4)
            to_x = float(match.group(5))
            to_y = float(match.group(6))
            distance = float(match.group(7))
            
            flow_breakdown_data.append({
                'Part': current_part,
                'Step': step_num,
                'From_Process_Area': from_area,
                'From_Center_X_ft': from_x,
                'From_Center_Y_ft': from_y,
                'To_Process_Area': to_area,
                'To_Center_X_ft': to_x,
                'To_Center_Y_ft': to_y,
                'Distance_ft': distance
            })
    
    # Parse total distance
    if in_flow_section and current_part and 'Total Distance per Unit:' in line:
        match = re.search(r'Total Distance per Unit:\s+([\d.]+)\s+ft', line)
        if match:
            total_distance = float(match.group(1))
            flow_breakdown_data.append({
                'Part': current_part,
                'Step': 'TOTAL',
                'From_Process_Area': '',
                'From_Center_X_ft': '',
                'From_Center_Y_ft': '',
                'To_Process_Area': '',
                'To_Center_X_ft': '',
                'To_Center_Y_ft': '',
                'Distance_ft': total_distance
            })

# Create DataFrame
df = pd.DataFrame(flow_breakdown_data)

# Save to CSV
output_path = r"c:\Users\jatin\OneDrive\Desktop\Georgia Tech\Coursework\6202 Benoit\Case Work\Case Study 3\ISYE6202_CW3\results\Task3\Part\Capacity\Part_Based_All_Parts_Flow_Distance_Breakdown.csv"
df.to_csv(output_path, index=False)

print("="*80)
print("FLOW DISTANCE BREAKDOWN CSV CREATED")
print("="*80)
print(f"\nOutput file: Part_Based_All_Parts_Flow_Distance_Breakdown.csv")
print(f"\nTotal rows: {len(df)}")

if len(df) > 0:
    total_rows = df[df['Step'] == 'TOTAL']
    print(f"Total parts: {len(total_rows)}")
    
    # Display sample
    print("\n" + "="*80)
    print("SAMPLE DATA - Part P1:")
    print("="*80)
    p1_data = df[df['Part'] == 'P1']
    if len(p1_data) > 0:
        print(p1_data.to_string(index=False))
    
    print("\n" + "="*80)
    print("SAMPLE DATA - Part P17 (KLM - shortest flow):")
    print("="*80)
    p17_data = df[df['Part'] == 'P17']
    if len(p17_data) > 0:
        print(p17_data.to_string(index=False))
    
    print("\n" + "="*80)
    print("SUMMARY BY PART:")
    print("="*80)
    summary = df[df['Step'] == 'TOTAL'][['Part', 'Distance_ft']].sort_values('Distance_ft', ascending=False)
    print(summary.to_string(index=False))

    print("\n" + "="*80)
    print("✓ File saved successfully!")
    print("="*80)
else:
    print("\n⚠️ WARNING: No data extracted. Check the report file format.")
