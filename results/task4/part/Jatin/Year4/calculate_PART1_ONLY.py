"""
Year 4 PART 1 ONLY - Machine Requirements (2 Shifts)
This calculates ONLY for P1 (28,500 units/week), not all parts!
"""

from pathlib import Path

# Part 1 process times (from Process_Workload_Breakdown.csv)
P1_PROCESSES = {
    'A': {'time_per_unit': 1.0, 'operations': 1},
    'B': {'time_per_unit': 2.5, 'operations': 2},  # P1 goes through B twice
    'C': {'time_per_unit': 0.5, 'operations': 1},
    'D': {'time_per_unit': 2.5, 'operations': 1},
    'I': {'time_per_unit': 1.25, 'operations': 1},
    'J': {'time_per_unit': 2.5, 'operations': 1},
}

# Constants
DEMAND_P1 = 28500  # units per week
MINUTES_PER_MACHINE_2SHIFT = 4800  # 2 shifts × 8 hours × 5 days × 60 min
TARGET_UTILIZATION = 0.99

def calculate_machines():
    print("YEAR 4 PART 1 ONLY - MACHINE REQUIREMENTS (2 SHIFTS)")
    print("=" * 70)
    print(f"Part 1 (P1) Weekly Demand: {DEMAND_P1:,} units")
    print(f"Machine Capacity (2-shift): {MINUTES_PER_MACHINE_2SHIFT:,} minutes/week")
    print()
    
    results = {}
    total_minutes = 0
    
    for process, data in P1_PROCESSES.items():
        # Calculate weekly minutes needed
        weekly_minutes = DEMAND_P1 * data['time_per_unit'] * data['operations']
        total_minutes += weekly_minutes
        
        # Calculate machines needed
        machines_needed = weekly_minutes / (MINUTES_PER_MACHINE_2SHIFT * TARGET_UTILIZATION)
        machines_rounded = int(machines_needed) + (1 if machines_needed % 1 > 0 else 0)
        
        # Calculate actual utilization
        actual_utilization = (weekly_minutes / (machines_rounded * MINUTES_PER_MACHINE_2SHIFT)) * 100
        
        results[process] = {
            'weekly_minutes': weekly_minutes,
            'machines': machines_rounded,
            'utilization': actual_utilization,
            'operations': data['operations']
        }
    
    # Display results
    print("Process-by-Process Breakdown:")
    print("-" * 70)
    print(f"{'Process':<10} {'Weekly Min':>12} {'Operations':>11} {'Machines':>10} {'Util %':>10}")
    print("-" * 70)
    
    total_machines = 0
    for process in ['A', 'B', 'C', 'D', 'I', 'J']:
        data = results[process]
        total_machines += data['machines']
        print(f"{process:<10} {data['weekly_minutes']:>12,.0f} {data['operations']:>11} "
              f"{data['machines']:>10} {data['utilization']:>9.1f}%")
    
    print("-" * 70)
    print(f"{'TOTAL':<10} {total_minutes:>12,.0f} {' ':>11} {total_machines:>10}")
    print()
    
    # B split (since P1 goes through B twice, split into B1 and B2)
    b_machines = results['B']['machines']
    b1 = b_machines // 2
    b2 = b_machines - b1
    
    print("Process Flow Grouping (B1 → A → B2 → C → D → I → J):")
    print("-" * 70)
    print(f"  B1: {b1} machines (first B operation)")
    print(f"  A:  {results['A']['machines']} machines")
    print(f"  B2: {b2} machines (second B operation)")
    print(f"  C:  {results['C']['machines']} machines")
    print(f"  D:  {results['D']['machines']} machines")
    print(f"  I:  {results['I']['machines']} machines")
    print(f"  J:  {results['J']['machines']} machines")
    print()
    print(f"TOTAL for Part 1 layout: {total_machines} machines")
    print()
    
    # Save output
    output_file = Path(__file__).parent / 'Year4_Part1_ONLY_Machine_Requirements.txt'
    with open(output_file, 'w') as f:
        f.write("Year 4 PART 1 ONLY - Machine Requirements (2-SHIFT)\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Part 1 (P1) Weekly Demand: {DEMAND_P1:,} units\n")
        f.write(f"Total Capacity Required: {total_minutes:,.0f} minutes/week\n")
        f.write(f"Total Equipment (2 shifts): {total_machines} machines\n\n")
        
        f.write("Machine Counts by Process:\n")
        for process in ['A', 'B', 'C', 'D', 'I', 'J']:
            data = results[process]
            f.write(f"  {process}: {data['machines']} machines ({data['utilization']:.1f}% utilization)\n")
        
        f.write(f"\nLayout Grouping:\n")
        f.write(f"  B1: {b1} | A: {results['A']['machines']} | B2: {b2} | C: {results['C']['machines']} | ")
        f.write(f"D: {results['D']['machines']} | I: {results['I']['machines']} | J: {results['J']['machines']}\n")
    
    print(f"Output saved to: {output_file}")
    
    # Comparison note
    print()
    print("COMPARISON:")
    print("-" * 70)
    print("Year 5 Part 1 (from Jatin folder): ~129 machines")
    print(f"Year 4 Part 1 (this calculation):  {total_machines} machines")
    print()
    if total_machines > 129:
        print(f"Year 4 needs {total_machines - 129} MORE machines than Year 5")
        print("This makes sense: Year 4 demand is 28,500 vs Year 5's 20,000 (42.5% higher)")

if __name__ == '__main__':
    calculate_machines()
