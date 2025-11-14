"""
task 3: fractal layout - comprehensive cost analysis

analyzes cost implications for all fractal configurations (f2, f3, f4, f5):

- capital investment costs (equipment installation)

- operating costs (labor) across multiple centers

- depreciation analysis

- comparative cost efficiency analysis

- scenario optimization recommendations

team: machas^2
date: november 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # go up to isye6202_cw3 directory
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results" / "Task3" / "Fractal"
COST_DIR = RESULTS_DIR / "Cost_Analysis"
VISUALS_DIR = RESULTS_DIR / "Fractal_Visuals"

# operating parameters
DAYS_PER_WEEK = 5
HOURS_PER_SHIFT = 8
SHIFTS_PER_DAY = 2
WEEKS_PER_YEAR = 52
HOURS_PER_YEAR = DAYS_PER_WEEK * HOURS_PER_SHIFT * SHIFTS_PER_DAY * WEEKS_PER_YEAR

# Fractal scenarios
FRACTAL_SCENARIOS = ['f2', 'f3', 'f4', 'f5']

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

def load_fractal_scenario_data(scenario):
    """
    Load equipment requirements and scenario data for a specific fractal configuration
    """
    design_dir = RESULTS_DIR / "Fractal_Design"

    # Load equipment requirements
    equip_file = design_dir / f"Fractal_{scenario}_Equipment_Requirements.csv"
    equipment_df = pd.read_csv(equip_file)

    # Load scenario comparison data
    comparison_df = pd.read_csv(design_dir / "Fractal_Comparison_All_Scenarios.csv")

    # Get scenario data
    scenario_num = int(scenario[1])  # Extract number from 'f2', 'f3', etc.
    scenario_data = comparison_df[comparison_df['Num_Fractals'] == scenario_num].iloc[0]

    # Calculate efficiency metrics
    total_equipment = scenario_data['Total_Equipment']
    avg_utilization = scenario_data['Avg_Utilization_%'] / 100

    # Calculate total weekly hours from equipment data
    total_weekly_hours = equipment_df['Total_Workload_Min'].sum() / 60  # Convert minutes to hours

    efficiency_metrics = {
        'total_workload_hours': total_weekly_hours,
        'total_equipment_units': total_equipment,
        'average_utilization': avg_utilization,
        'num_centers': scenario_num,
        'capacity_per_center_pct': scenario_data['Capacity_per_Center_%'] / 100,
        'avg_equipment_per_center': scenario_data['Avg_Equipment_per_Center']
    }

    return equipment_df, efficiency_metrics, scenario_data

def calculate_fractal_capital_costs(equipment_df, cost_df, scenario, num_centers):
    """
    Calculate total capital investment costs for fractal layout
    """
    capital_costs = []

    for _, row in equipment_df.iterrows():
        process = row['Process']
        total_equipment = int(row['Total_Equipment'])

        if total_equipment == 0:
            continue

        # Find equipment cost data for this process
        cost_row = cost_df[cost_df['Equipment'] == process]

        if cost_row.empty:
            print(f"Warning: No cost data found for process {process}")
            continue

        installed_price = cost_row['Installed price'].iloc[0]
        relocation_cost = cost_row['Relocation cost'].iloc[0] if pd.notna(cost_row['Relocation cost'].iloc[0]) else 0

        total_cost_per_unit = installed_price + relocation_cost
        total_process_cost = total_equipment * total_cost_per_unit

        capital_costs.append({
            'Scenario': scenario,
            'Process': process,
            'Units_Required': total_equipment,
            'Equipment_per_Center': row['Equipment_per_Center'],
            'Num_Centers': num_centers,
            'Cost_Per_Unit': total_cost_per_unit,
            'Total_Installed_Cost': installed_price * total_equipment,
            'Total_Relocation_Cost': relocation_cost * total_equipment,
            'Total_Process_Cost': total_process_cost,
            'Utilization_per_Center': row['Utilization_per_Center'],
            'Workload_per_Center_Min': row['Workload_per_Center_Min']
        })

    return pd.DataFrame(capital_costs)

def calculate_fractal_operating_costs(equipment_df, cost_df, scenario, num_centers):
    """
    Calculate annual operating costs (labor) for fractal layout
    """
    operating_costs = []

    for _, row in equipment_df.iterrows():
        process = row['Process']
        total_equipment = int(row['Total_Equipment'])

        if total_equipment == 0:
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

        total_operators = total_equipment * operators_per_unit
        annual_labor_cost = total_operators * hourly_cost * HOURS_PER_YEAR

        operating_costs.append({
            'Scenario': scenario,
            'Process': process,
            'Units_Required': total_equipment,
            'Equipment_per_Center': row['Equipment_per_Center'],
            'Num_Centers': num_centers,
            'Operators_Per_Unit': operators_per_unit,
            'Total_Operators': total_operators,
            'Hourly_Cost': hourly_cost,
            'Annual_Labor_Cost': annual_labor_cost,
            'Utilization_per_Center': row['Utilization_per_Center'],
            'Workload_per_Center_Min': row['Workload_per_Center_Min']
        })

    return pd.DataFrame(operating_costs)

def calculate_fractal_depreciation(capital_costs_df, cost_df, scenario):
    """
    Calculate annual depreciation for all equipment in fractal layout
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
            'Scenario': scenario,
            'Process': process,
            'Total_Installed_Cost': total_installed_cost,
            'Useful_Life_Years': useful_life,
            'Annual_Depreciation': annual_depreciation
        })

    return pd.DataFrame(depreciation_data)

def calculate_fractal_cost_kpis(capital_costs_df, operating_costs_df, depreciation_df, efficiency_metrics, scenario):
    """
    Calculate key cost performance indicators for fractal scenario
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

    # Fractal-specific metrics
    num_centers = efficiency_metrics.get('num_centers', 1)
    equipment_per_center = efficiency_metrics.get('avg_equipment_per_center', 0)
    capital_cost_per_center = total_capital_investment / num_centers
    operating_cost_per_center = total_annual_operating_cost / num_centers

    kpis = {
        'scenario': scenario,
        'num_centers': num_centers,
        'total_capital_investment': total_capital_investment,
        'total_annual_operating_cost': total_annual_operating_cost,
        'total_annual_depreciation': total_annual_depreciation,
        'total_annual_cost': total_annual_operating_cost + total_annual_depreciation,
        'total_equipment_units': total_equipment_units,
        'total_operators': total_operators,
        'equipment_per_center': equipment_per_center,
        'capital_cost_per_center': capital_cost_per_center,
        'operating_cost_per_center': operating_cost_per_center,
        'total_weekly_hours': total_weekly_hours,
        'total_annual_hours': total_annual_hours,
        'capital_cost_per_equipment_unit': capital_cost_per_equipment_unit,
        'operating_cost_per_hour': operating_cost_per_hour,
        'total_cost_per_hour': total_cost_per_hour,
        'average_utilization': average_utilization,
        'cost_per_utilization_point': cost_per_utilization_point
    }

    return kpis

def analyze_all_fractal_scenarios():
    """
    Analyze all fractal scenarios and create comprehensive cost analysis
    """
    print("="*80)
    print("TASK 3: FRACTAL LAYOUT - COMPREHENSIVE COST ANALYSIS")
    print("="*80)

    # Ensure output directories exist
    COST_DIR.mkdir(parents=True, exist_ok=True)
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Load cost data
    print("\n1. Loading equipment cost data...")
    cost_df = load_equipment_costs()

    # Analyze each fractal scenario
    all_capital_costs = []
    all_operating_costs = []
    all_depreciation = []
    all_kpis = []

    for scenario in FRACTAL_SCENARIOS:
        print(f"\n2. Analyzing Fractal Scenario {scenario}...")

        # Load scenario data
        equipment_df, efficiency_metrics, scenario_data = load_fractal_scenario_data(scenario)
        num_centers = efficiency_metrics['num_centers']

        print(f"   Centers: {num_centers}, Equipment: {efficiency_metrics['total_equipment_units']}, "
              f"Utilization: {efficiency_metrics['average_utilization']:.1%}")

        # Calculate costs
        capital_costs_df = calculate_fractal_capital_costs(equipment_df, cost_df, scenario, num_centers)
        operating_costs_df = calculate_fractal_operating_costs(equipment_df, cost_df, scenario, num_centers)
        depreciation_df = calculate_fractal_depreciation(capital_costs_df, cost_df, scenario)

        # Calculate KPIs
        kpis = calculate_fractal_cost_kpis(capital_costs_df, operating_costs_df, depreciation_df, efficiency_metrics, scenario)

        # Store results
        all_capital_costs.append(capital_costs_df)
        all_operating_costs.append(operating_costs_df)
        all_depreciation.append(depreciation_df)
        all_kpis.append(kpis)

    # Combine all results
    capital_df = pd.concat(all_capital_costs, ignore_index=True)
    operating_df = pd.concat(all_operating_costs, ignore_index=True)
    depreciation_df = pd.concat(all_depreciation, ignore_index=True)
    kpis_df = pd.DataFrame(all_kpis)

    print("\n3. Creating comprehensive cost analysis visualizations...")

    # Create visualizations
    create_fractal_cost_comparison_visualizations(capital_df, operating_df, kpis_df)

    print("\n4. Generating comprehensive cost analysis reports...")

    # Generate reports
    generate_fractal_cost_analysis_report(capital_df, operating_df, depreciation_df, kpis_df)

    # Save detailed results
    print("\n5. Saving detailed cost analysis results...")

    capital_df.to_csv(COST_DIR / "Fractal_All_Scenarios_Capital_Costs_Detailed.csv", index=False)
    operating_df.to_csv(COST_DIR / "Fractal_All_Scenarios_Operating_Costs_Detailed.csv", index=False)
    depreciation_df.to_csv(COST_DIR / "Fractal_All_Scenarios_Depreciation_Analysis.csv", index=False)
    kpis_df.to_csv(COST_DIR / "Fractal_All_Scenarios_Cost_KPIs.csv", index=False)

    print(f"  Capital costs saved: {COST_DIR / 'Fractal_All_Scenarios_Capital_Costs_Detailed.csv'}")
    print(f"  Operating costs saved: {COST_DIR / 'Fractal_All_Scenarios_Operating_Costs_Detailed.csv'}")
    print(f"  Depreciation saved: {COST_DIR / 'Fractal_All_Scenarios_Depreciation_Analysis.csv'}")
    print(f"  KPIs saved: {COST_DIR / 'Fractal_All_Scenarios_Cost_KPIs.csv'}")

    # Print summary comparison
    print("\n" + "="*80)
    print("FRACTAL LAYOUT COST ANALYSIS - SCENARIO COMPARISON")
    print("="*80)

    for _, row in kpis_df.iterrows():
        print(f"\nScenario {row['scenario'].upper()}:")
        print(f"  Centers: {row['num_centers']}")
        print(f"  Total Equipment: {row['total_equipment_units']}")
        print(f"  Equipment per Center: {row['equipment_per_center']:.1f}")
        print(f"  Capital Investment: ${row['total_capital_investment']:,.0f}")
        print(f"  Annual Operating Cost: ${row['total_annual_operating_cost']:,.0f}")
        print(f"  Capital Cost per Center: ${row['capital_cost_per_center']:,.0f}")
        print(f"  Operating Cost per Center: ${row['operating_cost_per_center']:,.0f}")
        print(f"  Average Utilization: {row['average_utilization']:.1%}")
        print(f"  Cost per Hour: ${row['total_cost_per_hour']:.2f}")

    # Find optimal scenario
    optimal_scenario = kpis_df.loc[kpis_df['total_cost_per_hour'].idxmin()]
    print(f"\nOPTIMAL SCENARIO: {optimal_scenario['scenario'].upper()}")
    print(f"  Lowest cost per hour: ${optimal_scenario['total_cost_per_hour']:.2f}")
    print(f"  Best balance of centers ({optimal_scenario['num_centers']}) and utilization ({optimal_scenario['average_utilization']:.1%})")

    print("="*80)

def create_fractal_cost_comparison_visualizations(capital_df, operating_df, kpis_df):
    """
    Create comprehensive cost comparison visualizations for all fractal scenarios
    """
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (15, 10)

    # 1. Scenario Comparison Dashboard
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('FRACTAL LAYOUT COST ANALYSIS - SCENARIO COMPARISON', fontsize=20, fontweight='bold',
                color='#2E86AB', y=0.98)

    scenarios = kpis_df['scenario'].str.upper()
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

    # Capital Investment by Scenario
    capital_costs = kpis_df['total_capital_investment'] / 1000000  # Millions
    bars1 = ax1.bar(scenarios, capital_costs, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax1.set_ylabel('Capital Investment (Millions USD)', fontsize=12, fontweight='bold')
    ax1.set_title('Capital Investment by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    for bar, cost in zip(bars1, capital_costs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${cost:.1f}M', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Operating Cost by Scenario
    operating_costs = kpis_df['total_annual_operating_cost'] / 1000  # Thousands
    bars2 = ax2.bar(scenarios, operating_costs, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax2.set_ylabel('Annual Operating Cost (Thousands USD)', fontsize=12, fontweight='bold')
    ax2.set_title('Operating Costs by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    for bar, cost in zip(bars2, operating_costs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'${cost:.0f}K', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Cost per Hour Comparison
    cost_per_hour = kpis_df['total_cost_per_hour']
    bars3 = ax3.bar(scenarios, cost_per_hour, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax3.set_ylabel('Total Cost per Operating Hour (USD)', fontsize=12, fontweight='bold')
    ax3.set_title('Cost Efficiency by Scenario', fontsize=14, fontweight='bold', pad=20)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')

    for bar, cost in zip(bars3, cost_per_hour):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'${cost:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Utilization vs Centers
    scatter = ax4.scatter(kpis_df['num_centers'], kpis_df['average_utilization'] * 100,
                         s=kpis_df['total_equipment_units'] * 5, c=colors, alpha=0.7,
                         edgecolors='black', linewidth=0.5)

    # Add scenario labels
    for i, row in kpis_df.iterrows():
        ax4.annotate(row['scenario'].upper(),
                    (row['num_centers'], row['average_utilization'] * 100),
                    xytext=(8, 8), textcoords='offset points',
                    fontsize=12, fontweight='bold')

    ax4.set_xlabel('Number of Centers', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Average Utilization (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Centers vs Utilization Efficiency\n(Bubble size = Total Equipment)', fontsize=14, fontweight='bold', pad=20)
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.set_xticks(kpis_df['num_centers'])

    plt.tight_layout()
    output_file = VISUALS_DIR / "Fractal_Layout_Scenario_Comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Scenario comparison saved: {output_file}")
    plt.close('all')

    # 2. Equipment Distribution by Scenario
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('EQUIPMENT DISTRIBUTION ANALYSIS BY FRACTAL SCENARIO', fontsize=20, fontweight='bold',
                color='#A23B72', y=0.98)

    for i, scenario in enumerate(FRACTAL_SCENARIOS):
        scenario_data = capital_df[capital_df['Scenario'] == scenario]

        if i == 0:
            ax = ax1
        elif i == 1:
            ax = ax2
        elif i == 2:
            ax = ax3
        else:
            ax = ax4

        # Equipment per process
        bars = ax.barh(scenario_data['Process'], scenario_data['Units_Required'],
                       color=colors[i], alpha=0.8, height=0.6)
        ax.set_xlabel('Equipment Units', fontsize=12, fontweight='bold')
        ax.set_ylabel('Process', fontsize=12, fontweight='bold')
        ax.set_title(f'Scenario {scenario.upper()}: Equipment Distribution', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Add total annotation
        total_equip = scenario_data['Units_Required'].sum()
        ax.text(0.02, 0.98, f'Total: {total_equip} units',
                transform=ax.transAxes, fontsize=12, fontweight='bold',
                verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3',
                facecolor='white', alpha=0.8))

    plt.tight_layout()
    output_file = VISUALS_DIR / "Fractal_Layout_Equipment_Distribution.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Equipment distribution saved: {output_file}")
    plt.close('all')

    # 3. Cost Breakdown by Process Across Scenarios
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('COST BREAKDOWN BY PROCESS ACROSS FRACTAL SCENARIOS', fontsize=20, fontweight='bold',
                color='#F18F01', y=0.98)

    axes = axes.flatten()
    processes = capital_df['Process'].unique()

    for i, process in enumerate(processes[:4]):  # Show first 4 processes
        ax = axes[i]

        process_data = capital_df[capital_df['Process'] == process]
        scenarios_proc = process_data['Scenario'].str.upper()
        capital_costs_proc = process_data['Total_Process_Cost'] / 1000000

        bars = ax.bar(scenarios_proc, capital_costs_proc, color=colors, alpha=0.8,
                      edgecolor='black', linewidth=0.5, width=0.6)

        ax.set_xlabel('Scenario', fontsize=12, fontweight='bold')
        ax.set_ylabel('Capital Cost (Millions USD)', fontsize=12, fontweight='bold')
        ax.set_title(f'Process {process}: Cost by Scenario', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        for bar, cost in zip(bars, capital_costs_proc):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    f'${cost:.2f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    output_file = VISUALS_DIR / "Fractal_Layout_Process_Cost_Breakdown.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Process cost breakdown saved: {output_file}")
    plt.close('all')

    # 4. Efficiency Frontier Analysis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))

    # Plot efficiency frontier
    scatter = ax.scatter(kpis_df['total_cost_per_hour'], kpis_df['average_utilization'] * 100,
                        s=kpis_df['num_centers'] * 200, c=range(len(kpis_df)),
                        cmap='viridis', alpha=0.7, edgecolors='black', linewidth=2)

    # Add scenario labels
    for i, row in kpis_df.iterrows():
        ax.annotate(f"{row['scenario'].upper()}\n({row['num_centers']} centers)",
                   (row['total_cost_per_hour'], row['average_utilization'] * 100),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9))

    # Add efficiency frontier line
    sorted_kpis = kpis_df.sort_values('total_cost_per_hour')
    ax.plot(sorted_kpis['total_cost_per_hour'], sorted_kpis['average_utilization'] * 100,
            'r--', linewidth=2, alpha=0.7, label='Efficiency Frontier')

    ax.set_xlabel('Total Cost per Operating Hour (USD)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Average Equipment Utilization (%)', fontsize=14, fontweight='bold')
    ax.set_title('FRACTAL LAYOUT EFFICIENCY FRONTIER ANALYSIS\n(Bubble size = Number of Centers)',
                fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right')

    plt.tight_layout()
    output_file = VISUALS_DIR / "Fractal_Layout_Efficiency_Frontier.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Efficiency frontier saved: {output_file}")
    plt.close('all')

def generate_fractal_cost_analysis_report(capital_df, operating_df, depreciation_df, kpis_df):
    """
    Generate comprehensive fractal cost analysis report
    """
    report = f"""
FRACTAL LAYOUT COMPREHENSIVE COST ANALYSIS REPORT
{'='*60}

EXECUTIVE SUMMARY
{'-'*20}
This report provides a comprehensive cost analysis for all fractal layout configurations (f2, f3, f4, f5),
including capital investment, operating costs, depreciation, and comparative efficiency analysis.

FRACTAL CONFIGURATION OVERVIEW
{'-'*35}
"""

    for _, row in kpis_df.iterrows():
        report += f"""
Scenario {row['scenario'].upper()}:
  Centers: {row['num_centers']}
  Total Equipment: {row['total_equipment_units']} units
  Equipment per Center: {row['equipment_per_center']:.1f}
  Average Utilization: {row['average_utilization']:.1%}
"""

    report += f"""

CAPITAL INVESTMENT ANALYSIS
{'-'*30}
"""

    # Capital costs summary by scenario
    for scenario in FRACTAL_SCENARIOS:
        scenario_capital = capital_df[capital_df['Scenario'] == scenario]
        total_capital = scenario_capital['Total_Process_Cost'].sum()

        report += f"""
Scenario {scenario.upper()} - Total Capital Investment: ${total_capital:,.0f}
Top cost components:
"""

        top_costs = scenario_capital.nlargest(5, 'Total_Process_Cost')
        for _, row in top_costs.iterrows():
            report += f"  Process {row['Process']}: ${row['Total_Process_Cost']:,.0f} ({row['Units_Required']} units)\n"

    report += f"""

OPERATING COST ANALYSIS
{'-'*25}
"""

    # Operating costs summary by scenario
    for scenario in FRACTAL_SCENARIOS:
        scenario_operating = operating_df[operating_df['Scenario'] == scenario]
        total_operating = scenario_operating['Annual_Labor_Cost'].sum()
        total_operators = scenario_operating['Total_Operators'].sum()

        report += f"""
Scenario {scenario.upper()}:
  Annual Operating Cost: ${total_operating:,.0f}
  Total Operators Required: {total_operators:.1f} FTEs
  Average Cost per Operator: ${total_operating/total_operators:,.0f}/year

Labor cost breakdown (top 5 processes):
"""

        top_labor = scenario_operating.nlargest(5, 'Annual_Labor_Cost')
        for _, row in top_labor.iterrows():
            report += f"  Process {row['Process']}: ${row['Annual_Labor_Cost']:,.0f}/year ({row['Total_Operators']:.1f} operators)\n"

    report += f"""

COST EFFICIENCY ANALYSIS
{'-'*26}
"""

    # Efficiency comparison
    efficiency_data = kpis_df[['scenario', 'total_cost_per_hour', 'average_utilization', 'num_centers']].copy()
    efficiency_data['scenario'] = efficiency_data['scenario'].str.upper()

    report += f"""
Cost Efficiency Comparison:
"""

    for _, row in efficiency_data.iterrows():
        report += f"  {row['scenario']}: ${row['total_cost_per_hour']:.2f}/hour, {row['average_utilization']:.1%} utilization\n"

    # Find optimal scenario
    optimal = kpis_df.loc[kpis_df['total_cost_per_hour'].idxmin()]
    report += f"""

OPTIMAL CONFIGURATION: {optimal['scenario'].upper()}
{'-'*30}
• Lowest cost per operating hour: ${optimal['total_cost_per_hour']:.2f}
• {optimal['num_centers']} fractal centers
• Average utilization: {optimal['average_utilization']:.1%}
• Total equipment: {optimal['total_equipment_units']} units
• Capital investment: ${optimal['total_capital_investment']:,.0f}
• Annual operating cost: ${optimal['total_annual_operating_cost']:,.0f}

SCALING ANALYSIS
{'-'*18}
Equipment scaling with centers:
"""

    for _, row in kpis_df.iterrows():
        report += f"  {row['scenario'].upper()}: {row['equipment_per_center']:.1f} equipment units per center\n"

    report += f"""

Cost scaling with centers:
"""

    for _, row in kpis_df.iterrows():
        report += f"  {row['scenario'].upper()}: ${row['capital_cost_per_center']:,.0f} capital per center\n"

    report += f"""

RECOMMENDATIONS
{'-'*15}
1. OPTIMAL CHOICE: {optimal['scenario'].upper()} configuration provides the best cost-efficiency balance
2. Equipment scaling shows diminishing returns beyond {optimal['num_centers']} centers
3. Higher center counts ({kpis_df['num_centers'].max()}) increase complexity without proportional efficiency gains
4. Focus on utilization optimization rather than excessive decentralization
5. Consider hybrid approaches combining fractal centers with functional specialization

All analysis results and visualizations saved to: {COST_DIR}
"""

    # Save report
    with open(COST_DIR / "Fractal_Layout_Cost_Analysis_Report.txt", 'w') as f:
        f.write(report)

    print(f"Comprehensive cost analysis report saved: {COST_DIR / 'Fractal_Layout_Cost_Analysis_Report.txt'}")

def main():
    """
    Main function for fractal layout comprehensive cost analysis
    """
    analyze_all_fractal_scenarios()

if __name__ == "__main__":
    main()