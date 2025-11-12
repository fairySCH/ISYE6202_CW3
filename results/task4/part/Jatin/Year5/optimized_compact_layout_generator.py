"""
Year5 Part 1 - OPTIMIZED Compact Layout Generator

Machine counts for Year5 Part 1:
- B1: 16, A: 7, B2: 16, C: 4, D: 16, I: 8, J: 16
- Total: 83 machines

OPTIMIZED: Zero waste grids + compact 2D arrangement
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

# Optimal grid configurations (COMPACT - taller, narrower)
AREAS = {
    "B1": {"group": "ABCD", "count": 16, "rows": 8, "cols": 2, "eff_w":  26, "eff_h": 98},
    "A": {"group": "ABCD", "count":  7, "rows": 7, "cols": 1, "eff_w":  14, "eff_h": 86},
    "B2": {"group": "ABCD", "count": 16, "rows": 8, "cols": 2, "eff_w":  26, "eff_h": 98},
    "C": {"group": "ABCD", "count":  4, "rows": 4, "cols": 1, "eff_w":  14, "eff_h": 50},
    "D": {"group": "ABCD", "count": 16, "rows": 8, "cols": 2, "eff_w":  26, "eff_h": 98},
    "I": {"group": "HIJ", "count":  8, "rows": 8, "cols": 1, "eff_w":  36, "eff_h": 112},
    "J": {"group": "HIJ", "count": 16, "rows": 8, "cols": 2, "eff_w":  72, "eff_h": 112},
}

PROCESS_ORDER = ["B1", "A", "B2", "C", "D", "I", "J"]
GAP = 5  # ft between areas

AREA_COLORS = {
    "B1": '#4c9aff',  # Blue
    "A":  '#ffa726',  # Orange
    "B2": '#4c9aff',  # Blue
    "C":  '#ab47bc',  # Purple
    "D":  '#26c6da',  # Cyan
    "I":  '#66bb6a',  # Green
    "J":  '#f06292',  # Pink
}

def pack_areas_left_to_right():
    """Pack all areas left to right in process order"""
    positions = {}
    x_offset = 0
    max_height = max([AREAS[p]["eff_h"] for p in PROCESS_ORDER])
    
    for process in PROCESS_ORDER:
        area = AREAS[process]
        # Center align vertically
        y_offset = (max_height - area["eff_h"]) / 2
        positions[process] = {"x": x_offset, "y": y_offset}
        x_offset += area["eff_w"] + GAP
    
    total_width = x_offset - GAP
    total_height = max_height
    
    return total_width, total_height, positions

def draw_area(ax, x0, y0, area_data, process_name):
    """Draw area with blocks and overlaps"""
    rows = area_data["rows"]
    cols = area_data["cols"]
    count = area_data["count"]
    group = area_data["group"]
    
    if group == "ABCD":
        unit_w, unit_h, overlap = 14, 14, 2
    else:
        unit_w, unit_h, overlap = 36, 14, 0
    
    # Draw boundary
    boundary = Rectangle((x0, y0), area_data["eff_w"], area_data["eff_h"],
                         facecolor='none', edgecolor='black', linewidth=2,
                         linestyle='--', alpha=0.5)
    ax.add_patch(boundary)
    
    # Draw blocks
    block_idx = 0
    for r in range(rows):
        for c in range(cols):
            if block_idx >= count:
                break
            
            if overlap > 0:
                bx = x0 + c * (unit_w - overlap)
                by = y0 + r * (unit_h - overlap)
            else:
                bx = x0 + c * unit_w
                by = y0 + r * unit_h
            
            block = Rectangle((bx, by), unit_w, unit_h,
                            facecolor=AREA_COLORS[process_name],
                            edgecolor='#333', linewidth=0.5, alpha=0.7)
            ax.add_patch(block)
            
            # Overlap zones
            if overlap > 0:
                if c < cols - 1:
                    ov = Rectangle((bx + unit_w - overlap, by), overlap, unit_h,
                                 facecolor='#ff6b6b', alpha=0.3)
                    ax.add_patch(ov)
                if r < rows - 1:
                    ov = Rectangle((bx, by + unit_h - overlap), unit_w, overlap,
                                 facecolor='#ff6b6b', alpha=0.3)
                    ax.add_patch(ov)
            
            block_idx += 1
    
    # Label - only process name
    ax.text(x0 + area_data["eff_w"]/2, y0 + area_data["eff_h"]/2,
           f"{process_name}",
           ha='center', va='center', fontsize=14, fontweight='bold',
           color='white', bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

def generate_layout():
    """Generate optimized layout"""
    total_w, total_h, positions = pack_areas_left_to_right()
    
    actual_area = sum(AREAS[p]["eff_w"] * AREAS[p]["eff_h"] for p in PROCESS_ORDER)
    total_area = total_w * total_h
    efficiency = (actual_area / total_area) * 100
    
    print("Creating left-to-right layout...")
    print(f"Layout: {total_w:.0f} ft × {total_h:.0f} ft = {total_area:,.0f} ft²")
    
    fig, ax = plt.subplots(figsize=(20, 6))
    
    for process in PROCESS_ORDER:
        area = AREAS[process]
        pos = positions[process]
        draw_area(ax, pos["x"], pos["y"], area, process)
    
    # Draw arrows
    for i in range(len(PROCESS_ORDER) - 1):
        p1, p2 = PROCESS_ORDER[i], PROCESS_ORDER[i + 1]
        x1 = positions[p1]["x"] + AREAS[p1]["eff_w"]
        y1 = positions[p1]["y"] + AREAS[p1]["eff_h"] / 2
        x2 = positions[p2]["x"]
        y2 = positions[p2]["y"] + AREAS[p2]["eff_h"] / 2
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='red', alpha=0.6))
    
    ax.set_xlim(-10, total_w + 10)
    ax.set_ylim(-10, total_h + 10)
    ax.set_aspect('equal')
    ax.set_title(f'Year5 Layout - {sum([AREAS[p]["count"] for p in PROCESS_ORDER])} Machines Total', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    output_dir = Path(__file__).parent
    png_file = output_dir / "Optimized_Compact_Layout.png"
    csv_file = output_dir / "Optimized_Compact_Layout_Summary.csv"
    
    plt.tight_layout()
    plt.savefig(png_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {png_file}")
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Area', 'X_ft', 'Y_ft', 'Width_ft', 'Height_ft', 'Rows', 'Cols', 'Machines'])
        for process in PROCESS_ORDER:
            area = AREAS[process]
            pos = positions[process]
            writer.writerow([process, f"{pos['x']:.1f}", f"{pos['y']:.1f}",
                           area["eff_w"], area["eff_h"], area["rows"], area["cols"], area["count"]])
    
    print(f"Saved: {csv_file}")
    plt.close()

if __name__ == "__main__":
    generate_layout()