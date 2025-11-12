"""
Calculate key metrics for Year 2 Part 1 Layout:
- Distance per trip
- Net utilization
- Cost of equipment
- Total Area
"""

import csv
from pathlib import Path
import math

# Machine data for Year 2 Part 1
AREAS = {
    "B1": {"count": 14, "rows": 5, "cols": 3, "group": "ABCD"},
    "A":  {"count": 6,  "rows": 6, "cols": 1, "group": "ABCD"},
    "B2": {"count": 14, "rows": 5, "cols": 3, "group": "ABCD"},
    "C":  {"count": 3,  "rows": 3, "cols": 1, "group": "ABCD"},
    "D":  {"count": 14, "rows": 5, "cols": 3, "group": "ABCD"},
    "I":  {"count": 7,  "rows": 2, "cols": 4, "group": "HIJ"},
    "J":  {"count": 14, "rows": 3, "cols": 5, "group": "HIJ"},
}

PROCESS_ORDER = ["B1", "A", "B2", "C", "D", "I", "J"]

# Layout dimensions
LAYOUT_WIDTH = 298.0  # ft
LAYOUT_HEIGHT = 108.0  # ft

# Equipment costs (per machine)
EQUIPMENT_COSTS = {
    "B1": 150000,
    "A":  200000,
    "B2": 150000,
    "C":  180000,
    "D":  175000,
    "I":  220000,
    "J":  195000,
}

# Part 1 process times (minutes per unit)
P1_PROCESS_TIMES = {
    'B1': 2.5,
    'A':  1.0,
    'B2': 2.5,
    'C':  0.5,
    'D':  2.5,
    'I':  1.25,
    'J':  2.5,
}

# Year 2 demand: 26,100 units/week for Part 1
DEMAND_YEAR2 = 26100
AVAILABLE_TIME_PER_MACHINE = 4800  # minutes per week (2-shift operation)

print("="*70)
print("YEAR 2 PART 1 - KEY METRICS CALCULATION")
print("="*70)

# ============================================================================
# 1. TOTAL AREA
# ============================================================================
print("\n1. TOTAL AREA:")
print("-" * 70)

area_per_abcd = 14 * 14  # 196 sq ft
area_per_hij = 14 * 36   # 504 sq ft

total_machine_area = 0
for area_name, data in AREAS.items():
    if data["group"] == "ABCD":
        area = data["count"] * area_per_abcd
    else:
        area = data["count"] * area_per_hij
    total_machine_area += area
    print(f"  {area_name}: {data['count']} machines × {area_per_abcd if data['group']=='ABCD' else area_per_hij} ft² = {area:,} ft²")

total_footprint = LAYOUT_WIDTH * LAYOUT_HEIGHT

print(f"\n  Total machine area: {total_machine_area:,} ft²")
print(f"  Total facility footprint: {total_footprint:,.0f} ft²")
print(f"  Utilization of footprint: {total_machine_area/total_footprint*100:.1f}%")

# ============================================================================
# 2. NET UTILIZATION (Machine Utilization)
# ============================================================================
print("\n2. NET UTILIZATION (Machine Utilization):")
print("-" * 70)

print(f"\n  Demand: {DEMAND_YEAR2:,} units/week")
print(f"  Available time per machine: {AVAILABLE_TIME_PER_MACHINE:,} min/week (2-shift)\n")

total_utilization = 0
count = 0
for step, time_per_unit in P1_PROCESS_TIMES.items():
    if step in AREAS:
        area_name = step
        num_machines = AREAS[area_name]["count"]
        
        # Total time needed per week
        total_time_needed = DEMAND_YEAR2 * time_per_unit
        
        # Total time available
        total_time_available = num_machines * AVAILABLE_TIME_PER_MACHINE
        
        # Utilization
        utilization = (total_time_needed / total_time_available) * 100
        total_utilization += utilization
        count += 1
        
        print(f"  {area_name}: {num_machines} machines")
        print(f"    - Time per unit: {time_per_unit:.2f} min")
        print(f"    - Total time needed: {total_time_needed:,.0f} min/week")
        print(f"    - Total time available: {total_time_available:,.0f} min/week")
        print(f"    - Utilization: {utilization:.1f}%\n")

avg_utilization = total_utilization / count if count > 0 else 0
print(f"  Average machine utilization across all areas: {avg_utilization:.1f}%")

# ============================================================================
# 3. COST OF EQUIPMENT
# ============================================================================
print("\n3. COST OF EQUIPMENT:")
print("-" * 70)

total_equipment_cost = 0
for area_name, data in AREAS.items():
    cost_per_machine = EQUIPMENT_COSTS[area_name]
    total_cost = data["count"] * cost_per_machine
    total_equipment_cost += total_cost
    print(f"  {area_name}: {data['count']} machines × ${cost_per_machine:,} = ${total_cost:,}")

print(f"\n  Total equipment cost: ${total_equipment_cost:,}")

# ============================================================================
# 4. DISTANCE PER TRIP
# ============================================================================
print("\n4. DISTANCE PER TRIP:")
print("-" * 70)

summary_path = Path(r"c:\Users\jatin\OneDrive\Desktop\Georgia Tech\Coursework\6202 Benoit\Case Work\Case Study 3\ISYE6202_CW3\results\task4\part\Jatin\Year2\Optimized_Layout_Summary.csv")

if summary_path.exists():
    centers = {}
    with open(summary_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            area_name = row['Area']
            center_x = float(row['X_ft']) + float(row['Width_ft']) / 2
            center_y = float(row['Y_ft']) + float(row['Height_ft']) / 2
            centers[area_name] = (center_x, center_y)
    
    distances = []
    print(f"\n  Process flow: {' → '.join(PROCESS_ORDER)}\n")
    
    total_distance = 0
    for i in range(len(PROCESS_ORDER) - 1):
        from_area = PROCESS_ORDER[i]
        to_area = PROCESS_ORDER[i + 1]
        
        x1, y1 = centers[from_area]
        x2, y2 = centers[to_area]
        
        # Rectilinear distance (Manhattan distance)
        distance = abs(x2 - x1) + abs(y2 - y1)
        distances.append(distance)
        total_distance += distance
        
        print(f"  {from_area} → {to_area}: {distance:.1f} ft")
    
    print(f"\n  Total distance per trip: {total_distance:.1f} ft")
    print(f"  Average distance per transfer: {total_distance/len(distances):.1f} ft")
    
    trips_per_week = DEMAND_YEAR2
    total_distance_per_week = total_distance * trips_per_week
    print(f"\n  Weekly material movement: {total_distance_per_week:,.0f} ft")
    print(f"  Weekly material movement: {total_distance_per_week/5280:,.1f} miles")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("SUMMARY - YEAR 2 PART 1 METRICS")
print("="*70)
print(f"  Total Area (Footprint): {total_footprint:,.0f} ft²")
print(f"  Machine Area Used: {total_machine_area:,} ft² ({total_machine_area/total_footprint*100:.1f}%)")
print(f"  Average Net Utilization: {avg_utilization:.1f}%")
print(f"  Total Equipment Cost: ${total_equipment_cost:,}")
if summary_path.exists():
    print(f"  Distance per Trip: {total_distance:.1f} ft")
print("="*70)
