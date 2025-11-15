"""
Optimize grid layouts to minimize wasted space
Find the most compact rectangular arrangement for each machine count
"""

import math

def find_optimal_grid(machine_count):
    """
    Find the most compact grid (rows × cols) for a given machine count.
    Prioritizes square-like arrangements (aspect ratio closest to 1).
    """
    if machine_count == 0:
        return 0, 0, 0
    
    best_config = None
    best_aspect = float('inf')
    
    # Try all possible rectangular arrangements
    for rows in range(1, machine_count + 1):
        cols = math.ceil(machine_count / rows)
        total_slots = rows * cols
        waste = total_slots - machine_count
        aspect_ratio = max(rows, cols) / min(rows, cols)
        
        # Prefer arrangements with minimal waste and aspect ratio close to 1
        if best_config is None or (waste <= best_config[2] and aspect_ratio < best_aspect):
            best_config = (rows, cols, waste)
            best_aspect = aspect_ratio
    
    return best_config

def calculate_area_dimensions(rows, cols, unit_w, unit_h, overlap=0):
    """Calculate effective width and height with overlap"""
    if overlap > 0:
        eff_w = cols * unit_w - (cols - 1) * overlap if cols > 0 else 0
        eff_h = rows * unit_h - (rows - 1) * overlap if rows > 0 else 0
    else:
        eff_w = cols * unit_w
        eff_h = rows * unit_h
    return eff_w, eff_h

# Machine counts for all years
YEARS = {
    "Year1": {"B1": 12, "A": 5, "B2": 12, "C": 3, "D": 12, "I": 6, "J": 12},
    "Year2": {"B1": 14, "A": 6, "B2": 14, "C": 3, "D": 14, "I": 7, "J": 14},
    "Year3": {"B1": 15, "A": 6, "B2": 15, "C": 3, "D": 15, "I": 8, "J": 15},
    "Year4": {"B1": 15, "A": 6, "B2": 15, "C": 3, "D": 15, "I": 8, "J": 15},
    "Year5": {"B1": 16, "A": 7, "B2": 16, "C": 4, "D": 16, "I": 8, "J": 16},
}

# Unit dimensions and overlap
ABCD_UNIT_W, ABCD_UNIT_H, ABCD_OVERLAP = 14, 14, 2
HIJ_UNIT_W, HIJ_UNIT_H, HIJ_OVERLAP = 36, 14, 0

print("OPTIMIZED GRID CONFIGURATIONS FOR MINIMAL AREA")
print("=" * 80)

for year, machines in YEARS.items():
    print(f"\n{year.upper()} - Total: {sum(machines.values())} machines")
    print("-" * 80)
    
    total_area_current = 0
    total_area_optimized = 0
    
    for process in ["B1", "A", "B2", "C", "D", "I", "J"]:
        count = machines[process]
        
        # Determine unit size and overlap based on group
        if process in ["B1", "A", "B2", "C", "D"]:
            unit_w, unit_h, overlap = ABCD_UNIT_W, ABCD_UNIT_H, ABCD_OVERLAP
            group = "ABCD"
        else:
            unit_w, unit_h, overlap = HIJ_UNIT_W, HIJ_UNIT_H, HIJ_OVERLAP
            group = "HIJ"
        
        # Find optimal grid
        rows, cols, waste = find_optimal_grid(count)
        
        # Calculate dimensions
        eff_w, eff_h = calculate_area_dimensions(rows, cols, unit_w, unit_h, overlap)
        area = eff_w * eff_h
        
        print(f"{process:3s}: {count:2d} machines → {rows}×{cols} grid ({rows*cols} slots, {waste} waste)")
        print(f"     Dimensions: {eff_w:.0f} ft × {eff_h:.0f} ft = {area:,.0f} sq ft")
        
        total_area_optimized += area
    
    print(f"\nTotal optimized area: {total_area_optimized:,.0f} sq ft")
    print(f"Estimated layout (with 5ft gaps): ~{total_area_optimized * 1.15:,.0f} sq ft")

print("\n" + "=" * 80)
print("\nCOMPARISON WITH CURRENT LAYOUTS:")
print("-" * 80)

current_layouts = {
    "Year2": "520 ft × 62 ft = 32,240 sq ft",
    "Year3": "520 ft × 62 ft = 32,240 sq ft", 
    "Year4": "520 ft × 62 ft = 32,240 sq ft",
    "Year5": "592 ft × 50 ft = 29,600 sq ft",
}

for year, layout_str in current_layouts.items():
    print(f"{year}: Current = {layout_str}")

print("\n" + "=" * 80)
print("RECOMMENDATIONS:")
print("=" * 80)
print("1. Use optimal grid configurations to minimize wasted machine slots")
print("2. Arrange processes in compact 2D layouts (not just left-to-right)")
print("3. Consider 2-row or 3-row arrangements of process areas")
print("4. Target aspect ratios closer to 1.0 (square-like) for minimal perimeter")
print("5. Estimated space savings: 20-30% compared to current linear layouts")
