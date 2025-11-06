"""
Task 3: Functional Layout - Enhanced Analysis with Visualizations

Creates comprehensive visualizations for functional layout analysis.
Functional layout groups similar processes together for operational efficiency.

This script generates:
1. Equipment requirements comparison charts
2. Process workload distribution
3. Material flow analysis
4. Capacity utilization visualizations

Author: Analysis Team
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
RESULTS_DIR = BASE_DIR / "results" / "Task3" / "Functional"
VISUALS_DIR = RESULTS_DIR / "Visuals"

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def create_functional_visualizations():
    """
    Create comprehensive visualizations for functional layout analysis
    """

    # Load data from capacity analysis
    capacity_dir = RESULTS_DIR / "Capacity"
    equipment_df = pd.read_csv(capacity_dir / "Functional_Equipment_Requirements.csv")
    part_demand_df = pd.read_csv(capacity_dir / "Functional_Weekly_Part_Demand.csv")
    workload_df = pd.read_csv(capacity_dir / "Functional_Process_Workload_Breakdown.csv")

    # Load functional flow matrix
    flow_matrix_df = pd.read_csv(RESULTS_DIR / "Functional_Flow_Matrix.csv", index_col=0)
    flow_summary_df = pd.read_csv(RESULTS_DIR / "Flow_Matrix_Summary.csv")

    # Ensure visuals directory exists
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Create a comprehensive multi-panel figure
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
    ax1.set_title('Functional Layout: Equipment Requirements\n1-Shift vs 2-Shift Operation',
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

    # 2. Weekly Process Workload (Hours) - Functional Layout
    ax2 = plt.subplot(2, 3, 2)
    # Filter out processes with zero workload
    active_equipment = equipment_df[equipment_df['Weekly_Hours'] > 0]
    colors = plt.cm.viridis(np.linspace(0, 1, len(active_equipment)))
    bars = ax2.barh(active_equipment['Process'], active_equipment['Weekly_Hours'],
                    color=colors, alpha=0.8)
    ax2.set_xlabel('Weekly Hours Required', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Process', fontweight='bold', fontsize=11)
    ax2.set_title('Functional Layout: Weekly Workload by Process', fontweight='bold', fontsize=12)
    ax2.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (proc, hours) in enumerate(zip(active_equipment['Process'], active_equipment['Weekly_Hours'])):
        ax2.text(hours, i, f' {hours:.0f}h', va='center', fontsize=9)

    # 3. Material Flow Analysis - Functional Layout
    ax3 = plt.subplot(2, 3, 3)

    # Calculate total flow volume per process (in + out flows)
    process_flow_volume = flow_matrix_df.sum(axis=1) + flow_matrix_df.sum(axis=0)
    process_flow_volume = process_flow_volume[process_flow_volume > 0]

    if len(process_flow_volume) > 0:
        # Sort by flow volume
        process_flow_volume = process_flow_volume.sort_values(ascending=True)
        colors_flow = plt.cm.plasma(np.linspace(0, 1, len(process_flow_volume)))
        bars = ax3.barh(process_flow_volume.index, process_flow_volume.values / 1000,
                        color=colors_flow, alpha=0.8)
        ax3.set_xlabel('Total Flow Volume (thousands)', fontweight='bold', fontsize=11)
        ax3.set_ylabel('Process', fontweight='bold', fontsize=11)
        ax3.set_title('Functional Layout: Process Flow Volume', fontweight='bold', fontsize=12)
        ax3.grid(axis='x', alpha=0.3)

        # Add value labels for top flows
        for i, (proc, flow) in enumerate(zip(process_flow_volume.index, process_flow_volume.values)):
            if i >= len(process_flow_volume) - 3:  # Top 3
                ax3.text(flow/1000, i, f' {flow/1000:.1f}k', va='center', fontsize=8)
    else:
        ax3.text(0.5, 0.5, 'No flow data available',
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Functional Layout: Process Flow Volume', fontweight='bold', fontsize=12)

    # 4. Equipment Utilization Analysis
    ax4 = plt.subplot(2, 3, 4)

    # Filter for active processes and sort by utilization
    active_processes = equipment_df[equipment_df['Equipment_2_Shifts'] > 0].copy()
    active_processes = active_processes.sort_values('Utilization_2_Shifts', ascending=True)

    if len(active_processes) > 0:
        colors_util = plt.cm.RdYlGn(np.linspace(0, 1, len(active_processes)))
        bars = ax4.barh(active_processes['Process'], active_processes['Utilization_2_Shifts'],
                        color=colors_util, alpha=0.8)
        ax4.set_xlabel('Utilization Percentage (%)', fontweight='bold', fontsize=11)
        ax4.set_ylabel('Process', fontweight='bold', fontsize=11)
        ax4.set_title('Functional Layout: Equipment Utilization\n(2-Shift Operation)', fontweight='bold', fontsize=12)
        ax4.grid(axis='x', alpha=0.3)
        ax4.set_xlim(0, 100)

        # Add value labels
        for i, (proc, util) in enumerate(zip(active_processes['Process'], active_processes['Utilization_2_Shifts'])):
            ax4.text(util, i, f' {util:.1f}%', va='center', fontsize=9)
    else:
        ax4.text(0.5, 0.5, 'No active processes',
                ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('Functional Layout: Equipment Utilization', fontweight='bold', fontsize=12)

    # 5. Process Workload Distribution by Part Contribution
    ax5 = plt.subplot(2, 3, 5)

    # Group workload by process and calculate part contributions
    if not workload_df.empty:
        process_part_contribution = workload_df.groupby(['Process', 'Part'])['Total_Weekly_Minutes'].sum().unstack().fillna(0)

        # Get top processes by total workload
        process_totals = process_part_contribution.sum(axis=1).sort_values(ascending=False).head(5)
        top_processes = process_totals.index.tolist()

        # Create stacked bar chart for top processes
        if len(top_processes) > 0:
            data_to_plot = process_part_contribution.loc[top_processes].copy()
            data_to_plot = data_to_plot.div(data_to_plot.sum(axis=1), axis=0) * 100  # Convert to percentages

            # Plot only top contributing parts per process
            data_to_plot = data_to_plot.apply(lambda x: x.nlargest(3), axis=1).fillna(0)

            data_to_plot.plot(kind='bar', stacked=True, ax=ax5, colormap='tab20', alpha=0.8)
            ax5.set_xlabel('Process', fontweight='bold', fontsize=11)
            ax5.set_ylabel('Workload Contribution (%)', fontweight='bold', fontsize=11)
            ax5.set_title('Top 5 Processes: Part Contribution to Workload', fontweight='bold', fontsize=12)
            ax5.legend(title='Part', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax5.grid(axis='y', alpha=0.3)
        else:
            ax5.text(0.5, 0.5, 'No workload data available',
                    ha='center', va='center', transform=ax5.transAxes)
            ax5.set_title('Process Workload Distribution', fontweight='bold', fontsize=12)
    else:
        ax5.text(0.5, 0.5, 'No workload data available',
                ha='center', va='center', transform=ax5.transAxes)
        ax5.set_title('Process Workload Distribution', fontweight='bold', fontsize=12)

    # 6. Functional Layout Efficiency Metrics Summary
    ax6 = plt.subplot(2, 3, 6)

    # Load efficiency metrics
    efficiency_df = pd.read_csv(capacity_dir / "Functional_Layout_Efficiency_Metrics.csv")

    if not efficiency_df.empty:
        metrics = efficiency_df.iloc[0]

        # Create a simple bar chart of key metrics
        categories = ['Active Processes', 'Total Equipment\n(2 shifts)', 'Workload\n(Hours)', 'Avg Utilization\n(%)']
        values = [
            metrics['active_processes'],
            metrics['total_equipment_2shifts'],
            metrics['total_workload_hours'] / 100,  # Scale down for visibility
            metrics['average_utilization']
        ]

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        bars = ax6.bar(categories, values, color=colors, alpha=0.8)
        ax6.set_ylabel('Value', fontweight='bold', fontsize=11)
        ax6.set_title('Functional Layout Efficiency Metrics', fontweight='bold', fontsize=12)
        ax6.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar, value, category in zip(bars, values, categories):
            height = bar.get_height()
            if 'Workload' in category:
                ax6.text(bar.get_x() + bar.get_width()/2., height,
                        f'{metrics["total_workload_hours"]:,.0f}',
                        ha='center', va='bottom', fontsize=9)
            else:
                ax6.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}',
                        ha='center', va='bottom', fontsize=9)
    else:
        ax6.text(0.5, 0.5, 'Efficiency metrics not available',
                ha='center', va='center', transform=ax6.transAxes)
        ax6.set_title('Functional Layout Efficiency Metrics', fontweight='bold', fontsize=12)

    # Adjust layout and save
    plt.tight_layout()
    output_file = VISUALS_DIR / "Functional_Layout_Comprehensive_Analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Comprehensive analysis visualization saved: {output_file}")

    # Create additional focused visualizations

    # 1. Process Flow Heatmap
    plt.figure(figsize=(12, 10))
    if not flow_matrix_df.empty:
        # Create mask for zero values
        mask = flow_matrix_df == 0

        # Create heatmap
        sns.heatmap(flow_matrix_df, annot=True, fmt='.0f', cmap='YlOrRd',
                   mask=mask, cbar_kws={'label': 'Flow Units'}, square=True)

        plt.title('Functional Layout: Process-to-Process Flow Matrix', fontweight='bold', fontsize=14)
        plt.xlabel('To Process', fontweight='bold')
        plt.ylabel('From Process', fontweight='bold')

        output_file = VISUALS_DIR / "Functional_Flow_Matrix_Heatmap.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Flow matrix heatmap saved: {output_file}")

    # 2. Equipment Requirements Summary Chart
    plt.figure(figsize=(15, 8))

    # Prepare data for equipment summary
    equip_summary = equipment_df[equipment_df['Equipment_2_Shifts'] > 0].copy()
    equip_summary = equip_summary.sort_values('Equipment_2_Shifts', ascending=True)

    if len(equip_summary) > 0:
        # Create horizontal bar chart with utilization as color
        norm = plt.Normalize(equip_summary['Utilization_2_Shifts'].min(),
                           equip_summary['Utilization_2_Shifts'].max())
        colors = plt.cm.RdYlGn(norm(equip_summary['Utilization_2_Shifts']))

        bars = plt.barh(equip_summary['Process'], equip_summary['Equipment_2_Shifts'],
                       color=colors, alpha=0.8)

        # Add colorbar
        sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=plt.gca())
        cbar.set_label('Equipment Utilization (%)', fontweight='bold')

        plt.xlabel('Number of Equipment Units', fontweight='bold', fontsize=12)
        plt.ylabel('Process', fontweight='bold', fontsize=12)
        plt.title('Functional Layout: Equipment Requirements by Process\n(2-Shift Operation, Color = Utilization)',
                 fontweight='bold', fontsize=14)
        plt.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (proc, equip, util) in enumerate(zip(equip_summary['Process'],
                                                   equip_summary['Equipment_2_Shifts'],
                                                   equip_summary['Utilization_2_Shifts'])):
            plt.text(equip, i, f' {int(equip)} ({util:.1f}%)', va='center', fontsize=10)

        output_file = VISUALS_DIR / "Functional_Equipment_Summary.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Equipment summary saved: {output_file}")

    print(f"\nAll visualizations saved to: {VISUALS_DIR}")

def create_summary_report():
    """
    Create a comprehensive summary report for functional layout analysis
    """
    capacity_dir = RESULTS_DIR / "Capacity"

    # Load all data
    equipment_df = pd.read_csv(capacity_dir / "Functional_Equipment_Requirements.csv")
    efficiency_df = pd.read_csv(capacity_dir / "Functional_Layout_Efficiency_Metrics.csv")
    flow_summary_df = pd.read_csv(RESULTS_DIR / "Flow_Matrix_Summary.csv")

    # Generate summary report
    report = f"""
FUNCTIONAL LAYOUT ANALYSIS - COMPREHENSIVE SUMMARY REPORT
{'='*65}

ANALYSIS OVERVIEW:
The functional layout analysis evaluates organizing production by process type,
grouping similar operations together to maximize efficiency and minimize material handling.

KEY FINDINGS:
"""

    if not efficiency_df.empty:
        metrics = efficiency_df.iloc[0]
        report += f"""
• Active Processes: {metrics['active_processes']}/13 total processes utilized
• Total Equipment Required (2 shifts): {int(metrics['total_equipment_2shifts'])} units
• Total Weekly Workload: {metrics['total_workload_hours']:,.1f} hours
• Average Equipment Utilization: {metrics['average_utilization']:.1f}%
"""

    if not equipment_df.empty:
        active_equip = equipment_df[equipment_df['Equipment_2_Shifts'] > 0]
        high_util = active_equip[active_equip['Utilization_2_Shifts'] > 80]
        low_util = active_equip[active_equip['Utilization_2_Shifts'] < 60]

        report += f"""
• High Utilization Processes (>80%): {len(high_util)} processes
• Low Utilization Processes (<60%): {len(low_util)} processes
"""

    report += f"""

EQUIPMENT REQUIREMENTS BY PROCESS (2-Shift Operation):
{'-'*50}
"""

    if not equipment_df.empty:
        for _, row in equipment_df.iterrows():
            if row['Equipment_2_Shifts'] > 0:
                report += f"Process {row['Process']}: {int(row['Equipment_2_Shifts'])} units ({row['Utilization_2_Shifts']:.1f}% utilization)\n"

    report += f"""

MATERIAL FLOW ANALYSIS:
{'-'*25}
"""

    if not flow_summary_df.empty:
        total_flow = flow_summary_df['Total_In_Flow'].sum() + flow_summary_df['Total_Out_Flow'].sum()
        report += f"Total material flow volume: {total_flow:,.1f} units per week\n\n"

        # Top flow processes
        flow_summary_df['Total_Flow'] = flow_summary_df['Total_In_Flow'] + flow_summary_df['Total_Out_Flow']
        top_flow_processes = flow_summary_df.nlargest(3, 'Total_Flow')
        report += "Top 3 processes by flow volume:\n"
        for _, row in top_flow_processes.iterrows():
            report += f"  Process {row['Process']}: {row['Total_Flow']:,.1f} units/week\n"

    report += f"""

FUNCTIONAL LAYOUT ADVANTAGES:
{'-'*30}
• Specialized equipment grouping improves process efficiency
• Easier supervision and quality control per process type
• Simplified maintenance and equipment management
• Better skill specialization for operators
• Reduced setup times for similar operations

FUNCTIONAL LAYOUT CHALLENGES:
{'-'*30}
• Higher material handling requirements between processes
• Work-in-progress inventory accumulation
• Complex material flow patterns
• Potential bottlenecks at high-volume processes
• Longer production lead times

RECOMMENDATIONS:
{'-'*15}
1. Focus on balancing process capacities to avoid bottlenecks
2. Optimize material handling systems between functional areas
3. Implement pull systems to reduce work-in-progress
4. Consider hybrid layouts for high-volume product families
5. Regular monitoring of process utilization and flow efficiency

VISUALIZATIONS GENERATED:
{'-'*25}
• Comprehensive analysis dashboard (6-panel chart)
• Process flow matrix heatmap
• Equipment requirements summary with utilization

All results and visualizations saved to: {RESULTS_DIR}
"""

    # Save report
    output_file = RESULTS_DIR / "Functional_Layout_Analysis_Report.txt"
    with open(output_file, 'w') as f:
        f.write(report)

    print(f"Summary report saved: {output_file}")

def main():
    """
    Main function to run functional layout visualization analysis
    """
    print("="*80)
    print("TASK 3: FUNCTIONAL LAYOUT - VISUALIZATION ANALYSIS")
    print("="*80)

    try:
        # Create visualizations
        print("\n1. Creating comprehensive visualizations...")
        create_functional_visualizations()

        # Create summary report
        print("\n2. Generating summary report...")
        create_summary_report()

        print("\n" + "="*80)
        print("FUNCTIONAL LAYOUT VISUALIZATION ANALYSIS COMPLETE!")
        print("="*80)
        print(f"All results saved to: {RESULTS_DIR}")
        print("="*80)

    except Exception as e:
        print(f"Error during analysis: {e}")
        print("Please ensure capacity analysis has been run first.")

if __name__ == "__main__":
    main()