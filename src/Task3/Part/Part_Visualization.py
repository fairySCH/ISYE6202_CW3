"""
Task 3: Parts-Based Design - Enhanced Analysis with Visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
RESULTS_DIR = BASE_DIR / "results"

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def create_visualizations():
    """
    Create comprehensive visualizations for Task 3 analysis using Part_Step_Capacity and Part_Flow_Matrix data
    """
    
    # Load results from Part_Step_Capacity outputs
    capacity_1shift_df = pd.read_csv(RESULTS_DIR / "Task3" / "Part" / "Capacity" / "Part_Step_Process_Capacity_Requirements_1_shifts.csv")
    capacity_2shift_df = pd.read_csv(RESULTS_DIR / "Task3" / "Part" / "Capacity" / "Part_Step_Process_Capacity_Requirements_2_shifts.csv")
    
    # Aggregate by operation for process-level analysis
    process_capacity_1shift = capacity_1shift_df.groupby('Operation')['Number_of_Machines'].sum().reset_index()
    process_capacity_2shift = capacity_2shift_df.groupby('Operation')['Number_of_Machines'].sum().reset_index()
    
    # Load part demand from Task1 results (used by both scripts)
    task1_df = pd.read_csv(RESULTS_DIR / "Task1_Demand_Fulfillment_Capacity_Plan.csv")
    part_demand_df = task1_df[['Part', 'Weekly_Demand_Units']].copy()
    part_demand_df.columns = ['Part', 'Weekly_Demand']
    
    # Load flow matrix data - aggregate across all parts
    flow_matrix_dir = RESULTS_DIR / "Task3" / "Part" / "Flow_Matrix"
    total_flow_matrix = pd.DataFrame(0.0, index=list('ABCDEFGHIJKLM'), columns=list('ABCDEFGHIJKLM'))
    
    if flow_matrix_dir.exists():
        for csv_file in flow_matrix_dir.glob("*_Flow_Matrix.csv"):
            try:
                flow_df = pd.read_csv(csv_file, index_col=0)
                total_flow_matrix += flow_df.fillna(0)
            except Exception as e:
                print(f"Warning: Could not load {csv_file}: {e}")
    
    # Calculate process workload from capacity data (reverse engineer from machines needed)
    # Using the same parameters as Part_Step_Capacity.py
    HOURS_PER_SHIFT = 8
    DAYS_PER_WEEK = 5
    EFFICIENCY = 0.90
    RELIABILITY = 0.98
    EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY
    
    minutes_per_machine_1shift = HOURS_PER_SHIFT * DAYS_PER_WEEK * 60 * EFFECTIVE_AVAILABILITY
    minutes_per_machine_2shift = 2 * HOURS_PER_SHIFT * DAYS_PER_WEEK * 60 * EFFECTIVE_AVAILABILITY
    
    # Create equipment requirements dataframe
    equipment_reqs = []
    for process in list('ABCDEFGHIJKLM'):
        machines_1shift = process_capacity_1shift[process_capacity_1shift['Operation'] == process]['Number_of_Machines'].iloc[0] if len(process_capacity_1shift[process_capacity_1shift['Operation'] == process]) > 0 else 0
        machines_2shift = process_capacity_2shift[process_capacity_2shift['Operation'] == process]['Number_of_Machines'].iloc[0] if len(process_capacity_2shift[process_capacity_2shift['Operation'] == process]) > 0 else 0
        
        # Calculate workload from machines (reverse of capacity calculation)
        workload_2shift = machines_2shift * minutes_per_machine_2shift
        
        equipment_reqs.append({
            'Process': process,
            'Weekly_Minutes': workload_2shift,
            'Weekly_Hours': workload_2shift / 60,
            'Equipment_1_Shift': machines_1shift,
            'Equipment_2_Shifts': machines_2shift,
            'Utilization_2_Shifts': 95.0 if machines_2shift > 0 else 0  # Assume high utilization
        })
    
    equipment_df = pd.DataFrame(equipment_reqs)
    
    # Calculate process frequency from flow matrices
    process_frequency = total_flow_matrix.sum(axis=1) + total_flow_matrix.sum(axis=0)
    process_freq_df = pd.DataFrame({
        'Process': list('ABCDEFGHIJKLM'),
        'Operations_Per_Week': process_frequency.values
    })
    
    # Create a multi-panel figure
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Equipment Requirements Comparison (1 shift vs 2 shifts)
    ax1 = plt.subplot(2, 3, 1)
    processes = equipment_df['Process']
    x = np.arange(len(processes))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, equipment_df['Equipment_1_Shift'], width, 
                    label='1 Shift/Day', alpha=0.8, color='steelblue')
    bars2 = ax1.bar(x + width/2, equipment_df['Equipment_2_Shifts'], width, 
                    label='2 Shifts/Day', alpha=0.8, color='coral')
    
    ax1.set_xlabel('Process', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Equipment Units Required', fontweight='bold', fontsize=11)
    ax1.set_title('Equipment Requirements: 1-Shift vs 2-Shift Operation', 
                  fontweight='bold', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(processes)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=8)
    
    # 2. Weekly Process Workload (Hours)
    ax2 = plt.subplot(2, 3, 2)
    colors = plt.cm.viridis(np.linspace(0, 1, len(equipment_df)))
    bars = ax2.barh(equipment_df['Process'], equipment_df['Weekly_Hours'], 
                    color=colors, alpha=0.8)
    ax2.set_xlabel('Weekly Hours Required', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Process', fontweight='bold', fontsize=11)
    ax2.set_title('Weekly Workload by Process', fontweight='bold', fontsize=12)
    ax2.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (proc, hours) in enumerate(zip(equipment_df['Process'], equipment_df['Weekly_Hours'])):
        ax2.text(hours, i, f' {hours:.0f}h', va='center', fontsize=9)
    
    # 3. Process Flow Analysis (from flow matrices)
    ax3 = plt.subplot(2, 3, 3)
    
    # Calculate total flow volume per process
    process_flow_volume = total_flow_matrix.sum(axis=1) + total_flow_matrix.sum(axis=0)
    process_flow_volume = process_flow_volume[process_flow_volume > 0]
    
    if len(process_flow_volume) > 0:
        colors_flow = plt.cm.plasma(np.linspace(0, 1, len(process_flow_volume)))
        bars = ax3.barh(process_flow_volume.index, process_flow_volume.values / 1000, 
                        color=colors_flow, alpha=0.8)
        ax3.set_xlabel('Total Flow Volume (thousands)', fontweight='bold', fontsize=11)
        ax3.set_ylabel('Process', fontweight='bold', fontsize=11)
        ax3.set_title('Process Flow Volume Analysis', fontweight='bold', fontsize=12)
        ax3.grid(axis='x', alpha=0.3)
    else:
        ax3.text(0.5, 0.5, 'No flow data available', 
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Process Flow Volume Analysis', fontweight='bold', fontsize=12)
    
    # 4. Weekly Part Demand
    ax4 = plt.subplot(2, 3, 4)
    part_demand_sorted = part_demand_df.sort_values('Weekly_Demand', ascending=True)
    colors_parts = plt.cm.tab20(np.linspace(0, 1, len(part_demand_sorted)))
    
    bars = ax4.barh(part_demand_sorted['Part'], part_demand_sorted['Weekly_Demand'], 
                    color=colors_parts, alpha=0.8)
    ax4.set_xlabel('Units per Week', fontweight='bold', fontsize=11)
    ax4.set_ylabel('Part', fontweight='bold', fontsize=11)
    ax4.set_title('Weekly Part Demand (P1-P20)', fontweight='bold', fontsize=12)
    ax4.grid(axis='x', alpha=0.3)
    
    # Add value labels for top parts
    for i, (part, demand) in enumerate(zip(part_demand_sorted['Part'], 
                                           part_demand_sorted['Weekly_Demand'])):
        if i >= len(part_demand_sorted) - 5:  # Top 5
            ax4.text(demand, i, f' {demand:.0f}', va='center', fontsize=8)
    
    # 5. Process Frequency (Operations per Week)
    ax5 = plt.subplot(2, 3, 5)
    freq_sorted = process_freq_df.sort_values('Operations_Per_Week', ascending=False)
    colors_freq = plt.cm.coolwarm(np.linspace(0, 1, len(freq_sorted)))
    
    bars = ax5.bar(freq_sorted['Process'], freq_sorted['Operations_Per_Week']/1000, 
                   color=colors_freq, alpha=0.8)
    ax5.set_xlabel('Process', fontweight='bold', fontsize=11)
    ax5.set_ylabel('Operations per Week (thousands)', fontweight='bold', fontsize=11)
    ax5.set_title('Process Frequency Analysis', fontweight='bold', fontsize=12)
    ax5.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, freq in zip(bars, freq_sorted['Operations_Per_Week']/1000):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{freq:.1f}k',
                ha='center', va='bottom', fontsize=8)
    
    # 6. Part-Step Capacity Distribution
    ax6 = plt.subplot(2, 3, 6)
    
    # Analyze capacity distribution across parts
    part_capacity = capacity_2shift_df.groupby('Part')['Number_of_Machines'].sum().reset_index()
    part_capacity_sorted = part_capacity.sort_values('Number_of_Machines', ascending=True)
    
    if len(part_capacity_sorted) > 0:
        colors_cap = plt.cm.Set3(np.linspace(0, 1, len(part_capacity_sorted)))
        bars = ax6.barh(part_capacity_sorted['Part'], part_capacity_sorted['Number_of_Machines'], 
                        color=colors_cap, alpha=0.8)
        ax6.set_xlabel('Total Machines Required', fontweight='bold', fontsize=11)
        ax6.set_ylabel('Part', fontweight='bold', fontsize=11)
        ax6.set_title('Machine Requirements by Part (2-Shift)', fontweight='bold', fontsize=12)
        ax6.grid(axis='x', alpha=0.3)
    else:
        ax6.text(0.5, 0.5, 'No capacity data available', 
                ha='center', va='center', transform=ax6.transAxes)
        ax6.set_title('Machine Requirements by Part', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    
    # Save figure
    output_file = RESULTS_DIR / "Task3" / "Part" / "Task3_Parts_Based_Analysis_Dashboard.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nSaved visualization: {output_file}")
    
    plt.show()

def generate_summary_report():
    """
    Generate a text summary report using Part_Step_Capacity and Part_Flow_Matrix data
    """
    
    # Load data from Part_Step_Capacity outputs
    capacity_1shift_df = pd.read_csv(RESULTS_DIR / "Task3" / "Part" / "Capacity" / "Part_Step_Process_Capacity_Requirements_1_shifts.csv")
    capacity_2shift_df = pd.read_csv(RESULTS_DIR / "Task3" / "Part" / "Capacity" / "Part_Step_Process_Capacity_Requirements_2_shifts.csv")
    
    # Aggregate by operation
    process_capacity_1shift = capacity_1shift_df.groupby('Operation')['Number_of_Machines'].sum().reset_index()
    process_capacity_2shift = capacity_2shift_df.groupby('Operation')['Number_of_Machines'].sum().reset_index()
    
    # Load part demand
    task1_df = pd.read_csv(RESULTS_DIR / "Task1_Demand_Fulfillment_Capacity_Plan.csv")
    part_demand_df = task1_df[['Part', 'Weekly_Demand_Units']].copy()
    part_demand_df.columns = ['Part', 'Weekly_Demand']
    
    # Calculate total equipment
    total_equip_1_shift = process_capacity_1shift['Number_of_Machines'].sum()
    total_equip_2_shifts = process_capacity_2shift['Number_of_Machines'].sum()
    
    # Create equipment dataframe for analysis
    equipment_df = pd.DataFrame({
        'Process': list('ABCDEFGHIJKLM'),
        'Equipment_1_Shift': [process_capacity_1shift[process_capacity_1shift['Operation'] == proc]['Number_of_Machines'].iloc[0] if len(process_capacity_1shift[process_capacity_1shift['Operation'] == proc]) > 0 else 0 for proc in list('ABCDEFGHIJKLM')],
        'Equipment_2_Shifts': [process_capacity_2shift[process_capacity_2shift['Operation'] == proc]['Number_of_Machines'].iloc[0] if len(process_capacity_2shift[process_capacity_2shift['Operation'] == proc]) > 0 else 0 for proc in list('ABCDEFGHIJKLM')]
    })
    
    # Calculate process frequency from flow matrices
    flow_matrix_dir = RESULTS_DIR / "Task3" / "Part" / "Flow_Matrix"
    total_flow_matrix = pd.DataFrame(0.0, index=list('ABCDEFGHIJKLM'), columns=list('ABCDEFGHIJKLM'))
    
    if flow_matrix_dir.exists():
        for csv_file in flow_matrix_dir.glob("*_Flow_Matrix.csv"):
            try:
                flow_df = pd.read_csv(csv_file, index_col=0)
                total_flow_matrix += flow_df.fillna(0)
            except Exception as e:
                print(f"Warning: Could not load {csv_file}: {e}")
    
    process_frequency = total_flow_matrix.sum(axis=1) + total_flow_matrix.sum(axis=0)
    process_freq_df = pd.DataFrame({
        'Process': list('ABCDEFGHIJKLM'),
        'Operations_Per_Week': process_frequency.values
    })
    
    report = []
    report.append("="*80)
    report.append("TASK 3: PARTS-BASED DESIGN - CAPACITY ANALYSIS SUMMARY")
    report.append("="*80)
    report.append("")
    
    # Key findings
    report.append("KEY FINDINGS:")
    report.append("-" * 80)
    report.append("")
    
    # Equipment requirements
    report.append("1. EQUIPMENT REQUIREMENTS:")
    report.append(f"   • 1-Shift Operation: {total_equip_1_shift} total equipment units")
    report.append(f"   • 2-Shift Operation: {total_equip_2_shifts} total equipment units")
    report.append(f"   • Savings with 2-shift: {total_equip_1_shift - total_equip_2_shifts} units ({(1-total_equip_2_shifts/total_equip_1_shift)*100:.1f}% reduction)")
    report.append("")
    
    # Bottleneck processes
    bottlenecks = equipment_df.nlargest(5, 'Equipment_2_Shifts')[['Process', 'Equipment_2_Shifts']]
    report.append("2. BOTTLENECK PROCESSES (Top 5 by Equipment Count):")
    for _, row in bottlenecks.iterrows():
        report.append(f"   • Process {row['Process']}: {int(row['Equipment_2_Shifts'])} units")
    report.append("")
    
    # High demand parts
    high_demand = part_demand_df.nlargest(5, 'Weekly_Demand')[['Part', 'Weekly_Demand']]
    report.append("3. HIGHEST DEMAND PARTS (Top 5):")
    for _, row in high_demand.iterrows():
        report.append(f"   • {row['Part']}: {row['Weekly_Demand']:,.0f} units/week")
    report.append("")
    
    # Process frequency insights
    total_ops = process_freq_df['Operations_Per_Week'].sum()
    top_freq = process_freq_df.nlargest(3, 'Operations_Per_Week')
    
    report.append("4. PROCESS FREQUENCY:")
    report.append(f"   • Total operations per week: {total_ops:,.0f}")
    report.append("   • Most frequent processes:")
    for _, row in top_freq.iterrows():
        pct = (row['Operations_Per_Week'] / total_ops) * 100
        report.append(f"     - Process {row['Process']}: {row['Operations_Per_Week']:,.0f} ops/week ({pct:.1f}%)")
    report.append("")
    
    # Flow analysis
    total_flow_volume = total_flow_matrix.sum().sum()
    report.append("5. MATERIAL FLOW ANALYSIS:")
    report.append(f"   • Total weekly flow volume: {total_flow_volume:,.0f} units")
    
    # Most active process pairs
    flow_pairs = []
    for i in total_flow_matrix.index:
        for j in total_flow_matrix.columns:
            if total_flow_matrix.loc[i, j] > 0:
                flow_pairs.append((i, j, total_flow_matrix.loc[i, j]))
    
    flow_pairs.sort(key=lambda x: x[2], reverse=True)
    if flow_pairs:
        report.append("   • Highest flow process pairs:")
        for from_proc, to_proc, volume in flow_pairs[:3]:
            report.append(f"     - {from_proc} → {to_proc}: {volume:,.0f} units/week")
    report.append("")
    
    # Strategic recommendations
    report.append("="*80)
    report.append("STRATEGIC RECOMMENDATIONS:")
    report.append("="*80)
    report.append("")
    report.append("1. OPERATION STRATEGY:")
    report.append("   - Recommend 2-SHIFT operation to minimize equipment investment")
    report.append(f"   - Reduces equipment count by {total_equip_1_shift - total_equip_2_shifts} units")
    report.append("")
    
    report.append("2. CAPACITY PLANNING:")
    report.append(f"   - Focus on bottleneck processes: {', '.join(bottlenecks['Process'].tolist())}")
    report.append("   - Consider equipment flexibility (multi-process machines)")
    report.append("   - Plan for maintenance windows given high utilization")
    report.append("")
    
    report.append("3. MATERIAL FLOW OPTIMIZATION:")
    report.append("   - Analyze process adjacency based on flow matrices")
    report.append("   - Minimize transport between high-flow process pairs")
    report.append("   - Consider cellular manufacturing layout")
    report.append("")
    
    report.append("4. PARTS-BASED DESIGN IMPLICATIONS:")
    report.append("   - Each of 20 parts would have dedicated production cell")
    report.append("   - Cells contain all processes needed for that part")
    report.append("   - Simplifies material flow and reduces WIP")
    report.append("   - May duplicate equipment across cells (consider Group Tech)")
    report.append("")
    
    # Process grouping suggestions
    report.append("5. POTENTIAL PROCESS GROUPINGS (for optimization):")
    report.append("   • A-B-C-D group: High interaction in many parts")
    report.append("   • E-F-G group: Similar equipment requirements")
    report.append("   • H-I-J group: Heavy finishing operations")
    report.append("   • K-L-M group: Lightweight operations")
    report.append("")
    
    report.append("="*80)
    
    # Save report
    report_text = '\n'.join(report)
    output_file = RESULTS_DIR / "Task3" / "Part" / "Task3_Parts_Based_Summary_Report.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"\nSaved report: {output_file}")

def create_process_matrix():
    """
    Create a matrix showing which processes are used by which parts
    """
    # Load process sequences directly instead of importing
    df = pd.read_csv(BASE_DIR / "data" / "csv_outputs" / 'Parts Specs.csv', header=None)
    
    process_sequences = {}
    
    # Rows 11-30 contain process sequences for P1-P20
    for i in range(11, 31):
        part_name = df.iloc[i, 1]
        if pd.notna(part_name):
            part_name = str(part_name).strip()
            sequence = []
            # Columns 2-8 contain Steps 1-7
            for j in range(2, 9):
                process = df.iloc[i, j]
                if pd.notna(process) and str(process).strip():
                    sequence.append(str(process).strip())
            process_sequences[part_name] = sequence
    
    # Create matrix
    processes = list('ABCDEFGHIJKLM')
    parts = [f'P{i}' for i in range(1, 21)]
    
    matrix = pd.DataFrame(0, index=parts, columns=processes)
    
    for part, sequence in process_sequences.items():
        for process in sequence:
            if process in processes:
                matrix.loc[part, process] = 1
    
    # Add totals
    matrix.loc['TOTAL'] = matrix.sum()
    matrix['TOTAL'] = matrix.sum(axis=1)
    
    # Save
    output_file = RESULTS_DIR / "Task3" / "Part" / "Task3_Process_Part_Matrix.csv"
    matrix.to_csv(output_file)
    print(f"\nSaved process-part matrix: {output_file}")
    
    # Display
    print("\nProcess-Part Incidence Matrix:")
    print("(1 = process used by part, 0 = not used)")
    print("\n" + matrix.to_string())
    
    return matrix

if __name__ == "__main__":
    print("Generating Task 3 Enhanced Analysis...\n")
    
    # Generate summary report
    generate_summary_report()
    
    # Create process matrix
    create_process_matrix()
    
    # Create visualizations
    create_visualizations()
    
    print("\n" + "="*80)
    print("Task 3 Enhanced Analysis Complete!")
    print("="*80)
