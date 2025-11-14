"""
task 4: functional layout - enhanced analysis with visualizations (years 2-5)

creates comprehensive visualizations for functional layout analysis across years 2-5.
functional layout groups similar processes together for operational efficiency.

this script generates:
1. equipment requirements comparison charts by year
2. process workload distribution by year
3. material flow analysis by year
4. capacity utilization visualizations by year
5. year-over-year trend analysis

author: machas^2 team
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
RESULTS_DIR = BASE_DIR / "results" / "task4" / "functional"
VISUALS_DIR = RESULTS_DIR / "Visuals"

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def create_functional_visualizations():
    """
    Create comprehensive visualizations for functional layout analysis across years
    """

    # Load data from capacity and cost analysis
    capacity_dir = RESULTS_DIR / "Capacity"
    cost_dir = RESULTS_DIR / "Cost_Analysis"

    equipment_df = pd.read_csv(capacity_dir / "Functional_Equipment_Requirements_All_Years.csv")
    part_demand_df = pd.read_csv(capacity_dir / "Functional_Weekly_Part_Demand_All_Years.csv")
    workload_df = pd.read_csv(capacity_dir / "Functional_Process_Workload_Breakdown_All_Years.csv")

    # Load functional flow matrix data
    flow_summary_df = pd.read_csv(RESULTS_DIR / "AllYears_Flow_Matrix_Summary.csv")

    # load cost data if available
    try:
        capital_df = pd.read_csv(cost_dir / "Functional_Capital_Costs_All_Years.csv")
        operating_df = pd.read_csv(cost_dir / "Functional_Operating_Costs_All_Years.csv")
        cost_data_available = True
    except FileNotFoundError:
        cost_data_available = False
        print("Cost data not found - some visualizations will be skipped")

    # ensure visuals directory exists
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # create a comprehensive multi-panel figure for year +5 (most recent)
    year5_equipment = equipment_df[equipment_df['Year'] == '+5']
    year5_part_demand = part_demand_df[part_demand_df['Year'] == '+5']
    year5_workload = workload_df[workload_df['Year'] == '+5']

    if not year5_equipment.empty:
        fig = plt.figure(figsize=(20, 12))

        # 1. equipment requirements comparison (1 shift vs 2 shifts) - year +5
        ax1 = plt.subplot(2, 3, 1)
        processes = year5_equipment['Process']
        x = np.arange(len(processes))
        width = 0.35

        bars1 = ax1.bar(x - width/2, year5_equipment['Equipment_1_Shift'], width,
                        label='1 Shift/Day', alpha=0.8, color='steelblue')
        bars2 = ax1.bar(x + width/2, year5_equipment['Equipment_2_Shifts'], width,
                        label='2 Shifts/Day', alpha=0.8, color='coral')

        ax1.set_xlabel('Process', fontweight='bold', fontsize=11)
        ax1.set_ylabel('Equipment Units Required', fontweight='bold', fontsize=11)
        ax1.set_title('Functional Layout Year +5:\nEquipment Requirements\n1-Shift vs 2-Shift Operation',
                      fontweight='bold', fontsize=12)
        ax1.set_xticks(x)
        ax1.set_xticklabels(processes, rotation=45)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

        # add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=8)

        # 2. weekly process workload (hours) - year +5
        ax2 = plt.subplot(2, 3, 2)
        # filter out processes with zero workload
        active_equipment = year5_equipment[year5_equipment['Weekly_Hours'] > 0]
        colors = plt.cm.viridis(np.linspace(0, 1, len(active_equipment)))
        bars = ax2.barh(active_equipment['Process'], active_equipment['Weekly_Hours'],
                        color=colors, alpha=0.8)
        ax2.set_xlabel('Weekly Hours Required', fontweight='bold', fontsize=11)
        ax2.set_ylabel('Process', fontweight='bold', fontsize=11)
        ax2.set_title('Year +5: Weekly Workload by Process', fontweight='bold', fontsize=12)
        ax2.grid(axis='x', alpha=0.3)

        # add value labels
        for i, (proc, hours) in enumerate(zip(active_equipment['Process'], active_equipment['Weekly_Hours'])):
            ax2.text(hours, i, f' {hours:.0f}h', va='center', fontsize=9)

        # 3. year-over-year equipment requirements trend
        ax3 = plt.subplot(2, 3, 3)
        yearly_equipment = equipment_df.groupby('Year')['Equipment_2_Shifts'].sum().reset_index()
        yearly_equipment['Year_Num'] = yearly_equipment['Year'].str.replace('+', '').astype(int)

        ax3.plot(yearly_equipment['Year_Num'], yearly_equipment['Equipment_2_Shifts'],
                marker='o', linewidth=3, markersize=8, color='darkblue', alpha=0.8)
        ax3.set_xlabel('Year', fontweight='bold', fontsize=11)
        ax3.set_ylabel('Total Equipment Units (2 Shifts)', fontweight='bold', fontsize=11)
        ax3.set_title('Year-over-Year: Total Equipment Requirements', fontweight='bold', fontsize=12)
        ax3.set_xticks(yearly_equipment['Year_Num'])
        ax3.grid(alpha=0.3)

        # add value labels
        for x, y in zip(yearly_equipment['Year_Num'], yearly_equipment['Equipment_2_Shifts']):
            ax3.text(x, y, f'{int(y)}', ha='center', va='bottom', fontsize=10)

        # 4. process-wise capacity utilization - year +5
        ax4 = plt.subplot(2, 3, 4)
        utilization_data = active_equipment[['Process', 'Utilization_2_Shifts']].copy()
        utilization_data = utilization_data.sort_values('Utilization_2_Shifts', ascending=True)

        colors = plt.cm.RdYlGn(np.linspace(0, 1, len(utilization_data)))
        bars = ax4.barh(utilization_data['Process'], utilization_data['Utilization_2_Shifts'],
                       color=colors, alpha=0.8)
        ax4.set_xlabel('Utilization (%)', fontweight='bold', fontsize=11)
        ax4.set_ylabel('Process', fontweight='bold', fontsize=11)
        ax4.set_title('Year +5: Equipment Utilization by Process', fontweight='bold', fontsize=12)
        ax4.axvline(x=85, color='red', linestyle='--', alpha=0.7, label='85% Target')
        ax4.grid(axis='x', alpha=0.3)
        ax4.legend()

        # Add value labels
        for i, (proc, util) in enumerate(zip(utilization_data['Process'], utilization_data['Utilization_2_Shifts'])):
            ax4.text(util, i, f' {util:.1f}%', va='center', fontsize=9)

        # 5. Weekly Production Hours Trend
        ax5 = plt.subplot(2, 3, 5)
        yearly_hours = equipment_df.groupby('Year')['Weekly_Hours'].sum().reset_index()
        yearly_hours['Year_Num'] = yearly_hours['Year'].str.replace('+', '').astype(int)

        ax5.plot(yearly_hours['Year_Num'], yearly_hours['Weekly_Hours'],
                marker='s', linewidth=3, markersize=8, color='darkgreen', alpha=0.8)
        ax5.set_xlabel('Year', fontweight='bold', fontsize=11)
        ax5.set_ylabel('Total Weekly Production Hours', fontweight='bold', fontsize=11)
        ax5.set_title('Year-over-Year: Production Volume Trend', fontweight='bold', fontsize=12)
        ax5.set_xticks(yearly_hours['Year_Num'])
        ax5.grid(alpha=0.3)

        # Add value labels
        for x, y in zip(yearly_hours['Year_Num'], yearly_hours['Weekly_Hours']):
            ax5.text(x, y, f'{y:,.0f}h', ha='center', va='bottom', fontsize=9)

        # 6. Cost Efficiency Trend (if cost data available)
        ax6 = plt.subplot(2, 3, 6)
        if cost_data_available:
            cost_metrics_df = pd.read_csv(cost_dir / "Functional_Cost_Efficiency_Metrics_All_Years.csv")
            cost_metrics_df['Year_Num'] = cost_metrics_df['Year'].str.replace('+', '').astype(int)

            ax6.plot(cost_metrics_df['Year_Num'], cost_metrics_df['Total_Cost_Per_Hour'],
                    marker='^', linewidth=3, markersize=8, color='darkred', alpha=0.8)
            ax6.set_xlabel('Year', fontweight='bold', fontsize=11)
            ax6.set_ylabel('Total Cost per Production Hour ($)', fontweight='bold', fontsize=11)
            ax6.set_title('Year-over-Year: Cost Efficiency Trend', fontweight='bold', fontsize=12)
            ax6.set_xticks(cost_metrics_df['Year_Num'])
            ax6.grid(alpha=0.3)

            # Add value labels
            for x, y in zip(cost_metrics_df['Year_Num'], cost_metrics_df['Total_Cost_Per_Hour']):
                ax6.text(x, y, f'${y:.2f}', ha='center', va='bottom', fontsize=9)
        else:
            ax6.text(0.5, 0.5, 'Cost Data\nNot Available', ha='center', va='center',
                    transform=ax6.transAxes, fontsize=12, color='gray')
            ax6.set_title('Cost Efficiency Trend\n(Data Not Available)', fontweight='bold', fontsize=12)
            ax6.set_xlim(0, 1)
            ax6.set_ylim(0, 1)

        plt.tight_layout()
        plt.savefig(VISUALS_DIR / 'Functional_Layout_Analysis_Year5_Overview.png', dpi=300, bbox_inches='tight')
        plt.close()

    # Create year-by-year comparison charts
    years = sorted(equipment_df['Year'].unique())
    years = [str(y) for y in years]  # Ensure years are strings
    if len(years) > 1:
        create_year_comparison_charts(equipment_df, years)

    # Create process flow analysis visualizations
    if not flow_summary_df.empty:
        create_flow_analysis_visualizations(flow_summary_df)

    print(f"Functional layout visualizations saved to {VISUALS_DIR}")

def create_year_comparison_charts(equipment_df, years):
    """
    Create year-by-year comparison visualizations
    """
    # Equipment requirements by process across years
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()

    processes = sorted(equipment_df['Process'].unique())
    year_nums = [int(y.replace('+', '')) for y in years]

    for i, process in enumerate(processes[:4]):  # Show first 4 processes
        ax = axes[i]
        process_data = equipment_df[equipment_df['Process'] == process]

        ax.plot(year_nums, process_data['Equipment_2_Shifts'],
               marker='o', linewidth=2, markersize=6, alpha=0.8, label='2 Shifts')
        ax.plot(year_nums, process_data['Equipment_1_Shift'],
               marker='s', linewidth=2, markersize=6, alpha=0.8, label='1 Shift')

        ax.set_title(f'Process {process}: Equipment Requirements', fontweight='bold', fontsize=12)
        ax.set_xlabel('Year', fontweight='bold', fontsize=10)
        ax.set_ylabel('Equipment Units', fontweight='bold', fontsize=10)
        ax.set_xticks(year_nums)
        ax.legend()
        ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(VISUALS_DIR / 'Functional_Equipment_Comparison_By_Process.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Utilization comparison across years
    fig, ax = plt.subplots(figsize=(12, 8))

    utilization_data = []
    for year in years:
        year_data = equipment_df[equipment_df['Year'] == year]
        avg_util = year_data['Utilization_2_Shifts'].mean()
        utilization_data.append({'Year': year, 'Avg_Utilization': avg_util})

    util_df = pd.DataFrame(utilization_data)
    util_df['Year_Num'] = util_df['Year'].str.replace('+', '').astype(int)

    bars = ax.bar(util_df['Year_Num'], util_df['Avg_Utilization'], color='skyblue', alpha=0.8, width=0.6)
    ax.axhline(y=85, color='red', linestyle='--', alpha=0.7, label='85% Target')
    ax.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Average Equipment Utilization (%)', fontweight='bold', fontsize=12)
    ax.set_title('Functional Layout: Average Equipment Utilization by Year', fontweight='bold', fontsize=14)
    ax.set_xticks(util_df['Year_Num'])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar, util in zip(bars, util_df['Avg_Utilization']):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
               f'{util:.1f}%', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(VISUALS_DIR / 'Functional_Utilization_Comparison_By_Year.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_flow_analysis_visualizations(flow_summary_df):
    """
    Create material flow analysis visualizations
    """
    # Filter for latest year (+5) if available
    year5_flow = flow_summary_df[flow_summary_df['Year'] == '+5']

    if not year5_flow.empty:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Process flow intensity (incoming + outgoing)
        flow_data = year5_flow.copy()
        flow_data['Total_Flow'] = flow_data['Total_In_Flow'] + flow_data['Total_Out_Flow']
        flow_data = flow_data.sort_values('Total_Flow', ascending=True)

        colors = plt.cm.plasma(np.linspace(0, 1, len(flow_data)))
        bars = ax1.barh(flow_data['Process'], flow_data['Total_Flow'], color=colors, alpha=0.8)
        ax1.set_xlabel('Total Flow Intensity', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Process', fontweight='bold', fontsize=12)
        ax1.set_title('Year +5: Process Flow Intensity\n(In + Out Flows)', fontweight='bold', fontsize=14)
        ax1.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (proc, flow) in enumerate(zip(flow_data['Process'], flow_data['Total_Flow'])):
            ax1.text(flow, i, f' {flow:.0f}', va='center', fontsize=9)

        # Flow balance analysis (in vs out)
        flow_balance = year5_flow.copy()
        flow_balance['Flow_Balance'] = flow_balance['Total_In_Flow'] - flow_balance['Total_Out_Flow']
        flow_balance = flow_balance.sort_values('Flow_Balance')

        colors_balance = ['red' if x < 0 else 'green' for x in flow_balance['Flow_Balance']]
        bars2 = ax2.barh(flow_balance['Process'], flow_balance['Flow_Balance'], color=colors_balance, alpha=0.7)
        ax2.axvline(x=0, color='black', linewidth=1, alpha=0.8)
        ax2.set_xlabel('Flow Balance (In - Out)', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Process', fontweight='bold', fontsize=12)
        ax2.set_title('Year +5: Process Flow Balance\n(Positive = Net Receiver)', fontweight='bold', fontsize=14)
        ax2.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (proc, balance) in enumerate(zip(flow_balance['Process'], flow_balance['Flow_Balance'])):
            ax2.text(balance, i, f' {balance:.0f}', va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(VISUALS_DIR / 'Functional_Flow_Analysis_Year5.png', dpi=300, bbox_inches='tight')
        plt.close()

def create_summary_dashboard():
    """
    Create a summary dashboard with key metrics
    """
    # Load all relevant data
    capacity_dir = RESULTS_DIR / "Capacity"
    cost_dir = RESULTS_DIR / "Cost_Analysis"

    equipment_df = pd.read_csv(capacity_dir / "Functional_Equipment_Requirements_All_Years.csv")
    flow_summary_df = pd.read_csv(RESULTS_DIR / "AllYears_Flow_Matrix_Summary.csv")

    try:
        cost_metrics_df = pd.read_csv(cost_dir / "Functional_Cost_Efficiency_Metrics_All_Years.csv")
        cost_available = True
    except FileNotFoundError:
        cost_available = False

    # Create dashboard
    fig = plt.figure(figsize=(20, 12))

    # Key metrics summary
    years = sorted(equipment_df['Year'].unique())
    years = [str(y) for y in years]  # Ensure years are strings
    year_nums = [int(y.replace('+', '')) for y in years]

    # 1. Total Equipment Requirements Trend
    ax1 = plt.subplot(2, 3, 1)
    yearly_equip = equipment_df.groupby('Year')['Equipment_2_Shifts'].sum().reset_index()
    yearly_equip['Year'] = yearly_equip['Year'].astype(str)  # Ensure string
    yearly_equip['Year_Num'] = yearly_equip['Year'].str.replace('+', '').astype(int)

    ax1.plot(yearly_equip['Year_Num'], yearly_equip['Equipment_2_Shifts'],
            marker='o', linewidth=4, markersize=10, color='navy', alpha=0.9)
    ax1.set_title('Total Equipment Requirements\n(2-Shift Operation)', fontweight='bold', fontsize=14)
    ax1.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Equipment Units', fontweight='bold', fontsize=12)
    ax1.set_xticks(year_nums)
    ax1.grid(alpha=0.3)

    # 2. Average Utilization Trend
    ax2 = plt.subplot(2, 3, 2)
    yearly_util = equipment_df.groupby('Year')['Utilization_2_Shifts'].mean().reset_index()
    yearly_util['Year'] = yearly_util['Year'].astype(str)  # Ensure string
    yearly_util['Year_Num'] = yearly_util['Year'].str.replace('+', '').astype(int)

    ax2.plot(yearly_util['Year_Num'], yearly_util['Utilization_2_Shifts'],
            marker='s', linewidth=4, markersize=10, color='darkgreen', alpha=0.9)
    ax2.axhline(y=85, color='red', linestyle='--', alpha=0.7, linewidth=2, label='85% Target')
    ax2.set_title('Average Equipment Utilization', fontweight='bold', fontsize=14)
    ax2.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Utilization (%)', fontweight='bold', fontsize=12)
    ax2.set_xticks(year_nums)
    ax2.set_ylim(80, 100)
    ax2.legend()
    ax2.grid(alpha=0.3)

    # 3. Production Volume Trend
    ax3 = plt.subplot(2, 3, 3)
    yearly_hours = equipment_df.groupby('Year')['Weekly_Hours'].sum().reset_index()
    yearly_hours['Year'] = yearly_hours['Year'].astype(str)  # Ensure string
    yearly_hours['Year_Num'] = yearly_hours['Year'].str.replace('+', '').astype(int)

    ax3.plot(yearly_hours['Year_Num'], yearly_hours['Weekly_Hours'],
            marker='^', linewidth=4, markersize=10, color='darkorange', alpha=0.9)
    ax3.set_title('Weekly Production Volume', fontweight='bold', fontsize=14)
    ax3.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax3.set_ylabel('Production Hours/Week', fontweight='bold', fontsize=12)
    ax3.set_xticks(year_nums)
    ax3.grid(alpha=0.3)

    # 4. Cost Efficiency (if available)
    ax4 = plt.subplot(2, 3, 4)
    if cost_available:
        cost_metrics_df = pd.read_csv(cost_dir / "Functional_Cost_Efficiency_Metrics_All_Years.csv")
        cost_metrics_df['Year'] = cost_metrics_df['Year'].astype(str)  # Ensure string
        cost_metrics_df['Year_Num'] = cost_metrics_df['Year'].str.replace('+', '').astype(int)

        ax4.plot(cost_metrics_df['Year_Num'], cost_metrics_df['Total_Cost_Per_Hour'],
                marker='d', linewidth=4, markersize=10, color='darkred', alpha=0.9)
        ax4.set_title('Cost Efficiency Trend', fontweight='bold', fontsize=14)
        ax4.set_xlabel('Year', fontweight='bold', fontsize=12)
        ax4.set_ylabel('Cost per Production Hour ($)', fontweight='bold', fontsize=12)
        ax4.set_xticks(year_nums)
        ax4.grid(alpha=0.3)
    else:
        ax4.text(0.5, 0.5, 'Cost Analysis\nNot Available', ha='center', va='center',
                transform=ax4.transAxes, fontsize=14, color='gray')
        ax4.set_title('Cost Efficiency\n(Data Unavailable)', fontweight='bold', fontsize=14)

    # 5. Process Flow Complexity
    ax5 = plt.subplot(2, 3, 5)
    if not flow_summary_df.empty:
        yearly_flow = flow_summary_df.groupby('Year').agg({
            'Total_In_Flow': 'sum',
            'Total_Out_Flow': 'sum'
        }).reset_index()
        yearly_flow['Year'] = yearly_flow['Year'].astype(str)  # Ensure string
        yearly_flow['Total_Flow'] = yearly_flow['Total_In_Flow'] + yearly_flow['Total_Out_Flow']
        yearly_flow['Year_Num'] = yearly_flow['Year'].str.replace('Year ', '').astype(int)

        ax5.plot(yearly_flow['Year_Num'], yearly_flow['Total_Flow'],
                marker='p', linewidth=4, markersize=10, color='purple', alpha=0.9)
        ax5.set_title('Material Flow Complexity', fontweight='bold', fontsize=14)
        ax5.set_xlabel('Year', fontweight='bold', fontsize=12)
        ax5.set_ylabel('Total Flow Intensity', fontweight='bold', fontsize=12)
        ax5.set_xticks(year_nums)
        ax5.grid(alpha=0.3)
    else:
        ax5.text(0.5, 0.5, 'Flow Data\nNot Available', ha='center', va='center',
                transform=ax5.transAxes, fontsize=14, color='gray')
        ax5.set_title('Material Flow\n(Data Unavailable)', fontweight='bold', fontsize=14)

    # 6. Key Insights Summary
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')

    insights_text = f"""
FUNCTIONAL LAYOUT ANALYSIS SUMMARY
{'='*35}

Analysis Period: Years +2 to +5
Layout Type: Functional (Process Grouping)

KEY METRICS:
• Equipment Growth: {yearly_equip['Equipment_2_Shifts'].min()} → {yearly_equip['Equipment_2_Shifts'].max()} units
• Utilization Range: {yearly_util['Utilization_2_Shifts'].min():.1f}% → {yearly_util['Utilization_2_Shifts'].max():.1f}%
• Production Growth: {yearly_hours['Weekly_Hours'].min():,.0f} → {yearly_hours['Weekly_Hours'].max():,.0f} hours/week

INSIGHTS:
• All processes show increasing demand
• Utilization remains high (>{yearly_util['Utilization_2_Shifts'].min():.0f}%)
• Process D shows highest equipment requirements
• Functional layout provides process specialization benefits
• Material flow complexity increases with production volume
"""

    ax6.text(0.05, 0.95, insights_text, transform=ax6.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))

    plt.tight_layout()
    plt.savefig(VISUALS_DIR / 'Functional_Layout_Summary_Dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """
    Main visualization script for functional layout analysis
    """
    print("="*80)
    print("TASK 4: FUNCTIONAL LAYOUT - VISUALIZATION ANALYSIS (YEARS 2-5)")
    print("="*80)

    # Ensure output directories exist
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Create all visualizations
    print("\n1. Creating Comprehensive Visualizations...")
    create_functional_visualizations()

    print("\n2. Creating Summary Dashboard...")
    create_summary_dashboard()

    print("\n" + "="*80)
    print("FUNCTIONAL LAYOUT VISUALIZATION COMPLETE (YEARS 2-5)!")
    print("="*80)
    print(f"All visualizations saved to: {VISUALS_DIR}")
    print("="*80)

if __name__ == "__main__":
    main()