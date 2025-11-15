import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
RESULTS_DIR = BASE_DIR / "results" / "Task3" / "Part" / "Capacity"

def add_totals_to_machine_requirements_csv(filename):
    """Add row and column totals to Part_Operation_Machine_Requirements CSV"""
    df = pd.read_csv(filename)

    # Calculate row totals (total machines per part)
    df['Total_Machines'] = df.iloc[:, 1:].sum(axis=1)

    # Calculate column totals (total machines per operation)
    column_totals = df.iloc[:, 1:].sum(axis=0)
    column_totals_df = pd.DataFrame([column_totals.values], columns=column_totals.index)
    column_totals_df.insert(0, 'Part', 'TOTAL')

    # Append the totals row
    df_with_totals = pd.concat([df, column_totals_df], ignore_index=True)

    # Save back to CSV
    df_with_totals.to_csv(filename, index=False)
    print(f"Added totals to {filename}")

def add_totals_to_capacity_requirements_csv(filename):
    """Add totals to Part_Step_Process_Capacity_Requirements CSV"""
    df = pd.read_csv(filename)

    # Group by Part and sum Number_of_Machines
    part_totals = df.groupby('Part')['Number_of_Machines'].sum().reset_index()
    part_totals['Step'] = 'TOTAL'
    part_totals['Operation'] = 'ALL'
    part_totals['Weekly_Demand_Units'] = df.groupby('Part')['Weekly_Demand_Units'].first().values
    part_totals['Time_Required_Min_Week'] = df.groupby('Part')['Time_Required_Min_Week'].sum().values

    # Reorder columns to match original
    part_totals = part_totals[['Part', 'Step', 'Operation', 'Weekly_Demand_Units', 'Time_Required_Min_Week', 'Number_of_Machines']]

    # Append totals
    df_with_totals = pd.concat([df, part_totals], ignore_index=True)

    # Sort by Part, then by Step (with TOTAL at end for each part)
    df_with_totals['Step_Order'] = df_with_totals['Step'].apply(lambda x: 999 if x == 'TOTAL' else int(x))
    df_with_totals = df_with_totals.sort_values(['Part', 'Step_Order']).drop('Step_Order', axis=1)

    # Save back to CSV
    df_with_totals.to_csv(filename, index=False)
    print(f"Added totals to {filename}")

def add_totals_to_machines_summary_csv(filename):
    """Add total machines column to Part_Step_Machines_Summary CSV"""
    df = pd.read_csv(filename)

    # Calculate total machines per part by parsing the step columns
    def calculate_total_machines(row):
        total = 0
        for col in df.columns[1:]:  # Skip 'Part' column
            if pd.notna(row[col]) and row[col]:
                # Parse strings like "A: 5.0,B: 3.0" to sum the numbers
                parts = str(row[col]).split(',')
                for part in parts:
                    if ':' in part:
                        try:
                            num = float(part.split(':')[1].strip())
                            total += num
                        except:
                            pass
        return total

    df['Total_Machines'] = df.apply(calculate_total_machines, axis=1)

    # Save back to CSV
    df.to_csv(filename, index=False)
    print(f"Added totals to {filename}")

def create_utilization_matrix():
    """Create utilization matrix showing Parts vs Operations with utilization levels"""
    # Load the detailed capacity requirements for 2 shifts (more realistic scenario)
    detailed_df = pd.read_csv(RESULTS_DIR / "Part_Step_Process_Capacity_Requirements_2_shifts.csv")

    # Load equipment specs to get capacity per machine
    # From the code: capacity_2_shifts = DAYS_PER_WEEK * 2 * MINUTES_PER_SHIFT * EFFECTIVE_AVAILABILITY
    # DAYS_PER_WEEK = 5, MINUTES_PER_SHIFT = 480, EFFECTIVE_AVAILABILITY = 0.882
    capacity_per_machine_2_shifts = 5 * 2 * 480 * 0.882  # = 4233.6 minutes/week

    # Create pivot table: Parts vs Operations showing utilization
    utilization_data = []

    for part in detailed_df['Part'].unique():
        part_data = {'Part': part}
        part_df = detailed_df[detailed_df['Part'] == part]

        for operation in 'ABCDEFGHIJKLM':
            op_data = part_df[part_df['Operation'] == operation]
            if not op_data.empty:
                time_required = op_data['Time_Required_Min_Week'].sum()
                machines = op_data['Number_of_Machines'].iloc[0]  # Same for all rows of same part-operation
                if machines > 0:
                    utilization = (time_required / (machines * capacity_per_machine_2_shifts)) * 100
                    part_data[operation] = round(utilization, 1)
                else:
                    part_data[operation] = 0.0
            else:
                part_data[operation] = 0.0

        utilization_data.append(part_data)

    utilization_df = pd.DataFrame(utilization_data)
    utilization_df = utilization_df.sort_values('Part')

    # Save utilization matrix
    output_file = RESULTS_DIR / "Part_Operation_Utilization_Matrix_2_shifts.csv"
    utilization_df.to_csv(output_file, index=False)
    print(f"Created utilization matrix: {output_file}")

def add_totals_to_equipment_requirements_csv(filename):
    """Add total row to Task3_Parts_Based_Equipment_Requirements CSV"""
    df = pd.read_csv(filename)

    # Calculate totals
    totals = {}
    for col in df.columns[1:]:  # Skip 'Process' column
        if 'Equipment' in col:
            totals[col] = df[col].sum()
        elif 'Utilization' in col:
            # For utilization, calculate weighted average
            equipment_col = col.replace('Utilization_', 'Equipment_')
            if equipment_col in df.columns:
                weighted_sum = (df[col] * df[equipment_col]).sum()
                total_equipment = df[equipment_col].sum()
                totals[col] = weighted_sum / total_equipment if total_equipment > 0 else 0
        else:
            totals[col] = df[col].sum()

    # Create totals row
    totals_row = {'Process': 'TOTAL'}
    totals_row.update(totals)

    # Append totals row
    df_with_totals = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)

    # Save back to CSV
    df_with_totals.to_csv(filename, index=False)
    print(f"Added totals to {filename}")

def add_totals_to_process_frequency_csv(filename):
    """Add total row to Task3_Process_Frequency CSV"""
    df = pd.read_csv(filename)

    # Calculate total operations per week
    total_operations = df['Operations_Per_Week'].sum()

    # Create totals row
    totals_row = {'Process': 'TOTAL', 'Operations_Per_Week': total_operations}

    # Append totals row
    df_with_totals = pd.concat([df, pd.DataFrame([totals_row])], ignore_index=True)

    # Save back to CSV
    df_with_totals.to_csv(filename, index=False)
    print(f"Added totals to {filename}")

def add_totals_to_workload_breakdown_csv(filename):
    """Add subtotals per process to Task3_Process_Workload_Breakdown CSV"""
    df = pd.read_csv(filename)

    # Group by Process and add subtotals
    result_rows = []

    for process in df['Process'].unique():
        process_df = df[df['Process'] == process]
        result_rows.extend(process_df.to_dict('records'))

        # Add subtotal row for this process
        subtotal = {
            'Process': f'SUBTOTAL_{process}',
            'Part': 'ALL',
            'Weekly_Part_Demand': process_df['Weekly_Part_Demand'].sum(),
            'Time_Per_Unit_Minutes': '',  # Not meaningful for subtotal
            'Total_Weekly_Minutes': process_df['Total_Weekly_Minutes'].sum()
        }
        result_rows.append(subtotal)

    # Create new dataframe
    df_with_subtotals = pd.DataFrame(result_rows)

    # Save back to CSV
    df_with_subtotals.to_csv(filename, index=False)
    print(f"Added subtotals to {filename}")

def add_totals_to_flow_matrices():
    """Add row and column totals to all flow matrix CSVs"""
    flow_dir = RESULTS_DIR / "Flow_Matrix"

    for csv_file in flow_dir.glob("*_Flow_Matrix.csv"):
        df = pd.read_csv(csv_file)

        # Check if totals already exist
        if 'TOTAL_OUT' in df.columns or 'TOTAL_IN' in df.iloc[:, 0].values:
            print(f"Totals already exist in {csv_file}")
            continue

        # The first column is the operation names (A, B, C, etc.)
        operations = df.iloc[:, 0].values

        # Add row totals (total flow out of each operation)
        df['TOTAL_OUT'] = df.iloc[:, 1:].sum(axis=1)  # Skip the first column

        # Add column totals (total flow into each operation)
        column_totals = df.iloc[:, 1:].sum(axis=0)
        column_totals_df = pd.DataFrame([column_totals.values], columns=column_totals.index)
        column_totals_df.insert(0, df.columns[0], 'TOTAL_IN')

        # Append the totals row
        df_with_totals = pd.concat([df, column_totals_df], ignore_index=True)

        # Save back to CSV
        df_with_totals.to_csv(csv_file, index=False)
        print(f"Added totals to {csv_file}")

def main():
    print("Adding totals to CSV files...")

    # Add totals to Part_Operation_Machine_Requirements files
    add_totals_to_machine_requirements_csv(RESULTS_DIR / "Part_Operation_Machine_Requirements_1_shifts.csv")
    add_totals_to_machine_requirements_csv(RESULTS_DIR / "Part_Operation_Machine_Requirements_2_shifts.csv")

    # Add totals to Part_Step_Process_Capacity_Requirements files
    add_totals_to_capacity_requirements_csv(RESULTS_DIR / "Part_Step_Process_Capacity_Requirements_1_shifts.csv")
    add_totals_to_capacity_requirements_csv(RESULTS_DIR / "Part_Step_Process_Capacity_Requirements_2_shifts.csv")

    # Add totals to Part_Step_Machines_Summary files
    add_totals_to_machines_summary_csv(RESULTS_DIR / "Part_Step_Machines_Summary_1_shifts.csv")
    add_totals_to_machines_summary_csv(RESULTS_DIR / "Part_Step_Machines_Summary_2_shifts.csv")

    # Create utilization matrix
    create_utilization_matrix()

    # Add totals to other CSV files
    add_totals_to_equipment_requirements_csv(RESULTS_DIR / "Task3_Parts_Based_Equipment_Requirements.csv")
    add_totals_to_process_frequency_csv(RESULTS_DIR / "Task3_Process_Frequency.csv")
    add_totals_to_workload_breakdown_csv(RESULTS_DIR / "Task3_Process_Workload_Breakdown.csv")

    # Add totals to flow matrices
    add_totals_to_flow_matrices()

    print("All updates complete!")

if __name__ == "__main__":
    main()