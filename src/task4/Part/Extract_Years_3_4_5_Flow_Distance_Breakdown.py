"""
Extract Flow Distance Breakdown for Years 3, 4, and 5
Creates CSV files with step-by-step distance details for all parts in each year
"""

import pandas as pd
import re
import os

def extract_flow_breakdown(year_num, base_path):
    """Extract flow breakdown for a specific year"""
    
    print(f"\n{'='*80}")
    print(f"Extracting Flow Breakdown - Year {year_num}")
    print(f"{'='*80}")
    
    # Read the detailed report
    year_folder = f"{base_path}\\results\\task4\\part\\Year{year_num}"
    report_path = f"{year_folder}\\Part_Based_Year{year_num}_All_Parts_Detailed_Report.txt"
    
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
    output_path = f"{year_folder}\\Part_Based_Year{year_num}_All_Parts_Flow_Distance_Breakdown.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✓ Saved: Part_Based_Year{year_num}_All_Parts_Flow_Distance_Breakdown.csv")
    print(f"  Total rows: {len(df)}")
    
    if len(df) > 0:
        total_rows = df[df['Step'] == 'TOTAL']
        print(f"  Total parts: {len(total_rows)}")
    
    return len(df)

def main():
    print("="*80)
    print("Flow Distance Breakdown Extraction - Years 3, 4, and 5")
    print("="*80)
    
    base_path = r"c:\Users\jatin\OneDrive\Desktop\Georgia Tech\Coursework\6202 Benoit\Case Work\Case Study 3\ISYE6202_CW3"
    
    # Extract for each year
    for year_num in [3, 4, 5]:
        extract_flow_breakdown(year_num, base_path)
    
    print("\n" + "="*80)
    print("ALL FLOW BREAKDOWNS EXTRACTED!")
    print("="*80)
    print("\nFiles created:")
    print("  Year 3: results/task4/part/Year3/Part_Based_Year3_All_Parts_Flow_Distance_Breakdown.csv")
    print("  Year 4: results/task4/part/Year4/Part_Based_Year4_All_Parts_Flow_Distance_Breakdown.csv")
    print("  Year 5: results/task4/part/Year5/Part_Based_Year5_All_Parts_Flow_Distance_Breakdown.csv")
    print("="*80)

if __name__ == "__main__":
    main()
