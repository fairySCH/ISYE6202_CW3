"""
Batch update all year files to use Approach 1 (99% utilization)
"""
import os
from pathlib import Path

# Machine counts for each year using Approach 1
YEAR_CONFIGS = {
    'Year1': {'B1': 12, 'A': 5, 'B2': 12, 'C': 3, 'D': 12, 'I': 6, 'J': 12, 'demand': 20961.54},
    'Year2': {'B1': 14, 'A': 6, 'B2': 14, 'C': 3, 'D': 14, 'I': 7, 'J': 14, 'demand': 26100},
    'Year3': {'B1': 15, 'A': 6, 'B2': 15, 'C': 3, 'D': 15, 'I': 8, 'J': 15, 'demand': 27300},
    'Year4': {'B1': 15, 'A': 6, 'B2': 15, 'C': 3, 'D': 15, 'I': 8, 'J': 15, 'demand': 28500},
    'Year5': {'B1': 16, 'A': 7, 'B2': 16, 'C': 4, 'D': 16, 'I': 8, 'J': 16, 'demand': 29800},
}

def generate_calculate_script(year, config):
    """Generate calculate_PART1_ONLY.py content"""
    demand = int(config['demand'])
    year_num = year.replace('Year', '')
    
    content = f'''"""
{year} PART 1 ONLY - Machine Requirements (2 Shifts)
This calculates ONLY for P1 ({demand:,} units/week), not all parts!
Uses Process-Based approach (Approach 1) with 99% target utilization.
"""

from pathlib import Path
import math

# Part 1 process sequence - each step gets dedicated machines
P1_SEQUENCE = [
    {{'step': 1, 'process': 'B', 'time_per_unit': 2.5, 'label': 'B1'}},
    {{'step': 2, 'process': 'A', 'time_per_unit': 1.0, 'label': 'A'}},
    {{'step': 3, 'process': 'B', 'time_per_unit': 2.5, 'label': 'B2'}},
    {{'step': 4, 'process': 'C', 'time_per_unit': 0.5, 'label': 'C'}},
    {{'step': 5, 'process': 'D', 'time_per_unit': 2.5, 'label': 'D'}},
    {{'step': 6, 'process': 'I', 'time_per_unit': 1.25, 'label': 'I'}},
    {{'step': 7, 'process': 'J', 'time_per_unit': 2.5, 'label': 'J'}},
]

# Constants
DEMAND_P1 = {demand}  # units per week
MINUTES_PER_MACHINE_2SHIFT = 4800  # 2 shifts × 8 hours × 5 days × 60 min
TARGET_UTILIZATION = 0.99  # 99% target utilization

def calculate_machines():
    print("{year.upper()} PART 1 ONLY - MACHINE REQUIREMENTS (2 SHIFTS)")
    print("=" * 70)
    print(f"Part 1 (P1) Weekly Demand: {{DEMAND_P1:,}} units")
    print(f"Machine Capacity (2-shift): {{MINUTES_PER_MACHINE_2SHIFT:,}} minutes/week")
    print(f"Target Utilization: {{TARGET_UTILIZATION:.0%}}")
    print(f"Effective Capacity per Machine: {{MINUTES_PER_MACHINE_2SHIFT * TARGET_UTILIZATION:,.1f}} minutes/week")
    print()
    
    results = {{}}
    total_minutes = 0
    total_machines = 0
    effective_capacity = MINUTES_PER_MACHINE_2SHIFT * TARGET_UTILIZATION
    
    print("Process-by-Process Breakdown (Process-Based - 99% Utilization):")
    print("-" * 70)
    print(f"{{'Step':<6}} {{'Process':<10}} {{'Weekly Min':>12}} {{'Machines':>10}} {{'Util %':>10}}")
    print("-" * 70)
    
    for step_data in P1_SEQUENCE:
        # Calculate weekly minutes needed
        weekly_minutes = DEMAND_P1 * step_data['time_per_unit']
        total_minutes += weekly_minutes
        
        # Calculate machines needed using 99% target utilization
        machines_needed = weekly_minutes / effective_capacity
        machines_rounded = math.ceil(machines_needed)
        
        # Calculate actual utilization
        actual_utilization = (weekly_minutes / (machines_rounded * effective_capacity)) * 100
        
        label = step_data['label']
        results[label] = {{
            'step': step_data['step'],
            'process': step_data['process'],
            'weekly_minutes': weekly_minutes,
            'machines': machines_rounded,
            'utilization': actual_utilization
        }}
        
        total_machines += machines_rounded
        
        print(f"{{step_data['step']:<6}} {{label:<10}} {{weekly_minutes:>12,.0f}} {{machines_rounded:>10}} {{actual_utilization:>9.1f}}%")
    
    print("-" * 70)
    print(f"{{'TOTAL':<6}} {{'':<10}} {{total_minutes:>12,.0f}} {{total_machines:>10}}")
    print()
    
    print("Process Flow Grouping (B1 → A → B2 → C → D → I → J):")
    print("-" * 70)
    print(f"  B1: {{results['B1']['machines']}} machines")
    print(f"  A:  {{results['A']['machines']}} machines")
    print(f"  B2: {{results['B2']['machines']}} machines")
    print(f"  C:  {{results['C']['machines']}} machines")
    print(f"  D:  {{results['D']['machines']}} machines")
    print(f"  I:  {{results['I']['machines']}} machines")
    print(f"  J:  {{results['J']['machines']}} machines")
    print()
    print(f"TOTAL for Part 1 layout: {{total_machines}} machines")
    print()
    
    return {{
        'B1': results['B1']['machines'],
        'A': results['A']['machines'],
        'B2': results['B2']['machines'],
        'C': results['C']['machines'],
        'D': results['D']['machines'],
        'I': results['I']['machines'],
        'J': results['J']['machines'],
        'total': total_machines
    }}

if __name__ == "__main__":
    machine_counts = calculate_machines()
'''
    return content

# Update files
base_path = Path(__file__).parent / "results" / "task4" / "part" / "Jatin"

for year, config in YEAR_CONFIGS.items():
    year_path = base_path / year
    if year == 'Year1':
        year_path = Path(__file__).parent / "results" / "Task3" / "Part" / "Jatin"
    
    # Create calculate script
    calc_file = year_path / "calculate_PART1_ONLY.py"
    print(f"Updating {calc_file}...")
    with open(calc_file, 'w', encoding='utf-8') as f:
        f.write(generate_calculate_script(year, config))
    
    print(f"✓ {year} calculation script updated")

print("\nAll files updated successfully!")
print("\nSummary:")
for year, config in YEAR_CONFIGS.items():
    total = sum(v for k, v in config.items() if k != 'demand')
    print(f"{year}: {total} machines - B1={config['B1']}, A={config['A']}, B2={config['B2']}, C={config['C']}, D={config['D']}, I={config['I']}, J={config['J']}")
