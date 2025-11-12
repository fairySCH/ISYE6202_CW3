"""
Part-Based Metrics Calculator for Year 2
Computes: Layout Area, Flow Distance, Machine Usage for P1-P20 in Year 2
"""

import pandas as pd
import csv
import math
from collections import defaultdict

# Equipment specifications from Block_Specs.csv
EQUIPMENT_SPECS = {
    'A': {'group': 'ABCD', 'width': 14, 'depth': 14, 'overlap': 2},
    'B': {'group': 'ABCD', 'width': 14, 'depth': 14, 'overlap': 2},
    'C': {'group': 'ABCD', 'width': 14, 'depth': 14, 'overlap': 2},
    'D': {'group': 'ABCD', 'width': 14, 'depth': 14, 'overlap': 2},
    'E': {'group': 'EFG', 'width': 22, 'depth': 15, 'overlap': 0},
    'F': {'group': 'EFG', 'width': 22, 'depth': 15, 'overlap': 0},
    'G': {'group': 'EFG', 'width': 22, 'depth': 15, 'overlap': 0},
    'H': {'group': 'HIJ', 'width': 14, 'depth': 36, 'overlap': 0},
    'I': {'group': 'HIJ', 'width': 14, 'depth': 36, 'overlap': 0},
    'J': {'group': 'HIJ', 'width': 14, 'depth': 36, 'overlap': 0},
    'K': {'group': 'KLM', 'width': 3, 'depth': 6, 'overlap': 1},
    'L': {'group': 'KLM', 'width': 3, 'depth': 6, 'overlap': 1},
    'M': {'group': 'KLM', 'width': 3, 'depth': 6, 'overlap': 1},
}

def calculate_grid_dimensions(machine_count):
    """Calculate optimal grid dimensions (rows x cols) for compact vertical stacking"""
    if machine_count <= 0:
        return 0, 0
    
    # Prefer taller grids (more rows) for vertical stacking
    best_rows = math.ceil(math.sqrt(machine_count * 2))
    best_cols = math.ceil(machine_count / best_rows)
    
    return best_rows, best_cols

def calculate_effective_dimensions(process, machine_count, rows, cols):
    """Calculate effective width and height considering overlaps"""
    spec = EQUIPMENT_SPECS[process]
    unit_w = spec['width']
    unit_h = spec['depth']
    overlap = spec['overlap']
    
    if machine_count == 0:
        return 0, 0
    
    if machine_count == 1:
        return unit_w, unit_h
    
    # Effective dimensions with overlaps
    if overlap > 0:
        eff_width = unit_w * cols - overlap * (cols - 1) if cols > 1 else unit_w
        eff_height = unit_h * rows - overlap * (rows - 1) if rows > 1 else unit_h
    else:
        eff_width = unit_w * cols
        eff_height = unit_h * rows
    
    return eff_width, eff_height

def parse_process_sequence(part_row):
    """Parse process sequence from Part_Step_Machines_Summary"""
    processes = []
    machine_counts = []
    
    for step_col in ['Step_1', 'Step_2', 'Step_3', 'Step_4', 'Step_5', 'Step_6', 'Step_7']:
        if step_col in part_row and pd.notna(part_row[step_col]) and part_row[step_col] != '':
            step_val = str(part_row[step_col]).strip()
            if step_val:
                # Parse "B: 13" format
                parts = step_val.split(':')
                if len(parts) == 2:
                    process = parts[0].strip()
                    count = float(parts[1].strip())
                    processes.append(process)
                    machine_counts.append(int(count))
    
    return processes, machine_counts

def calculate_layout_for_part(part_name, processes, machine_counts):
    """Calculate compact layout area for a part"""
    areas = []
    total_width = 0
    max_height = 0
    
    # Track process occurrences to differentiate duplicates
    process_occurrence = defaultdict(int)
    
    for i, (process, count) in enumerate(zip(processes, machine_counts)):
        process_occurrence[process] += 1
        occurrence = process_occurrence[process]
        
        # Create unique area name
        if occurrence > 1:
            area_name = f"{process}{occurrence}"
        else:
            area_name = process
        
        rows, cols = calculate_grid_dimensions(count)
        eff_w, eff_h = calculate_effective_dimensions(process, count, rows, cols)
        
        area_info = {
            'area_name': area_name,
            'process': process,
            'occurrence': occurrence,
            'machine_count': count,
            'rows': rows,
            'cols': cols,
            'unit_width': EQUIPMENT_SPECS[process]['width'],
            'unit_depth': EQUIPMENT_SPECS[process]['depth'],
            'overlap': EQUIPMENT_SPECS[process]['overlap'],
            'eff_width': eff_w,
            'eff_height': eff_h,
            'group': EQUIPMENT_SPECS[process]['group']
        }
        areas.append(area_info)
        
        total_width += eff_w
        max_height = max(max_height, eff_h)
    
    total_area = total_width * max_height
    
    return areas, total_width, max_height, total_area

def calculate_flow_distance(areas):
    """Calculate center-to-center flow distance through layout"""
    if len(areas) == 0:
        return 0, []
    
    distances = []
    cumulative_x = 0
    
    # Calculate center positions
    centers = []
    for area in areas:
        center_x = cumulative_x + area['eff_width'] / 2
        center_y = area['eff_height'] / 2
        centers.append((center_x, center_y, area['area_name']))
        cumulative_x += area['eff_width']
    
    # Calculate distances between consecutive centers
    total_distance = 0
    for i in range(len(centers) - 1):
        x1, y1, name1 = centers[i]
        x2, y2, name2 = centers[i + 1]
        
        # Euclidean distance
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        total_distance += dist
        
        distances.append({
            'from_area': name1,
            'to_area': name2,
            'from_center': f"({x1:.1f}, {y1:.1f})",
            'to_center': f"({x2:.1f}, {y2:.1f})",
            'distance_ft': round(dist, 2)
        })
    
    return round(total_distance, 2), distances

def count_machines_by_process(processes):
    """Count total machines per process type (including duplicates)"""
    machine_count = defaultdict(int)
    
    # Initialize all processes to 0
    for proc in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
        machine_count[proc] = 0
    
    # Count occurrences
    for process in processes:
        machine_count[process] += 1
    
    return dict(machine_count)

def main():
    print("="*80)
    print("Part-Based Metrics Calculator - Year 2 (All 20 Parts)")
    print("="*80)
    
    # Load data
    base_path = r"c:\Users\jatin\OneDrive\Desktop\Georgia Tech\Coursework\6202 Benoit\Case Work\Case Study 3\ISYE6202_CW3"
    
    print("\nLoading data files...")
    machine_summary_df = pd.read_csv(f"{base_path}\\results\\task4\\part\\capacity\\Part_Step_Machines_Summary_2_shifts.csv")
    demand_df = pd.read_csv(f"{base_path}\\results\\task4\\part\\capacity\\Weekly_Part_Demand.csv")
    
    # Filter for Year 2 only
    machine_summary_year2 = machine_summary_df[machine_summary_df['Year'] == 'Year 2'].copy()
    demand_year2 = demand_df[demand_df['Year'] == 'Year 2'].copy()
    
    print(f"Year 2 parts found: {len(machine_summary_year2)}")
    print(f"Year 2 demand records: {len(demand_year2)}")
    
    # Create output lists
    layout_results = []
    flow_results = []
    machine_usage_results = []
    
    # Detailed report lines
    report_lines = []
    report_lines.append("="*100)
    report_lines.append("COMPREHENSIVE METRICS REPORT - ALL 20 PARTS (YEAR 2)")
    report_lines.append("="*100)
    report_lines.append("")
    
    # Process each part
    all_parts = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10',
                 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20']
    
    total_machines_check = 0
    total_area_all_parts = 0
    
    for part_name in all_parts:
        print(f"\nProcessing {part_name}...")
        
        # Get part data
        part_row = machine_summary_year2[machine_summary_year2['Part'] == part_name].iloc[0]
        demand_row = demand_year2[demand_year2['Part'] == part_name].iloc[0]
        weekly_demand = demand_row['Weekly_Demand']
        
        # Parse process sequence
        processes, machine_counts = parse_process_sequence(part_row)
        total_machines = sum(machine_counts)
        total_machines_check += total_machines
        
        # Calculate layout
        areas, total_width, max_height, total_area = calculate_layout_for_part(
            part_name, processes, machine_counts
        )
        total_area_all_parts += total_area
        
        # Calculate flow distance
        distance_per_unit, distance_details = calculate_flow_distance(areas)
        total_flow = weekly_demand * distance_per_unit
        
        # Count machine usage by process type
        process_usage = count_machines_by_process(processes)
        
        # Store layout results
        layout_results.append({
            'Part': part_name,
            'Process_Sequence': ' → '.join([f"{p}{i+1}" if processes[:i+1].count(p) > 1 else p 
                                            for i, p in enumerate(processes)]),
            'Total_Machines': total_machines,
            'Layout_Width_ft': total_width,
            'Layout_Height_ft': max_height,
            'Total_Area_sqft': total_area,
            'Number_of_Steps': len(processes)
        })
        
        # Store flow results
        flow_results.append({
            'Part': part_name,
            'Weekly_Demand': round(weekly_demand, 2),
            'Distance_Per_Unit_ft': distance_per_unit,
            'Total_Weekly_Flow_unit_ft': round(total_flow, 2),
            'Formula': f"{round(weekly_demand, 2)} × {distance_per_unit} ft"
        })
        
        # Store machine usage
        usage_row = {'Part': part_name}
        usage_row.update(process_usage)
        usage_row['Total_Process_Areas'] = len(processes)
        machine_usage_results.append(usage_row)
        
        # Add to detailed report
        report_lines.append(f"\n{'='*100}")
        report_lines.append(f"{part_name} - DETAILED METRICS")
        report_lines.append(f"{'='*100}")
        report_lines.append(f"\nWeekly Demand: {weekly_demand:,.2f} units")
        report_lines.append(f"Total Machines Required: {total_machines}")
        report_lines.append(f"\nProcess Sequence: {' → '.join(processes)}")
        
        report_lines.append(f"\n{'-'*100}")
        report_lines.append("LAYOUT AREA CALCULATION:")
        report_lines.append(f"{'-'*100}")
        
        for area in areas:
            report_lines.append(f"\nArea: {area['area_name']} (Process {area['process']}, Occurrence {area['occurrence']})")
            report_lines.append(f"  - Machines: {area['machine_count']}")
            report_lines.append(f"  - Grid: {area['rows']} rows × {area['cols']} cols")
            report_lines.append(f"  - Unit Size: {area['unit_width']} ft × {area['unit_depth']} ft")
            report_lines.append(f"  - Overlap: {area['overlap']} ft")
            report_lines.append(f"  - Effective Size: {area['eff_width']} ft × {area['eff_height']} ft")
            report_lines.append(f"  - Group: {area['group']}")
        
        report_lines.append(f"\nTotal Layout Dimensions: {total_width} ft (W) × {max_height} ft (H)")
        report_lines.append(f"Total Area: {total_area:,.0f} sq ft")
        
        report_lines.append(f"\n{'-'*100}")
        report_lines.append("FLOW DISTANCE CALCULATION:")
        report_lines.append(f"{'-'*100}")
        
        if distance_details:
            for detail in distance_details:
                report_lines.append(f"  {detail['from_area']} center {detail['from_center']} → "
                                  f"{detail['to_area']} center {detail['to_center']} = {detail['distance_ft']} ft")
            
            report_lines.append(f"\nTotal Distance per Unit: {distance_per_unit} ft")
            report_lines.append(f"Total Weekly Flow: {weekly_demand:,.2f} units × {distance_per_unit} ft = {total_flow:,.2f} unit-ft/week")
        else:
            report_lines.append("  Single process - no flow distance")
        
        report_lines.append(f"\n{'-'*100}")
        report_lines.append("MACHINE USAGE BY PROCESS:")
        report_lines.append(f"{'-'*100}")
        
        for proc in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']:
            count = process_usage[proc]
            if count > 0:
                report_lines.append(f"  Process {proc}: {count} area(s)")
        
        report_lines.append(f"\nTotal Process Areas: {len(processes)}")
    
    # Add summary section
    report_lines.append(f"\n\n{'='*100}")
    report_lines.append("SUMMARY - ALL 20 PARTS (YEAR 2)")
    report_lines.append(f"{'='*100}")
    report_lines.append(f"\nTotal Machines Across All Parts: {total_machines_check}")
    report_lines.append(f"Total Area Across All Parts: {total_area_all_parts:,.0f} sq ft")
    report_lines.append(f"\nNote: Each part has a dedicated manufacturing area (separate factory floors)")
    report_lines.append(f"Machine counts include duplicates (e.g., if process B appears twice, counted twice)")
    
    # Save results
    output_path = f"{base_path}\\results\\task4\\part\\capacity"
    
    print("\nSaving results...")
    
    # 1. Layout Summary CSV
    layout_df = pd.DataFrame(layout_results)
    layout_file = f"{output_path}\\Part_Based_Year2_All_Parts_Layout_Summary.csv"
    layout_df.to_csv(layout_file, index=False)
    print(f"✓ Saved: {layout_file}")
    
    # 2. Flow Analysis CSV
    flow_df = pd.DataFrame(flow_results)
    flow_file = f"{output_path}\\Part_Based_Year2_All_Parts_Flow_Analysis.csv"
    flow_df.to_csv(flow_file, index=False)
    print(f"✓ Saved: {flow_file}")
    
    # 3. Machine Usage CSV
    machine_df = pd.DataFrame(machine_usage_results)
    machine_file = f"{output_path}\\Part_Based_Year2_All_Parts_Machine_Usage.csv"
    machine_df.to_csv(machine_file, index=False)
    print(f"✓ Saved: {machine_file}")
    
    # 4. Detailed Report TXT
    report_file = f"{output_path}\\Part_Based_Year2_All_Parts_Detailed_Report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"✓ Saved: {report_file}")
    
    print("\n" + "="*80)
    print("COMPUTATION COMPLETE - YEAR 2!")
    print("="*80)
    print(f"\nTotal Parts Processed: 20")
    print(f"Total Machines: {total_machines_check}")
    print(f"Total Area: {total_area_all_parts:,.0f} sq ft")
    print(f"\nOutput Files:")
    print(f"  1. Layout Summary: Part_Based_Year2_All_Parts_Layout_Summary.csv")
    print(f"  2. Flow Analysis: Part_Based_Year2_All_Parts_Flow_Analysis.csv")
    print(f"  3. Machine Usage: Part_Based_Year2_All_Parts_Machine_Usage.csv")
    print(f"  4. Detailed Report: Part_Based_Year2_All_Parts_Detailed_Report.txt")
    print("="*80)

if __name__ == "__main__":
    main()
