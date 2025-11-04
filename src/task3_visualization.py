"""
Task 3: Parts-Based Design - Enhanced Analysis with Visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
BASE_DIR = Path(r"d:\Adarsh GATech Files\6335 Benoit SC1\CW3\ISYE6202_CW3")
RESULTS_DIR = BASE_DIR / "results"

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def create_visualizations():
    """
    Create comprehensive visualizations for Task 3 analysis
    """
    
    # Load results
    equipment_df = pd.read_csv(RESULTS_DIR / "Task3_Parts_Based_Equipment_Requirements.csv")
    part_demand_df = pd.read_csv(RESULTS_DIR / "Task3_Weekly_Part_Demand.csv")
    process_freq_df = pd.read_csv(RESULTS_DIR / "Task3_Process_Frequency.csv")
    breakdown_df = pd.read_csv(RESULTS_DIR / "Task3_Process_Workload_Breakdown.csv")
    
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
    
    # 3. Utilization Rates (2-Shift Operation)
    ax3 = plt.subplot(2, 3, 3)
    util_data = equipment_df[equipment_df['Equipment_2_Shifts'] > 0]
    colors_util = ['green' if u >= 95 else 'orange' if u >= 85 else 'red' 
                   for u in util_data['Utilization_2_Shifts']]
    
    bars = ax3.barh(util_data['Process'], util_data['Utilization_2_Shifts'], 
                    color=colors_util, alpha=0.7)
    ax3.set_xlabel('Utilization (%)', fontweight='bold', fontsize=11)
    ax3.set_ylabel('Process', fontweight='bold', fontsize=11)
    ax3.set_title('Equipment Utilization (2-Shift Operation)', fontweight='bold', fontsize=12)
    ax3.axvline(x=95, color='green', linestyle='--', alpha=0.5, label='95% Target')
    ax3.axvline(x=85, color='orange', linestyle='--', alpha=0.5, label='85% Min')
    ax3.legend(loc='lower right', fontsize=9)
    ax3.grid(axis='x', alpha=0.3)
    ax3.set_xlim([0, 105])
    
    # Add percentage labels
    for i, (proc, util) in enumerate(zip(util_data['Process'], util_data['Utilization_2_Shifts'])):
        ax3.text(util, i, f' {util:.1f}%', va='center', fontsize=9)
    
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
    
    # 6. Process Workload Distribution by Part (Top Processes)
    ax6 = plt.subplot(2, 3, 6)
    
    # Get top 5 most demanding processes
    top_processes = equipment_df.nlargest(5, 'Weekly_Hours')['Process'].tolist()
    
    # Filter breakdown for these processes
    top_breakdown = breakdown_df[breakdown_df['Process'].isin(top_processes)]
    
    # Pivot for stacked bar chart
    pivot_data = top_breakdown.pivot_table(
        index='Process', 
        columns='Part', 
        values='Total_Weekly_Minutes', 
        aggfunc='sum',
        fill_value=0
    )
    
    # Convert to hours
    pivot_data = pivot_data / 60
    
    # Plot stacked bar
    pivot_data.plot(kind='bar', stacked=True, ax=ax6, legend=False, 
                    colormap='tab20', alpha=0.8)
    ax6.set_xlabel('Process', fontweight='bold', fontsize=11)
    ax6.set_ylabel('Weekly Hours', fontweight='bold', fontsize=11)
    ax6.set_title('Workload Distribution by Part (Top 5 Processes)', 
                  fontweight='bold', fontsize=12)
    ax6.grid(axis='y', alpha=0.3)
    ax6.set_xticklabels(ax6.get_xticklabels(), rotation=0)
    
    plt.tight_layout()
    
    # Save figure
    output_file = RESULTS_DIR / "Task3_Parts_Based_Analysis_Dashboard.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nSaved visualization: {output_file}")
    
    plt.show()

def generate_summary_report():
    """
    Generate a text summary report
    """
    
    equipment_df = pd.read_csv(RESULTS_DIR / "Task3_Parts_Based_Equipment_Requirements.csv")
    part_demand_df = pd.read_csv(RESULTS_DIR / "Task3_Weekly_Part_Demand.csv")
    process_freq_df = pd.read_csv(RESULTS_DIR / "Task3_Process_Frequency.csv")
    
    report = []
    report.append("="*80)
    report.append("TASK 3: PARTS-BASED DESIGN - EXECUTIVE SUMMARY")
    report.append("="*80)
    report.append("")
    
    # Key findings
    report.append("KEY FINDINGS:")
    report.append("-" * 80)
    report.append("")
    
    # Total equipment
    total_equip_1_shift = equipment_df['Equipment_1_Shift'].sum()
    total_equip_2_shifts = equipment_df['Equipment_2_Shifts'].sum()
    
    report.append(f"1. EQUIPMENT REQUIREMENTS:")
    report.append(f"   • 1-Shift Operation: {total_equip_1_shift} total equipment units")
    report.append(f"   • 2-Shift Operation: {total_equip_2_shifts} total equipment units")
    report.append(f"   • Savings with 2-shift: {total_equip_1_shift - total_equip_2_shifts} units ({(1-total_equip_2_shifts/total_equip_1_shift)*100:.1f}% reduction)")
    report.append("")
    
    # Bottleneck processes
    bottlenecks = equipment_df.nlargest(5, 'Equipment_2_Shifts')[['Process', 'Equipment_2_Shifts', 'Weekly_Hours']]
    report.append("2. BOTTLENECK PROCESSES (Top 5 by Equipment Count):")
    for _, row in bottlenecks.iterrows():
        report.append(f"   • Process {row['Process']}: {int(row['Equipment_2_Shifts'])} units, {row['Weekly_Hours']:.1f} hrs/week")
    report.append("")
    
    # High demand parts
    high_demand = part_demand_df.nlargest(5, 'Weekly_Demand')[['Part', 'Weekly_Demand']]
    report.append("3. HIGHEST DEMAND PARTS (Top 5):")
    for _, row in high_demand.iterrows():
        report.append(f"   • {row['Part']}: {row['Weekly_Demand']:,.0f} units/week")
    report.append("")
    
    # Utilization summary
    avg_util_2_shift = equipment_df[equipment_df['Equipment_2_Shifts'] > 0]['Utilization_2_Shifts'].mean()
    high_util = equipment_df[equipment_df['Utilization_2_Shifts'] >= 95]
    low_util = equipment_df[(equipment_df['Utilization_2_Shifts'] < 90) & (equipment_df['Equipment_2_Shifts'] > 0)]
    
    report.append("4. UTILIZATION ANALYSIS (2-Shift Operation):")
    report.append(f"   • Average utilization: {avg_util_2_shift:.1f}%")
    report.append(f"   • High utilization (>=95%): {len(high_util)} processes")
    report.append(f"   • Low utilization (<90%): {len(low_util)} processes")
    
    if len(low_util) > 0:
        report.append("   • Low utilization processes:")
        for _, row in low_util.iterrows():
            report.append(f"     - Process {row['Process']}: {row['Utilization_2_Shifts']:.1f}%")
    report.append("")
    
    # Process frequency insights
    total_ops = process_freq_df['Operations_Per_Week'].sum()
    top_freq = process_freq_df.nlargest(3, 'Operations_Per_Week')
    
    report.append("5. PROCESS FREQUENCY:")
    report.append(f"   • Total operations per week: {total_ops:,.0f}")
    report.append("   • Most frequent processes:")
    for _, row in top_freq.iterrows():
        pct = (row['Operations_Per_Week'] / total_ops) * 100
        report.append(f"     - Process {row['Process']}: {row['Operations_Per_Week']:,.0f} ops/week ({pct:.1f}%)")
    report.append("")
    
    # Strategic recommendations
    report.append("="*80)
    report.append("STRATEGIC RECOMMENDATIONS:")
    report.append("="*80)
    report.append("")
    report.append("1. OPERATION STRATEGY:")
    report.append("   - Recommend 2-SHIFT operation to minimize equipment investment")
    report.append(f"   - Reduces equipment count by {total_equip_1_shift - total_equip_2_shifts} units")
    report.append(f"   - Maintains high utilization (avg {avg_util_2_shift:.1f}%)")
    report.append("")
    
    report.append("2. CAPACITY PLANNING:")
    report.append(f"   - Focus on bottleneck processes: {', '.join(bottlenecks['Process'].tolist())}")
    report.append("   - Consider equipment flexibility (multi-process machines)")
    report.append("   - Plan for maintenance windows given high utilization")
    report.append("")
    
    report.append("3. PARTS-BASED DESIGN IMPLICATIONS:")
    report.append("   - Each of 20 parts would have dedicated production cell")
    report.append("   - Cells contain all processes needed for that part")
    report.append("   - Simplifies material flow and reduces WIP")
    report.append("   - May duplicate equipment across cells (consider Group Tech)")
    report.append("")
    
    # Process grouping suggestions
    report.append("4. POTENTIAL PROCESS GROUPINGS (for optimization):")
    report.append("   • A-B-C-D group: High interaction in many parts")
    report.append("   • E-F-G group: Similar equipment requirements")
    report.append("   • H-I-J group: Heavy finishing operations")
    report.append("   • K-L-M group: Lightweight operations")
    report.append("")
    
    report.append("="*80)
    
    # Save report
    report_text = '\n'.join(report)
    output_file = RESULTS_DIR / "Task3_Parts_Based_Summary_Report.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(report_text)
    print(f"\nSaved report: {output_file}")

def create_process_matrix():
    """
    Create a matrix showing which processes are used by which parts
    """
    from task3_parts_based_design import load_process_sequences
    
    sequences = load_process_sequences()
    
    # Create matrix
    processes = list('ABCDEFGHIJKLM')
    parts = [f'P{i}' for i in range(1, 21)]
    
    matrix = pd.DataFrame(0, index=parts, columns=processes)
    
    for part, sequence in sequences.items():
        for process in sequence:
            if process in processes:
                matrix.loc[part, process] = 1
    
    # Add totals
    matrix.loc['TOTAL'] = matrix.sum()
    matrix['TOTAL'] = matrix.sum(axis=1)
    
    # Save
    output_file = RESULTS_DIR / "Task3_Process_Part_Matrix.csv"
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
