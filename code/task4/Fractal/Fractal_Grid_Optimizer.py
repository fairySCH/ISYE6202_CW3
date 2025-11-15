"""
fractal optimal grid configuration generator (reusable)
========================================================

this script generates the optimal grid layout for each process (a-m) in a single fractal center,
considering the shareability of machine spaces.

shareability rules:
- a, b, c, d: same machine type, 14×14 ft, can share 2ft on three sides
- k, l, m: 14×7 ft, can share 1ft on either side of the 7ft dimension
- e, f, g: 22×15 ft, no sharing
- h, i, j: 14×36 ft, no sharing

optimization goals:
1. minimize wasted spaces (unused grid slots)
2. minimize total block area (considering overlap)
3. optimize aspect ratio (prefer square-like blocks)
4. maximize utilization efficiency
5. minimize perimeter (reduces material handling distance)

usage:
    python script.py <year> <num_fractals>
    example: python script.py 5 4
             python script.py 1 4

team: machas^2
date: november 2025
"""

import math
import sys
from pathlib import Path
import pandas as pd

# ============================================================================
# configuration
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent.parent

# machine specifications
MACHINE_SPECS = {
    # Process: (width_ft, depth_ft, overlap_x_ft, overlap_y_ft, group)
    'A': (14, 14, 2, 2, 'ABCD'),  # Can share 2ft on 3 sides
    'B': (14, 14, 2, 2, 'ABCD'),
    'C': (14, 14, 2, 2, 'ABCD'),
    'D': (14, 14, 2, 2, 'ABCD'),
    'E': (22, 15, 0, 0, 'EFG'),   # No sharing
    'F': (22, 15, 0, 0, 'EFG'),
    'G': (22, 15, 0, 0, 'EFG'),
    'H': (14, 36, 0, 0, 'HIJ'),   # No sharing
    'I': (14, 36, 0, 0, 'HIJ'),
    'J': (14, 36, 0, 0, 'HIJ'),
    'K': (14, 7, 0, 1, 'KLM'),    # 14ft width, 7ft depth, share 1ft along depth (y-direction)
    'L': (14, 7, 0, 1, 'KLM'),
    'M': (14, 7, 0, 1, 'KLM'),
}

# ============================================================================
# CORE OPTIMIZATION FUNCTIONS
# ============================================================================

def calculate_block_dimensions(rows, cols, machine_w, machine_h, overlap_x, overlap_y):
    """
    Calculate the actual block dimensions considering overlap.
    
    When machines share space:
    - Effective width = n * width - (n-1) * overlap_x
    - Effective height = n * height - (n-1) * overlap_y
    
    Args:
        rows: Number of rows in grid
        cols: Number of columns in grid
        machine_w: Individual machine width
        machine_h: Individual machine height
        overlap_x: Overlap in x-direction (horizontal)
        overlap_y: Overlap in y-direction (vertical)
    
    Returns:
        (block_width, block_depth, block_area)
    """
    if rows == 0 or cols == 0:
        return 0, 0, 0
    
    # Apply overlap formula
    if overlap_x > 0:
        block_width = cols * machine_w - (cols - 1) * overlap_x
    else:
        block_width = cols * machine_w
    
    if overlap_y > 0:
        block_depth = rows * machine_h - (rows - 1) * overlap_y
    else:
        block_depth = rows * machine_h
    
    block_area = block_width * block_depth
    
    return block_width, block_depth, block_area


def calculate_optimization_score(machine_count, rows, cols, block_area, aspect_ratio, utilization):
    """
    Calculate composite optimization score.
    
    Lower score = better configuration
    
    Scoring factors:
    - Area efficiency: Favor smaller total area
    - Aspect ratio: Prefer square-like shapes (ratio close to 1)
    - Utilization: Maximize (minimize wasted spaces)
    - Perimeter: Minimize (better for material handling)
    
    Args:
        machine_count: Number of machines to place
        rows, cols: Grid dimensions
        block_area: Total block area in sq ft
        aspect_ratio: max(rows,cols) / min(rows,cols)
        utilization: machine_count / total_spaces
    
    Returns:
        optimization_score (lower is better)
    """
    # Normalize factors
    waste_penalty = (rows * cols - machine_count) * 100  # Penalize wasted spaces heavily
    area_factor = block_area / 100  # Normalize area
    aspect_penalty = (aspect_ratio - 1) * 50  # Penalize deviation from square
    utilization_bonus = (1 - utilization) * 200  # Reward high utilization
    
    # Perimeter penalty (prefer compact shapes)
    block_width = cols  # Relative
    block_depth = rows   # Relative
    perimeter = 2 * (block_width + block_depth)
    perimeter_penalty = perimeter * 5
    
    score = waste_penalty + area_factor + aspect_penalty + utilization_bonus + perimeter_penalty
    
    return round(score, 2)


def find_optimal_grid(machine_count, machine_w, machine_h, overlap_x, overlap_y, process_name):
    """
    Find the optimal grid configuration for a given number of machines.
    
    Strategy:
    1. Try all possible grid configurations (rows × cols)
    2. Calculate dimensions considering overlap
    3. Score each configuration
    4. Return the best one
    
    Args:
        machine_count: Number of machines to arrange
        machine_w, machine_h: Individual machine dimensions
        overlap_x, overlap_y: Overlap amounts
        process_name: Name for logging
    
    Returns:
        dict with optimal configuration details
    """
    if machine_count == 0:
        return {
            'process': process_name,
            'machine_count': 0,
            'rows': 0,
            'cols': 0,
            'total_spaces': 0,
            'wasted_spaces': 0,
            'block_width': 0,
            'block_depth': 0,
            'block_area': 0,
            'aspect_ratio': 0,
            'utilization': 0,
            'score': 0
        }
    
    best_config = None
    best_score = float('inf')
    
    # Try all possible rectangular arrangements
    for rows in range(1, machine_count + 1):
        cols = math.ceil(machine_count / rows)
        total_spaces = rows * cols
        
        # Only consider valid arrangements
        if total_spaces < machine_count:
            continue
        
        wasted_spaces = total_spaces - machine_count
        
        # Calculate actual block dimensions with overlap
        block_width, block_depth, block_area = calculate_block_dimensions(
            rows, cols, machine_w, machine_h, overlap_x, overlap_y
        )
        
        # Calculate metrics
        aspect_ratio = max(rows, cols) / min(rows, cols) if min(rows, cols) > 0 else float('inf')
        utilization = machine_count / total_spaces
        perimeter = 2 * (block_width + block_depth)
        
        # Calculate optimization score
        score = calculate_optimization_score(
            machine_count, rows, cols, block_area, aspect_ratio, utilization
        )
        
        # Track best configuration
        if score < best_score:
            best_score = score
            best_config = {
                'process': process_name,
                'group': MACHINE_SPECS[process_name][4],
                'equipment_count': machine_count,
                'layout_grid': f"{rows}×{cols}",
                'rows': rows,
                'cols': cols,
                'total_spaces': total_spaces,
                'wasted_spaces': wasted_spaces,
                'machine_width_ft': machine_w,
                'machine_depth_ft': machine_h,
                'block_width_ft': block_width,
                'block_depth_ft': block_depth,
                'block_area_sqft': block_area,
                'aspect_ratio': round(aspect_ratio, 3),
                'utilization': round(utilization, 4),
                'perimeter_ft': perimeter,
                'optimization_score': score
            }
    
    return best_config


# ============================================================================
# MAIN OPTIMIZATION ROUTINE
# ============================================================================

def optimize_all_processes(year, num_fractals):
    """
    Load equipment requirements and optimize grid layout for each process.
    
    Args:
        year: Year number (1-5)
        num_fractals: Number of fractal centers (e.g., 4)
    
    Outputs:
        1. CSV with optimal configurations
        2. Summary statistics
    
    Returns:
        DataFrame with optimal configurations
    """
    # Determine equipment file path based on year
    if year == 1:
        # Year 1 is in Task3
        equipment_file = BASE_DIR / "results" / "Task3" / "Fractal" / "Fractal_Design" / f"Fractal_f{num_fractals}_Equipment_Requirements.csv"
    else:
        # Years 2-5 are in task4
        equipment_file = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Design" / f"Year{year}_Fractal_f{num_fractals}_Equipment_Requirements.csv"
    
    # Create output directory
    output_dir = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / f"Year{year}_F{num_fractals}_Optimized"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print(f"YEAR {year} FRACTAL F{num_fractals} - OPTIMAL GRID CONFIGURATION GENERATOR")
    print("=" * 80)
    print()
    
    # Load equipment requirements
    print(f"Loading equipment requirements from:")
    print(f"  {equipment_file.relative_to(BASE_DIR)}")
    print()
    
    df_equipment = pd.read_csv(equipment_file)
    
    # Filter for specific year (only needed for task4 files)
    if year > 1:
        df_year = df_equipment[df_equipment['Year'] == year].copy()
    else:
        # Year 1 file doesn't have Year column
        df_year = df_equipment.copy()
    
    # Optimize each process
    optimal_configs = []
    
    print("OPTIMIZING GRID CONFIGURATIONS:")
    print("-" * 80)
    print(f"{'Process':<8} {'Count':<6} {'Grid':<8} {'Waste':<6} {'Dimensions (ft)':<20} {'Area (sqft)':<12} {'Score':<8}")
    print("-" * 80)
    
    total_machines = 0
    total_area = 0
    
    for _, row in df_year.iterrows():
        process = row['Process']
        
        # Skip TOTAL row
        if process == 'TOTAL':
            continue
        
        equipment_count = int(row['Equipment_per_Center'])
        
        # Get machine specs
        if process not in MACHINE_SPECS:
            print(f"Warning: Unknown process {process}, skipping...")
            continue
        
        machine_w, machine_h, overlap_x, overlap_y, group = MACHINE_SPECS[process]
        
        # Find optimal grid
        config = find_optimal_grid(
            equipment_count, machine_w, machine_h, 
            overlap_x, overlap_y, process
        )
        
        if config is None:
            continue
        
        optimal_configs.append(config)
        
        # Display
        print(f"{process:<8} {equipment_count:<6} {config['layout_grid']:<8} "
              f"{config['wasted_spaces']:<6} "
              f"{config['block_width_ft']:.0f} × {config['block_depth_ft']:.0f}"
              f"{'':<8} {config['block_area_sqft']:<12.0f} {config['optimization_score']:<8.2f}")
        
        total_machines += equipment_count
        total_area += config['block_area_sqft']
    
    print("-" * 80)
    print(f"TOTAL: {total_machines} machines, {total_area:,.0f} sq ft")
    print()
    
    # Create DataFrame
    df_optimal = pd.DataFrame(optimal_configs)
    
    # Reorder columns for clarity
    column_order = [
        'process', 'group', 'equipment_count', 'layout_grid', 'rows', 'cols',
        'total_spaces', 'wasted_spaces', 
        'machine_width_ft', 'machine_depth_ft',
        'block_width_ft', 'block_depth_ft', 'block_area_sqft',
        'aspect_ratio', 'utilization', 'perimeter_ft', 'optimization_score'
    ]
    
    df_optimal = df_optimal[column_order]
    
    # Save to CSV
    output_file = output_dir / f"Year{year}_F{num_fractals}_Optimal_Grid_Configurations.csv"
    df_optimal.to_csv(output_file, index=False)
    
    print(f"✓ Saved optimal configurations to:")
    print(f"  {output_file.relative_to(BASE_DIR)}")
    print()
    
    # Generate summary statistics
    generate_summary_stats(df_optimal)
    
    return df_optimal, output_dir


def generate_summary_stats(df_optimal):
    """Generate and display summary statistics."""
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print()
    
    # Group-level statistics
    print("BY GROUP:")
    print("-" * 80)
    
    for group in ['ABCD', 'EFG', 'HIJ', 'KLM']:
        df_group = df_optimal[df_optimal['group'] == group]
        
        if len(df_group) == 0:
            continue
        
        total_machines = df_group['equipment_count'].sum()
        total_area = df_group['block_area_sqft'].sum()
        avg_utilization = df_group['utilization'].mean()
        avg_waste = df_group['wasted_spaces'].mean()
        
        print(f"\n{group}:")
        print(f"  Processes: {', '.join(df_group['process'].tolist())}")
        print(f"  Total machines: {total_machines}")
        print(f"  Total area: {total_area:,.0f} sq ft")
        print(f"  Avg utilization: {avg_utilization:.2%}")
        print(f"  Avg wasted spaces: {avg_waste:.1f}")
    
    print()
    print("-" * 80)
    
    # Overall statistics
    total_machines = df_optimal['equipment_count'].sum()
    total_area = df_optimal['block_area_sqft'].sum()
    total_wasted = df_optimal['wasted_spaces'].sum()
    avg_utilization = df_optimal['utilization'].mean()
    
    print(f"\nOVERALL:")
    print(f"  Total machines: {total_machines}")
    print(f"  Total block area: {total_area:,.0f} sq ft")
    print(f"  Total wasted spaces: {total_wasted}")
    print(f"  Average utilization: {avg_utilization:.2%}")
    print(f"  Average aspect ratio: {df_optimal['aspect_ratio'].mean():.3f}")
    
    # Best and worst configurations
    print()
    print("-" * 80)
    print("\nBEST CONFIGURATIONS (by optimization score):")
    df_sorted = df_optimal.sort_values('optimization_score')
    for idx, row in df_sorted.head(3).iterrows():
        print(f"  {row['process']}: {row['layout_grid']} grid, "
              f"{row['block_area_sqft']:.0f} sq ft, "
              f"score={row['optimization_score']:.2f}")
    
    print()
    print("=" * 80)


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) >= 3:
        year = int(sys.argv[1])
        num_fractals = int(sys.argv[2])
    else:
        # Default to running all requested configurations: Year 2,3,4,5 with f=4
        print("Usage: python script.py <year> <num_fractals>")
        print("Example: python script.py 5 4")
        print("\nRunning for all requested configurations: Years 2,3,4,5 with f=4")
        
        # Run for all requested years with f=4
        requested_years = [2, 3, 4, 5]
        num_fractals = 4
        
        for year in requested_years:
            print(f"\n{'='*60}")
            print(f"PROCESSING YEAR {year}, F{num_fractals}")
            print(f"{'='*60}")
            try:
                df_results, output_dir = optimize_all_processes(year, num_fractals)
                print(f"✓ Year {year} F{num_fractals} optimization completed successfully!")
            except Exception as e:
                print(f"✗ Error processing Year {year} F{num_fractals}: {e}")
        
        print(f"\n{'='*80}")
        print("BATCH PROCESSING COMPLETE!")
        print(f"{'='*80}")
        print("\nGenerated files:")
        for year in requested_years:
            output_dir = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / f"Year{year}_F{num_fractals}_Optimized"
            csv_file = output_dir / f"Year{year}_F{num_fractals}_Optimal_Grid_Configurations.csv"
            print(f"  ✓ {csv_file.relative_to(BASE_DIR)}")
        
        print(f"\nNext step: Run the block visualizer for each year:")
        for year in requested_years:
            print(f"  python Fractal_Individual_Block_Visualizer.py {year} {num_fractals}")
        
        sys.exit(0)
    
    # Single run mode (original behavior)
    df_results, output_dir = optimize_all_processes(year, num_fractals)
    
    print("\n✓ Optimization complete!")
    print()
    print(f"Next step: Run the block visualizer to generate A-M images!")
    print(f"  python Fractal_Individual_Block_Visualizer.py {year} {num_fractals}")
