"""
Fractal Organization - Flow Matrix Generator

Creates flow matrices for fractal organization:
1. Flow matrix for each individual fractal center
2. Aggregate flow matrix for entire factory
3. Inter-center flow analysis

Each fractal center handles 1/f total demand and has complete
process capability (A through M).

Author: FeMoaSa Design Team
Date: November 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to project root
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results"
FRACTAL_FLOW_DIR = Path("/Users/shankaraadhithyaa/Desktop/Python/ISYE6202_CW3/results/Task3/Fractal/Fractal_Flowmatrix")

PROCESSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']


def load_weekly_part_demand():
    """Load weekly part demand from Task1 results"""
    task1_file = RESULTS_DIR / 'Task1_Demand_Fulfillment_Capacity_Plan.csv'
    if task1_file.exists():
        df = pd.read_csv(task1_file)
        return dict(zip(df['Part'], df['Weekly_Demand_Units']))
    else:
        # Alternative: calculate from product demand and BOM
        print("Warning: Task1 file not found, calculating from source data...")
        return calculate_part_demand_from_source()


def calculate_part_demand_from_source():
    """Calculate weekly part demand from product demand and BOM"""
    # Load product demand
    df = pd.read_csv(DATA_DIR / '+1 Year Product Demand.csv', header=None)
    products = ['A1', 'A2', 'A3', 'B1', 'B2']
    weekly_demand_values = df.iloc[12, 2:7].astype(float).tolist()
    weekly_product_demand = dict(zip(products, weekly_demand_values))
    
    # Load BOM
    bom_lines = []
    with open(DATA_DIR / '+1 Year Parts per Product.csv', 'r', encoding='utf-8') as f:
        for line in f:
            bom_lines.append(line.strip().split(','))
    
    bom = {}
    for i in range(2, 22):
        part_name = bom_lines[i][1].strip()
        bom[part_name] = {}
        for j, product in enumerate(products):
            qty_str = bom_lines[i][2+j].strip()
            if qty_str:
                bom[part_name][product] = int(float(qty_str))
    
    # Calculate part demand
    weekly_part_demand = {f'P{i}': 0.0 for i in range(1, 21)}
    for part, products_dict in bom.items():
        for product, qty_per_product in products_dict.items():
            weekly_part_demand[part] += weekly_product_demand[product] * qty_per_product
    
    return weekly_part_demand


def load_process_sequences():
    """Load process sequences for each part"""
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
    return process_sequences


def create_flow_matrix_for_center(part_demand_per_center, process_sequences):
    """
    Create flow matrix for a single fractal center
    Shows part movements between processes within the center
    """
    flow_matrix = pd.DataFrame(0.0, index=PROCESSES, columns=PROCESSES, dtype=float)
    
    for part, demand in part_demand_per_center.items():
        if part not in process_sequences:
            continue
        
        operations = process_sequences[part]
        
        # Create transitions between consecutive operations
        for i in range(len(operations) - 1):
            from_process = operations[i]
            to_process = operations[i + 1]
            flow_matrix.loc[from_process, to_process] += demand
    
    return flow_matrix


def generate_fractal_flow_matrices(num_fractals):
    """
    Generate flow matrices for fractal organization
    
    Parameters:
    - num_fractals: Number of fractal centers (f)
    
    Returns:
    - Dictionary with flow matrices for each center and aggregate
    """
    print(f"\nGenerating flow matrices for f={num_fractals} fractal centers...")
    
    # Load data
    weekly_part_demand = load_weekly_part_demand()
    process_sequences = load_process_sequences()
    
    # Calculate demand per fractal center (each center handles 1/f of total)
    part_demand_per_center = {part: demand / num_fractals 
                              for part, demand in weekly_part_demand.items()}
    
    # Create flow matrix for a single fractal center
    center_flow_matrix = create_flow_matrix_for_center(part_demand_per_center, 
                                                        process_sequences)
    
    # Aggregate flow matrix (sum across all centers)
    aggregate_flow_matrix = center_flow_matrix * num_fractals
    
    # Create output directory
    center_dir = FRACTAL_FLOW_DIR / f"f{num_fractals}_centers"
    center_dir.mkdir(parents=True, exist_ok=True)
    
    # Save flow matrix for single center
    center_file = center_dir / f"Single_Center_Flow_Matrix.csv"
    center_flow_matrix.to_csv(center_file)
    print(f"  Saved: {center_file.relative_to(RESULTS_DIR)}")
    
    # Save aggregate flow matrix
    aggregate_file = center_dir / f"Aggregate_Factory_Flow_Matrix.csv"
    aggregate_flow_matrix.to_csv(aggregate_file)
    print(f"  Saved: {aggregate_file.relative_to(RESULTS_DIR)}")
    
    # Create flow summary
    total_in_flow = center_flow_matrix.sum(axis=0)
    total_out_flow = center_flow_matrix.sum(axis=1)
    
    flow_summary = pd.DataFrame({
        'Process': PROCESSES,
        'In_Flow_per_Center': total_in_flow.values,
        'Out_Flow_per_Center': total_out_flow.values,
        'Total_In_Flow': (total_in_flow * num_fractals).values,
        'Total_Out_Flow': (total_out_flow * num_fractals).values
    })
    
    summary_file = center_dir / f"Flow_Summary.csv"
    flow_summary.to_csv(summary_file, index=False)
    print(f"  Saved: {summary_file.relative_to(RESULTS_DIR)}")
    
    # Generate individual center flow matrices (for layout purposes)
    for center_num in range(1, num_fractals + 1):
        individual_file = center_dir / f"Center_{center_num}_Flow_Matrix.csv"
        center_flow_matrix.to_csv(individual_file)
    
    print(f"  Generated {num_fractals} individual center flow matrices")
    
    return {
        'center_flow': center_flow_matrix,
        'aggregate_flow': aggregate_flow_matrix,
        'flow_summary': flow_summary
    }


def create_process_adjacency_matrix(flow_matrix):
    """
    Create adjacency matrix for layout optimization
    Higher values indicate processes that should be located closer together
    """
    # Bidirectional flow (sum of flow in both directions)
    adjacency = flow_matrix + flow_matrix.T
    
    return adjacency


def generate_layout_data_for_center(flow_matrix, center_id=1):
    """
    Generate layout data for a single fractal center
    Includes process coordinates and connection strengths
    """
    adjacency = create_process_adjacency_matrix(flow_matrix)
    
    # Create edge list with flow weights (for layout visualization)
    edges = []
    for i, from_proc in enumerate(PROCESSES):
        for j, to_proc in enumerate(PROCESSES):
            flow = flow_matrix.loc[from_proc, to_proc]
            if flow > 0:
                edges.append({
                    'From': from_proc,
                    'To': to_proc,
                    'Flow': flow,
                    'Center_ID': center_id
                })
    
    return pd.DataFrame(edges)


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION - FLOW MATRIX GENERATION")
    print("="*80 + "\n")
    
    # Create output directory
    FRACTAL_FLOW_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate flow matrices for different fractal configurations
    all_results = {}
    
    for f in [2, 3, 4, 5]:
        results = generate_fractal_flow_matrices(f)
        all_results[f] = results
        
        # Generate layout data for first center of each configuration
        center_dir = FRACTAL_FLOW_DIR / f"f{f}_centers"
        layout_edges = generate_layout_data_for_center(results['center_flow'], center_id=1)
        layout_file = center_dir / "Layout_Edges.csv"
        layout_edges.to_csv(layout_file, index=False)
        print(f"  Saved: {layout_file.relative_to(RESULTS_DIR)}")
    
    print("\n" + "="*80)
    print("Flow Matrix Generation Complete!")
    print("="*80 + "\n")
    
    print("Generated directories:")
    for f in [2, 3, 4, 5]:
        print(f"  - Task3/Fractal/Fractal_Flowmatrix/f{f}_centers/")
    
    print("\nEach directory contains:")
    print("  - Single_Center_Flow_Matrix.csv (flow within one center)")
    print("  - Aggregate_Factory_Flow_Matrix.csv (total factory flow)")
    print("  - Flow_Summary.csv (flow statistics)")
    print("  - Center_X_Flow_Matrix.csv (individual center matrices)")
    print("  - Layout_Edges.csv (for visualization)")
    
    # Print sample from f=3 configuration
    if 3 in all_results:
        print("\n" + "="*80)
        print("SAMPLE: f=3 Configuration Flow Summary")
        print("="*80)
        print(all_results[3]['flow_summary'].to_string(index=False))


if __name__ == "__main__":
    main()
