"""
Task 3: Part-Based Layout - Cost Analysis

Comprehensive cost analysis for part-based layout including:
1. Capital investment costs (equipment installation)
2. Operating costs (labor)
3. Depreciation analysis
4. Cost KPIs and efficiency metrics
5. Cost visualizations and comparisons

Author: Analysis Team
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results" / "Task3" / "Part"
COST_DIR = RESULTS_DIR / "Cost_Analysis"
VISUALS_DIR = RESULTS_DIR / "Visuals"

# Operating parameters
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
SHIFTS_PER_DAY = 2
WEEKS_PER_YEAR = 52
HOURS_PER_YEAR = DAYS_PER_WEEK * HOURS_PER_SHIFT * SHIFTS_PER_DAY * WEEKS_PER_YEAR

def load_equipment_costs():
    """
    Load equipment cost data from Equip+Operator Specs.csv
    """
    df = pd.read_csv(DATA_DIR / 'Equip+Operator Specs.csv')

    # Clean up the data
    df['Installed price'] = pd.to_numeric(df['Installed price'], errors='coerce')
    df['Relocation cost'] = pd.to_numeric(df['Relocation cost'], errors='coerce')
    df['Useful life (years)'] = pd.to_numeric(df['Useful life (years)'], errors='coerce')
    df['Hourly Cost'] = pd.to_numeric(df['Hourly Cost'], errors='coerce')

    print("Equipment cost data loaded:")
    print(f"  Total equipment types: {len(df)}")
    print(f"  Equipment with cost data: {df['Installed price'].notna().sum()}")

    return df

def load_equipment_requirements():
    """
    Load equipment requirements from part-based layout analysis
    """
    equipment_df = pd.read_csv(COST_DIR.parent / "Capacity" / "Task3_Parts_Based_Equipment_Requirements.csv")

    # Calculate efficiency metrics from equipment requirements
    total_weekly_hours = equipment_df['Weekly_Hours'].sum()
    total_equipment_2_shifts = equipment_df['Equipment_2_Shifts'].sum()
    avg_utilization_2_shifts = equipment_df['Utilization_2_Shifts'].mean()

    efficiency_metrics = {
        'total_workload_hours': total_weekly_hours,
        'total_equipment_units': total_equipment_2_shifts,
        'average_utilization': avg_utilization_2_shifts
    }

    return equipment_df, efficiency_metrics

def calculate_capital_costs(equipment_df, cost_df):
    """
    Calculate total capital investment costs for part-based layout
    """
    capital_costs = []

    for _, row in equipment_df.iterrows():
        process = row['Process']
        units_needed = int(row['Equipment_2_Shifts'])  # Using 2-shift requirements

        if units_needed == 0:
            continue

        # Find equipment cost data for this process
        cost_row = cost_df[cost_df['Equipment'] == process]

        if cost_row.empty:
            print(f"Warning: No cost data found for process {process}")
            continue

        installed_price = cost_row['Installed price'].iloc[0]
        relocation_cost = cost_row['Relocation cost'].iloc[0] if pd.notna(cost_row['Relocation cost'].iloc[0]) else 0

        total_cost_per_unit = installed_price + relocation_cost
        total_process_cost = units_needed * total_cost_per_unit

        capital_costs.append({
            'Process': process,
            'Units_Required': units_needed,
            'Cost_Per_Unit': total_cost_per_unit,
            'Total_Installed_Cost': installed_price * units_needed,
            'Total_Relocation_Cost': relocation_cost * units_needed,
            'Total_Process_Cost': total_process_cost,
            'Utilization_2_Shifts': row['Utilization_2_Shifts'],
            'Weekly_Hours': row['Weekly_Hours']
        })

    return pd.DataFrame(capital_costs)

def calculate_operating_costs(equipment_df, cost_df):
    """
    Calculate annual operating costs (labor) for part-based layout
    """
    operating_costs = []

    for _, row in equipment_df.iterrows():
        process = row['Process']
        units_needed = int(row['Equipment_2_Shifts'])

        if units_needed == 0:
            continue

        # Find equipment cost data for this process
        cost_row = cost_df[cost_df['Equipment'] == process]

        if cost_row.empty:
            continue

        # Parse operator requirements
        operator_info = cost_row['Number of operators'].iloc[0] if pd.notna(cost_row['Number of operators'].iloc[0]) else '1 C1'
        hourly_cost = cost_row['Hourly Cost'].iloc[0] if pd.notna(cost_row['Hourly Cost'].iloc[0]) else 20

        # Calculate operators per unit
        operators_per_unit = 1.0  # Default
        if pd.notna(operator_info):
            # Parse operator requirements (e.g., "1 C1+1/4 C2", "2 C3", "1/2 C2")
            operator_str = str(operator_info).strip()
            if 'C1' in operator_str and 'C2' in operator_str:
                operators_per_unit = 1 + 0.25  # 1 C1 + 1/4 C2
            elif 'C1' in operator_str and 'C3' in operator_str:
                if '1/2' in operator_str:
                    operators_per_unit = 0.5 + 0.5  # 1/2 C3 (assuming C1 + 1/2 C3)
                else:
                    operators_per_unit = 1 + 0.5  # 1 C1 + 1/2 C3
            elif operator_str.startswith('2'):
                operators_per_unit = 2.0  # 2 C3
            elif operator_str.startswith('1/2'):
                operators_per_unit = 0.5  # 1/2 C2
            else:
                operators_per_unit = 1.0  # Default

        total_operators = units_needed * operators_per_unit
        annual_labor_cost = total_operators * hourly_cost * HOURS_PER_YEAR

        operating_costs.append({
            'Process': process,
            'Units_Required': units_needed,
            'Operators_Per_Unit': operators_per_unit,
            'Total_Operators': total_operators,
            'Hourly_Cost': hourly_cost,
            'Annual_Labor_Cost': annual_labor_cost,
            'Utilization_2_Shifts': row['Utilization_2_Shifts'],
            'Weekly_Hours': row['Weekly_Hours']
        })

    return pd.DataFrame(operating_costs)

def calculate_depreciation(capital_costs_df, cost_df):
    """
    Calculate annual depreciation for all equipment
    """
    depreciation_data = []

    for _, row in capital_costs_df.iterrows():
        process = row['Process']

        # Find useful life for this equipment
        cost_row = cost_df[cost_df['Equipment'] == process]
        if cost_row.empty:
            continue

        useful_life = cost_row['Useful life (years)'].iloc[0] if pd.notna(cost_row['Useful life (years)'].iloc[0]) else 10

        total_installed_cost = row['Total_Installed_Cost']
        annual_depreciation = total_installed_cost / useful_life

        depreciation_data.append({
            'Process': process,
            'Total_Installed_Cost': total_installed_cost,
            'Useful_Life_Years': useful_life,
            'Annual_Depreciation': annual_depreciation
        })

    return pd.DataFrame(depreciation_data)

def calculate_cost_kpis(capital_costs_df, operating_costs_df, depreciation_df, efficiency_metrics):
    """
    Calculate key cost performance indicators
    """
    # Total costs
    total_capital_investment = capital_costs_df['Total_Process_Cost'].sum()
    total_annual_operating_cost = operating_costs_df['Annual_Labor_Cost'].sum()
    total_annual_depreciation = depreciation_df['Annual_Depreciation'].sum()

    # Equipment and labor totals
    total_equipment_units = capital_costs_df['Units_Required'].sum()
    total_operators = operating_costs_df['Total_Operators'].sum()

    # Production metrics
    total_weekly_hours = efficiency_metrics.get('total_workload_hours', 0)
    total_annual_hours = total_weekly_hours * WEEKS_PER_YEAR

    # Cost per unit calculations
    capital_cost_per_equipment_unit = total_capital_investment / total_equipment_units if total_equipment_units > 0 else 0
    operating_cost_per_hour = total_annual_operating_cost / total_annual_hours if total_annual_hours > 0 else 0
    total_cost_per_hour = (total_annual_operating_cost + total_annual_depreciation) / total_annual_hours if total_annual_hours > 0 else 0

    # Efficiency metrics
    average_utilization = efficiency_metrics.get('average_utilization', 0)
    cost_per_utilization_point = total_annual_operating_cost / (average_utilization * total_equipment_units) if average_utilization > 0 and total_equipment_units > 0 else 0

    kpis = {
        'total_capital_investment': total_capital_investment,
        'total_annual_operating_cost': total_annual_operating_cost,
        'total_annual_depreciation': total_annual_depreciation,
        'total_annual_cost': total_annual_operating_cost + total_annual_depreciation,
        'total_equipment_units': total_equipment_units,
        'total_operators': total_operators,
        'total_weekly_hours': total_weekly_hours,
        'total_annual_hours': total_annual_hours,
        'capital_cost_per_equipment_unit': capital_cost_per_equipment_unit,
        'operating_cost_per_hour': operating_cost_per_hour,
        'total_cost_per_hour': total_cost_per_hour,
        'average_utilization': average_utilization,
        'cost_per_utilization_point': cost_per_utilization_point
    }

    return kpis

def create_cost_visualizations(capital_costs_df, operating_costs_df, depreciation_df, kpis):
    """
    Create comprehensive cost analysis visualizations
    """
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (15, 10)

    # 1. Cost Breakdown by Process
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

    # Capital costs by process
    capital_sorted = capital_costs_df.sort_values('Total_Process_Cost', ascending=True)
    bars1 = ax1.barh(capital_sorted['Process'], capital_sorted['Total_Process_Cost'] / 1000000)  # Convert to millions
    ax1.set_xlabel('Capital Cost (Millions $)', fontweight='bold')
    ax1.set_ylabel('Process', fontweight='bold')
    ax1.set_title('Capital Investment by Process', fontweight='bold', fontsize=14)
    ax1.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (proc, cost) in enumerate(zip(capital_sorted['Process'], capital_sorted['Total_Process_Cost'])):
        ax1.text(cost/1000000, i, f' ${cost/1000000:.1f}M', va='center', fontsize=9)

    # Operating costs by process
    operating_sorted = operating_costs_df.sort_values('Annual_Labor_Cost', ascending=True)
    bars2 = ax2.barh(operating_sorted['Process'], operating_costs_df['Annual_Labor_Cost'] / 1000)  # Convert to thousands
    ax2.set_xlabel('Annual Labor Cost (Thousands $)', fontweight='bold')
    ax2.set_ylabel('Process', fontweight='bold')
    ax2.set_title('Operating Costs by Process', fontweight='bold', fontsize=14)
    ax2.grid(axis='x', alpha=0.3)

    # Add value labels
    for i, (proc, cost) in enumerate(zip(operating_sorted['Process'], operating_sorted['Annual_Labor_Cost'])):
        ax2.text(cost/1000, i, f' ${cost/1000:.0f}K', va='center', fontsize=9)

    # Cost vs Utilization scatter plot
    combined_df = pd.merge(capital_costs_df[['Process', 'Total_Process_Cost', 'Utilization_2_Shifts']],
                          operating_costs_df[['Process', 'Annual_Labor_Cost']],
                          on='Process', how='outer').fillna(0)

    scatter = ax3.scatter(combined_df['Utilization_2_Shifts'],
                         combined_df['Total_Process_Cost'] / 1000000,
                         s=combined_df['Annual_Labor_Cost'] / 10000,  # Size by operating cost
                         alpha=0.7, c=combined_df['Utilization_2_Shifts'], cmap='RdYlGn')

    # Add process labels
    for _, row in combined_df.iterrows():
        ax3.annotate(row['Process'],
                    (row['Utilization_2_Shifts'], row['Total_Process_Cost'] / 1000000),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)

    ax3.set_xlabel('Equipment Utilization (%)', fontweight='bold')
    ax3.set_ylabel('Capital Cost (Millions $)', fontweight='bold')
    ax3.set_title('Cost vs Utilization Analysis\n(Bubble size = Annual Operating Cost)', fontweight='bold', fontsize=14)
    ax3.grid(True, alpha=0.3)

    # Cost structure pie chart
    cost_components = [
        'Annual Labor Cost',
        'Annual Depreciation',
        'Capital Investment (Annualized)'
    ]

    # Annualize capital investment (simple payback period assumption of 5 years)
    annualized_capital = kpis['total_capital_investment'] / 5

    cost_values = [
        kpis['total_annual_operating_cost'],
        kpis['total_annual_depreciation'],
        annualized_capital
    ]

    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = ax4.pie(cost_values, labels=cost_components, autopct='%1.1f%%',
                                      colors=colors, startangle=90)
    ax4.set_title('Annual Cost Structure Breakdown', fontweight='bold', fontsize=14)

    # Add dollar values to pie chart
    for i, (wedge, value) in enumerate(zip(wedges, cost_values)):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = 0.7 * np.cos(np.radians(angle))
        y = 0.7 * np.sin(np.radians(angle))
        ax4.text(x, y, f'${value/1000000:.1f}M', ha='center', va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    output_file = VISUALS_DIR / "Part_Based_Layout_Cost_Analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight', bbox_extra_artists=[])
    print(f"Cost analysis visualization saved: {output_file}")
    plt.close('all')

    # 2. Cost Efficiency Dashboard
    print("Creating KPI dashboard...")
    plt.figure(figsize=(16, 12))

    # Create KPI dashboard
    kpi_labels = [
        'Total Capital\nInvestment',
        'Annual Operating\nCost',
        'Annual Depreciation',
        'Total Annual\nCost',
        'Cost per\nEquipment Unit',
        'Cost per\nOperating Hour',
        'Average\nUtilization'
    ]

    kpi_values = [
        kpis['total_capital_investment'] / 1000000,  # Millions
        kpis['total_annual_operating_cost'] / 1000,  # Thousands
        kpis['total_annual_depreciation'] / 1000,    # Thousands
        kpis['total_annual_cost'] / 1000,            # Thousands
        kpis['capital_cost_per_equipment_unit'] / 1000,  # Thousands
        kpis['operating_cost_per_hour'],             # Per hour
        kpis['average_utilization']                   # Percentage
    ]

    # Create 2x4 grid for KPIs
    for i, (label, value) in enumerate(zip(kpi_labels, kpi_values)):
        plt.subplot(2, 4, i+1)

        if 'Cost' in label or 'Investment' in label:
            if 'per' in label.lower():
                plt.text(0.5, 0.5, f'${value:,.0f}', ha='center', va='center',
                        fontsize=18, fontweight='bold', color='#2E86AB')
            else:
                plt.text(0.5, 0.5, f'${value:,.1f}M', ha='center', va='center',
                        fontsize=18, fontweight='bold', color='#2E86AB')
        elif 'Utilization' in label:
            plt.text(0.5, 0.5, f'{value:.1f}%', ha='center', va='center',
                    fontsize=18, fontweight='bold', color='#A23B72')
        else:
            plt.text(0.5, 0.5, f'${value:,.0f}', ha='center', va='center',
                    fontsize=18, fontweight='bold', color='#F18F01')

        plt.title(label, fontweight='bold', fontsize=12)
        plt.axis('off')

    plt.tight_layout()
    output_file = VISUALS_DIR / "Part_Based_Layout_Cost_KPI_Dashboard.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Cost KPI dashboard saved: {output_file}")
    plt.close('all')

def generate_cost_report(capital_costs_df, operating_costs_df, depreciation_df, kpis):
    """
    Generate comprehensive cost analysis report
    """
    report = f"""
PART-BASED LAYOUT COST ANALYSIS REPORT
{'='*50}

EXECUTIVE SUMMARY
{'-'*20}
This report provides a comprehensive cost analysis for the part-based layout implementation,
including capital investment, operating costs, depreciation, and key performance indicators.

CAPITAL INVESTMENT ANALYSIS
{'-'*30}
"""

    # Capital costs summary
    total_capital = capital_costs_df['Total_Process_Cost'].sum()
    report += f"""
Total Capital Investment Required: ${total_capital:,.0f}
Breakdown by major cost components:
"""

    # Group by cost ranges for summary
    high_cost_processes = capital_costs_df[capital_costs_df['Total_Process_Cost'] > 10000000]  # > $10M
    if not high_cost_processes.empty:
        report += f"\nHigh-cost processes (>$10M each):"
        for _, row in high_cost_processes.iterrows():
            report += f"\n  Process {row['Process']}: ${row['Total_Process_Cost']:,.0f} ({row['Units_Required']} units)"

    report += f"""

OPERATING COST ANALYSIS
{'-'*25}
"""

    total_operating = operating_costs_df['Annual_Labor_Cost'].sum()
    total_operators = operating_costs_df['Total_Operators'].sum()

    report += f"""
Annual Operating Cost: ${total_operating:,.0f}
Total Operators Required: {total_operators:.1f} FTEs
Average Cost per Operator: ${total_operating/total_operators:,.0f}/year

Labor cost breakdown by process:
"""

    labor_sorted = operating_costs_df.sort_values('Annual_Labor_Cost', ascending=False)
    for _, row in labor_sorted.iterrows():
        if row['Annual_Labor_Cost'] > 0:
            report += f"  Process {row['Process']}: ${row['Annual_Labor_Cost']:,.0f}/year ({row['Total_Operators']:.1f} operators)\n"

    report += f"""

DEPRECIATION ANALYSIS
{'-'*22}
"""

    total_depreciation = depreciation_df['Annual_Depreciation'].sum()
    report += f"""
Annual Depreciation: ${total_depreciation:,.0f}
Average equipment useful life: {depreciation_df['Useful_Life_Years'].mean():.1f} years

KEY PERFORMANCE INDICATORS
{'-'*28}
• Total Equipment Units Required: {kpis['total_equipment_units']}
• Total Annual Production Hours: {kpis['total_annual_hours']:,.0f}
• Average Equipment Utilization: {kpis['average_utilization']:.1f}%
• Capital Cost per Equipment Unit: ${kpis['capital_cost_per_equipment_unit']:,.0f}
• Operating Cost per Hour: ${kpis['operating_cost_per_hour']:.2f}
• Total Cost per Hour: ${kpis['total_cost_per_hour']:.2f}

COST EFFICIENCY ANALYSIS
{'-'*26}
"""

    # Calculate efficiency metrics
    cost_per_hour_per_utilization = kpis['total_cost_per_hour'] / kpis['average_utilization'] * 100 if kpis['average_utilization'] > 0 else 0

    report += f"""
• Cost Efficiency Ratio: ${cost_per_hour_per_utilization:.2f} per hour per utilization percentage point
• Labor Cost as % of Total Annual Cost: {(kpis['total_annual_operating_cost'] / kpis['total_annual_cost'] * 100):.1f}%
• Depreciation as % of Total Annual Cost: {(kpis['total_annual_depreciation'] / kpis['total_annual_cost'] * 100):.1f}%

BREAK-EVEN ANALYSIS
{'-'*20}
Assuming 5-year payback period for capital investment:
• Annual Capital Recovery: ${(kpis['total_capital_investment'] / 5):,.0f}
• Total Annual Cost (including capital recovery): ${(kpis['total_annual_cost'] + kpis['total_capital_investment'] / 5):,.0f}
• Break-even Hourly Rate Required: ${((kpis['total_annual_cost'] + kpis['total_capital_investment'] / 5) / kpis['total_annual_hours']):.2f}/hour

RECOMMENDATIONS
{'-'*15}
1. Focus on high-utilization processes (M, J, D, I, H) for maximum ROI
2. Consider preventive maintenance to extend equipment life and reduce depreciation costs
3. Optimize operator scheduling to maximize utilization during peak hours
4. Evaluate automation opportunities for high-volume processes to reduce labor costs
5. Monitor cost per hour metrics regularly to identify efficiency improvements

All cost analysis results and visualizations saved to: {COST_DIR}
"""

    return report

def main():
    """
    Main function for part-based layout cost analysis
    """
    print("="*80)
    print("TASK 3: PART-BASED LAYOUT - COST ANALYSIS")
    print("="*80)

    # Ensure output directory exists
    COST_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Load data
        print("\n1. Loading cost and equipment data...")
        cost_df = load_equipment_costs()
        equipment_df, efficiency_metrics = load_equipment_requirements()

        # Step 2: Calculate capital costs
        print("\n2. Calculating capital investment costs...")
        capital_costs_df = calculate_capital_costs(equipment_df, cost_df)

        # Step 3: Calculate operating costs
        print("\n3. Calculating annual operating costs...")
        operating_costs_df = calculate_operating_costs(equipment_df, cost_df)

        # Step 4: Calculate depreciation
        print("\n4. Calculating depreciation...")
        depreciation_df = calculate_depreciation(capital_costs_df, cost_df)

        # Step 5: Calculate KPIs
        print("\n5. Calculating cost KPIs...")
        kpis = calculate_cost_kpis(capital_costs_df, operating_costs_df, depreciation_df, efficiency_metrics)
        print(f"KPI calculation completed. Total capital investment: {kpis['total_capital_investment']}")
        print(f"Total annual operating cost: {kpis['total_annual_operating_cost']}")
        print(f"Total annual depreciation: {kpis['total_annual_depreciation']}")

        # Step 6: Create visualizations
        print("\n6. Creating cost analysis visualizations...")
        create_cost_visualizations(capital_costs_df, operating_costs_df, depreciation_df, kpis)

        # Step 7: Generate cost report
        print("\n7. Generating comprehensive cost report...")
        cost_report = generate_cost_report(capital_costs_df, operating_costs_df, depreciation_df, kpis)
        print("Cost report generated successfully")

        # Save all results
        print("\n8. Saving all results...")
        print(f"COST_DIR path: {COST_DIR}")
        print(f"COST_DIR exists: {COST_DIR.exists()}")

        # Ensure directory exists
        COST_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Directory created/verified: {COST_DIR}")

        # Save detailed cost breakdowns
        capital_costs_df.to_csv(COST_DIR / "Part_Based_Capital_Costs_Detailed.csv", index=False)
        operating_costs_df.to_csv(COST_DIR / "Part_Based_Operating_Costs_Detailed.csv", index=False)
        depreciation_df.to_csv(COST_DIR / "Part_Based_Depreciation_Analysis.csv", index=False)

        # Save KPIs
        kpis_df = pd.DataFrame([kpis])
        kpis_df.to_csv(COST_DIR / "Part_Based_Cost_KPIs.csv", index=False)

        # Save cost report
        with open(COST_DIR / "Part_Based_Layout_Cost_Analysis_Report.txt", 'w') as f:
            f.write(cost_report)

        print(f"  Capital costs saved: {COST_DIR / 'Part_Based_Capital_Costs_Detailed.csv'}")
        print(f"  Operating costs saved: {COST_DIR / 'Part_Based_Operating_Costs_Detailed.csv'}")
        print(f"  Depreciation saved: {COST_DIR / 'Part_Based_Depreciation_Analysis.csv'}")
        print(f"  KPIs saved: {COST_DIR / 'Part_Based_Cost_KPIs.csv'}")
        print(f"  Report saved: {COST_DIR / 'Part_Based_Layout_Cost_Analysis_Report.txt'}")

        # Print summary
        print("\n" + "="*80)
        print("PART-BASED LAYOUT COST ANALYSIS SUMMARY")
        print("="*80)
        print(f"Total Capital Investment: ${kpis['total_capital_investment']:,.0f}")
        print(f"Annual Operating Cost: ${kpis['total_annual_operating_cost']:,.0f}")
        print(f"Annual Depreciation: ${kpis['total_annual_depreciation']:,.0f}")
        print(f"Total Equipment Units: {kpis['total_equipment_units']}")
        print(f"Total Operators: {kpis['total_operators']:.1f}")
        print(f"Cost per Operating Hour: ${kpis['operating_cost_per_hour']:.2f}")
        print(f"Average Utilization: {kpis['average_utilization']:.1f}%")
        print("="*80)

    except Exception as e:
        print(f"Error during cost analysis: {e}")
        print("Please ensure all required data files are available.")

if __name__ == "__main__":
    main()