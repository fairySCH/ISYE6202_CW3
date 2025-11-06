"""
Fractal Organization Design - Main Analysis Script

A fractal organization consists of f identical centers, each capable of producing
all products with approximately 1/f of the total factory capacity.

This script calculates:
1. Equipment requirements per fractal center
2. Equipment requirements for entire factory
3. Comparison with other organization types
4. Operating parameters and capacity utilization

Author: FeMoaSa Design Team
Date: November 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Configuration
BASE_DIR = Path(r"d:\Adarsh GATech Files\6335 Benoit SC1\CW3\ISYE6202_CW3")
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results"

# Operating parameters
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
MINUTES_PER_SHIFT = HOURS_PER_SHIFT * 60  # 480 minutes
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY  # 0.882 or 88.2%

# Processes
PROCESSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']


def load_weekly_product_demand():
    """Load Year +1 weekly product demand"""
    df = pd.read_csv(DATA_DIR / '+1 Year Product Demand.csv', header=None)
    products = ['A1', 'A2', 'A3', 'B1', 'B2']
    weekly_demand_values = df.iloc[12, 2:7].astype(float).tolist()
    return dict(zip(products, weekly_demand_values))


def load_bom():
    """Load Bill of Materials"""
    bom_lines = []
    with open(DATA_DIR / '+1 Year Parts per Product.csv', 'r', encoding='utf-8') as f:
        for line in f:
            bom_lines.append(line.strip().split(','))
    
    bom = {}
    products = ['A1', 'A2', 'A3', 'B1', 'B2']
    
    for i in range(2, 22):
        part_name = bom_lines[i][1].strip()
        bom[part_name] = {}
        for j, product in enumerate(products):
            qty_str = bom_lines[i][2+j].strip()
            if qty_str:
                bom[part_name][product] = int(float(qty_str))
    
    return bom


def calculate_weekly_part_demand(weekly_product_demand, bom):
    """Calculate weekly demand for each part"""
    weekly_part_demand = {}
    
    for i in range(1, 21):
        part = f'P{i}'
        weekly_part_demand[part] = 0.0
    
    for part, products_dict in bom.items():
        for product, qty_per_product in products_dict.items():
            product_weekly_demand = weekly_product_demand.get(product, 0)
            weekly_part_demand[part] += product_weekly_demand * qty_per_product
    
    return weekly_part_demand


def load_process_data():
    """Load process sequences and times for all parts"""
    # Process sequences
    df_specs = pd.read_csv(DATA_DIR / 'Parts Specs.csv', header=None)
    process_sequences = {}
    
    for i in range(11, 31):
        part_name = df_specs.iloc[i, 1]
        if pd.notna(part_name):
            part_name = str(part_name).strip()
            sequence = []
            for j in range(2, 9):
                process = df_specs.iloc[i, j]
                if pd.notna(process) and str(process).strip():
                    sequence.append(str(process).strip())
            process_sequences[part_name] = sequence
    
    # Process times
    df_times = pd.read_csv(DATA_DIR / 'Parts_Step_Time.csv')
    process_times = {}
    
    for _, row in df_times.iterrows():
        part = row['Part']
        times = []
        for step in ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6', 'Step 7']:
            if pd.notna(row[step]):
                times.append(float(row[step]))
            else:
                times.append(0)
        process_times[part] = times
    
    return process_sequences, process_times


def calculate_total_process_workload(weekly_part_demand, process_sequences, process_times):
    """
    Calculate total weekly workload (minutes) for each process type (A-M)
    This is the baseline for the entire factory
    """
    process_workload = {proc: 0.0 for proc in PROCESSES}
    
    for part, weekly_demand in weekly_part_demand.items():
        if part not in process_sequences:
            continue
        
        sequence = process_sequences[part]
        times = process_times[part]
        
        for step_idx, process in enumerate(sequence):
            time_per_unit = times[step_idx]
            total_minutes = weekly_demand * time_per_unit
            process_workload[process] += total_minutes
    
    return process_workload


def calculate_fractal_requirements(num_fractals, process_workload, num_shifts=2):
    """
    Calculate equipment requirements for fractal organization
    
    Parameters:
    - num_fractals: Number of fractal centers (f)
    - process_workload: Total weekly workload per process
    - num_shifts: 1 or 2 shifts per day
    
    Returns:
    - DataFrame with equipment requirements per center and total
    """
    # Available capacity per equipment unit
    capacity_per_equipment = (DAYS_PER_WEEK * num_shifts * MINUTES_PER_SHIFT * 
                             EFFECTIVE_AVAILABILITY)
    
    results = []
    
    for process in PROCESSES:
        total_workload = process_workload[process]
        
        # Workload per fractal center
        workload_per_center = total_workload / num_fractals
        
        # Equipment needed per center (round up)
        equipment_per_center = np.ceil(workload_per_center / capacity_per_equipment)
        
        # Total equipment across all centers
        total_equipment = equipment_per_center * num_fractals
        
        # Utilization per center
        if equipment_per_center > 0:
            utilization_per_center = (workload_per_center / 
                                     (equipment_per_center * capacity_per_equipment))
        else:
            utilization_per_center = 0.0
        
        results.append({
            'Process': process,
            'Total_Workload_Min': total_workload,
            'Workload_per_Center_Min': workload_per_center,
            'Equipment_per_Center': int(equipment_per_center),
            'Total_Equipment': int(total_equipment),
            'Utilization_per_Center': utilization_per_center,
            'Capacity_per_Equipment': capacity_per_equipment
        })
    
    return pd.DataFrame(results)


def generate_fractal_summary(num_fractals, requirements_df):
    """Generate summary report for fractal organization"""
    total_equipment = requirements_df['Total_Equipment'].sum()
    avg_utilization = requirements_df['Utilization_per_Center'].mean()
    
    summary = f"""
{'='*80}
FRACTAL ORGANIZATION ANALYSIS
{'='*80}

Configuration:
- Number of Fractal Centers: {num_fractals}
- Each center handles: {100/num_fractals:.1f}% of total demand
- Operating Schedule: {DAYS_PER_WEEK} days/week, 2 shifts/day, {HOURS_PER_SHIFT} hours/shift
- Effective Availability: {EFFECTIVE_AVAILABILITY*100:.1f}% (Efficiency: {EFFICIENCY*100:.0f}%, Reliability: {RELIABILITY*100:.0f}%)

Summary Statistics:
- Total Equipment Units: {total_equipment}
- Equipment per Center: {total_equipment/num_fractals:.1f} (average)
- Average Utilization per Center: {avg_utilization*100:.1f}%

Equipment Distribution by Process:
"""
    
    for _, row in requirements_df.iterrows():
        summary += f"\n{row['Process']:>3}: {int(row['Equipment_per_Center']):>3} units/center × {num_fractals} centers = {int(row['Total_Equipment']):>3} total ({row['Utilization_per_Center']*100:>5.1f}% utilization)"
    
    summary += f"\n\n{'='*80}\n"
    
    return summary


def compare_fractal_scenarios():
    """Compare different numbers of fractal centers (f = 2, 3, 4, 5)"""
    print("Loading data...")
    weekly_product_demand = load_weekly_product_demand()
    bom = load_bom()
    weekly_part_demand = calculate_weekly_part_demand(weekly_product_demand, bom)
    process_sequences, process_times = load_process_data()
    process_workload = calculate_total_process_workload(weekly_part_demand, 
                                                         process_sequences, 
                                                         process_times)
    
    comparison_results = []
    
    for f in [2, 3, 4, 5]:
        print(f"\nAnalyzing f = {f} fractal centers...")
        requirements = calculate_fractal_requirements(f, process_workload, num_shifts=2)
        
        total_equipment = requirements['Total_Equipment'].sum()
        avg_utilization = requirements['Utilization_per_Center'].mean()
        
        comparison_results.append({
            'Num_Fractals': f,
            'Capacity_per_Center_%': 100/f,
            'Total_Equipment': total_equipment,
            'Avg_Equipment_per_Center': total_equipment/f,
            'Avg_Utilization_%': avg_utilization * 100
        })
        
        # Save detailed requirements
        output_file = RESULTS_DIR / f'Fractal_f{f}_Equipment_Requirements.csv'
        requirements.to_csv(output_file, index=False)
        print(f"  Saved: {output_file.name}")
        
        # Save summary report
        summary = generate_fractal_summary(f, requirements)
        summary_file = RESULTS_DIR / f'Fractal_f{f}_Summary_Report.txt'
        with open(summary_file, 'w') as file:
            file.write(summary)
        print(f"  Saved: {summary_file.name}")
    
    # Create comparison table
    comparison_df = pd.DataFrame(comparison_results)
    comparison_file = RESULTS_DIR / 'Fractal_Comparison_All_Scenarios.csv'
    comparison_df.to_csv(comparison_file, index=False)
    
    print(f"\n{'='*80}")
    print("FRACTAL SCENARIOS COMPARISON")
    print(f"{'='*80}")
    print(comparison_df.to_string(index=False))
    print(f"\nComparison saved: {comparison_file.name}")
    
    return comparison_df


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION DESIGN ANALYSIS")
    print("="*80 + "\n")
    
    # Create results directory if it doesn't exist
    RESULTS_DIR.mkdir(exist_ok=True)
    
    # Run comparison of different fractal scenarios
    comparison_df = compare_fractal_scenarios()
    
    print("\n" + "="*80)
    print("Analysis Complete!")
    print("="*80 + "\n")
    print("Generated files:")
    print("  - Fractal_f2_Equipment_Requirements.csv")
    print("  - Fractal_f2_Summary_Report.txt")
    print("  - Fractal_f3_Equipment_Requirements.csv")
    print("  - Fractal_f3_Summary_Report.txt")
    print("  - Fractal_f4_Equipment_Requirements.csv")
    print("  - Fractal_f4_Summary_Report.txt")
    print("  - Fractal_f5_Equipment_Requirements.csv")
    print("  - Fractal_f5_Summary_Report.txt")
    print("  - Fractal_Comparison_All_Scenarios.csv")
    print("\nNext steps:")
    print("  - Run fractal_flow_matrix.py to generate flow matrices")
    print("  - Run fractal_layout_generator.py to create layout coordinates")


if __name__ == "__main__":
    main()
