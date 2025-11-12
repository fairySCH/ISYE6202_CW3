"""
Task 3 - Parts-Based Design: Metrics Calculator
Calculates 4 key metrics for the parts-based layout:
1. Distance per trip (rectilinear/Manhattan distance)
2. Net utilization (weighted average across all processes)
3. Cost of equipment
4. Total area
"""

import csv
from pathlib import Path

# Machine counts for Task 3
AREAS = {
    "A": {"count": 10, "rows": 5, "cols": 2},
    "B": {"count": 32, "rows": 8, "cols": 4},
    "C": {"count": 9,  "rows": 3, "cols": 3},
    "D": {"count": 45, "rows": 9, "cols": 5},
    "E": {"count": 20, "rows": 4, "cols": 5},
    "F": {"count": 24, "rows": 4, "cols": 6},
    "G": {"count": 9,  "rows": 3, "cols": 3},
    "H": {"count": 31, "rows": 4, "cols": 8},
    "I": {"count": 28, "rows": 4, "cols": 7},
    "J": {"count": 49, "rows": 7, "cols": 7},
    "K": {"count": 7,  "rows": 2, "cols": 4},
    "L": {"count": 31, "rows": 4, "cols": 8},
    "M": {"count": 49, "rows": 7, "cols": 7},
}

# Equipment unit costs (in dollars) - from Equip+Operator Specs.csv
EQUIPMENT_COSTS = {
    "A": 200000,   # $200k
    "B": 150000,   # $150k
    "C": 180000,   # $180k
    "D": 175000,   # $175k
    "E": 220000,   # $220k
    "F": 195000,   # $195k
    "G": 210000,   # $210k
    "H": 185000,   # $185k
    "I": 220000,   # $220k
    "J": 195000,   # $195k
    "K": 230000,   # $230k
    "L": 240000,   # $240k
    "M": 250000,   # $250k
}

# Process times and weekly workload (from calculate_ALL_PROCESSES.py)
PROCESS_WORKLOAD = {
    "A": 47163.46,
    "B": 149471.15,
    "C": 38269.23,
    "D": 211250.00,
    "E": 93846.15,
    "F": 110480.77,
    "G": 38365.38,
    "H": 142980.77,
    "I": 131057.69,
    "J": 230625.00,
    "K": 29759.62,
    "L": 144519.23,
    "M": 231634.62,
}

# 2-shift capacity
MINUTES_PER_WEEK = 4800  # 2 shifts × 5 days × 8 hours × 60 min

def load_layout_centers():
    """Load area center coordinates from layout summary CSV"""
    layout_file = Path(__file__).parent / "Optimized_Layout_Summary.csv"
    
    centers = {}
    with open(layout_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Area'] in AREAS:
                centers[row['Area']] = {
                    'x': float(row['Center_X']),
                    'y': float(row['Center_Y'])
                }
    
    return centers

def calculate_distance_per_trip(centers):
    """
    Calculate average distance per trip using rectilinear (Manhattan) distance
    Based on process flow sequences from all 20 parts
    """
    # Define all process transitions from the 20 parts
    # P1: B→A→B→C→D→I→J
    # P2: A→C→D→H→J
    # P3: B→D→C→I→J
    # P4: A→B→D→G→H
    # P5: B→C→D→I
    # P6: A→B→C→D→H→I→J
    # P7: C→D→E→F→I→J
    # P8: E→H→I→J
    # P9: E→F→G→I→J
    # P10: E→F→I→J
    # P11: E→G→I
    # P12: E→F→G→I→J
    # P13: E→F→G→H→I
    # P14: E→F→G→H
    # P15: E→F→G→H→J
    # P16: F→H→I→J
    # P17: K→L→M
    # P18: K→L→M
    # P19: L→M
    # P20: K→L→M
    
    transitions = [
        # P1: B→A, A→B, B→C, C→D, D→I, I→J
        ("B", "A"), ("A", "B"), ("B", "C"), ("C", "D"), ("D", "I"), ("I", "J"),
        # P2: A→C, C→D, D→H, H→J
        ("A", "C"), ("C", "D"), ("D", "H"), ("H", "J"),
        # P3: B→D, D→C, C→I, I→J
        ("B", "D"), ("D", "C"), ("C", "I"), ("I", "J"),
        # P4: A→B, B→D, D→G, G→H
        ("A", "B"), ("B", "D"), ("D", "G"), ("G", "H"),
        # P5: B→C, C→D, D→I
        ("B", "C"), ("C", "D"), ("D", "I"),
        # P6: A→B, B→C, C→D, D→H, H→I, I→J
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "H"), ("H", "I"), ("I", "J"),
        # P7: C→D, D→E, E→F, F→I, I→J
        ("C", "D"), ("D", "E"), ("E", "F"), ("F", "I"), ("I", "J"),
        # P8: E→H, H→I, I→J
        ("E", "H"), ("H", "I"), ("I", "J"),
        # P9: E→F, F→G, G→I, I→J
        ("E", "F"), ("F", "G"), ("G", "I"), ("I", "J"),
        # P10: E→F, F→I, I→J
        ("E", "F"), ("F", "I"), ("I", "J"),
        # P11: E→G, G→I
        ("E", "G"), ("G", "I"),
        # P12: E→F, F→G, G→I, I→J
        ("E", "F"), ("F", "G"), ("G", "I"), ("I", "J"),
        # P13: E→F, F→G, G→H, H→I
        ("E", "F"), ("F", "G"), ("G", "H"), ("H", "I"),
        # P14: E→F, F→G, G→H
        ("E", "F"), ("F", "G"), ("G", "H"),
        # P15: E→F, F→G, G→H, H→J
        ("E", "F"), ("F", "G"), ("G", "H"), ("H", "J"),
        # P16: F→H, H→I, I→J
        ("F", "H"), ("H", "I"), ("I", "J"),
        # P17: K→L, L→M
        ("K", "L"), ("L", "M"),
        # P18: K→L, L→M
        ("K", "L"), ("L", "M"),
        # P19: L→M
        ("L", "M"),
        # P20: K→L, L→M
        ("K", "L"), ("L", "M"),
    ]
    
    total_distance = 0
    trip_count = 0
    
    for from_area, to_area in transitions:
        if from_area in centers and to_area in centers:
            # Calculate rectilinear distance
            dx = abs(centers[to_area]['x'] - centers[from_area]['x'])
            dy = abs(centers[to_area]['y'] - centers[from_area]['y'])
            distance = dx + dy
            
            total_distance += distance
            trip_count += 1
    
    avg_distance = total_distance / trip_count if trip_count > 0 else 0
    
    return avg_distance, total_distance, trip_count

def calculate_utilization():
    """Calculate net utilization (weighted average across all processes)"""
    total_time_needed = 0
    total_time_available = 0
    
    utilizations = {}
    
    for process, weekly_minutes in PROCESS_WORKLOAD.items():
        machines = AREAS[process]["count"]
        available_minutes = machines * MINUTES_PER_WEEK
        
        utilization = (weekly_minutes / available_minutes) * 100 if available_minutes > 0 else 0
        utilizations[process] = utilization
        
        total_time_needed += weekly_minutes
        total_time_available += available_minutes
    
    # Weighted average utilization
    net_utilization = (total_time_needed / total_time_available) * 100
    
    return net_utilization, utilizations

def calculate_cost():
    """Calculate total cost of equipment"""
    total_cost = 0
    cost_breakdown = {}
    
    for process in AREAS.keys():
        count = AREAS[process]["count"]
        unit_cost = EQUIPMENT_COSTS[process]
        process_cost = count * unit_cost
        
        cost_breakdown[process] = process_cost
        total_cost += process_cost
    
    return total_cost, cost_breakdown

def calculate_area():
    """Calculate total facility area from layout summary"""
    layout_file = Path(__file__).parent / "Optimized_Layout_Summary.csv"
    
    with open(layout_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'Total Area' in line:
                # Extract area value - handle quoted numbers with commas
                parts = line.strip().split(',', 1)  # Split only on first comma
                if len(parts) > 1:
                    area_str = parts[1].replace(',', '').replace('"', '').strip()
                    return float(area_str)
    
    return 0

def main():
    """Main execution"""
    print("=" * 80)
    print("TASK 3 - PARTS-BASED DESIGN: METRICS CALCULATOR")
    print("=" * 80)
    
    # Load layout centers
    centers = load_layout_centers()
    print(f"\nLoaded {len(centers)} area centers from layout")
    
    # 1. Calculate distance per trip
    print("\n" + "=" * 80)
    print("METRIC 1: DISTANCE PER TRIP")
    print("=" * 80)
    avg_distance, total_distance, trip_count = calculate_distance_per_trip(centers)
    print(f"Calculation method: Rectilinear (Manhattan) distance")
    print(f"Total transitions: {trip_count}")
    print(f"Total distance: {total_distance:,.2f} ft")
    print(f"Average distance per trip: {avg_distance:.2f} ft")
    
    # 2. Calculate net utilization
    print("\n" + "=" * 80)
    print("METRIC 2: NET UTILIZATION")
    print("=" * 80)
    net_utilization, utilizations = calculate_utilization()
    print(f"Weighted average utilization: {net_utilization:.1f}%")
    print("\nUtilization by process:")
    for process in sorted(utilizations.keys()):
        print(f"  {process}: {utilizations[process]:.1f}%")
    
    # 3. Calculate cost
    print("\n" + "=" * 80)
    print("METRIC 3: COST OF EQUIPMENT")
    print("=" * 80)
    total_cost, cost_breakdown = calculate_cost()
    print(f"Total equipment cost: ${total_cost:,.2f}")
    print("\nCost breakdown by process:")
    for process in sorted(cost_breakdown.keys()):
        print(f"  {process}: ${cost_breakdown[process]:,.2f} "
              f"({AREAS[process]['count']} machines × ${EQUIPMENT_COSTS[process]:,})")
    
    # 4. Calculate area
    print("\n" + "=" * 80)
    print("METRIC 4: TOTAL AREA")
    print("=" * 80)
    total_area = calculate_area()
    print(f"Total facility area: {total_area:,.2f} sq ft")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY - ALL 4 KEY METRICS")
    print("=" * 80)
    print(f"1. Distance per trip:     {avg_distance:.2f} ft")
    print(f"2. Net utilization:       {net_utilization:.1f}%")
    print(f"3. Cost of equipment:     ${total_cost:,.2f}")
    print(f"4. Total area:            {total_area:,.2f} sq ft")
    print("=" * 80)
    
    # Save summary to file
    output_file = Path(__file__).parent / "Metrics_Summary.txt"
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("TASK 3 - PARTS-BASED DESIGN: METRICS SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"1. Distance per trip:     {avg_distance:.2f} ft\n")
        f.write(f"2. Net utilization:       {net_utilization:.1f}%\n")
        f.write(f"3. Cost of equipment:     ${total_cost:,.2f}\n")
        f.write(f"4. Total area:            {total_area:,.2f} sq ft\n")
        f.write("\n" + "=" * 80 + "\n")
        f.write("DETAILED BREAKDOWN\n")
        f.write("=" * 80 + "\n\n")
        f.write("Total Machines: 344\n")
        f.write("Machine Distribution:\n")
        for process in sorted(AREAS.keys()):
            f.write(f"  {process}: {AREAS[process]['count']:3d} machines\n")
    
    print(f"\nMetrics summary saved to: {output_file}")

if __name__ == "__main__":
    main()
