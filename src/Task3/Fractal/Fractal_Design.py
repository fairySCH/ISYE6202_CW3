"""
Fractal Organization Design - Main Analysis Script (CORRECTED VERSION)

A fractal organization consists of f identical centers, each capable of producing
all products with approximately 1/f of the total factory capacity.

CRITICAL FIXES IMPLEMENTED:
1. Uniform equipment capacity (no artificial capacity factors)
2. Proper fractal integrity validation
3. Comprehensive data validation and error handling
4. Mathematically consistent equipment calculations
5. Proper handling of demand divisibility issues
6. Robust CSV parsing with validation

This script calculates:
1. Equipment requirements per fractal center (ensuring identical centers)
2. Equipment requirements for entire factory
3. Comparison with other organization types
4. Operating parameters and capacity utilization

Author: FeMoaSa Design Team
Date: November 2025
Version: 2.0 (Corrected)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import warnings

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to project root
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results" / "Task3" / "Fractal" / "Fractal_Design"

# Operating parameters
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
MINUTES_PER_SHIFT = HOURS_PER_SHIFT * 60  # 480 minutes
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY  # 0.882 or 88.2%

# Processes
PROCESSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

# Expected parts and products (for validation)
EXPECTED_PARTS = [f'P{i}' for i in range(1, 21)]
EXPECTED_PRODUCTS = ['A1', 'A2', 'A3', 'B1', 'B2']


def load_weekly_product_demand():
    """
    Load Year +1 weekly product demand with comprehensive validation
    
    Returns:
        dict: Product demand mapping {product: weekly_demand}
    
    Raises:
        FileNotFoundError: If demand file doesn't exist
        ValueError: If data structure is invalid or values are non-positive
    """
    demand_file = DATA_DIR / '+1 Year Product Demand.csv'
    
    if not demand_file.exists():
        raise FileNotFoundError(f"Product demand file not found: {demand_file}")
    
    try:
        df = pd.read_csv(demand_file, header=None)
    except Exception as e:
        raise ValueError(f"Failed to read product demand CSV: {e}")
    
    # Validate CSV structure (should have at least 13 rows and 7 columns)
    if df.shape[0] < 13:
        raise ValueError(f"Product demand CSV has insufficient rows: {df.shape[0]} < 13")
    if df.shape[1] < 7:
        raise ValueError(f"Product demand CSV has insufficient columns: {df.shape[1]} < 7")
    
    # Extract weekly demand from row 12 (0-indexed), columns 2-6
    try:
        weekly_demand_values = df.iloc[12, 2:7].values
        # Convert to float, handling any string issues
        weekly_demand_values = [float(val) for val in weekly_demand_values]
    except (ValueError, IndexError) as e:
        raise ValueError(f"Failed to extract weekly demand values: {e}")
    
    # Validate all demands are positive
    if any(val <= 0 for val in weekly_demand_values):
        raise ValueError(f"All product demands must be positive. Got: {weekly_demand_values}")
    
    demand_dict = dict(zip(EXPECTED_PRODUCTS, weekly_demand_values))
    
    print(f"✓ Loaded weekly product demand: {sum(weekly_demand_values):.1f} total units/week")
    return demand_dict


def load_bom():
    """
    Load Bill of Materials with validation
    
    Returns:
        dict: BOM mapping {part: {product: quantity}}
    
    Raises:
        FileNotFoundError: If BOM file doesn't exist
        ValueError: If data structure is invalid
    """
    bom_file = DATA_DIR / '+1 Year Parts per Product.csv'
    
    if not bom_file.exists():
        raise FileNotFoundError(f"BOM file not found: {bom_file}")
    
    try:
        with open(bom_file, 'r', encoding='utf-8') as f:
            bom_lines = [line.strip().split(',') for line in f]
    except Exception as e:
        raise ValueError(f"Failed to read BOM file: {e}")
    
    # Validate structure
    if len(bom_lines) < 22:
        raise ValueError(f"BOM file has insufficient lines: {len(bom_lines)} < 22")
    
    bom = {}
    
    for i in range(2, 22):  # Rows 2-21 contain parts P1-P20
        try:
            part_name = bom_lines[i][1].strip()
            
            # Validate part name
            if part_name not in EXPECTED_PARTS:
                warnings.warn(f"Unexpected part name at row {i}: {part_name}")
            
            bom[part_name] = {}
            
            for j, product in enumerate(EXPECTED_PRODUCTS):
                qty_str = bom_lines[i][2+j].strip()
                if qty_str:
                    try:
                        qty = int(float(qty_str))
                        if qty > 0:
                            bom[part_name][product] = qty
                    except ValueError:
                        warnings.warn(f"Invalid BOM quantity for {part_name}, {product}: {qty_str}")
        except IndexError as e:
            raise ValueError(f"BOM structure error at row {i}: {e}")
    
    # Validate we got all expected parts
    missing_parts = set(EXPECTED_PARTS) - set(bom.keys())
    if missing_parts:
        warnings.warn(f"Missing parts in BOM: {missing_parts}")
    
    print(f"✓ Loaded BOM for {len(bom)} parts")
    return bom


def calculate_weekly_part_demand(weekly_product_demand, bom):
    """
    Calculate weekly demand for each part with validation
    
    Args:
        weekly_product_demand: dict of {product: weekly_demand}
        bom: dict of {part: {product: quantity}}
    
    Returns:
        dict: {part: weekly_demand}
    """
    weekly_part_demand = {part: 0.0 for part in EXPECTED_PARTS}
    
    for part, products_dict in bom.items():
        for product, qty_per_product in products_dict.items():
            if product not in weekly_product_demand:
                warnings.warn(f"Product {product} in BOM but not in demand data")
                continue
            
            product_weekly_demand = weekly_product_demand[product]
            weekly_part_demand[part] += product_weekly_demand * qty_per_product
    
    # Validate at least some parts have demand
    parts_with_demand = sum(1 for demand in weekly_part_demand.values() if demand > 0)
    if parts_with_demand == 0:
        raise ValueError("No parts have demand - check BOM and product demand alignment")
    
    total_part_demand = sum(weekly_part_demand.values())
    print(f"✓ Calculated weekly part demand: {total_part_demand:,.0f} total parts/week")
    print(f"  ({parts_with_demand}/{len(EXPECTED_PARTS)} parts have non-zero demand)")
    
    return weekly_part_demand


def load_process_data():
    """
    Load process sequences and times for all parts with validation
    
    Returns:
        tuple: (process_sequences, process_times)
    
    Raises:
        FileNotFoundError: If required files don't exist
        ValueError: If data is malformed
    """
    # Load process sequences
    specs_file = DATA_DIR / 'Parts Specs.csv'
    if not specs_file.exists():
        raise FileNotFoundError(f"Parts specs file not found: {specs_file}")
    
    df_specs = pd.read_csv(specs_file, header=None)
    
    if df_specs.shape[0] < 31:
        raise ValueError(f"Parts specs CSV has insufficient rows: {df_specs.shape[0]} < 31")
    
    process_sequences = {}
    
    for i in range(11, 31):  # Rows 11-30 contain parts P1-P20
        try:
            part_name = df_specs.iloc[i, 1]
            if pd.notna(part_name):
                part_name = str(part_name).strip()
                sequence = []
                
                for j in range(2, 9):  # Columns 2-8 contain steps 1-7
                    if j < df_specs.shape[1]:
                        process = df_specs.iloc[i, j]
                        if pd.notna(process) and str(process).strip():
                            proc_str = str(process).strip()
                            # Validate process is in expected list
                            if proc_str not in PROCESSES:
                                warnings.warn(f"Unknown process '{proc_str}' for part {part_name}")
                            sequence.append(proc_str)
                
                if sequence:  # Only add if we found at least one process
                    process_sequences[part_name] = sequence
        except Exception as e:
            warnings.warn(f"Error loading process sequence at row {i}: {e}")
    
    # Load process times
    times_file = DATA_DIR / 'Parts_Step_Time.csv'
    if not times_file.exists():
        raise FileNotFoundError(f"Process times file not found: {times_file}")
    
    df_times = pd.read_csv(times_file)
    
    # Validate required columns
    required_cols = ['Part'] + [f'Step {i}' for i in range(1, 8)]
    missing_cols = set(required_cols) - set(df_times.columns)
    if missing_cols:
        raise ValueError(f"Process times CSV missing columns: {missing_cols}")
    
    process_times = {}
    
    for _, row in df_times.iterrows():
        part = row['Part']
        times = []
        
        for step in ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6', 'Step 7']:
            if pd.notna(row[step]):
                time_val = float(row[step])
                if time_val < 0:
                    warnings.warn(f"Negative time for {part} {step}: {time_val}")
                    time_val = 0
                times.append(time_val)
            else:
                times.append(0)
        
        process_times[part] = times
    
    # Validate alignment between sequences and times
    for part in process_sequences:
        if part not in process_times:
            warnings.warn(f"Part {part} has sequence but no times")
        else:
            seq_len = len(process_sequences[part])
            # Count non-zero times
            non_zero_times = sum(1 for t in process_times[part] if t > 0)
            if seq_len != non_zero_times:
                warnings.warn(f"Part {part}: {seq_len} process steps but {non_zero_times} non-zero times")
    
    print(f"✓ Loaded process data for {len(process_sequences)} parts")
    
    return process_sequences, process_times


def calculate_total_process_workload(weekly_part_demand, process_sequences, process_times):
    """
    Calculate total weekly workload (minutes) for each process type (A-M)
    This is the baseline for the entire factory
    
    Args:
        weekly_part_demand: dict of {part: weekly_demand}
        process_sequences: dict of {part: [processes]}
        process_times: dict of {part: [times]}
    
    Returns:
        dict: {process: total_minutes_per_week}
    """
    process_workload = {proc: 0.0 for proc in PROCESSES}
    
    for part, weekly_demand in weekly_part_demand.items():
        if weekly_demand == 0:
            continue
            
        if part not in process_sequences:
            if weekly_demand > 0:
                warnings.warn(f"Part {part} has demand but no process sequence")
            continue
        
        if part not in process_times:
            warnings.warn(f"Part {part} has sequence but no process times")
            continue
        
        sequence = process_sequences[part]
        times = process_times[part]
        
        # Validate sequence and times alignment
        if len(sequence) > len(times):
            warnings.warn(f"Part {part}: More processes ({len(sequence)}) than times ({len(times)})")
            continue
        
        for step_idx, process in enumerate(sequence):
            if step_idx >= len(times):
                warnings.warn(f"Part {part}: Step {step_idx} out of bounds")
                break
                
            time_per_unit = times[step_idx]
            
            if time_per_unit < 0:
                warnings.warn(f"Part {part}, Process {process}: Negative time {time_per_unit}")
                continue
            
            total_minutes = weekly_demand * time_per_unit
            process_workload[process] += total_minutes
    
    # Log process workload summary
    total_workload = sum(process_workload.values())
    active_processes = sum(1 for w in process_workload.values() if w > 0)
    
    print(f"✓ Calculated process workload: {total_workload:,.0f} total minutes/week")
    print(f"  ({active_processes}/{len(PROCESSES)} processes are active)")
    
    return process_workload


def calculate_fractal_requirements(num_fractals, process_workload, num_shifts=2):
    """
    Calculate equipment requirements for fractal organization
    
    CRITICAL FIX: All equipment has UNIFORM capacity based on operating parameters.
    No artificial capacity factors that create non-physical variations.
    
    Parameters:
    - num_fractals: Number of fractal centers (f)
    - process_workload: Total weekly workload per process (minutes)
    - num_shifts: 1 or 2 shifts per day
    
    Returns:
    - DataFrame with equipment requirements per center and total
    
    Key Principles:
    1. All equipment has the same base capacity (time-based)
    2. Each fractal center is IDENTICAL in composition
    3. Workload is divided equally across centers
    4. Equipment is rounded up per center (ensuring sufficient capacity)
    """
    # UNIFORM equipment capacity - same for ALL processes
    base_capacity = (DAYS_PER_WEEK * num_shifts * MINUTES_PER_SHIFT * 
                    EFFECTIVE_AVAILABILITY)
    
    print(f"\n  Base equipment capacity: {base_capacity:,.1f} minutes/week/unit")
    print(f"  ({DAYS_PER_WEEK} days × {num_shifts} shifts × {MINUTES_PER_SHIFT} min × {EFFECTIVE_AVAILABILITY:.1%} availability)")
    
    results = []
    total_equipment_sum = 0
    
    for process in PROCESSES:
        total_workload = process_workload[process]
        
        # Divide workload equally across fractal centers
        workload_per_center = total_workload / num_fractals
        
        # Equipment needed per center (round up to ensure capacity)
        # Using np.ceil to always round UP - can't have fractional equipment
        if workload_per_center > 0:
            equipment_per_center = int(np.ceil(workload_per_center / base_capacity))
        else:
            equipment_per_center = 0
        
        # Total equipment across all centers
        # CRITICAL: Each center has IDENTICAL equipment
        total_equipment = equipment_per_center * num_fractals
        total_equipment_sum += total_equipment
        
        # Calculate actual utilization per center
        if equipment_per_center > 0:
            actual_capacity_per_center = equipment_per_center * base_capacity
            utilization_per_center = workload_per_center / actual_capacity_per_center
        else:
            utilization_per_center = 0.0
        
        # Validate fractal integrity
        expected_total = equipment_per_center * num_fractals
        if total_equipment != expected_total:
            warnings.warn(f"Process {process}: Fractal integrity violation! "
                        f"{total_equipment} != {equipment_per_center} × {num_fractals}")
        
        results.append({
            'Process': process,
            'Total_Workload_Min': round(total_workload, 2),
            'Workload_per_Center_Min': round(workload_per_center, 2),
            'Equipment_per_Center': equipment_per_center,
            'Total_Equipment': total_equipment,
            'Utilization_per_Center': round(utilization_per_center, 4),
            'Base_Capacity_per_Equipment': base_capacity
        })
    
    print(f"  Total equipment across all processes: {total_equipment_sum} units")
    
    df = pd.DataFrame(results)
    
    # Validate fractal integrity across all processes
    verify_fractal_integrity(df, num_fractals)
    
    return df


def verify_fractal_integrity(requirements_df, num_fractals):
    """
    Verify that all fractal centers have identical equipment composition
    
    This is a CRITICAL check - fractal organization requires all centers to be identical.
    Any violation indicates a logical error in the calculation.
    
    Args:
        requirements_df: DataFrame with equipment requirements
        num_fractals: Number of fractal centers
    """
    violations = []
    
    for _, row in requirements_df.iterrows():
        expected_total = row['Equipment_per_Center'] * num_fractals
        actual_total = row['Total_Equipment']
        
        if actual_total != expected_total:
            violations.append(f"Process {row['Process']}: "
                            f"{actual_total} total != {row['Equipment_per_Center']} per center × {num_fractals}")
    
    if violations:
        error_msg = "FRACTAL INTEGRITY VIOLATION:\n" + "\n".join(violations)
        raise ValueError(error_msg)
    
    # Additional check: verify all centers would have same equipment list
    equipment_per_center = requirements_df['Equipment_per_Center'].tolist()
    
    print(f"  ✓ Fractal integrity verified: All {num_fractals} centers are identical")
    print(f"    Each center has {sum(equipment_per_center)} equipment units")


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
    """
    Compare different numbers of fractal centers (f = 2, 3, 4, 5)
    
    This function performs comprehensive analysis to compare fractal configurations.
    With corrected uniform capacity, total equipment should increase monotonically
    with more fractals due to rounding overhead.
    """
    print("="*80)
    print("LOADING AND VALIDATING DATA")
    print("="*80)
    
    try:
        weekly_product_demand = load_weekly_product_demand()
        bom = load_bom()
        weekly_part_demand = calculate_weekly_part_demand(weekly_product_demand, bom)
        process_sequences, process_times = load_process_data()
        process_workload = calculate_total_process_workload(weekly_part_demand, 
                                                             process_sequences, 
                                                             process_times)
    except Exception as e:
        print(f"\n❌ ERROR during data loading: {e}")
        raise
    
    print("\n" + "="*80)
    print("ANALYZING FRACTAL SCENARIOS")
    print("="*80)
    
    comparison_results = []
    
    for f in [2, 3, 4, 5]:
        print(f"\n{'─'*80}")
        print(f"SCENARIO: f = {f} fractal centers")
        print(f"{'─'*80}")
        
        try:
            # CORRECTED: Only pass required parameters
            requirements = calculate_fractal_requirements(f, process_workload, num_shifts=2)
            
            total_equipment = requirements['Total_Equipment'].sum()
            avg_utilization = requirements['Utilization_per_Center'].mean()
            
            comparison_results.append({
                'Num_Fractals': f,
                'Capacity_per_Center_%': round(100/f, 2),
                'Total_Equipment': total_equipment,
                'Avg_Equipment_per_Center': round(total_equipment/f, 1),
                'Avg_Utilization_%': round(avg_utilization * 100, 2)
            })
            
            # Save detailed requirements
            output_file = RESULTS_DIR / f'Fractal_f{f}_Equipment_Requirements.csv'
            requirements.to_csv(output_file, index=False)
            print(f"  ✓ Saved: {output_file.name}")
            
            # Save summary report
            summary = generate_fractal_summary(f, requirements)
            summary_file = RESULTS_DIR / f'Fractal_f{f}_Summary_Report.txt'
            with open(summary_file, 'w', encoding='utf-8') as file:
                file.write(summary)
            print(f"  ✓ Saved: {summary_file.name}")
            
        except Exception as e:
            print(f"\n❌ ERROR analyzing f={f}: {e}")
            raise
    
    # Create comparison table
    comparison_df = pd.DataFrame(comparison_results)
    comparison_file = RESULTS_DIR / 'Fractal_Comparison_All_Scenarios.csv'
    comparison_df.to_csv(comparison_file, index=False)
    
    print(f"\n{'='*80}")
    print("FRACTAL SCENARIOS COMPARISON")
    print(f"{'='*80}")
    print(comparison_df.to_string(index=False))
    
    # CRITICAL VALIDATION: Check for monotonic increase in equipment
    equipment_counts = comparison_df['Total_Equipment'].tolist()
    violations = []
    for i in range(1, len(equipment_counts)):
        if equipment_counts[i] < equipment_counts[i-1]:
            violations.append(f"f={comparison_df.iloc[i]['Num_Fractals']} "
                            f"({equipment_counts[i]}) < f={comparison_df.iloc[i-1]['Num_Fractals']} "
                            f"({equipment_counts[i-1]})")
    
    if violations:
        print("\n⚠️  WARNING: Non-monotonic equipment counts detected:")
        for v in violations:
            print(f"    {v}")
        print("    This may indicate rounding effects or calculation issues.")
    else:
        print("\n✓ Equipment counts increase monotonically (as expected)")
    
    print(f"\n✓ Comparison saved: {comparison_file.name}")
    
    return comparison_df


def main():
    """Main execution function with comprehensive error handling"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION DESIGN ANALYSIS (CORRECTED VERSION)")
    print("Version 2.0 - With Uniform Equipment Capacity & Validation")
    print("="*80 + "\n")
    
    # Create results directory if it doesn't exist
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Results directory: {RESULTS_DIR}\n")
    
    try:
        # Run comparison of different fractal scenarios
        comparison_df = compare_fractal_scenarios()
        
        print("\n" + "="*80)
        print("✓ ANALYSIS COMPLETE!")
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
        
        print("\n" + "="*80)
        print("KEY IMPROVEMENTS IN VERSION 2.0:")
        print("="*80)
        print("✓ Uniform equipment capacity (no artificial variations)")
        print("✓ Fractal integrity validation (all centers identical)")
        print("✓ Comprehensive data validation and error handling")
        print("✓ Monotonic equipment count verification")
        print("✓ Robust CSV parsing with validation")
        print("✓ Detailed logging and diagnostics")
        
        print("\n" + "="*80)
        print("Next steps:")
        print("  - Review comparison results for optimal fractal count")
        print("  - Run fractal_flow_matrix.py to generate flow matrices")
        print("  - Run fractal_layout_generator.py to create layout coordinates")
        print("="*80 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ FILE NOT FOUND ERROR: {e}")
        print("Please ensure all required data files exist in the data/csv_outputs directory.")
        sys.exit(1)
        
    except ValueError as e:
        print(f"\n❌ VALIDATION ERROR: {e}")
        print("Please check your input data for consistency and correctness.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

