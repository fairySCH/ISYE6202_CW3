"""
Task 3 - Parts-Based Design: Optimized Layout Generator
Generates facility layout for all 13 processes (A-M) with overlap visualization

Machine counts for Task 3 Parts-Based Design:
- A: 10, B: 32, C: 9, D: 45, E: 20, F: 24, G: 9, H: 31, I: 28, J: 49, K: 7, L: 31, M: 49
- Total: 344 machines

Block specifications:
- ABCD blocks: 14×14 ft with 2 ft overlap (12 ft effective spacing)
- EFGH blocks: 14×36 ft with no overlap (full 36 ft spacing)
- IJKLM blocks: 14×36 ft with no overlap (full 36 ft spacing)
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

# Area data - Task 3 actual machine counts and grid configurations
AREAS = {
    # ABCD group - 14×14 ft blocks with 2 ft overlap
    "A":  {"group": "ABCD", "count": 10, "rows": 5, "cols": 2, "eff_w": 26, "eff_h": 62},
    "B":  {"group": "ABCD", "count": 32, "rows": 8, "cols": 4, "eff_w": 50, "eff_h": 98},
    "C":  {"group": "ABCD", "count": 9,  "rows": 3, "cols": 3, "eff_w": 38, "eff_h": 38},
    "D":  {"group": "ABCD", "count": 45, "rows": 9, "cols": 5, "eff_w": 62, "eff_h": 110},
    
    # EFGH group - 14×36 ft blocks, no overlap
    "E":  {"group": "EFGH", "count": 20, "rows": 4, "cols": 5, "eff_w": 70, "eff_h": 144},
    "F":  {"group": "EFGH", "count": 24, "rows": 4, "cols": 6, "eff_w": 84, "eff_h": 144},
    "G":  {"group": "EFGH", "count": 9,  "rows": 3, "cols": 3, "eff_w": 42, "eff_h": 108},
    "H":  {"group": "EFGH", "count": 31, "rows": 4, "cols": 8, "eff_w": 112, "eff_h": 144},
    
    # IJKLM group - 14×36 ft blocks, no overlap
    "I":  {"group": "IJKLM", "count": 28, "rows": 4, "cols": 7, "eff_w": 98, "eff_h": 144},
    "J":  {"group": "IJKLM", "count": 49, "rows": 7, "cols": 7, "eff_w": 98, "eff_h": 252},
    "K":  {"group": "IJKLM", "count": 7,  "rows": 2, "cols": 4, "eff_w": 56, "eff_h": 72},
    "L":  {"group": "IJKLM", "count": 31, "rows": 4, "cols": 8, "eff_w": 112, "eff_h": 144},
    "M":  {"group": "IJKLM", "count": 49, "rows": 7, "cols": 7, "eff_w": 98, "eff_h": 252},
}

PROCESS_ORDER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
GAP = 5  # ft between areas

# Color scheme for each area
AREA_COLORS = {
    "A": '#4c9aff',  # Blue
    "B": '#ffa726',  # Orange
    "C": '#ab47bc',  # Purple
    "D": '#26c6da',  # Cyan
    "E": '#66bb6a',  # Green
    "F": '#f06292',  # Pink
    "G": '#ffeb3b',  # Yellow
    "H": '#8d6e63',  # Brown
    "I": '#78909c',  # Blue Grey
    "J": '#9c27b0',  # Deep Purple
    "K": '#ff5722',  # Deep Orange
    "L": '#00bcd4',  # Light Blue
    "M": '#4caf50',  # Light Green
}

def try_left_to_right_packing(areas_order):
    """Arrange areas left-to-right with center alignment"""
    positions = {}
    x_offset = 0
    max_height = 0
    
    # First pass: calculate max height
    for name in areas_order:
        area = AREAS[name]
        h = area["eff_h"]
        max_height = max(max_height, h)
    
    # Second pass: position each area
    for name in areas_order:
        area = AREAS[name]
        w = area["eff_w"]
        h = area["eff_h"]
        
        # Center vertically
        y_pos = (max_height - h) / 2
        
        positions[name] = {
            "x": x_offset,
            "y": y_pos,
            "w": w,
            "h": h
        }
        
        x_offset += w + GAP
    
    # Remove trailing gap
    total_width = x_offset - GAP
    total_height = max_height
    
    return positions, total_width, total_height

def visualize_layout(positions, total_width, total_height):
    """Generate layout visualization with machine counts"""
    fig, ax = plt.subplots(figsize=(24, 10))
    
    # Draw each area
    for name in PROCESS_ORDER:
        pos = positions[name]
        area = AREAS[name]
        
        # Draw rectangle
        rect = Rectangle(
            (pos["x"], pos["y"]),
            pos["w"],
            pos["h"],
            linewidth=2,
            edgecolor='black',
            facecolor=AREA_COLORS[name],
            alpha=0.6
        )
        ax.add_patch(rect)
        
        # Add label with machine count
        center_x = pos["x"] + pos["w"] / 2
        center_y = pos["y"] + pos["h"] / 2
        
        label = f"{name}\n{area['count']} machines"
        ax.text(center_x, center_y, label,
                ha='center', va='center',
                fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
    
    # Set limits and labels
    ax.set_xlim(-10, total_width + 10)
    ax.set_ylim(-10, total_height + 10)
    ax.set_aspect('equal')
    ax.set_xlabel('Width (feet)', fontsize=12)
    ax.set_ylabel('Height (feet)', fontsize=12)
    ax.set_title(f'Task 3 Parts-Based Layout - All 13 Processes (344 machines)\n'
                 f'Layout: {total_width:.0f} ft × {total_height:.0f} ft = {total_width * total_height:,.0f} sq ft',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add legend
    legend_elements = []
    for name in PROCESS_ORDER:
        area = AREAS[name]
        legend_elements.append(
            plt.Rectangle((0, 0), 1, 1, fc=AREA_COLORS[name], alpha=0.6, 
                         label=f'{name}: {area["count"]} machines ({area["group"]})')
        )
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    
    plt.tight_layout()
    
    return fig

def save_layout_summary(positions, total_width, total_height, output_dir):
    """Save layout summary to CSV"""
    output_file = output_dir / "Optimized_Layout_Summary.csv"
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Area', 'Machines', 'Grid_Rows', 'Grid_Cols', 'X', 'Y', 
                        'Width', 'Height', 'Center_X', 'Center_Y', 'Group'])
        
        for name in PROCESS_ORDER:
            pos = positions[name]
            area = AREAS[name]
            center_x = pos["x"] + pos["w"] / 2
            center_y = pos["y"] + pos["h"] / 2
            
            writer.writerow([
                name,
                area["count"],
                area["rows"],
                area["cols"],
                f"{pos['x']:.2f}",
                f"{pos['y']:.2f}",
                f"{pos['w']:.2f}",
                f"{pos['h']:.2f}",
                f"{center_x:.2f}",
                f"{center_y:.2f}",
                area["group"]
            ])
        
        # Add summary
        writer.writerow([])
        writer.writerow(['LAYOUT SUMMARY'])
        writer.writerow(['Total Width (ft)', f"{total_width:.2f}"])
        writer.writerow(['Total Height (ft)', f"{total_height:.2f}"])
        writer.writerow(['Total Area (sq ft)', f"{total_width * total_height:,.2f}"])
        writer.writerow(['Total Machines', sum(AREAS[name]["count"] for name in PROCESS_ORDER)])
    
    print(f"Layout summary saved to: {output_file}")

def main():
    """Main execution"""
    output_dir = Path(__file__).parent
    
    print("=" * 80)
    print("TASK 3 - PARTS-BASED DESIGN: LAYOUT GENERATOR")
    print("=" * 80)
    
    # Verify grid capacities
    print("\nGrid Capacity Verification:")
    print("-" * 80)
    for name in PROCESS_ORDER:
        area = AREAS[name]
        grid_capacity = area["rows"] * area["cols"]
        status = "OK" if area["count"] <= grid_capacity else "OVERFLOW"
        print(f"  {name}: {area['count']:2d} machines in {area['rows']}×{area['cols']} grid "
              f"(capacity={grid_capacity:2d}) [{status}]")
    
    # Generate layout
    print("\n" + "=" * 80)
    print("Generating optimized layout...")
    positions, total_width, total_height = try_left_to_right_packing(PROCESS_ORDER)
    
    print(f"Layout dimensions: {total_width:.0f} ft × {total_height:.0f} ft")
    print(f"Total area: {total_width * total_height:,.0f} sq ft")
    
    # Save layout summary
    save_layout_summary(positions, total_width, total_height, output_dir)
    
    # Generate visualization
    print("\nGenerating layout visualization...")
    fig = visualize_layout(positions, total_width, total_height)
    
    output_png = output_dir / "Task3_Parts_Based_Layout.png"
    fig.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"Layout visualization saved to: {output_png}")
    
    plt.close()
    
    print("\n" + "=" * 80)
    print("Layout generation complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
