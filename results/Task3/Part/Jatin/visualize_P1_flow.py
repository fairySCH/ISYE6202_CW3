"""
Task 3 Year +1 - Part 1 (P1) Flow Visualization
Shows the material flow for Part 1 through the facility layout

P1 Process Sequence: B → A → B → C → D → I → J
P1 Demand: 20,961.54 units/week
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import csv
from pathlib import Path

# P1 specific data
P1_DEMAND = 20961.54  # units/week
P1_SEQUENCE = ["B", "A", "B", "C", "D", "I", "J"]
P1_TOTAL_TIME = 12.75  # Total process time (2.5 + 1.0 + 2.5 + 0.5 + 2.5 + 1.25 + 2.5)

# Process times for P1 (minutes per unit)
P1_TIMES = {
    "B": 2.5,   # Step 1
    "A": 1.0,   # Step 2
    # B: 2.5,   # Step 3 (B appears twice)
    "C": 0.5,   # Step 4
    "D": 2.5,   # Step 5
    "I": 1.25,  # Step 6
    "J": 2.5,   # Step 7
}

# Color scheme matching the layout
AREA_COLORS = {
    "A": '#4c9aff',  # Blue
    "B": '#ffa726',  # Orange
    "C": '#ab47bc',  # Purple
    "D": '#26c6da',  # Cyan
    "I": '#78909c',  # Blue Grey
    "J": '#9c27b0',  # Deep Purple
}

def load_layout_data():
    """Load machine counts from the Jatin folder"""
    layout_file = Path(__file__).parent / "Optimized_Layout_Summary.csv"
    
    areas = {}
    with open(layout_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Area'] in AREA_COLORS:
                areas[row['Area']] = {
                    'machines': int(row['Machines'])
                }
    
    return areas

def calculate_compact_positions():
    """Calculate compact left-to-right positions for P1 processes only"""
    # Grid configurations for P1 processes
    grid_configs = {
        "B": (8, 4),   # 8 rows × 4 cols
        "A": (5, 2),   # 5 rows × 2 cols
        "C": (3, 3),   # 3 rows × 3 cols
        "D": (9, 5),   # 9 rows × 5 cols
        "I": (4, 7),   # 4 rows × 7 cols
        "J": (7, 7),   # 7 rows × 7 cols
    }
    
    # Block specifications by group
    # ABCD: 14×14 ft, share 2 ft on front/left/right (NOT back - worker side)
    # HIJ: 14×36 ft, NO sharing
    block_specs = {
        "A": {"unit_w": 14, "unit_h": 14, "share": 2, "group": "ABCD"},
        "B": {"unit_w": 14, "unit_h": 14, "share": 2, "group": "ABCD"},
        "C": {"unit_w": 14, "unit_h": 14, "share": 2, "group": "ABCD"},
        "D": {"unit_w": 14, "unit_h": 14, "share": 2, "group": "ABCD"},
        "I": {"unit_w": 14, "unit_h": 36, "share": 0, "group": "HIJ"},
        "J": {"unit_w": 14, "unit_h": 36, "share": 0, "group": "HIJ"},
    }
    
    gap = 5  # Gap between process areas
    
    positions = {}
    x_offset = 0
    max_height = 0
    
    # First pass: calculate max height
    for name in P1_SEQUENCE:
        if name not in grid_configs or name not in block_specs:
            continue
        rows, cols = grid_configs[name]
        spec = block_specs[name]
        
        # Calculate height with proper overlap
        h = rows * spec["unit_h"] - (rows - 1) * spec["share"]
        max_height = max(max_height, h)
    
    # Second pass: position areas left-to-right with center alignment
    for name in P1_SEQUENCE:
        if name not in grid_configs or name not in block_specs:
            continue
        rows, cols = grid_configs[name]
        spec = block_specs[name]
        
        # Calculate effective dimensions with overlap
        w = cols * spec["unit_w"] - (cols - 1) * spec["share"]
        h = rows * spec["unit_h"] - (rows - 1) * spec["share"]
        
        # Center-align vertically
        y_offset = (max_height - h) / 2
        
        positions[name] = {
            'x': x_offset,
            'y': y_offset,
            'width': w,
            'height': h,
            'center_x': x_offset + w / 2,
            'center_y': y_offset + h / 2,
            'rows': rows,
            'cols': cols,
            'unit_w': spec["unit_w"],
            'unit_h': spec["unit_h"],
            'share': spec["share"],
            'group': spec["group"]
        }
        
        x_offset += w + gap
    
    return positions

def create_flow_visualization():
    """Create flow diagram for P1"""
    machine_counts = load_layout_data()
    p1_positions = calculate_compact_positions()
    
    fig, ax = plt.subplots(figsize=(20, 10))
    
    # Draw only P1 process areas with individual machine blocks
    for name in P1_SEQUENCE:
        if name not in p1_positions:
            continue
            
        data = p1_positions[name]
        x, y, w, h = data['x'], data['y'], data['width'], data['height']
        rows, cols = data['rows'], data['cols']
        unit_w, unit_h, share = data['unit_w'], data['unit_h'], data['share']
        machines = machine_counts[name]['machines']
        
        # Draw dashed boundary box
        boundary = plt.Rectangle(
            (x, y), w, h,
            facecolor='none',
            edgecolor='black',
            linewidth=2,
            linestyle='--',
            alpha=0.5
        )
        ax.add_patch(boundary)
        
        # Draw individual machine blocks with overlaps
        machine_count = 0
        overlap_color = '#ff6b6b'  # Red for overlap zones
        
        for row in range(rows):
            for col in range(cols):
                if machine_count >= machines:
                    break
                
                # Block position with sharing applied (only if share > 0)
                if share > 0:
                    block_x = x + col * (unit_w - share)
                    block_y = y + row * (unit_h - share)
                else:
                    block_x = x + col * unit_w
                    block_y = y + row * unit_h
                
                # Draw main machine block
                machine_rect = plt.Rectangle(
                    (block_x, block_y),
                    unit_w,
                    unit_h,
                    linewidth=0.5,
                    edgecolor='#333333',
                    facecolor=AREA_COLORS[name],
                    alpha=0.7
                )
                ax.add_patch(machine_rect)
                
                # Draw overlap zones in red (only for ABCD blocks with share > 0)
                if share > 0:
                    # Right overlap
                    if col < cols - 1:
                        overlap = plt.Rectangle(
                            (block_x + unit_w - share, block_y),
                            share,
                            unit_h,
                            facecolor=overlap_color,
                            alpha=0.5,
                            edgecolor='none'
                        )
                        ax.add_patch(overlap)
                    
                    # Bottom overlap
                    if row < rows - 1:
                        overlap = plt.Rectangle(
                            (block_x, block_y + unit_h - share),
                            unit_w,
                            share,
                            facecolor=overlap_color,
                            alpha=0.5,
                            edgecolor='none'
                        )
                        ax.add_patch(overlap)
                    
                    # Corner overlap (where both right and bottom meet)
                    if row < rows - 1 and col < cols - 1:
                        overlap = plt.Rectangle(
                            (block_x + unit_w - share, block_y + unit_h - share),
                            share,
                            share,
                            facecolor=overlap_color,
                            alpha=0.7,
                            edgecolor='none'
                        )
                        ax.add_patch(overlap)
                
                machine_count += 1
        
        # Add process label
        label = f"Process {name}\n{rows}×{cols}\n{machines} machines"
        ax.text(data['center_x'], data['center_y'], label,
                ha='center', va='center',
                fontsize=9, fontweight='bold',
                color='white',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='black', alpha=0.7))
    
    # Draw flow arrows for P1 sequence
    # P1: B → A → B → C → D → I → J
    flow_pairs = [
        ("B", "A"),
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "I"),
        ("I", "J")
    ]
    
    for i, (from_area, to_area) in enumerate(flow_pairs):
        from_data = p1_positions[from_area]
        to_data = p1_positions[to_area]
        
        # Calculate arrow start and end points (slightly offset from center)
        start_x = from_data['center_x']
        start_y = from_data['center_y']
        end_x = to_data['center_x']
        end_y = to_data['center_y']
        
        # Draw curved arrow
        arrow = FancyArrowPatch(
            (start_x, start_y),
            (end_x, end_y),
            arrowstyle='->,head_width=1.2,head_length=1.5',
            color='red',
            linewidth=4,
            alpha=0.7,
            connectionstyle="arc3,rad=0.1"
        )
        ax.add_patch(arrow)
        
        # Add flow quantity label
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2 + 15
        
        # Calculate distance
        distance = abs(end_x - start_x) + abs(end_y - start_y)
        
        label = f"Step {i+1}\n{P1_DEMAND:,.0f} units/week\n{distance:.0f} ft"
        ax.text(mid_x, mid_y, label,
                ha='center', va='center',
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))
    
    # Calculate plot limits based on P1 positions only
    all_x = [data['x'] for data in p1_positions.values()] + [data['x'] + data['width'] for data in p1_positions.values()]
    all_y = [data['y'] for data in p1_positions.values()] + [data['y'] + data['height'] for data in p1_positions.values()]
    
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    # Add padding
    padding = 30
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)
    ax.set_aspect('equal')
    ax.set_xlabel('Width (feet)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Depth (feet)', fontsize=12, fontweight='bold')
    
    # Title with P1 information
    title = (f'Task 3 Part 1 (P1) Flow Visualization - Year +1\n'
             f'Grid Layout: Individual Machine Blocks\n'
             f'Sequence: B → A → B → C → D → I → J')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add legend for grid layout with overlaps
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightblue', edgecolor='#333333', linewidth=0.5, label='ABCD Block (14×14 ft)'),
        Patch(facecolor='lightgreen', edgecolor='#333333', linewidth=0.5, label='HIJ Block (14×36 ft)'),
        Patch(facecolor='#ff6b6b', alpha=0.5, label='Overlap Zone (2 ft, ABCD only)'),
        Patch(facecolor='none', edgecolor='black', linewidth=2, linestyle='--', label='Process Boundary'),
        FancyArrowPatch((0, 0), (1, 0), arrowstyle='->', color='red', linewidth=4, label='P1 Flow Path')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # Add summary box
    summary_text = (
        f"P1 Demand: {P1_DEMAND:,.2f} units/week\n"
        f"P1 Sequence: B→A→B→C→D→I→J (7 steps)\n"
        f"Total P1 Time: {P1_TOTAL_TIME:.2f} min/unit\n"
        f"Blocks: ABCD=14×14ft(share 2ft), HIJ=14×36ft(no share)\n"
        f"Grids: A(5×2) B(8×4) C(3×3) D(9×5) I(4×7) J(7×7)"
    )
    ax.text(0.02, 0.98, summary_text,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    return fig

def main():
    """Main execution"""
    print("=" * 80)
    print("TASK 3 YEAR +1 - PART 1 (P1) FLOW VISUALIZATION")
    print("=" * 80)
    
    print(f"\nP1 Demand: {P1_DEMAND:,.2f} units/week")
    print(f"Process Sequence: {' → '.join(P1_SEQUENCE)}")
    print(f"Total Steps: {len(P1_SEQUENCE)}")
    print(f"Total Process Time: 12.75 minutes/unit")
    
    print("\nGenerating flow visualization...")
    fig = create_flow_visualization()
    
    output_file = Path(__file__).parent / "P1_Flow_Visualization_Task3_Year1.png"
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Flow visualization saved to: {output_file}")
    
    plt.close()
    
    print("\n" + "=" * 80)
    print("P1 Flow visualization complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
