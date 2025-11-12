"""
Fractal Individual Parent Block Visualizer (REUSABLE)
======================================================

This script creates individual visualization images for each process (A-M),
showing the parent block with child equipment blocks inside.

Features:
- One image per process (A.png through M.png)
- Shows individual child equipment blocks with shareability zones
- Professional annotations and dimensions
- Color-coded by process group
- Reusable for any year/fractal combination

USAGE:
    python script.py <year> <num_fractals>
    Example: python script.py 5 4
             python script.py 1 4

Author: Fractal Block Visualization Team
Date: November 2025
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent.parent

# Process colors - professional palette
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

# Group labels
GROUP_LABELS = {
    'ABCD': 'Shareable 3-sides (2ft)',
    'EFG': 'No sharing',
    'HIJ': 'No sharing',
    'KLM': 'Shareable 2-sides (1ft)'
}

# Shareability zones color
OVERLAP_COLOR = '#FF4757'  # Bright red
OVERLAP_ALPHA = 0.4

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def draw_individual_process_block(process, config, output_dir):
    """
    Create a detailed visualization for a single process showing parent block
    with all child equipment blocks inside.
    
    Args:
        process: Process letter (A-M)
        config: Configuration row from optimal configs DataFrame
        output_dir: Directory to save output image
    """
    # Create figure with generous size
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='white')
    ax.set_facecolor('#F9FAFB')  # Very light gray
    
    # Extract configuration
    rows = config['rows']
    cols = config['cols']
    equipment_count = config['equipment_count']
    machine_w = config['machine_width_ft']
    machine_h = config['machine_depth_ft']
    block_w = config['block_width_ft']
    block_h = config['block_depth_ft']
    group = config['group']
    
    # Determine overlap based on group
    if group == 'ABCD':
        overlap_x, overlap_y = 2, 2
    elif group == 'KLM':
        overlap_x, overlap_y = 0, 1  # Share 1ft along the depth (y-direction) for 14×7 ft machines
    else:
        overlap_x, overlap_y = 0, 0
    
    # Draw parent block boundary (dashed)
    parent_rect = Rectangle(
        (0, 0), 
        block_w, 
        block_h,
        facecolor='none',
        edgecolor='black',
        linewidth=3.0,
        linestyle='--',
        alpha=0.7,
        zorder=1
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
                machine_x = col * (machine_w - overlap_x)
            else:
                machine_x = col * machine_w
            
            if overlap_y > 0:
                machine_y = row * (machine_h - overlap_y)
            else:
                machine_y = row * machine_h
            
            # Draw machine rectangle
            machine_rect = Rectangle(
                (machine_x, machine_y),
                machine_w,
                machine_h,
                facecolor=PROCESS_COLORS[process],
                edgecolor='#2d3436',
                linewidth=1.5,
                alpha=0.8,
                zorder=2
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
                    alpha=OVERLAP_ALPHA,
                    zorder=3
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
                    alpha=OVERLAP_ALPHA,
                    zorder=3
                )
                ax.add_patch(overlap_rect)
            
            # Add machine number
            ax.text(
                machine_x + machine_w / 2,
                machine_y + machine_h / 2,
                f"{machine_idx + 1}",
                ha='center',
                va='center',
                fontsize=9,
                color='white',
                fontweight='bold',
                alpha=0.9,
                zorder=4
            )
            
            machine_idx += 1
    
    # Configure axes
    padding = max(block_w, block_h) * 0.15
    ax.set_xlim(-padding * 0.3, block_w + padding)
    ax.set_ylim(-padding * 0.3, block_h + padding)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle=':', linewidth=0.5, color='gray')
    ax.set_xlabel('Width (ft)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Depth (ft)', fontsize=12, fontweight='bold')
    
    # Title
    title = (
        f"Process {process} - Parent Block Layout\n"
        f"{equipment_count} Equipment Units | {config['layout_grid']} Grid | "
        f"{block_w:.0f}×{block_h:.0f} ft | {config['utilization']:.1%} Utilization"
    )
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    
    # Add dimension annotations
    # Width annotation (above block)
    width_y = block_h + padding * 0.6
    ax.annotate('', xy=(0, width_y), xytext=(block_w, width_y),
               arrowprops=dict(arrowstyle='<->', color='#2E8B57', lw=2.5,
                             shrinkA=0, shrinkB=0))
    ax.text(block_w / 2, width_y + padding * 0.15, f"{block_w:.0f} ft",
           ha='center', va='bottom', fontsize=11,
           color='#2E8B57', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor='#2E8B57', linewidth=1.5))
    
    # Depth annotation (right of block)
    depth_x = block_w + padding * 0.6
    ax.annotate('', xy=(depth_x, 0), xytext=(depth_x, block_h),
               arrowprops=dict(arrowstyle='<->', color='#2E8B57', lw=2.5,
                             shrinkA=0, shrinkB=0))
    ax.text(depth_x + padding * 0.15, block_h / 2, f"{block_h:.0f} ft",
           ha='left', va='center', fontsize=11,
           color='#2E8B57', fontweight='bold', rotation=90,
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor='#2E8B57', linewidth=1.5))
    
    # Add information box
    info_text = (
        f"GROUP: {group} - {GROUP_LABELS[group]}\n"
        f"Machine Size: {machine_w:.0f}×{machine_h:.0f} ft\n"
        f"Grid: {rows} rows × {cols} cols\n"
        f"Total Spaces: {config['total_spaces']}\n"
        f"Wasted Spaces: {config['wasted_spaces']}\n"
        f"Block Area: {config['block_area_sqft']:.0f} sq ft\n"
        f"Aspect Ratio: {config['aspect_ratio']:.2f}"
    )
    
    ax.text(
        0.02, 0.98,
        info_text,
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
        family='monospace',
        zorder=10
    )
    
    # Add shareability legend if applicable
    if overlap_x > 0 or overlap_y > 0:
        overlap_legend = Rectangle(
            (0, 0), 1, 1, 
            fc=OVERLAP_COLOR, 
            alpha=OVERLAP_ALPHA, 
            label='Shareability Zone'
        )
        ax.legend(
            handles=[overlap_legend],
            loc='lower right',
            fontsize=9,
            framealpha=0.95
        )
    
    # Save figure
    plt.tight_layout()
    output_file = output_dir / f"Process_{process}_Block.png"
    plt.savefig(str(output_file), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_file


def visualize_all_blocks(year, num_fractals):
    """
    Generate individual block visualizations for all processes.
    
    Args:
        year: Year number (1-5)
        num_fractals: Number of fractal centers
    """
    # Load optimal configurations
    config_file = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / f"Year{year}_F{num_fractals}_Optimized" / f"Year{year}_F{num_fractals}_Optimal_Grid_Configurations.csv"
    
    if not config_file.exists():
        print(f"ERROR: Configuration file not found: {config_file}")
        print("Please run the optimizer script first!")
        sys.exit(1)
    
    # Output directory (same as config file)
    output_dir = config_file.parent
    
    print("=" * 80)
    print(f"FRACTAL INDIVIDUAL BLOCK VISUALIZER - Year {year}, F{num_fractals}")
    print("=" * 80)
    print()
    print(f"Loading configurations from:")
    print(f"  {config_file.relative_to(BASE_DIR)}")
    print()
    
    df_configs = pd.read_csv(config_file)
    
    print(f"Generating individual block images for {len(df_configs)} processes...")
    print("-" * 80)
    
    generated_files = []
    
    for _, config in df_configs.iterrows():
        process = config['process']
        
        print(f"  Creating image for Process {process}...", end=' ')
        
        output_file = draw_individual_process_block(process, config, output_dir)
        generated_files.append(output_file)
        
        print(f"✓ {output_file.name}")
    
    print("-" * 80)
    print()
    print("=" * 80)
    print("✓ ALL BLOCK VISUALIZATIONS COMPLETE!")
    print("=" * 80)
    print()
    print(f"Output directory: {output_dir.relative_to(BASE_DIR)}")
    print()
    print(f"Generated {len(generated_files)} images:")
    for f in generated_files:
        print(f"  - {f.name}")
    print()
    print("These images show parent blocks with child equipment blocks inside,")
    print("including shareability zones where applicable.")


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) >= 3:
        year = int(sys.argv[1])
        num_fractals = int(sys.argv[2])
    else:
        # Default to Year 5, F4
        print("Usage: python script.py <year> <num_fractals>")
        print("Example: python script.py 5 4")
        print("\nUsing defaults: Year 5, F4")
        year = 5
        num_fractals = 4
    
    visualize_all_blocks(year, num_fractals)
