# Script to create an aggregated flow matrix from all part flow matrices

import pandas as pd
import os

# List of all processes
processes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

# Initialize aggregated flow matrix
total_flow_matrix = pd.DataFrame(0.0, index=processes, columns=processes, dtype=float)

# Path to flow matrices folder
flow_dir = '../results/flow_matrices'

# Read each part's flow matrix and add to total
for filename in os.listdir(flow_dir):
    if filename.endswith('_Flow_Matrix.csv'):
        filepath = os.path.join(flow_dir, filename)
        part_matrix = pd.read_csv(filepath, index_col=0)
        total_flow_matrix += part_matrix

# Save the aggregated flow matrix
total_flow_matrix.to_csv('../results/Functional_Flow_Matrix.csv')
print("Functional flow matrix saved to ../results/Functional_Flow_Matrix.csv")

# Also create a summary showing total flows per process
total_in_flow = total_flow_matrix.sum(axis=0)  # Sum of columns (incoming to each process)
total_out_flow = total_flow_matrix.sum(axis=1)  # Sum of rows (outgoing from each process)

summary_df = pd.DataFrame({
    'Process': processes,
    'Total_In_Flow': total_in_flow.values,
    'Total_Out_Flow': total_out_flow.values
})

summary_df.to_csv('../results/Flow_Matrix_Summary.csv', index=False)
print("Flow matrix summary saved to ../results/Flow_Matrix_Summary.csv")