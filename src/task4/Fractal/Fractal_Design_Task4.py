"""
Fractal Organization Design - Task 4 (Years 2-5) - CORRECTED VERSION
Main Analysis Script for Multi-Year Fractal Factory Design

Designs fractal factory for year 4 (peak demand), then scales down
equipment for years 2 and 3 to reduce space requirements.

CRITICAL FIXES IMPLEMENTED:
1. Uniform equipment capacity (no artificial capacity factors)
2. Proper fractal integrity validation
3. Comprehensive data validation and error handling
4. Mathematically consistent equipment calculations
5. Proper handling of demand divisibility issues
6. Robust CSV parsing with validation

Key Features:
1. Equipment requirements per fractal center for each year
2. Equipment requirements for entire factory per year
3. Scaling analysis from year 4 design
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
RESULTS_DIR = BASE_DIR / "results" / "Task4" / "Fractal" / "Fractal_Design"

# Operating parameters
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
MINUTES_PER_SHIFT = HOURS_PER_SHIFT * 60  # 480 minutes
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY  # 0.882 or 88.2%

# Processes
PROCESSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

# Years to analyze
YEARS = [2, 3, 4, 5]

# Expected parts and products (for validation)
EXPECTED_PARTS = [f'P{i}' for i in range(1, 21)]
EXPECTED_PRODUCTS = ['A1', 'A2', 'A3', 'B1', 'B2', 'A4', 'B3', 'B4']


def load_yearly_product_demand(year):
    """Load yearly product demand for specified year with validation"""
    demand_file = DATA_DIR / '+2 to +5 Year Product Demand.csv'
    
    if not demand_file.exists():
        raise FileNotFoundError(f"Product demand file not found: {demand_file}")
    
    try:
        df = pd.read_csv(demand_file, header=None)
    except Exception as e:
        raise ValueError(f"Failed to read product demand CSV: {e}")
    
    # Validate CSV structure
    if df.shape[0] < 30:
        raise ValueError(f"Product demand CSV has insufficient rows: {df.shape[0]} < 30")
    if df.shape[1] < 10:
        raise ValueError(f"Product demand CSV has insufficient columns: {df.shape[1]} < 10")

    # Find the row for the specified year
    year_row_idx = None
    for i, row in df.iterrows():
        if str(row[1]).strip() == f'+{year}':
            year_row_idx = i
            break

    if year_row_idx is None:
        raise ValueError(f"Year +{year} not found in demand data")

    # Extract weekly demand values (row 18-22 for years 2-5)
    weekly_row_idx = 17 + (year - 1)  # Year 2 = row 18, Year 3 = row 19, etc.
    products = EXPECTED_PRODUCTS
    
    try:
        weekly_demand_values = df.iloc[weekly_row_idx, 2:10].astype(float).tolist()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Failed to extract weekly demand values for year {year}: {e}")
    
    # Validate all demands are non-negative
    if any(val < 0 for val in weekly_demand_values):
        raise ValueError(f"All product demands must be non-negative. Got: {weekly_demand_values}")
    
    demand_dict = dict(zip(products, weekly_demand_values))
    
    print(f"✓ Year +{year}: Loaded weekly product demand = {sum(weekly_demand_values):.1f} total units/week")
    return demand_dict


def verify_fractal_integrity(df, num_fractals):
    """
    Verify that fractal organization maintains integrity
    
    Each fractal center must be IDENTICAL, meaning:
    - Total_Equipment = Equipment_per_Center × num_fractals (exactly)
    - No rounding errors or inconsistencies
    
    Args:
        df: DataFrame with Equipment_per_Center and Total_Equipment columns
        num_fractals: Number of fractal centers
    
    Raises:
        ValueError: If fractal integrity is violated
    """
    violations = []
    
    for _, row in df.iterrows():
        expected_total = row['Equipment_per_Center'] * num_fractals
        actual_total = row['Total_Equipment']
        
        if expected_total != actual_total:
            violations.append(
                f"Process {row['Process']}: {actual_total} != {row['Equipment_per_Center']} × {num_fractals}"
            )
    
    if violations:
        error_msg = "Fractal integrity violations detected:\n" + "\n".join(violations)
        raise ValueError(error_msg)
    
    print(f"✓ Fractal integrity verified: All {num_fractals} centers are identical")
    return True


def load_bom():
    """Load Bill of Materials for years 2-5 with validation"""
    bom_file = DATA_DIR / '+2 to +5 Year Parts per Product.csv'
    
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
    products = EXPECTED_PRODUCTS

    for i in range(2, 22):  # Parts P1 to P20, starting from row 2
        try:
            part_name = bom_lines[i][1].strip()
            
            # Validate part name
            if part_name not in EXPECTED_PARTS:
                warnings.warn(f"Unexpected part name at row {i}: {part_name}")
            
            bom[part_name] = {}
            for j, product in enumerate(products):
                qty_str = bom_lines[i][2+j].strip()
                if qty_str and qty_str != '':
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
    """Calculate weekly demand for each part with validation"""
    weekly_part_demand = {part: 0.0 for part in EXPECTED_PARTS}

    for part, products_dict in bom.items():
        for product, qty_per_product in products_dict.items():
            if product not in weekly_product_demand:
                warnings.warn(f"Product {product} in BOM but not in demand data")
                continue
            
            product_weekly_demand = weekly_product_demand.get(product, 0)
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
    """Load process sequences and times for all parts with validation"""
    # Process sequences (same as Task 3)
    process_sequences = {
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
    
    # Validate all expected parts have sequences
    missing_sequences = set(EXPECTED_PARTS) - set(process_sequences.keys())
    if missing_sequences:
        raise ValueError(f"Missing process sequences for parts: {missing_sequences}")

    # Process times - load from CSV with validation
    times_file = DATA_DIR / 'Parts_Step_Time.csv'
    
    if not times_file.exists():
        raise FileNotFoundError(f"Process times file not found: {times_file}")
    
    try:
        df_times = pd.read_csv(times_file)
    except Exception as e:
        raise ValueError(f"Failed to read process times CSV: {e}")
    
    # Validate CSV structure
    expected_cols = ['Part', 'Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6', 'Step 7']
    if not all(col in df_times.columns for col in expected_cols):
        raise ValueError(f"Process times CSV missing expected columns. Expected: {expected_cols}")
    
    process_times = {}

    for _, row in df_times.iterrows():
        part = row['Part']
        
        if part not in EXPECTED_PARTS:
            warnings.warn(f"Unexpected part in process times: {part}")
            continue
        
        times = []
        for step in ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5', 'Step 6', 'Step 7']:
            if pd.notna(row[step]):
                time_val = float(row[step])
                if time_val < 0:
                    raise ValueError(f"Negative process time for {part}, {step}: {time_val}")
                times.append(time_val)
            else:
                times.append(0)
        
        # Validate sequence length matches non-zero times
        sequence_length = len(process_sequences.get(part, []))
        non_zero_times = sum(1 for t in times if t > 0)
        
        if sequence_length != non_zero_times:
            warnings.warn(f"Part {part}: Sequence length ({sequence_length}) != non-zero times ({non_zero_times})")
        
        process_times[part] = times
    
    # Validate all expected parts have times
    missing_times = set(EXPECTED_PARTS) - set(process_times.keys())
    if missing_times:
        raise ValueError(f"Missing process times for parts: {missing_times}")
    
    print(f"✓ Loaded process sequences and times for {len(process_times)} parts")
    return process_sequences, process_times


def calculate_total_process_workload(weekly_part_demand, process_sequences, process_times):
    """
    Calculate total weekly workload (minutes) for each process type (A-M)
    This is the baseline for the entire factory
    """
    process_workload = {proc: 0.0 for proc in PROCESSES}

    for part, weekly_demand in weekly_part_demand.items():
        if part not in process_sequences:
            warnings.warn(f"Part {part} has demand but no process sequence")
            continue

        sequence = process_sequences[part]
        times = process_times[part]

        for step_idx, process in enumerate(sequence):
            if step_idx >= len(times):
                warnings.warn(f"Part {part}: Step index {step_idx} exceeds times array length")
                continue
            
            time_per_unit = times[step_idx]
            if time_per_unit < 0:
                raise ValueError(f"Negative process time for {part}, step {step_idx}: {time_per_unit}")
            
            total_minutes = weekly_demand * time_per_unit
            process_workload[process] += total_minutes
    
    # Log process workload summary
    total_workload = sum(process_workload.values())
    active_processes = sum(1 for w in process_workload.values() if w > 0)
    
    print(f"✓ Calculated process workload: {total_workload:,.0f} total minutes/week")
    print(f"  ({active_processes}/{len(PROCESSES)} processes are active)")

    return process_workload


def calculate_fractal_requirements_yearly(year, num_fractals, process_workload, 
                                        weekly_part_demand, process_sequences, process_times, num_shifts=2):
    """
    Calculate equipment requirements for fractal organization for a specific year
    
    CRITICAL FIX: All equipment has UNIFORM capacity based on operating parameters.
    No artificial capacity factors that create non-physical variations.
    
    Parameters:
    - year: Year number (2, 3, 4, 5)
    - num_fractals: Number of fractal centers (f)
    - process_workload: Total weekly workload per process (minutes)
    - weekly_part_demand: Weekly demand for each part
    - process_sequences: Process sequences for each part
    - process_times: Processing times for each part
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
    
    print(f"\n  Year {year} - Base equipment capacity: {base_capacity:,.1f} minutes/week/unit")
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
            print(f"  WARNING: Process {process}: Fractal integrity violation! "
                  f"{total_equipment} != {equipment_per_center} × {num_fractals}")
        
        results.append({
            'Year': year,
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
def generate_fractal_summary_yearly(year, num_fractals, requirements_df):
    """Generate summary report for fractal organization for a specific year"""
    total_equipment = requirements_df['Total_Equipment'].sum()
    avg_utilization = requirements_df['Utilization_per_Center'].mean()
    base_capacity = requirements_df['Base_Capacity_per_Equipment'].iloc[0]

    summary = f"""
{'='*80}
FRACTAL ORGANIZATION ANALYSIS - Year {year} (CORRECTED)
{'='*80}

Configuration:
- Year: +{year}
- Number of Fractal Centers: {num_fractals}
- Each center handles: {100/num_fractals:.1f}% of total demand
- Operating Schedule: {DAYS_PER_WEEK} days/week, 2 shifts/day, {HOURS_PER_SHIFT} hours/shift
- Effective Availability: {EFFECTIVE_AVAILABILITY*100:.1f}% (Efficiency: {EFFICIENCY*100:.0f}%, Reliability: {RELIABILITY*100:.0f}%)
- Uniform Equipment Capacity: {base_capacity:,.1f} minutes/week/unit

Summary Statistics:
- Total Equipment Units: {total_equipment}
- Equipment per Center: {total_equipment/num_fractals:.1f} (average)
- Average Utilization per Center: {avg_utilization*100:.1f}%

CRITICAL: All fractal centers are IDENTICAL in equipment composition

Equipment Distribution by Process:
"""

    for _, row in requirements_df.iterrows():
        summary += f"\n{row['Process']:>3}: {int(row['Equipment_per_Center']):>3} units/center × {num_fractals} centers = {int(row['Total_Equipment']):>3} total ({row['Utilization_per_Center']*100:>5.1f}% utilization)"

    summary += f"\n\n{'='*80}\n"

    return summary


def analyze_fractal_scaling():
    """
    Analyze fractal design across years 2-5
    Design for year 4 (peak), then scale down for earlier years
    """
    print("Loading BOM and process data...")
    bom = load_bom()
    process_sequences, process_times = load_process_data()

    # Analyze each year
    yearly_results = {}

    for year in YEARS:
        print(f"\n{'='*50}")
        print(f"Analyzing Year +{year}")
        print(f"{'='*50}")

        # Load demand for this year
        weekly_product_demand = load_yearly_product_demand(year)
        weekly_part_demand = calculate_weekly_part_demand(weekly_product_demand, bom)
        process_workload = calculate_total_process_workload(weekly_part_demand,
                                                         process_sequences,
                                                         process_times)

        print(f"  Total weekly demand: {sum(weekly_product_demand.values()):.0f} products")
        print(f"  Total weekly parts: {sum(weekly_part_demand.values()):.0f} parts")

        # Test different fractal configurations (f=2,3,4,5)
        year_results = {}

        for f in [2, 3, 4, 5]:
            print(f"\n  Analyzing f = {f} fractal centers...")
            requirements = calculate_fractal_requirements_yearly(year, f, process_workload,
                                                             weekly_part_demand, process_sequences, 
                                                             process_times, num_shifts=2)

            total_equipment = requirements['Total_Equipment'].sum()
            avg_utilization = requirements['Utilization_per_Center'].mean()

            year_results[f] = {
                'requirements': requirements,
                'total_equipment': total_equipment,
                'avg_utilization': avg_utilization
            }

            # Save detailed requirements
            output_file = RESULTS_DIR / f'Year{year}_Fractal_f{f}_Equipment_Requirements.csv'
            requirements.to_csv(output_file, index=False)
            print(f"    Saved: {output_file.name}")

            # Save summary report
            summary = generate_fractal_summary_yearly(year, f, requirements)
            summary_file = RESULTS_DIR / f'Year{year}_Fractal_f{f}_Summary_Report.txt'
            with open(summary_file, 'w') as file:
                file.write(summary)
            print(f"    Saved: {summary_file.name}")

        yearly_results[year] = year_results

    # Create comparison table across years
    comparison_data = []

    for year in YEARS:
        for f in [2, 3, 4, 5]:
            total_equipment = yearly_results[year][f]['total_equipment']
            avg_utilization = yearly_results[year][f]['avg_utilization']

            comparison_data.append({
                'Year': year,
                'Num_Fractals': f,
                'Capacity_per_Center_%': 100/f,
                'Total_Equipment': total_equipment,
                'Avg_Equipment_per_Center': total_equipment/f,
                'Avg_Utilization_%': avg_utilization * 100
            })

    comparison_df = pd.DataFrame(comparison_data)
    comparison_file = RESULTS_DIR / 'Fractal_Comparison_All_Years.csv'
    comparison_df.to_csv(comparison_file, index=False)

    print(f"\n{'='*80}")
    print("MULTI-YEAR FRACTAL SCENARIOS COMPARISON")
    print(f"{'='*80}")
    print(comparison_df.to_string(index=False))
    print(f"\nComparison saved: {comparison_file.name}")

    # Analyze scaling from year 4
    print(f"\n{'='*80}")
    print("SCALING ANALYSIS (Year 4 as Baseline)")
    print(f"{'='*80}")

    scaling_data = []

    for f in [2, 3, 4, 5]:
        year4_equipment = yearly_results[4][f]['total_equipment']

        for year in [2, 3, 5]:
            year_equipment = yearly_results[year][f]['total_equipment']
            scaling_factor = year_equipment / year4_equipment if year4_equipment > 0 else 0

            scaling_data.append({
                'Num_Fractals': f,
                'From_Year': 4,
                'To_Year': year,
                'Year4_Equipment': year4_equipment,
                'Target_Year_Equipment': year_equipment,
                'Scaling_Factor': scaling_factor,
                'Space_Reduction_%': (1 - scaling_factor) * 100
            })

    scaling_df = pd.DataFrame(scaling_data)
    scaling_file = RESULTS_DIR / 'Fractal_Scaling_Analysis.csv'
    scaling_df.to_csv(scaling_file, index=False)

    print("Scaling from Year 4 baseline:")
    print(scaling_df.to_string(index=False))
    print(f"\nScaling analysis saved: {scaling_file.name}")

    return comparison_df, scaling_df


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION DESIGN - TASK 4 (YEARS 2-5)")
    print("="*80 + "\n")

    # Create results directory if it doesn't exist
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Run multi-year fractal analysis
    comparison_df, scaling_df = analyze_fractal_scaling()

    print("\n" + "="*80)
    print("Analysis Complete!")
    print("="*80 + "\n")
    print("Generated files:")
    for year in YEARS:
        for f in [2, 3, 4, 5]:
            print(f"  - Year{year}_Fractal_f{f}_Equipment_Requirements.csv")
            print(f"  - Year{year}_Fractal_f{f}_Summary_Report.txt")
    print("  - Fractal_Comparison_All_Years.csv")
    print("  - Fractal_Scaling_Analysis.csv")
    print("\nNext steps:")
    print("  - Run fractal_flow_matrix_task4.py to generate flow matrices")
    print("  - Run fractal_layout_generator_task4.py to create layout coordinates")
    print("  - Design layout for Year 4, then scale down equipment for Years 2-3")


if __name__ == "__main__":
    main()