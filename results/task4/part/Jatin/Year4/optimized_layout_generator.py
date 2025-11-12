"""
Year 4 Part 1 - Optimized Layout Generator with Overlap Visualization
IMPORTANT: Uses SAME layout size as Year 5 (310 ft × 110 ft) since we're forecasting
Year 5 in advance. Year 4 has fewer machines (77 vs 129) so areas are less utilized.

Machine counts for Year 4 Part 1:
- B1: 15, A: 6, B2: 15, C: 3, D: 15, I: 8, J: 15
- Total: 77 machines (fit into Year 5's 129-machine capacity)
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

# Area data - Year 4 actual machine counts and grid configurations
# Year 4 actual:   B1=15, A=6, B2=15, C=3, D=15, I=8, J=15 (77 total)
AREAS = {
    "B1": {"group": "ABCD", "count": 15, "rows": 5, "cols": 3, "eff_w": 38, "eff_h": 62},
    "A":  {"group": "ABCD", "count": 6,  "rows": 6, "cols": 1, "eff_w": 14, "eff_h": 74},
    "B2": {"group": "ABCD", "count": 15, "rows": 5, "cols": 3, "eff_w": 38, "eff_h": 62},
    "C":  {"group": "ABCD", "count": 3,  "rows": 3, "cols": 1, "eff_w": 14, "eff_h": 38},
    "D":  {"group": "ABCD", "count": 15, "rows": 5, "cols": 3, "eff_w": 38, "eff_h": 62},
    "I":  {"group": "HIJ",  "count": 8,  "rows": 2, "cols": 4, "eff_w": 56, "eff_h": 72},
    "J":  {"group": "HIJ",  "count": 15, "rows": 3, "cols": 5, "eff_w": 70, "eff_h": 108},
}

PROCESS_ORDER = ["B1", "A", "B2", "C", "D", "I", "J"]
GAP = 5  # ft between areas

# Color scheme for each area
AREA_COLORS = {
    "B1": '#4c9aff',  # Blue
    "A":  '#ffa726',  # Orange
    "B2": '#4c9aff',  # Blue (same as B1)
    "C":  '#ab47bc',  # Purple
    "D":  '#26c6da',  # Cyan
    "I":  '#66bb6a',  # Green
    "J":  '#f06292',  # Pink
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
    
    # Second pass: position areas with center alignment
    for name in areas_order:
        area = AREAS[name]
        w = area["eff_w"]
        h = area["eff_h"]
        
        # Center-align vertically
        y_offset = (max_height - h) / 2
        
        positions[name] = {"x": x_offset, "y": y_offset}
        x_offset += w + GAP
    
    total_w = x_offset - GAP
    total_h = max_height
    aspect = max(total_w, total_h) / min(total_w, total_h) if min(total_w, total_h) > 0 else 999
    
    return total_w, total_h, positions, aspect

def find_best_layout():
    """Create left-to-right layout in process order"""
    w, h, pos, aspect = try_left_to_right_packing(PROCESS_ORDER)
    
    best_layout = {
        "width": w,
        "height": h,
        "positions": pos,
        "num_cols": len(PROCESS_ORDER),
        "aspect": aspect
    }
    
    return best_layout

def draw_block_with_overlaps(ax, x0, y0, rows, cols, group, area_name, actual_count):
    """Draw individual unit blocks with overlap zones"""
    if group == "ABCD":
        unit_w, unit_h, share = 14, 14, 2
    else:  # HIJ
        unit_w, unit_h, share = 14, 36, 0
    
    block_color = AREA_COLORS[area_name]
    overlap_color = '#ff6b6b'
    edge_color = '#333333'
    
    # Draw area boundary box
    area_w = cols * unit_w - (cols - 1) * share if share > 0 else cols * unit_w
    area_h = rows * unit_h - (rows - 1) * share if share > 0 else rows * unit_h
    
    boundary = Rectangle((x0, y0), area_w, area_h,
                         facecolor='none',
                         edgecolor='black',
                         linewidth=2,
                         linestyle='--',
                         alpha=0.5)
    ax.add_patch(boundary)
    
    for r in range(rows):
        for c in range(cols):
            # Block position with sharing applied
            if share > 0:
                bx = x0 + c * (unit_w - share)
                by = y0 + r * (unit_h - share)
            else:
                bx = x0 + c * unit_w
                by = y0 + r * unit_h
            
            # Draw main block
            block = Rectangle((bx, by), unit_w, unit_h, 
                            facecolor=block_color, 
                            edgecolor=edge_color, 
                            linewidth=0.5, 
                            alpha=0.7)
            ax.add_patch(block)
            
            # Draw overlap zones (only for ABCD)
            if share > 0:
                if c < cols - 1:
                    overlap = Rectangle((bx + unit_w - share, by), share, unit_h,
                                      facecolor=overlap_color, alpha=0.5, 
                                      edgecolor='none')
                    ax.add_patch(overlap)
                
                if r < rows - 1:
                    overlap = Rectangle((bx, by + unit_h - share), unit_w, share,
                                      facecolor=overlap_color, alpha=0.5,
                                      edgecolor='none')
                    ax.add_patch(overlap)
                
                if r < rows - 1 and c < cols - 1:
                    overlap = Rectangle((bx + unit_w - share, by + unit_h - share), 
                                      share, share,
                                      facecolor=overlap_color, alpha=0.7,
                                      edgecolor='none')
                    ax.add_patch(overlap)
    
    # Area label
    cx = x0 + area_w / 2
    cy = y0 + area_h / 2
    ax.text(cx, cy, f"{area_name}\n{rows}×{cols}\n{actual_count} machines", 
           ha='center', va='center', fontsize=9, 
           fontweight='bold', color='white',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='black', alpha=0.7))

def draw_flow_arrows(ax, layout):
    """Draw arrows showing process flow"""
    positions = layout["positions"]
    arrow_color = '#d63031'
    
    for i in range(len(PROCESS_ORDER) - 1):
        from_area = PROCESS_ORDER[i]
        to_area = PROCESS_ORDER[i + 1]
        
        from_data = AREAS[from_area]
        to_data = AREAS[to_area]
        
        from_pos = positions[from_area]
        to_pos = positions[to_area]
        
        from_x = from_pos["x"] + from_data["eff_w"] / 2
        from_y = from_pos["y"] + from_data["eff_h"] / 2
        to_x = to_pos["x"] + to_data["eff_w"] / 2
        to_y = to_pos["y"] + to_data["eff_h"] / 2
        
        ax.annotate('', xy=(to_x, to_y), xytext=(from_x, from_y),
                   arrowprops=dict(arrowstyle='->', lw=2, color=arrow_color))

def create_layout_diagram():
    """Main function to create the optimized layout diagram"""
    
    print("Creating Year 4 Part 1 layout...")
    print("  Year 4 actual: 77 machines")
    print("  - All areas center-aligned vertically for straight arrows")
    print("  - No overlap between different areas (GAP = 5 ft)")
    print("  - Overlap zones only within each area's internal blocks")
    
    layout = find_best_layout()
    
    print(f"\nLayout configuration:")
    print(f"  Arrangement: Left-to-right in process order")
    print(f"  Dimensions: {layout['width']:.1f} ft × {layout['height']:.1f} ft")
    print(f"  Total footprint: {layout['width'] * layout['height']:.0f} ft²")
    
    # Calculate actual area used
    actual_machines = sum(AREAS[a]["count"] for a in PROCESS_ORDER)
    total_area = sum(AREAS[a]["count"] * (196 if AREAS[a]["group"]=="ABCD" else 504) for a in PROCESS_ORDER)
    
    print(f"  Total machines: {actual_machines}")
    print(f"  Actual area used: {total_area:,} ft²")
    
    # Create figure
    fig_w = layout['width'] / 15
    fig_h = layout['height'] / 15
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    
    # Draw each area with blocks and overlaps
    for area_name in PROCESS_ORDER:
        area = AREAS[area_name]
        pos = layout["positions"][area_name]
        
        draw_block_with_overlaps(
            ax, pos["x"], pos["y"],
            area["rows"], area["cols"],
            area["group"], area_name,
            area["count"]
        )
    
    # Draw flow arrows
    draw_flow_arrows(ax, layout)
    
    # Add legend
    legend_elements = [
        plt.matplotlib.patches.Patch(facecolor=AREA_COLORS['B1'], alpha=0.7, label='B1 & B2 Areas'),
        plt.matplotlib.patches.Patch(facecolor=AREA_COLORS['A'], alpha=0.7, label='A Area'),
        plt.matplotlib.patches.Patch(facecolor=AREA_COLORS['C'], alpha=0.7, label='C Area'),
        plt.matplotlib.patches.Patch(facecolor=AREA_COLORS['D'], alpha=0.7, label='D Area'),
        plt.matplotlib.patches.Patch(facecolor=AREA_COLORS['I'], alpha=0.7, label='I Area'),
        plt.matplotlib.patches.Patch(facecolor=AREA_COLORS['J'], alpha=0.7, label='J Area'),
        plt.matplotlib.patches.Patch(facecolor='#ff6b6b', alpha=0.5, label='Overlap Zones (2 ft)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # Set axis properties
    ax.set_xlim(-10, layout['width'] + 10)
    ax.set_ylim(-10, layout['height'] + 10)
    ax.set_aspect('equal')
    ax.set_xlabel('Width (ft)', fontsize=10)
    ax.set_ylabel('Height (ft)', fontsize=10)
    ax.set_title(f'Year 4 Part 1 Layout: {layout["width"]:.0f} ft × {layout["height"]:.0f} ft\n77 machines total', 
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Save
    output_path = Path(__file__).parent / 'Optimized_Layout_with_Overlaps.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    # Save layout data
    csv_path = Path(__file__).parent / 'Optimized_Layout_Summary.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Area', 'X_ft', 'Y_ft', 'Width_ft', 'Height_ft', 'Rows', 'Cols', 'Blocks'])
        for area_name in PROCESS_ORDER:
            area = AREAS[area_name]
            pos = layout["positions"][area_name]
            writer.writerow([
                area_name,
                f"{pos['x']:.1f}",
                f"{pos['y']:.1f}",
                f"{area['eff_w']:.1f}",
                f"{area['eff_h']:.1f}",
                area['rows'],
                area['cols'],
                area['count']
            ])
    
    print(f"\nOutput saved to:")
    print(f"  {output_path}")
    print(f"  {csv_path}")
    
    return output_path, layout

if __name__ == '__main__':
    create_layout_diagram()
