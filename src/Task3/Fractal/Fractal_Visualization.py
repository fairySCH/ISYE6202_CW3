"""
Fractal Organization - Layout Visualization

Creates publication-quality visualizations of fractal organization layouts.
Generates PNG images for presentations and reports.

Author: FeMoaSa Design Team
Date: November 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to project root
RESULTS_DIR = BASE_DIR / "results"
LAYOUT_DIR = RESULTS_DIR / "Task3" / "Fractal" / "Fractal_Layout"
VIZ_DIR = RESULTS_DIR / "Task3" / "Fractal" / "Fractal_Visuals"


def create_layout_visualization(num_fractals=3, show_flows=True, flow_threshold=1000):
    """
    Create publication-quality visualization of fractal layout
    
    Parameters:
    - num_fractals: Number of fractal centers to visualize
    - show_flows: Whether to show material flow arrows
    - flow_threshold: Minimum flow to display (filters out small flows)
    """
    # Load data
    layout_path = LAYOUT_DIR / f"f{num_fractals}_layout"
    processes = pd.read_csv(layout_path / "Process_Locations.csv")
    flows = pd.read_csv(layout_path / "Flow_Connections.csv")
    centers = pd.read_csv(layout_path / "Center_Boundaries.csv")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 14))
    
    # Define colors for each center
    center_colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#C7CEEA']
    
    # Draw center boundaries
    for _, center in centers.iterrows():
        center_id = int(center['center_id'])
        color = center_colors[(center_id - 1) % len(center_colors)]
        
        # Rectangle for center boundary
        rect = mpatches.Rectangle(
            (center['x'] - center['width']/2, center['y'] - center['height']/2),
            center['width'], center['height'],
            fill=True, facecolor=color, alpha=0.1,
            edgecolor=color, linewidth=3, linestyle='--'
        )
        ax.add_patch(rect)
        
        # Label
        ax.text(center['x'], center['y'] - center['height']/2 - 5, 
                f"Fractal Center {center_id}", 
                ha='center', va='top',
                fontsize=16, weight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor=color, linewidth=2))
    
    # Draw material flows (if enabled)
    if show_flows:
        # Filter flows by threshold
        flows_filtered = flows[flows['Flow_Units'] >= flow_threshold]
        max_flow = flows_filtered['Flow_Units'].max()
        
        for _, flow in flows_filtered.iterrows():
            # Arrow width proportional to flow
            width = max(0.5, (flow['Flow_Units'] / max_flow) * 3)
            
            ax.annotate('',
                       xy=(flow['To_X'], flow['To_Y']),
                       xytext=(flow['From_X'], flow['From_Y']),
                       arrowprops=dict(
                           arrowstyle='->', 
                           lw=width,
                           color='gray', 
                           alpha=0.4,
                           connectionstyle="arc3,rad=0.1"
                       ))
    
    # Draw processes
    for _, proc in processes.iterrows():
        center_id = int(proc['Center_ID'])
        color = center_colors[(center_id - 1) % len(center_colors)]
        
        # Circle for process
        circle = plt.Circle(
            (proc['Global_X'], proc['Global_Y']), 
            proc['Width']/2,
            color=color, alpha=0.7,
            edgecolor='black', linewidth=2.5
        )
        ax.add_patch(circle)
        
        # Label with process name and equipment count
        label = f"{proc['Process']}\n({int(proc['Equipment_Count'])})"
        ax.text(proc['Global_X'], proc['Global_Y'], 
               label,
               ha='center', va='center', 
               fontsize=11, weight='bold',
               color='white' if proc['Equipment_Count'] > 5 else 'black')
    
    # Set axis properties
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.set_xlabel('X Position (meters)', fontsize=14, weight='bold')
    ax.set_ylabel('Y Position (meters)', fontsize=14, weight='bold')
    
    # Set axis limits based on data
    x_margin = 20
    y_margin = 20
    ax.set_xlim(processes['Global_X'].min() - x_margin, 
               processes['Global_X'].max() + x_margin)
    ax.set_ylim(processes['Global_Y'].min() - y_margin, 
               processes['Global_Y'].max() + y_margin)
    
    title = f'Fractal Organization Layout - {num_fractals} Centers\n'
    title += f'Each center handles {100/num_fractals:.1f}% of production capacity'
    ax.set_title(title, fontsize=18, weight='bold', pad=20)
    
    # Add legend
    legend_elements = []
    for i in range(num_fractals):
        color = center_colors[i % len(center_colors)]
        legend_elements.append(
            mpatches.Patch(facecolor=color, edgecolor='black', 
                          label=f'Center {i+1}', alpha=0.7)
        )
    
    ax.legend(handles=legend_elements, loc='upper right', 
             fontsize=12, framealpha=0.9, title='Fractal Centers',
             title_fontsize=13)
    
    # Add statistics box
    total_equipment = processes.groupby('Center_ID')['Equipment_Count'].sum().iloc[0]
    stats_text = f"Per Center:\n• {len(processes)//num_fractals} processes\n"
    stats_text += f"• {total_equipment} equipment units\n"
    stats_text += f"• {100/num_fractals:.1f}% capacity"
    
    ax.text(0.02, 0.98, stats_text,
           transform=ax.transAxes,
           fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # Save
    VIZ_DIR.mkdir(exist_ok=True)
    output_file = VIZ_DIR / f"Fractal_Layout_f{num_fractals}.png"
    plt.savefig(output_file, dpi=150)
    print(f"Saved: {output_file.name}")
    
    return fig, ax


def create_comparison_chart():
    """Create bar chart comparing equipment requirements across configurations"""
    comparison_file = RESULTS_DIR / "Task3" / "Fractal" / "Fractal_Design" / "Fractal_Comparison_All_Scenarios.csv"
    df = pd.read_csv(comparison_file)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Chart 1: Total Equipment
    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3']
    ax1.bar(df['Num_Fractals'], df['Total_Equipment'], color=colors, 
           edgecolor='black', linewidth=2, alpha=0.8)
    ax1.axhline(y=386, color='red', linestyle='--', linewidth=2, 
               label='Functional Baseline (386)')
    ax1.set_xlabel('Number of Fractal Centers (f)', fontsize=13, weight='bold')
    ax1.set_ylabel('Total Equipment Units', fontsize=13, weight='bold')
    ax1.set_title('Equipment Requirements by Configuration', 
                 fontsize=15, weight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_xticks(df['Num_Fractals'])
    
    # Add value labels on bars
    for i, (f, equip) in enumerate(zip(df['Num_Fractals'], df['Total_Equipment'])):
        overhead = ((equip - 386) / 386 * 100)
        ax1.text(f, equip + 5, f"{int(equip)}\n(+{overhead:.1f}%)", 
                ha='center', va='bottom', fontsize=10, weight='bold')
    
    # Chart 2: Average Utilization
    ax2.bar(df['Num_Fractals'], df['Avg_Utilization_%'], color=colors,
           edgecolor='black', linewidth=2, alpha=0.8)
    ax2.axhline(y=95, color='green', linestyle='--', linewidth=2,
               label='Target: 95%')
    ax2.set_xlabel('Number of Fractal Centers (f)', fontsize=13, weight='bold')
    ax2.set_ylabel('Average Utilization (%)', fontsize=13, weight='bold')
    ax2.set_title('Equipment Utilization by Configuration', 
                 fontsize=15, weight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_xticks(df['Num_Fractals'])
    ax2.set_ylim(85, 100)
    
    # Add value labels
    for f, util in zip(df['Num_Fractals'], df['Avg_Utilization_%']):
        ax2.text(f, util + 0.5, f"{util:.1f}%", 
                ha='center', va='bottom', fontsize=10, weight='bold')
    
    plt.tight_layout()
    
    output_file = VIZ_DIR / "Fractal_Equipment_Comparison.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_file.name}")
    
    return fig


def create_flow_matrix_heatmap(num_fractals=3):
    """Create heatmap visualization of flow matrix"""
    flow_file = RESULTS_DIR / "Task3" / "Fractal" / "Fractal_Flowmatrix" / f"f{num_fractals}_centers" / "Single_Center_Flow_Matrix.csv"
    flow_matrix = pd.read_csv(flow_file, index_col=0)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create heatmap
    im = ax.imshow(flow_matrix.values, cmap='YlOrRd', aspect='auto')
    
    # Set ticks
    ax.set_xticks(range(len(flow_matrix.columns)))
    ax.set_yticks(range(len(flow_matrix.index)))
    ax.set_xticklabels(flow_matrix.columns)
    ax.set_yticklabels(flow_matrix.index)
    
    # Rotate labels
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", fontsize=11)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Weekly Flow (units)', rotation=270, labelpad=20, 
                   fontsize=12, weight='bold')
    
    # Add values in cells
    for i in range(len(flow_matrix.index)):
        for j in range(len(flow_matrix.columns)):
            value = flow_matrix.iloc[i, j]
            if value > 0:
                text_color = 'white' if value > flow_matrix.values.max()/2 else 'black'
                ax.text(j, i, f'{int(value)}', 
                       ha="center", va="center", 
                       color=text_color, fontsize=8, weight='bold')
    
    ax.set_xlabel('To Process', fontsize=13, weight='bold')
    ax.set_ylabel('From Process', fontsize=13, weight='bold')
    
    title = f'Flow Matrix - Single Fractal Center (f={num_fractals})\n'
    title += f'Material flow between processes (units/week)'
    ax.set_title(title, fontsize=15, weight='bold', pad=15)
    
    plt.tight_layout()
    
    output_file = VIZ_DIR / f"Fractal_Flow_Matrix_f{num_fractals}.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Saved: {output_file.name}")
    
    return fig


def main():
    """Generate all visualizations"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION - VISUALIZATION GENERATION")
    print("="*80 + "\n")
    
    VIZ_DIR.mkdir(exist_ok=True)
    
    print("Generating layout visualizations...")
    for f in [2, 3, 4]:
        create_layout_visualization(f, show_flows=True, flow_threshold=2000)
        plt.close()
    
    print("\nGenerating comparison chart...")
    create_comparison_chart()
    plt.close()
    
    print("\nGenerating flow matrix heatmaps...")
    for f in [2, 3, 4]:
        create_flow_matrix_heatmap(f)
        plt.close()
    
    print("\n" + "="*80)
    print("Visualization Generation Complete!")
    print("="*80 + "\n")
    
    print(f"All visualizations saved to: {VIZ_DIR.relative_to(BASE_DIR)}")
    print("\nGenerated files:")
    print("  - Fractal_Layout_f2.png")
    print("  - Fractal_Layout_f3.png")
    print("  - Fractal_Layout_f4.png")
    print("  - Fractal_Equipment_Comparison.png")
    print("  - Fractal_Flow_Matrix_f2.png")
    print("  - Fractal_Flow_Matrix_f3.png")
    print("  - Fractal_Flow_Matrix_f4.png")
    print("\nUse these images for presentations and reports!")


if __name__ == "__main__":
    main()
