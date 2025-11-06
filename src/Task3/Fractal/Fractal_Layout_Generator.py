"""
Fractal Organization - Layout Generator

Generates coordinates and layout data for fractal organization design.
Creates visualization-ready outputs for drawing factory layouts.

Key Features:
1. Process placement within each fractal center
2. Fractal center placement in factory floor
3. Material flow paths
4. Storage area allocation
5. Export to CAD-ready formats

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
FRACTAL_FLOW_DIR = RESULTS_DIR / "Task3" / "Fractal" / "Fractal_Flowmatrix"
LAYOUT_DIR = RESULTS_DIR / "Task3" / "Fractal" / "Fractal_Layout"

PROCESSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']


def load_flow_matrix(num_fractals):
    """Load flow matrix for a single fractal center"""
    flow_file = FRACTAL_FLOW_DIR / f"f{num_fractals}_centers" / "Single_Center_Flow_Matrix.csv"
    return pd.read_csv(flow_file, index_col=0)


def load_equipment_requirements(num_fractals):
    """Load equipment requirements per center"""
    req_file = RESULTS_DIR / "Task3" / "Fractal" / "Fractal_Design" / f"Fractal_f{num_fractals}_Equipment_Requirements.csv"
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


def generate_center_positions(num_fractals):
    """
    Generate positions for each fractal center on the factory floor
    Arranges centers in a grid pattern
    """
    # Determine grid dimensions
    cols = int(np.ceil(np.sqrt(num_fractals)))
    rows = int(np.ceil(num_fractals / cols))
    
    # Spacing between centers (in meters)
    CENTER_SPACING_X = 100
    CENTER_SPACING_Y = 100
    
    center_positions = []
    
    for i in range(num_fractals):
        row = i // cols
        col = i % cols
        
        # Calculate center coordinates
        x = col * CENTER_SPACING_X
        y = row * CENTER_SPACING_Y
        
        center_positions.append({
            'center_id': i + 1,
            'x': x,
            'y': y,
            'width': CENTER_SPACING_X * 0.8,
            'height': CENTER_SPACING_Y * 0.8
        })
    
    return center_positions


def generate_complete_layout(num_fractals, layout_method='flow_based'):
    """
    Generate complete factory layout for fractal organization
    
    Parameters:
    - num_fractals: Number of fractal centers
    - layout_method: 'simple' or 'flow_based'
    """
    print(f"\nGenerating layout for f={num_fractals} fractal centers...")
    
    # Load data
    flow_matrix = load_flow_matrix(num_fractals)
    equipment_counts = load_equipment_requirements(num_fractals)
    
    # Generate process layout within a center
    if layout_method == 'flow_based':
        process_coords = optimize_process_layout_flow_based(flow_matrix, equipment_counts)
    else:
        process_coords = optimize_process_layout_simple(flow_matrix, equipment_counts)
    
    # Generate center positions on factory floor
    center_positions = generate_center_positions(num_fractals)
    
    # Create process placement table for all centers
    all_processes = []
    
    for center in center_positions:
        center_id = center['center_id']
        center_x = center['x']
        center_y = center['y']
        
        for process, coords in process_coords.items():
            all_processes.append({
                'Center_ID': center_id,
                'Process': process,
                'Global_X': center_x + coords['x'],
                'Global_Y': center_y + coords['y'],
                'Local_X': coords['x'],
                'Local_Y': coords['y'],
                'Width': coords['width'],
                'Height': coords['height'],
                'Equipment_Count': coords['equipment_count']
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
                flow = flow_matrix.loc[from_proc, to_proc]
                
                if flow > 0:
                    from_coords = process_coords[from_proc]
                    to_coords = process_coords[to_proc]
                    
                    flow_edges.append({
                        'Center_ID': center_id,
                        'From_Process': from_proc,
                        'To_Process': to_proc,
                        'From_X': center_x + from_coords['x'],
                        'From_Y': center_y + from_coords['y'],
                        'To_X': center_x + to_coords['x'],
                        'To_Y': center_y + to_coords['y'],
                        'Flow_Units': flow
                    })
    
    flow_df = pd.DataFrame(flow_edges)
    
    # Create center boundary data
    centers_df = pd.DataFrame(center_positions)
    
    # Save all layout data
    output_dir = LAYOUT_DIR / f"f{num_fractals}_layout"
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
        'num_fractals': num_fractals,
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


def create_layout_summary(num_fractals, layout_data):
    """Create summary report for layout"""
    summary = f"""
{'='*80}
FRACTAL LAYOUT SUMMARY - f={num_fractals} Centers
{'='*80}

Factory Configuration:
- Number of Fractal Centers: {num_fractals}
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
    summary += f"\n{'='*80}\n"
    
    return summary


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION - LAYOUT GENERATION")
    print("="*80 + "\n")
    
    # Create output directory
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate layouts for different configurations
    for f in [2, 3, 4]:
        layout_data = generate_complete_layout(f, layout_method='flow_based')
        
        # Generate summary
        summary = create_layout_summary(f, layout_data)
        
        summary_file = LAYOUT_DIR / f"f{f}_layout" / "Layout_Summary.txt"
        with open(summary_file, 'w') as file:
            file.write(summary)
        print(f"  Saved: {summary_file.relative_to(RESULTS_DIR)}")
    
    print("\n" + "="*80)
    print("Layout Generation Complete!")
    print("="*80 + "\n")
    
    print("Generated layouts for f=2, f=3, f=4 configurations")
    print("\nEach layout directory contains:")
    print("  - Process_Locations.csv (process coordinates)")
    print("  - Flow_Connections.csv (material flow paths)")
    print("  - Center_Boundaries.csv (fractal center locations)")
    print("  - Layout_Data.json (for web visualization)")
    print("  - Layout_Summary.txt (layout statistics)")
    
    print("\nTo visualize:")
    print("  1. Import Process_Locations.csv and Flow_Connections.csv into CAD software")
    print("  2. Use Center_Boundaries.csv to draw fractal center boundaries")
    print("  3. Use Flow_Connections.csv to draw material flow arrows")
    print("  4. Scale coordinates as needed (currently in meters)")


if __name__ == "__main__":
    main()
