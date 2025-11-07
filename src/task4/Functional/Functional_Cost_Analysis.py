"""
Task 4: Functional Layout - Cost Analysis (Years 2-5)

Comprehensive cost analysis for functional layout across years 2-5 including:
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
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to ISYE6202_CW3 directory
DATA_DIR = BASE_DIR / "data" / "csv_outputs"
RESULTS_DIR = BASE_DIR / "results" / "task4" / "functional"
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
    Load equipment requirements from functional layout analysis
    """
    equipment_df = pd.read_csv(COST_DIR.parent / "Capacity" / "Functional_Equipment_Requirements_All_Years.csv")
    efficiency_df = pd.read_csv(COST_DIR.parent / "Capacity" / "Functional_Layout_Efficiency_Metrics_All_Years.csv")

    return equipment_df, efficiency_df

def calculate_capital_costs(equipment_df, cost_df):
    """
    Calculate total capital investment costs for functional layout across years
    """
    capital_costs = []

    for _, row in equipment_df.iterrows():
        year = row['Year']
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
            'Year': year,
            'Process': process,
            'Units_Required': units_needed,
            'Cost_Per_Unit': total_cost_per_unit,
            'Total_Installed_Cost': installed_price * units_needed,
            'Total_Relocation_Cost': relocation_cost * units_needed,
            'Total_Process_Cost': total_process_cost,
            'Utilization_2_Shifts': row['Utilization_2_Shifts']
        })

    return pd.DataFrame(capital_costs)

def calculate_operating_costs(equipment_df, cost_df):
    """
    Calculate annual operating costs (labor) for functional layout
    """
    operating_costs = []

    for _, row in equipment_df.iterrows():
        year = row['Year']
        process = row['Process']
        units_2shift = int(row['Equipment_2_Shifts'])

        if units_2shift == 0:
            continue

        # Find hourly labor cost for this process
        cost_row = cost_df[cost_df['Equipment'] == process]

        if cost_row.empty:
            print(f"Warning: No labor cost data found for process {process}")
            continue

        hourly_cost = cost_row['Hourly Cost'].iloc[0]
        if pd.isna(hourly_cost):
            continue

        # Calculate annual operating cost
        # 2 shifts per day, each requiring one operator per machine
        annual_operating_cost = units_2shift * hourly_cost * HOURS_PER_YEAR

        operating_costs.append({
            'Year': year,
            'Process': process,
            'Units_2_Shifts': units_2shift,
            'Hourly_Cost': hourly_cost,
            'Annual_Operating_Cost': annual_operating_cost,
            'Utilization_2_Shifts': row['Utilization_2_Shifts']
        })

    return pd.DataFrame(operating_costs)

def calculate_depreciation(cost_df, useful_life_years=10):
    """
    Calculate annual depreciation costs
    """
    depreciation_costs = []

    for _, row in cost_df.iterrows():
        year = row['Year']
        process = row['Process']
        total_installed_cost = row['Total_Installed_Cost']
        units = row['Units_Required']

        if total_installed_cost == 0:
            continue

        # Straight-line depreciation
        annual_depreciation = total_installed_cost / useful_life_years

        depreciation_costs.append({
            'Year': year,
            'Process': process,
            'Total_Installed_Cost': total_installed_cost,
            'Units': units,
            'Useful_Life_Years': useful_life_years,
            'Annual_Depreciation': annual_depreciation
        })

    return pd.DataFrame(depreciation_costs)

def calculate_cost_efficiency_metrics(capital_df, operating_df, depreciation_df, equipment_df):
    """
    Calculate comprehensive cost efficiency metrics
    """
    metrics = []

    for year in equipment_df['Year'].unique():
        year_equipment = equipment_df[equipment_df['Year'] == year]
        year_capital = capital_df[capital_df['Year'] == year]
        year_operating = operating_df[operating_df['Year'] == year]
        year_depreciation = depreciation_df[depreciation_df['Year'] == year]

        # Total costs
        total_capital = year_capital['Total_Process_Cost'].sum()
        total_operating = year_operating['Annual_Operating_Cost'].sum()
        total_depreciation = year_depreciation['Annual_Depreciation'].sum()

        # Equipment efficiency
        total_equipment = year_equipment['Equipment_2_Shifts'].sum()
        avg_utilization = year_equipment['Utilization_2_Shifts'].mean()

        # Cost per unit of capacity
        total_weekly_hours = year_equipment['Weekly_Hours'].sum()
        if total_weekly_hours > 0:
            capital_cost_per_hour = (total_capital / 10) / (total_weekly_hours * WEEKS_PER_YEAR)  # Annualized
            operating_cost_per_hour = total_operating / (total_weekly_hours * WEEKS_PER_YEAR)
            total_cost_per_hour = capital_cost_per_hour + operating_cost_per_hour
        else:
            capital_cost_per_hour = operating_cost_per_hour = total_cost_per_hour = 0

        metrics.append({
            'Year': year,
            'Total_Capital_Cost': total_capital,
            'Total_Annual_Operating_Cost': total_operating,
            'Total_Annual_Depreciation': total_depreciation,
            'Total_Equipment_Units': total_equipment,
            'Average_Utilization': avg_utilization,
            'Capital_Cost_Per_Hour': capital_cost_per_hour,
            'Operating_Cost_Per_Hour': operating_cost_per_hour,
            'Total_Cost_Per_Hour': total_cost_per_hour,
            'Total_Weekly_Production_Hours': total_weekly_hours
        })

    return pd.DataFrame(metrics)

def create_cost_visualizations(capital_df, operating_df, metrics_df):
    """
    Create comprehensive cost analysis visualizations
    """
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (16, 10)

    # 1. Capital Cost Breakdown by Year and Process
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))

    # Capital costs by year
    yearly_capital = capital_df.groupby('Year')['Total_Process_Cost'].sum().reset_index()
    bars1 = ax1.bar(yearly_capital['Year'], yearly_capital['Total_Process_Cost']/1e6, color='steelblue', alpha=0.8)
    ax1.set_title('Functional Layout: Total Capital Investment by Year', fontweight='bold', fontsize=14)
    ax1.set_ylabel('Capital Cost (Millions $)', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'${height:.1f}M', ha='center', va='bottom', fontsize=10)

    # Operating costs by year
    yearly_operating = operating_df.groupby('Year')['Annual_Operating_Cost'].sum().reset_index()
    bars2 = ax2.bar(yearly_operating['Year'], yearly_operating['Annual_Operating_Cost']/1e6, color='coral', alpha=0.8)
    ax2.set_title('Functional Layout: Annual Operating Costs by Year', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Operating Cost (Millions $/year)', fontweight='bold', fontsize=12)
    ax2.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height, f'${height:.1f}M', ha='center', va='bottom', fontsize=10)

    # Cost per hour comparison
    years = metrics_df['Year']
    capital_per_hour = metrics_df['Capital_Cost_Per_Hour']
    operating_per_hour = metrics_df['Operating_Cost_Per_Hour']

    x = np.arange(len(years))
    width = 0.35

    bars3 = ax3.bar(x - width/2, capital_per_hour, width, label='Capital Cost/Hour', color='steelblue', alpha=0.8)
    bars4 = ax3.bar(x + width/2, operating_per_hour, width, label='Operating Cost/Hour', color='coral', alpha=0.8)

    ax3.set_title('Functional Layout: Cost Efficiency by Year', fontweight='bold', fontsize=14)
    ax3.set_ylabel('Cost per Production Hour ($)', fontweight='bold', fontsize=12)
    ax3.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax3.set_xticks(x)
    ax3.set_xticklabels(years)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)

    # Equipment utilization vs cost efficiency
    utilization = metrics_df['Average_Utilization']
    total_cost_per_hour = metrics_df['Total_Cost_Per_Hour']

    # Use numerical year values for coloring
    year_nums = [int(str(y).replace('+', '')) for y in metrics_df['Year']]
    scatter = ax4.scatter(utilization, total_cost_per_hour, s=100, c=year_nums, cmap='viridis', alpha=0.8)
    ax4.set_title('Functional Layout: Utilization vs Cost Efficiency', fontweight='bold', fontsize=14)
    ax4.set_xlabel('Average Equipment Utilization (%)', fontweight='bold', fontsize=12)
    ax4.set_ylabel('Total Cost per Production Hour ($)', fontweight='bold', fontsize=12)
    ax4.grid(alpha=0.3)

    # Add year labels to points
    for i, year in enumerate(metrics_df['Year']):
        ax4.annotate(f'Year {year}', (utilization.iloc[i], total_cost_per_hour.iloc[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=10)

    plt.tight_layout()
    plt.savefig(VISUALS_DIR / 'Functional_Cost_Analysis_Overview.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Process-wise cost distribution (Year +5 as example)
    year5_capital = capital_df[capital_df['Year'] == '+5']
    year5_operating = operating_df[operating_df['Year'] == '+5']

    if not year5_capital.empty and not year5_operating.empty:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Capital cost by process
        capital_by_process = year5_capital.set_index('Process')['Total_Process_Cost']/1e3
        capital_by_process.plot(kind='barh', ax=ax1, color='steelblue', alpha=0.8)
        ax1.set_title('Year +5: Capital Cost by Process', fontweight='bold', fontsize=14)
        ax1.set_xlabel('Capital Cost (Thousands $)', fontweight='bold', fontsize=12)
        ax1.grid(axis='x', alpha=0.3)

        # Operating cost by process
        operating_by_process = year5_operating.set_index('Process')['Annual_Operating_Cost']/1e3
        operating_by_process.plot(kind='barh', ax=ax2, color='coral', alpha=0.8)
        ax2.set_title('Year +5: Annual Operating Cost by Process', fontweight='bold', fontsize=14)
        ax2.set_xlabel('Operating Cost (Thousands $/year)', fontweight='bold', fontsize=12)
        ax2.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        plt.savefig(VISUALS_DIR / 'Functional_Cost_By_Process_Year5.png', dpi=300, bbox_inches='tight')
        plt.close()

    print(f"Cost visualizations saved to {VISUALS_DIR}")

def main():
    """
    Main cost analysis for functional layout across years 2-5
    """
    print("="*80)
    print("TASK 4: FUNCTIONAL LAYOUT - COST ANALYSIS (YEARS 2-5)")
    print("="*80)

    # Ensure output directories exist
    COST_DIR.mkdir(parents=True, exist_ok=True)
    VISUALS_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Load data
    print("\n1. Loading Data...")
    cost_df = load_equipment_costs()
    equipment_df, efficiency_df = load_equipment_requirements()

    # Step 2: Calculate capital costs
    print("\n2. Calculating Capital Costs...")
    capital_df = calculate_capital_costs(equipment_df, cost_df)

    # Step 3: Calculate operating costs
    print("\n3. Calculating Operating Costs...")
    operating_df = calculate_operating_costs(equipment_df, cost_df)

    # Step 4: Calculate depreciation
    print("\n4. Calculating Depreciation...")
    depreciation_df = calculate_depreciation(capital_df)

    # Step 5: Calculate cost efficiency metrics
    print("\n5. Calculating Cost Efficiency Metrics...")
    metrics_df = calculate_cost_efficiency_metrics(capital_df, operating_df, depreciation_df, equipment_df)

    # Step 6: Create visualizations
    print("\n6. Creating Visualizations...")
    create_cost_visualizations(capital_df, operating_df, metrics_df)

    # Step 7: Save all results
    print("\n7. Saving Results...")

    # Save detailed cost breakdowns
    capital_df.to_csv(COST_DIR / "Functional_Capital_Costs_All_Years.csv", index=False)
    print(f"  Saved: {COST_DIR / 'Functional_Capital_Costs_All_Years.csv'}")

    operating_df.to_csv(COST_DIR / "Functional_Operating_Costs_All_Years.csv", index=False)
    print(f"  Saved: {COST_DIR / 'Functional_Operating_Costs_All_Years.csv'}")

    depreciation_df.to_csv(COST_DIR / "Functional_Depreciation_Costs_All_Years.csv", index=False)
    print(f"  Saved: {COST_DIR / 'Functional_Depreciation_Costs_All_Years.csv'}")

    metrics_df.to_csv(COST_DIR / "Functional_Cost_Efficiency_Metrics_All_Years.csv", index=False)
    print(f"  Saved: {COST_DIR / 'Functional_Cost_Efficiency_Metrics_All_Years.csv'}")

    # Generate summary report
    print("\n8. Generating Summary Report...")
    summary_report = f"""
FUNCTIONAL LAYOUT COST ANALYSIS SUMMARY (YEARS 2-5)
{'='*60}

Cost Analysis Overview:
- Analysis Period: Years +2 to +5
- Depreciation Period: 10 years (straight-line)
- Operating Schedule: 2 shifts/day, 5 days/week

YEAR-BY-YEAR COST SUMMARY:
"""

    for _, row in metrics_df.iterrows():
        summary_report += f"""
Year {row['Year']}:
- Total Capital Investment: ${row['Total_Capital_Cost']/1e6:,.1f}M
- Annual Operating Cost: ${row['Total_Annual_Operating_Cost']/1e6:,.1f}M
- Annual Depreciation: ${row['Total_Annual_Depreciation']/1e6:,.1f}M
- Total Equipment Units: {row['Total_Equipment_Units']}
- Average Utilization: {row['Average_Utilization']:.1f}%
- Capital Cost/Hour: ${row['Capital_Cost_Per_Hour']:.2f}
- Operating Cost/Hour: ${row['Operating_Cost_Per_Hour']:.2f}
- Total Cost/Hour: ${row['Total_Cost_Per_Hour']:.2f}
"""

    # Cost trends analysis
    capital_trend = metrics_df['Total_Capital_Cost'].pct_change().mean() * 100
    operating_trend = metrics_df['Total_Annual_Operating_Cost'].pct_change().mean() * 100

    summary_report += f"""

COST TRENDS ANALYSIS:
- Average Annual Capital Cost Growth: {capital_trend:.1f}%
- Average Annual Operating Cost Growth: {operating_trend:.1f}%

KEY INSIGHTS:
- All processes require equipment investment (functional layout specialization)
- Operating costs scale with equipment requirements and utilization
- Higher utilization in later years improves cost efficiency
- Capital costs represent significant long-term investment

RECOMMENDATIONS:
- Consider equipment sharing opportunities between similar processes
- Monitor utilization rates for capacity optimization
- Plan for technology upgrades to improve cost efficiency
"""

    # Save summary report
    with open(COST_DIR / "Functional_Cost_Analysis_Summary_All_Years.txt", 'w') as f:
        f.write(summary_report)
    print(f"  Saved: {COST_DIR / 'Functional_Cost_Analysis_Summary_All_Years.txt'}")

    print("\n" + "="*80)
    print("FUNCTIONAL LAYOUT COST ANALYSIS COMPLETE (YEARS 2-5)!")
    print("="*80)
    print(f"All results saved to: {COST_DIR}")
    print("="*80)

if __name__ == "__main__":
    main()