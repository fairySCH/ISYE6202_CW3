# Script to create flow matrices for each part showing transitions between processes

import pandas as pd
import numpy as np

# Load weekly demand from Task1 results
task1_df = pd.read_csv('../results/Task1_Demand_Fulfillment_Capacity_Plan.csv')
weekly_demand = dict(zip(task1_df['Part'], task1_df['Weekly_Demand_Units']))

# Process operations from Parts Specs
process_operations = {
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

# List of all processes
processes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

# Create flow matrix for each part
for part in process_operations:
    operations = process_operations[part]
    demand = weekly_demand[part]

    # Initialize matrix with float dtype
    flow_matrix = pd.DataFrame(0.0, index=processes, columns=processes, dtype=float)

    # Fill transitions
    for i in range(len(operations) - 1):
        from_op = operations[i]
        to_op = operations[i + 1]
        flow_matrix.loc[from_op, to_op] += demand

    # Save to CSV
    filename = f'../results/Task3/Part/Flow_Matrix/{part}_Flow_Matrix.csv'
    flow_matrix.to_csv(filename)
    print(f"Flow matrix for {part} saved to {filename}")

print("All flow matrices generated!")