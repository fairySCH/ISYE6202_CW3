"""
fractal organization - flow matrix generator - task 4

this script creates flow matrices for the fractal organization setup across years 2 through 5. it generates:

1. flow matrix for each individual fractal center per year
2. aggregate flow matrix for the entire factory per year
3. inter-center flow analysis per year

each fractal center handles 1/f of the total demand and has complete process capability from a through m.

team: machas^2
date: november 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path

# configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # go up to project root
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results"
FRACTAL_FLOW_DIR = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Flowmatrix"

PROCESSES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
YEARS = [2, 3, 4, 5]


def load_yearly_product_demand(year):
    """load yearly product demand for specified year"""
    df = pd.read_csv(DATA_DIR / '+2 to +5 Year Product Demand.csv', header=None)

    # find the row for the specified year
    year_row_idx = None
    for i, row in df.iterrows():
        if str(row[1]).strip() == f'+{year}':
            year_row_idx = i
            break

    if year_row_idx is None:
        raise ValueError(f"Year +{year} not found in demand data")

    # extract weekly demand values (row 18-22 for years 2-5)
    weekly_row_idx = 17 + (year - 1)  # year 2 = row 18, year 3 = row 19, etc.
    products = ['A1', 'A2', 'A3', 'B1', 'B2', 'A4', 'B3', 'B4']
    weekly_demand_values = df.iloc[weekly_row_idx, 2:10].astype(float).tolist()

    return dict(zip(products, weekly_demand_values))


def load_bom():
    """load bill of materials for years 2-5"""
    bom_lines = []
    with open(DATA_DIR / '+2 to +5 Year Parts per Product.csv', 'r', encoding='utf-8') as f:
        for line in f:
            bom_lines.append(line.strip().split(','))

    bom = {}
    products = ['A1', 'A2', 'A3', 'B1', 'B2', 'A4', 'B3', 'B4']

    for i in range(2, 22):  # parts p1 to p20, starting from row 2
        part_name = bom_lines[i][1].strip()
        bom[part_name] = {}
        for j, product in enumerate(products):
            qty_str = bom_lines[i][2+j].strip()
            if qty_str and qty_str != '':
                try:
                    bom[part_name][product] = int(float(qty_str))
                except ValueError:
                    bom[part_name][product] = 0
            else:
                bom[part_name][product] = 0

    return bom


def calculate_weekly_part_demand(weekly_product_demand, bom):
    """calculate weekly demand for each part"""
    weekly_part_demand = {}

    for i in range(1, 21):
        part = f'P{i}'
        weekly_part_demand[part] = 0.0

    for part, products_dict in bom.items():
        for product, qty_per_product in products_dict.items():
            product_weekly_demand = weekly_product_demand.get(product, 0)
            weekly_part_demand[part] += product_weekly_demand * qty_per_product

    return weekly_part_demand


def load_process_sequences():
    """load process sequences for each part"""
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
    create flow matrix for a single fractal center
    shows part movements between processes within the center
    """
    flow_matrix = pd.DataFrame(0.0, index=PROCESSES, columns=PROCESSES, dtype=float)

    for part, demand in part_demand_per_center.items():
        if part not in process_sequences:
            continue

        operations = process_sequences[part]

        # create transitions between consecutive operations
        for i in range(len(operations) - 1):
            from_process = operations[i]
            to_process = operations[i + 1]
            flow_matrix.loc[from_process, to_process] += demand

    return flow_matrix


def generate_fractal_flow_matrices_yearly(year, num_fractals):
    """
    generate flow matrices for fractal organization for a specific year

    parameters:
    - year: year number (2, 3, 4, 5)
    - num_fractals: number of fractal centers (f)

    returns:
    - dictionary with flow matrices for each center and aggregate
    """
    print(f"\nGenerating flow matrices for Year {year}, f={num_fractals} fractal centers...")

    # load data
    weekly_product_demand = load_yearly_product_demand(year)
    bom = load_bom()
    weekly_part_demand = calculate_weekly_part_demand(weekly_product_demand, bom)
    process_sequences = load_process_sequences()

    # calculate demand per fractal center (each center handles 1/f of total)
    part_demand_per_center = {part: demand / num_fractals
                              for part, demand in weekly_part_demand.items()}

    # create flow matrix for a single fractal center
    center_flow_matrix = create_flow_matrix_for_center(part_demand_per_center,
                                                        process_sequences)

    # aggregate flow matrix (sum across all centers)
    aggregate_flow_matrix = center_flow_matrix * num_fractals

    # create output directory
    year_dir = FRACTAL_FLOW_DIR / f"year{year}"
    center_dir = year_dir / f"f{num_fractals}_centers"
    center_dir.mkdir(parents=True, exist_ok=True)

    # save flow matrix for single center
    center_file = center_dir / f"Single_Center_Flow_Matrix.csv"
    center_flow_matrix.to_csv(center_file)
    print(f"  Saved: {center_file.relative_to(RESULTS_DIR)}")

    # save aggregate flow matrix
    aggregate_file = center_dir / f"Aggregate_Factory_Flow_Matrix.csv"
    aggregate_flow_matrix.to_csv(aggregate_file)
    print(f"  Saved: {aggregate_file.relative_to(RESULTS_DIR)}")

    # create flow summary
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

    # generate individual center flow matrices (for layout purposes)
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
    create adjacency matrix for layout optimization
    higher values indicate processes that should be located closer together
    """
    # Bidirectional flow (sum of flow in both directions)
    adjacency = flow_matrix + flow_matrix.T

    return adjacency


def generate_layout_data_for_center(flow_matrix, center_id=1, year=None):
    """
    generate layout data for a single fractal center
    includes process coordinates and connection strengths
    """
    adjacency = create_process_adjacency_matrix(flow_matrix)

    # Create edge list with flow weights (for layout visualization)
    edges = []
    for i, from_proc in enumerate(PROCESSES):
        for j, to_proc in enumerate(PROCESSES):
            flow = flow_matrix.loc[from_proc, to_proc]
            if flow > 0:
                edges.append({
                    'Year': year,
                    'From': from_proc,
                    'To': to_proc,
                    'Flow': flow,
                    'Center_ID': center_id
                })

    return pd.DataFrame(edges)


def main():
    """main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION - FLOW MATRIX GENERATION - TASK 4")
    print("="*80 + "\n")

    # create output directory
    FRACTAL_FLOW_DIR.mkdir(parents=True, exist_ok=True)

    # generate flow matrices for different years and fractal configurations
    all_results = {}

    for year in YEARS:
        print(f"\n{'='*60}")
        print(f"YEAR {year} ANALYSIS")
        print(f"{'='*60}")

        year_results = {}

        for f in [2, 3, 4, 5]:
            results = generate_fractal_flow_matrices_yearly(year, f)
            year_results[f] = results

            # generate layout data for first center of each configuration
            year_dir = FRACTAL_FLOW_DIR / f"year{year}"
            center_dir = year_dir / f"f{f}_centers"
            layout_edges = generate_layout_data_for_center(results['center_flow'], center_id=1, year=year)
            layout_file = center_dir / "Layout_Edges.csv"
            layout_edges.to_csv(layout_file, index=False)
            print(f"  Saved: {layout_file.relative_to(RESULTS_DIR)}")

        all_results[year] = year_results

    print("\n" + "="*80)
    print("Flow Matrix Generation Complete!")
    print("="*80 + "\n")

    print("Generated directories:")
    for year in YEARS:
        print(f"  - Task4/Fractal/Fractal_Flowmatrix/year{year}/")
        for f in [2, 3, 4, 5]:
            print(f"    - f{f}_centers/")

    print("\nEach directory contains:")
    print("  - Single_Center_Flow_Matrix.csv (flow within one center)")
    print("  - Aggregate_Factory_Flow_Matrix.csv (total factory flow)")
    print("  - Flow_Summary.csv (flow statistics)")
    print("  - Center_X_Flow_Matrix.csv (individual center matrices)")
    print("  - Layout_Edges.csv (for visualization)")

    # print sample from year 4, f=3 configuration
    if 4 in all_results and 3 in all_results[4]:
        print("\n" + "="*80)
        print("SAMPLE: Year 4, f=3 Configuration Flow Summary")
        print("="*80)
        print(all_results[4][3]['flow_summary'].to_string(index=False))


if __name__ == "__main__":
    main()