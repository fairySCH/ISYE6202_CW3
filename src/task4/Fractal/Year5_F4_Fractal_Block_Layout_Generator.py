"""
Year 5 Fractal F4 - Parent Block Layout Generator with Child Equipment Blocks
==============================================================================

This script creates beautiful visualizations of the fractal layout showing:
1. Parent blocks (A-M process areas)
2. Child blocks (individual equipment units within each process)
3. Shareability zones (overlap areas between machines)
4. Process flow arrows
5. Detailed annotations

The layout considers:
- ABCD group: 14×14 ft machines, 2ft overlap on 3 sides
- EFG group: 22×15 ft machines, no overlap
- HIJ group: 14×36 ft machines, no overlap
- KLM group: 14×7 ft machines, 1ft overlap on sides

Author: Fractal Layout Visualization Team
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch
from matplotlib.collections import PatchCollection
from pathlib import Path
import csv

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent.parent
OPTIMAL_CONFIG_FILE = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / "Year5_F4_Optimized" / "Year5_F4_Optimal_Grid_Configurations.csv"
OUTPUT_DIR = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / "Year5_F4_Optimized"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Process flow sequence
PROCESS_ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

# Color scheme - professional and distinct
PROCESS_COLORS = {
    'A': '#FF6B6B',  # Coral Red
    'B': '#4ECDC4',  # Turquoise
    'C': '#45B7D1',  # Sky Blue
    'D': '#FFA07A',  # Light Salmon
    'E': '#98D8C8',  # Mint
    'F': '#6C5CE7',  # Purple
    'G': '#A29BFE',  # Lavender
    'H': '#FDCB6E',  # Yellow
    'I': '#55EFC4',  # Aquamarine
    'J': '#74B9FF',  # Light Blue
    'K': '#DFE6E9',  # Light Gray
    'L': '#FD79A8',  # Pink
    'M': '#FFEAA7',  # Cream
}

# Shareability zones color
OVERLAP_COLOR = '#FF4757'  # Bright red for overlap zones
OVERLAP_ALPHA = 0.35

GAP_BETWEEN_BLOCKS = 8  # ft - spacing between parent blocks

# ============================================================================
# LAYOUT GENERATION FUNCTIONS
# ============================================================================

def load_optimal_configurations():
    """Load the optimal grid configurations from CSV."""
    df = pd.read_csv(OPTIMAL_CONFIG_FILE)
    return df


def arrange_parent_blocks_2d(df_config):
    """
    Arrange parent blocks in a 2D compact layout.
    
    Strategy:
    - Row 1: ABCD group (smaller machines)
    - Row 2: EFG group (medium machines)
    - Row 3: HIJ group (large machines)
    - Row 4: KLM group (small machines)
    
    Returns:
        positions: dict with {process: {'x': x, 'y': y, 'config': config_row}}
        total_width, total_height: Overall layout dimensions
    """
    positions = {}
    
    # Group processes by machine group
    groups = {
        'ABCD': ['A', 'B', 'C', 'D'],
        'EFG': ['E', 'F', 'G'],
        'HIJ': ['H', 'I', 'J'],
        'KLM': ['K', 'L', 'M']
    }
    
    current_y = 0
    max_width = 0
    
    for group_name, processes in groups.items():
        # Get configs for this group
        group_configs = df_config[df_config['process'].isin(processes)]
        
        # Place horizontally
        current_x = 0
        row_height = 0
        
        for _, config in group_configs.iterrows():
            process = config['process']
            
            positions[process] = {
                'x': current_x,
                'y': current_y,
                'config': config
            }
            
            current_x += config['block_width_ft'] + GAP_BETWEEN_BLOCKS
            row_height = max(row_height, config['block_depth_ft'])
        
        max_width = max(max_width, current_x - GAP_BETWEEN_BLOCKS)
        current_y += row_height + GAP_BETWEEN_BLOCKS
    
    total_height = current_y - GAP_BETWEEN_BLOCKS
    total_width = max_width
    
    return positions, total_width, total_height


def draw_child_equipment_blocks(ax, x0, y0, config, process_name):
    """
    Draw individual equipment blocks (child blocks) within a parent block.
    
    Shows:
    - Individual machine rectangles
    - Overlap zones (shareability areas)
    - Machine numbering
    
    Args:
        ax: Matplotlib axis
        x0, y0: Bottom-left corner of parent block
        config: Configuration row from optimal_configs
        process_name: Process identifier
    """
    rows = config['rows']
    cols = config['cols']
    equipment_count = config['equipment_count']
    machine_w = config['machine_width_ft']
    machine_h = config['machine_depth_ft']
    
    # Determine overlap based on group
    group = config['group']
    if group == 'ABCD':
        overlap_x, overlap_y = 2, 2
    elif group == 'KLM':
        overlap_x, overlap_y = 1, 0
    else:
        overlap_x, overlap_y = 0, 0
    
    # Draw parent block boundary (dashed)
    parent_rect = Rectangle(
        (x0, y0), 
        config['block_width_ft'], 
        config['block_depth_ft'],
        facecolor='none',
        edgecolor='black',
        linewidth=2.5,
        linestyle='--',
        alpha=0.6
    )
    ax.add_patch(parent_rect)
    
    # Draw each child equipment block
    machine_idx = 0
    
    for row in range(rows):
        for col in range(cols):
            if machine_idx >= equipment_count:
                break
            
            # Calculate position with overlap
            if overlap_x > 0:
                machine_x = x0 + col * (machine_w - overlap_x)
            else:
                machine_x = x0 + col * machine_w
            
            if overlap_y > 0:
                machine_y = y0 + row * (machine_h - overlap_y)
            else:
                machine_y = y0 + row * machine_h
            
            # Draw machine rectangle
            machine_rect = Rectangle(
                (machine_x, machine_y),
                machine_w,
                machine_h,
                facecolor=PROCESS_COLORS[process_name],
                edgecolor='#2d3436',
                linewidth=1.0,
                alpha=0.75
            )
            ax.add_patch(machine_rect)
            
            # Draw overlap zones if applicable
            if overlap_x > 0 and col < cols - 1:
                # Horizontal overlap (right side)
                overlap_rect = Rectangle(
                    (machine_x + machine_w - overlap_x, machine_y),
                    overlap_x,
                    machine_h,
                    facecolor=OVERLAP_COLOR,
                    edgecolor='none',
                    alpha=OVERLAP_ALPHA
                )
                ax.add_patch(overlap_rect)
            
            if overlap_y > 0 and row < rows - 1:
                # Vertical overlap (top side)
                overlap_rect = Rectangle(
                    (machine_x, machine_y + machine_h - overlap_y),
                    machine_w,
                    overlap_y,
                    facecolor=OVERLAP_COLOR,
                    edgecolor='none',
                    alpha=OVERLAP_ALPHA
                )
                ax.add_patch(overlap_rect)
            
            # Add machine number (small text)
            ax.text(
                machine_x + machine_w / 2,
                machine_y + machine_h / 2,
                f"{machine_idx + 1}",
                ha='center',
                va='center',
                fontsize=6,
                color='white',
                fontweight='bold',
                alpha=0.8
            )
            
            machine_idx += 1
    
    # Add parent block label (outside, at top)
    label_text = f"{process_name}\n{equipment_count} units\n{config['layout_grid']}"
    
    ax.text(
        x0 + config['block_width_ft'] / 2,
        y0 + config['block_depth_ft'] + 3,
        label_text,
        ha='center',
        va='bottom',
        fontsize=11,
        fontweight='bold',
        bbox=dict(
            boxstyle='round,pad=0.5',
            facecolor=PROCESS_COLORS[process_name],
            edgecolor='black',
            linewidth=1.5,
            alpha=0.9
        )
    )


def draw_process_flow_arrows(ax, positions):
    """
    Draw arrows showing the process flow sequence.
    
    Arrows connect from center of one parent block to center of next.
    """
    for i in range(len(PROCESS_ORDER) - 1):
        process_from = PROCESS_ORDER[i]
        process_to = PROCESS_ORDER[i + 1]
        
        if process_from not in positions or process_to not in positions:
            continue
        
        pos_from = positions[process_from]
        pos_to = positions[process_to]
        
        config_from = pos_from['config']
        config_to = pos_to['config']
        
        # Calculate center points
        x_from = pos_from['x'] + config_from['block_width_ft'] / 2
        y_from = pos_from['y'] + config_from['block_depth_ft'] / 2
        
        x_to = pos_to['x'] + config_to['block_width_ft'] / 2
        y_to = pos_to['y'] + config_to['block_depth_ft'] / 2
        
        # Draw arrow
        arrow = FancyArrowPatch(
            (x_from, y_from),
            (x_to, y_to),
            arrowstyle='->,head_width=0.8,head_length=1.2',
            color='#e74c3c',
            linewidth=2.5,
            alpha=0.7,
            zorder=1  # Behind blocks
        )
        ax.add_patch(arrow)


def create_layout_visualization(df_config, positions, total_width, total_height):
    """
    Create the main layout visualization.
    
    Shows:
    - All parent blocks with child equipment
    - Process flow arrows
    - Legend
    - Summary statistics
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(20, 14))
    
    # Draw process flow arrows first (background layer)
    draw_process_flow_arrows(ax, positions)
    
    # Draw each parent block with child equipment
    for process in PROCESS_ORDER:
        if process not in positions:
            continue
        
        pos = positions[process]
        config = pos['config']
        
        draw_child_equipment_blocks(
            ax,
            pos['x'],
            pos['y'],
            config,
            process
        )
    
    # Configure axes
    margin = 20
    ax.set_xlim(-margin, total_width + margin)
    ax.set_ylim(-margin, total_height + margin * 3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle=':', linewidth=0.5)
    ax.set_xlabel('Width (ft)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Depth (ft)', fontsize=12, fontweight='bold')
    
    # Title
    total_machines = df_config['equipment_count'].sum()
    total_area = df_config['block_area_sqft'].sum()
    
    title_text = (
        f"Year 5 Fractal F4 - Single Center Layout\n"
        f"Total: {total_machines} machines, {total_area:,.0f} sq ft "
        f"(Layout: {total_width:.0f} × {total_height:.0f} ft)"
    )
    ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20)
    
    # Add legend for overlap zones
    legend_elements = [
        Rectangle((0, 0), 1, 1, fc=OVERLAP_COLOR, alpha=OVERLAP_ALPHA, label='Shareability Zone')
    ]
    ax.legend(
        handles=legend_elements,
        loc='upper right',
        fontsize=10,
        framealpha=0.95
    )
    
    # Add summary statistics box
    stats_text = (
        f"CONFIGURATION SUMMARY:\n"
        f"• Total Equipment: {total_machines} units\n"
        f"• Total Block Area: {total_area:,.0f} sq ft\n"
        f"• Layout Dimensions: {total_width:.0f} × {total_height:.0f} ft\n"
        f"• Layout Area: {total_width * total_height:,.0f} sq ft\n"
        f"• Avg Utilization: {df_config['utilization'].mean():.1%}\n"
        f"• Total Wasted Spaces: {df_config['wasted_spaces'].sum():.0f}"
    )
    
    ax.text(
        0.02, 0.98,
        stats_text,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment='top',
        bbox=dict(
            boxstyle='round,pad=0.8',
            facecolor='white',
            edgecolor='black',
            linewidth=1.5,
            alpha=0.95
        ),
        family='monospace'
    )
    
    plt.tight_layout()
    
    return fig, ax


def generate_detail_reports(df_config, positions, total_width, total_height):
    """Generate detailed CSV reports of the layout."""
    
    # Report 1: Parent block positions
    block_positions = []
    for process in PROCESS_ORDER:
        if process not in positions:
            continue
        
        pos = positions[process]
        config = pos['config']
        
        block_positions.append({
            'Process': process,
            'Group': config['group'],
            'X_Position_ft': pos['x'],
            'Y_Position_ft': pos['y'],
            'Width_ft': config['block_width_ft'],
            'Depth_ft': config['block_depth_ft'],
            'Area_sqft': config['block_area_sqft'],
            'Equipment_Count': config['equipment_count'],
            'Grid_Layout': config['layout_grid'],
            'Utilization': f"{config['utilization']:.2%}"
        })
    
    df_positions = pd.DataFrame(block_positions)
    positions_file = OUTPUT_DIR / "Year5_F4_Parent_Block_Positions.csv"
    df_positions.to_csv(positions_file, index=False)
    
    # Report 2: Individual equipment coordinates
    equipment_coords = []
    
    for process in PROCESS_ORDER:
        if process not in positions:
            continue
        
        pos = positions[process]
        config = pos['config']
        
        rows = config['rows']
        cols = config['cols']
        equipment_count = config['equipment_count']
        machine_w = config['machine_width_ft']
        machine_h = config['machine_depth_ft']
        
        # Determine overlap
        group = config['group']
        if group == 'ABCD':
            overlap_x, overlap_y = 2, 2
        elif group == 'KLM':
            overlap_x, overlap_y = 1, 0
        else:
            overlap_x, overlap_y = 0, 0
        
        machine_idx = 0
        for row in range(rows):
            for col in range(cols):
                if machine_idx >= equipment_count:
                    break
                
                # Calculate position with overlap
                if overlap_x > 0:
                    machine_x = pos['x'] + col * (machine_w - overlap_x)
                else:
                    machine_x = pos['x'] + col * machine_w
                
                if overlap_y > 0:
                    machine_y = pos['y'] + row * (machine_h - overlap_y)
                else:
                    machine_y = pos['y'] + row * machine_h
                
                equipment_coords.append({
                    'Process': process,
                    'Equipment_ID': f"{process}{machine_idx + 1:02d}",
                    'Grid_Row': row,
                    'Grid_Col': col,
                    'X_Position_ft': machine_x,
                    'Y_Position_ft': machine_y,
                    'Width_ft': machine_w,
                    'Depth_ft': machine_h,
                    'Center_X_ft': machine_x + machine_w / 2,
                    'Center_Y_ft': machine_y + machine_h / 2
                })
                
                machine_idx += 1
    
    df_equipment = pd.DataFrame(equipment_coords)
    equipment_file = OUTPUT_DIR / "Year5_F4_Individual_Equipment_Coordinates.csv"
    df_equipment.to_csv(equipment_file, index=False)
    
    # Report 3: Layout summary
    summary_data = {
        'Metric': [
            'Total Machines',
            'Total Block Area (sq ft)',
            'Layout Width (ft)',
            'Layout Depth (ft)',
            'Total Layout Area (sq ft)',
            'Average Utilization (%)',
            'Total Wasted Spaces',
            'Average Aspect Ratio',
            'Number of Process Areas'
        ],
        'Value': [
            df_config['equipment_count'].sum(),
            f"{df_config['block_area_sqft'].sum():,.0f}",
            f"{total_width:.0f}",
            f"{total_height:.0f}",
            f"{total_width * total_height:,.0f}",
            f"{df_config['utilization'].mean() * 100:.1f}",
            df_config['wasted_spaces'].sum(),
            f"{df_config['aspect_ratio'].mean():.3f}",
            len(df_config)
        ]
    }
    
    df_summary = pd.DataFrame(summary_data)
    summary_file = OUTPUT_DIR / "Year5_F4_Layout_Summary.csv"
    df_summary.to_csv(summary_file, index=False)
    
    return positions_file, equipment_file, summary_file


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def generate_fractal_layout():
    """Main function to generate the fractal layout visualization."""
    
    print("=" * 80)
    print("YEAR 5 FRACTAL F4 - LAYOUT GENERATOR WITH CHILD BLOCKS")
    print("=" * 80)
    print()
    
    # Load optimal configurations
    print(f"Loading optimal configurations from:")
    print(f"  {OPTIMAL_CONFIG_FILE.relative_to(BASE_DIR)}")
    print()
    
    df_config = load_optimal_configurations()
    
    # Arrange parent blocks
    print("Arranging parent blocks in 2D layout...")
    positions, total_width, total_height = arrange_parent_blocks_2d(df_config)
    print(f"  Layout dimensions: {total_width:.0f} ft × {total_height:.0f} ft")
    print()
    
    # Create visualization
    print("Creating visualization with child equipment blocks...")
    fig, ax = create_layout_visualization(df_config, positions, total_width, total_height)
    
    # Save figure
    output_png = OUTPUT_DIR / "Year5_F4_Fractal_Layout_Detailed.png"
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved visualization: {output_png.relative_to(BASE_DIR)}")
    
    # Generate detailed reports
    print()
    print("Generating detailed CSV reports...")
    pos_file, equip_file, summ_file = generate_detail_reports(
        df_config, positions, total_width, total_height
    )
    
    print(f"  ✓ Parent block positions: {pos_file.relative_to(BASE_DIR)}")
    print(f"  ✓ Equipment coordinates: {equip_file.relative_to(BASE_DIR)}")
    print(f"  ✓ Layout summary: {summ_file.relative_to(BASE_DIR)}")
    
    print()
    print("=" * 80)
    print("✓ LAYOUT GENERATION COMPLETE!")
    print("=" * 80)
    print()
    print(f"Output directory: {OUTPUT_DIR.relative_to(BASE_DIR)}")
    print()
    print("Files generated:")
    print("  1. Year5_F4_Fractal_Layout_Detailed.png - Visual layout")
    print("  2. Year5_F4_Parent_Block_Positions.csv - Block positions")
    print("  3. Year5_F4_Individual_Equipment_Coordinates.csv - Equipment details")
    print("  4. Year5_F4_Layout_Summary.csv - Summary statistics")
    
    plt.show()


if __name__ == "__main__":
    generate_fractal_layout()
