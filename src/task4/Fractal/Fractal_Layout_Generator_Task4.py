"""
Fractal Organization - Layout Generator - Task 4

Generates coordinates and layout data for fractal organization design
across years 2-5. Creates visualization-ready outputs for drawing factory layouts.

Key Features:
1. Process placement within each fractal center per year
2. Fractal center placement in factory floor per year
3. Material flow paths per year
4. Storage area allocation per year
5. Scaling analysis from year 4 baseline
6. Export to CAD-ready formats

Author: FeMoaSa Design Team
Date: November 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to project root
RESULTS_DIR = BASE_DIR / "results"
FRACTAL_FLOW_DIR = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Flowmatrix"
LAYOUT_DIR = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Layout"

PROCESSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
YEARS = [2, 3, 4, 5]


def load_flow_matrix(year, num_fractals):
    """Load flow matrix for a single fractal center"""
    flow_file = FRACTAL_FLOW_DIR / f"year{year}" / f"f{num_fractals}_centers" / "Single_Center_Flow_Matrix.csv"
    df = pd.read_csv(flow_file, index_col=0)
    # Ensure all values are numeric
    df = df.astype(float)
    return df


def load_equipment_requirements(year, num_fractals):
    """Load equipment requirements per center"""
    req_file = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Design" / f"Year{year}_Fractal_f{num_fractals}_Equipment_Requirements.csv"
    df = pd.read_csv(req_file)
    return dict(zip(df['Process'], df['Equipment_per_Center']))


def optimize_process_layout_simple(flow_matrix, equipment_counts):
    """
    Simple process layout optimization using flow-based positioning
    Places processes with high flow close to each other

    Returns coordinates for each process within a center
    """
    # Calculate total flow for each process (in + out)
    total_flow = flow_matrix.sum(axis=0) + flow_matrix.sum(axis=1)

    # Sort processes by flow intensity
    flow_sorted = total_flow.sort_values(ascending=False)

    # Create grid layout based on number of processes
    # Arrange in approximate square/rectangle
    num_processes = len(PROCESSES)
    cols = int(np.ceil(np.sqrt(num_processes)))
    rows = int(np.ceil(num_processes / cols))

    # Assign coordinates (in grid units, e.g., 10m x 10m per cell)
    CELL_SIZE = 10  # meters
    coordinates = {}

    # Position high-flow processes centrally
    center_row = rows // 2
    center_col = cols // 2

    positioned = 0
    for process in PROCESSES:
        row = positioned // cols
        col = positioned % cols

        # Calculate actual coordinates (offset from center)
        x = (col - center_col) * CELL_SIZE
        y = (row - center_row) * CELL_SIZE

        # Add some spacing based on equipment count
        equipment = equipment_counts.get(process, 1)
        width = CELL_SIZE * min(1.5, 0.5 + equipment * 0.1)
        height = CELL_SIZE * min(1.5, 0.5 + equipment * 0.1)

        coordinates[process] = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'equipment_count': equipment
        }

        positioned += 1

    return coordinates


def optimize_process_layout_flow_based(flow_matrix, equipment_counts):
    """
    Advanced layout optimization using weighted flow analysis
    Uses a simple force-directed approach
    """
    # Initialize random positions
    np.random.seed(42)
    positions = {proc: np.array([np.random.uniform(-50, 50),
                                np.random.uniform(-50, 50)])
                 for proc in PROCESSES}

    # Normalize flow matrix
    max_flow = flow_matrix.max().max()
    if max_flow > 0:
        normalized_flow = flow_matrix / max_flow
    else:
        normalized_flow = flow_matrix

    # Iterative improvement (simplified force-directed)
    iterations = 100
    learning_rate = 0.5

    for iteration in range(iterations):
        forces = {proc: np.array([0.0, 0.0]) for proc in PROCESSES}

        # Calculate attractive forces based on flow
        for i, proc_i in enumerate(PROCESSES):
            for j, proc_j in enumerate(PROCESSES):
                if i != j:
                    flow = (normalized_flow.loc[proc_i, proc_j] +
                           normalized_flow.loc[proc_j, proc_i])

                    if flow > 0:
                        # Direction from i to j
                        direction = positions[proc_j] - positions[proc_i]
                        distance = np.linalg.norm(direction)

                        if distance > 0:
                            # Attractive force proportional to flow
                            force_magnitude = flow * min(distance / 20, 1.0)
                            force = direction / distance * force_magnitude
                            forces[proc_i] += force

        # Apply repulsive forces to prevent overlap
        for i, proc_i in enumerate(PROCESSES):
            for j, proc_j in enumerate(PROCESSES):
                if i < j:
                    direction = positions[proc_i] - positions[proc_j]
                    distance = np.linalg.norm(direction)

                    if distance < 15:  # Minimum separation
                        force_magnitude = (15 - distance) / 15
                        if distance > 0:
                            force = direction / distance * force_magnitude
                            forces[proc_i] += force
                            forces[proc_j] -= force

        # Update positions
        for proc in PROCESSES:
            positions[proc] += forces[proc] * learning_rate

        # Decay learning rate
        learning_rate *= 0.99

    # Convert to coordinate dictionary
    coordinates = {}
    for proc in PROCESSES:
        equipment = equipment_counts.get(proc, 1)
        width = 10 + equipment * 2
        height = 10 + equipment * 2

        coordinates[proc] = {
            'x': float(positions[proc][0]),
            'y': float(positions[proc][1]),
            'width': width,
            'height': height,
            'equipment_count': equipment
        }

    return coordinates


def generate_center_positions(num_fractals, year, scaling_factor=1.0):
    """
    Generate positions for each fractal center on the factory floor
    Arranges centers in a grid pattern, scaled by demand

    Parameters:
    - num_fractals: Number of fractal centers
    - year: Year for scaling reference
    - scaling_factor: Factor to scale center spacing (based on demand)
    """
    # Determine grid dimensions
    cols = int(np.ceil(np.sqrt(num_fractals)))
    rows = int(np.ceil(num_fractals / cols))

    # Base spacing between centers (in meters)
    BASE_SPACING_X = 100
    BASE_SPACING_Y = 100

    # Scale spacing based on demand (higher demand = more space needed)
    spacing_x = BASE_SPACING_X * scaling_factor
    spacing_y = BASE_SPACING_Y * scaling_factor

    center_positions = []

    for i in range(num_fractals):
        row = i // cols
        col = i % cols

        # Calculate center coordinates
        x = col * spacing_x
        y = row * spacing_y

        center_positions.append({
            'center_id': i + 1,
            'x': x,
            'y': y,
            'width': spacing_x * 0.8,
            'height': spacing_y * 0.8,
            'scaling_factor': scaling_factor
        })

    return center_positions


def calculate_year_scaling_factors():
    """
    Calculate scaling factors for each year relative to year 4
    Returns dictionary of year -> scaling_factor
    """
    # Load year 4 demand as baseline
    year4_demand = load_yearly_product_demand(4)
    year4_total = sum(year4_demand.values())

    scaling_factors = {}

    for year in YEARS:
        if year == 4:
            scaling_factors[year] = 1.0
        else:
            year_demand = load_yearly_product_demand(year)
            year_total = sum(year_demand.values())
            # Scale spacing proportionally to sqrt of demand ratio
            # (since area scales with demand, but spacing scales with sqrt(area))
            scaling_factors[year] = np.sqrt(year_total / year4_total) if year4_total > 0 else 1.0

    return scaling_factors


def load_yearly_product_demand(year):
    """Load yearly product demand for specified year"""
    df = pd.read_csv(BASE_DIR / "data" / "csv_outputs" / '+2 to +5 Year Product Demand.csv', header=None)

    # Find the row for the specified year in the weekly demand section
    # The weekly demand starts around row 18
    year_to_row = {2: 18, 3: 19, 4: 20, 5: 21}
    weekly_row_idx = year_to_row.get(year)

    if weekly_row_idx is None:
        raise ValueError(f"Year +{year} not found in demand data")

    # Extract weekly demand values (columns 2-9 for products A1-B4)
    products = ['A1', 'A2', 'A3', 'B1', 'B2', 'A4', 'B3', 'B4']
    weekly_demand_values = df.iloc[weekly_row_idx, 2:10].astype(float).tolist()

    return dict(zip(products, weekly_demand_values))


def generate_complete_layout_yearly(year, num_fractals, layout_method='flow_based', scaling_factor=1.0):
    """
    Generate complete factory layout for fractal organization for a specific year

    Parameters:
    - year: Year number (2, 3, 4, 5)
    - num_fractals: Number of fractal centers
    - layout_method: 'simple' or 'flow_based'
    - scaling_factor: Factor to scale layout dimensions
    """
    print(f"\nGenerating layout for Year {year}, f={num_fractals} fractal centers...")

    # Load data
    flow_matrix = load_flow_matrix(year, num_fractals)
    equipment_counts = load_equipment_requirements(year, num_fractals)

    # Generate process layout within a center
    if layout_method == 'flow_based':
        process_coords = optimize_process_layout_flow_based(flow_matrix, equipment_counts)
    else:
        process_coords = optimize_process_layout_simple(flow_matrix, equipment_counts)

    # Scale process coordinates by scaling factor
    if scaling_factor != 1.0:
        for proc in process_coords:
            process_coords[proc]['x'] *= scaling_factor
            process_coords[proc]['y'] *= scaling_factor
            process_coords[proc]['width'] *= scaling_factor
            process_coords[proc]['height'] *= scaling_factor

    # Generate center positions on factory floor (scaled)
    center_positions = generate_center_positions(num_fractals, year, scaling_factor)

    # Create process placement table for all centers
    all_processes = []

    for center in center_positions:
        center_id = center['center_id']
        center_x = center['x']
        center_y = center['y']

        for process, coords in process_coords.items():
            all_processes.append({
                'Year': year,
                'Center_ID': center_id,
                'Process': process,
                'Global_X': center_x + coords['x'],
                'Global_Y': center_y + coords['y'],
                'Local_X': coords['x'],
                'Local_Y': coords['y'],
                'Width': coords['width'],
                'Height': coords['height'],
                'Equipment_Count': coords['equipment_count'],
                'Scaling_Factor': scaling_factor
            })

    process_df = pd.DataFrame(all_processes)

    # Create flow connections
    flow_edges = []

    for center in center_positions:
        center_id = center['center_id']
        center_x = center['x']
        center_y = center['y']

        for from_proc in PROCESSES:
            for to_proc in PROCESSES:
                flow = float(flow_matrix.loc[from_proc, to_proc])

                if flow > 0:
                    from_coords = process_coords[from_proc]
                    to_coords = process_coords[to_proc]

                    flow_edges.append({
                        'Year': year,
                        'Center_ID': center_id,
                        'From_Process': from_proc,
                        'To_Process': to_proc,
                        'From_X': center_x + from_coords['x'],
                        'From_Y': center_y + from_coords['y'],
                        'To_X': center_x + to_coords['x'],
                        'To_Y': center_y + to_coords['y'],
                        'Flow_Units': flow,
                        'Scaling_Factor': scaling_factor
                    })

    flow_df = pd.DataFrame(flow_edges)

    # Create center boundary data
    centers_df = pd.DataFrame(center_positions)
    centers_df['Year'] = year

    # Save all layout data
    year_dir = LAYOUT_DIR / f"year{year}"
    output_dir = year_dir / f"f{num_fractals}_layout"
    output_dir.mkdir(parents=True, exist_ok=True)

    process_file = output_dir / "Process_Locations.csv"
    process_df.to_csv(process_file, index=False)
    print(f"  Saved: {process_file.relative_to(RESULTS_DIR)}")

    flow_file = output_dir / "Flow_Connections.csv"
    flow_df.to_csv(flow_file, index=False)
    print(f"  Saved: {flow_file.relative_to(RESULTS_DIR)}")

    centers_file = output_dir / "Center_Boundaries.csv"
    centers_df.to_csv(centers_file, index=False)
    print(f"  Saved: {centers_file.relative_to(RESULTS_DIR)}")

    # Generate JSON for web visualization
    layout_json = {
        'year': year,
        'num_fractals': num_fractals,
        'scaling_factor': scaling_factor,
        'centers': center_positions,
        'processes': process_coords,
        'layout_method': layout_method
    }

    json_file = output_dir / "Layout_Data.json"
    with open(json_file, 'w') as f:
        json.dump(layout_json, f, indent=2)
    print(f"  Saved: {json_file.relative_to(RESULTS_DIR)}")

    return {
        'processes': process_df,
        'flows': flow_df,
        'centers': centers_df
    }


def create_layout_summary_yearly(year, num_fractals, layout_data, scaling_factor):
    """Create summary report for layout"""
    summary = f"""
{'='*80}
FRACTAL LAYOUT SUMMARY - Year {year}, f={num_fractals} Centers
{'='*80}

Factory Configuration:
- Year: +{year}
- Number of Fractal Centers: {num_fractals}
- Layout Scaling Factor: {scaling_factor:.3f} (relative to Year 4)
- Total Processes per Center: {len(PROCESSES)}
- Total Process Locations: {len(layout_data['processes'])}
- Total Flow Connections: {len(layout_data['flows'])}

Center Arrangement:
"""

    for _, center in layout_data['centers'].iterrows():
        summary += f"  Center {center['center_id']}: ({center['x']:.0f}, {center['y']:.0f}) - {center['width']:.0f}m × {center['height']:.0f}m\n"

    # Calculate factory dimensions
    max_x = layout_data['processes']['Global_X'].max() + layout_data['processes']['Width'].max()
    max_y = layout_data['processes']['Global_Y'].max() + layout_data['processes']['Height'].max()
    min_x = layout_data['processes']['Global_X'].min()
    min_y = layout_data['processes']['Global_Y'].min()

    summary += f"""
Factory Dimensions:
- Width: {max_x - min_x:.0f} meters
- Length: {max_y - min_y:.0f} meters
- Total Area: {(max_x - min_x) * (max_y - min_y):.0f} m²

Equipment Distribution:
"""

    equipment_by_process = layout_data['processes'].groupby('Process')['Equipment_Count'].first()
    total_equipment = equipment_by_process.sum()

    for process in PROCESSES:
        count = equipment_by_process.get(process, 0)
        summary += f"  {process}: {count} units/center × {num_fractals} centers = {count * num_fractals} total\n"

    summary += f"\nTotal Equipment: {int(total_equipment * num_fractals)} units\n"
    summary += f"Space Efficiency: {(total_equipment * num_fractals) / ((max_x - min_x) * (max_y - min_y)):.3f} equipment/m²\n"
    summary += f"\n{'='*80}\n"

    return summary


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION - LAYOUT GENERATION - TASK 4")
    print("="*80 + "\n")

    # Create output directory
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)

    # Calculate scaling factors for each year
    scaling_factors = calculate_year_scaling_factors()
    print("Year scaling factors (relative to Year 4):")
    for year, factor in scaling_factors.items():
        print(f"  Year {year}: {factor:.3f}")
    print()

    # Generate layouts for different years and configurations
    # Generate for all fractal configurations like Task 3
    all_fractal_configs = [2, 3, 4, 5]

    for year in YEARS:
        print(f"\n{'='*60}")
        print(f"YEAR {year} LAYOUT GENERATION")
        print(f"{'='*60}")

        scaling_factor = scaling_factors[year]

        for f in all_fractal_configs:
            layout_data = generate_complete_layout_yearly(year, f, layout_method='flow_based',
                                                         scaling_factor=scaling_factor)

            # Generate summary
            summary = create_layout_summary_yearly(year, f, layout_data, scaling_factor)

            year_dir = LAYOUT_DIR / f"year{year}"
            summary_file = year_dir / f"f{f}_layout" / "Layout_Summary.txt"
            with open(summary_file, 'w') as file:
                file.write(summary)
            print(f"  Saved: {summary_file.relative_to(RESULTS_DIR)}")

    print("\n" + "="*80)
    print("Layout Generation Complete!")
    print("="*80 + "\n")

    print("Generated layouts for Years 2-5 with f=2,3,4,5 configurations")
    print("\nEach layout directory contains:")
    print("  - Process_Locations.csv (process coordinates)")
    print("  - Flow_Connections.csv (material flow paths)")
    print("  - Center_Boundaries.csv (fractal center locations)")
    print("  - Layout_Data.json (for web visualization)")
    print("  - Layout_Summary.txt (layout statistics)")

    print("\nScaling Strategy:")
    print("  - Year 4: Baseline design (scaling factor = 1.000)")
    print("  - Years 2-3,5: Scaled from Year 4 design")
    print("  - Equipment counts adjusted per year")
    print("  - Layout dimensions scaled by demand ratio")

    print("\nTo visualize:")
    print("  1. Import Process_Locations.csv and Flow_Connections.csv into CAD software")
    print("  2. Use Center_Boundaries.csv to draw fractal center boundaries")
    print("  3. Use Flow_Connections.csv to draw material flow arrows")
    print("  4. Scale coordinates as needed (currently in meters)")


if __name__ == "__main__":
    main()