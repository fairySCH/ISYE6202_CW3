"""
Year 2 PART 1 ONLY - Machine Requirements (2 Shifts)
This calculates ONLY for P1 (26,100 units/week), not all parts!
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
DEMAND_P1 = 26100  # units per week
MINUTES_PER_MACHINE_2SHIFT = 4800  # 2 shifts × 8 hours × 5 days × 60 min
TARGET_UTILIZATION = 0.99

def calculate_machines():
    print("YEAR 2 PART 1 ONLY - MACHINE REQUIREMENTS (2 SHIFTS)")
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
    
    return {
        'B1': b1,
        'A': results['A']['machines'],
        'B2': b2,
        'C': results['C']['machines'],
        'D': results['D']['machines'],
        'I': results['I']['machines'],
        'J': results['J']['machines'],
        'total': total_machines
    }

if __name__ == "__main__":
    machine_counts = calculate_machines()
