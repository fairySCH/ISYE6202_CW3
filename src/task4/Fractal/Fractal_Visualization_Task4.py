"""
fractal organization - layout visualization - task 4

creates publication-quality visualizations of fractal organization layouts
for years 2-5. generates png images for presentations and reports.

team: machas^2
date: november 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent.parent  # go up to project root
RESULTS_DIR = BASE_DIR / "results"
LAYOUT_DIR = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Layout"
VIZ_DIR = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Visuals"

YEARS = [2, 3, 4, 5]


def create_layout_visualization_yearly(year, num_fractals=3, show_flows=True, flow_threshold=1000):
    """
    Create publication-quality visualization of fractal layout for a specific year

    Parameters:
    - year: Year number (2, 3, 4, 5)
    - num_fractals: Number of fractal centers to visualize
    - show_flows: Whether to show material flow arrows
    - flow_threshold: Minimum flow to display (filters out small flows)
    """
    # Load data
    year_dir = LAYOUT_DIR / f"year{year}"
    layout_path = year_dir / f"f{num_fractals}_layout"
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
        if not flows_filtered.empty:
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

    # Get scaling factor for this year
    scaling_factor = centers['scaling_factor'].iloc[0] if 'scaling_factor' in centers.columns else 1.0

    title = f'Fractal Organization Layout - Year {year}, {num_fractals} Centers\n'
    title += f'Each center handles {100/num_fractals:.1f}% of production capacity'
    if scaling_factor != 1.0:
        title += f' (Scaled by {scaling_factor:.3f} from Year 4)'
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
    stats_text = f"Year +{year} - Per Center:\n• {len(processes)//num_fractals} processes\n"
    stats_text += f"• {total_equipment} equipment units\n"
    stats_text += f"• {100/num_fractals:.1f}% capacity"
    if scaling_factor != 1.0:
        stats_text += f"\n• Scaled: {scaling_factor:.3f}"

    ax.text(0.02, 0.98, stats_text,
           transform=ax.transAxes,
           fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    # Save the visualization
    VIZ_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"Year{year}_Fractal_f{num_fractals}_Layout.png"
    filepath = VIZ_DIR / filename
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"  Saved: {filepath}")

    plt.close()


def create_comparison_visualization():
    """
    Create comparison visualization showing scaling across years
    """
    # Load scaling analysis data
    scaling_file = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Design" / "Fractal_Scaling_Analysis.csv"
    scaling_df = pd.read_csv(scaling_file)

    # Create figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    fractal_configs = [2, 3, 4, 5]
    axes = [ax1, ax2, ax3, ax4]

    for i, f in enumerate(fractal_configs):
        ax = axes[i]

        # Filter data for this fractal configuration
        data = scaling_df[scaling_df['Num_Fractals'] == f]

        years = ['Year 2', 'Year 3', 'Year 5']
        scaling_factors = []

        for year in [2, 3, 5]:
            row = data[data['To_Year'] == year]
            if not row.empty:
                scaling_factors.append(row['Scaling_Factor'].iloc[0])
            else:
                scaling_factors.append(1.0)  # Year 4 baseline

        # Create bar chart
        bars = ax.bar(years, scaling_factors, color=['#FF6B6B', '#4ECDC4', '#FFE66D'])

        # Add value labels on bars
        for bar, factor in zip(bars, scaling_factors):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{factor:.3f}', ha='center', va='bottom', fontsize=11, weight='bold')

        ax.set_title(f'Fractal Configuration f={f}\n(Scaling Relative to Year 4)', fontsize=14, weight='bold')
        ax.set_ylabel('Scaling Factor', fontsize=12)
        ax.set_ylim(0, max(scaling_factors) * 1.2)
        ax.grid(True, alpha=0.3, axis='y')

        # Add reference line at 1.0
        ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Year 4 Baseline')
        ax.legend()

    plt.suptitle('Fractal Organization Scaling Analysis Across Years 2-5\n(Year 4 as Baseline Design)',
                fontsize=16, weight='bold', y=0.98)
    plt.tight_layout()

    # Save the comparison visualization
    VIZ_DIR.mkdir(parents=True, exist_ok=True)
    filename = "Fractal_Scaling_Comparison.png"
    filepath = VIZ_DIR / filename
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"  Saved: {filepath}")
    plt.close()


def create_yearly_equipment_comparison():
    """
    Create visualization comparing equipment requirements across years
    """
    # Load comparison data
    comparison_file = RESULTS_DIR / "Task4" / "Fractal" / "Fractal_Design" / "Fractal_Comparison_All_Years.csv"
    df = pd.read_csv(comparison_file)

    # Create figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    metrics = ['Total_Equipment', 'Avg_Equipment_per_Center', 'Avg_Utilization_%']
    titles = ['Total Equipment Units', 'Equipment per Center (avg)', 'Average Utilization (%)']
    axes = [ax1, ax2, ax3, ax4]

    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3']

    for i, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[i]

        for j, year in enumerate([2, 3, 4, 5]):
            year_data = df[df['Year'] == year]
            ax.plot(year_data['Num_Fractals'], year_data[metric],
                   marker='o', linewidth=3, markersize=8,
                   label=f'Year {year}', color=colors[j])

        ax.set_title(title, fontsize=14, weight='bold')
        ax.set_xlabel('Number of Fractal Centers', fontsize=12)
        ax.set_ylabel(title, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()

    plt.suptitle('Fractal Organization Equipment Analysis Across Years 2-5',
                fontsize=16, weight='bold', y=0.98)
    plt.tight_layout()

    # Save the equipment comparison
    VIZ_DIR.mkdir(parents=True, exist_ok=True)
    filename = "Fractal_Yearly_Equipment_Comparison.png"
    filepath = VIZ_DIR / filename
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"  Saved: {filepath}")
    plt.close()


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION - LAYOUT VISUALIZATION - TASK 4")
    print("="*80 + "\n")

    # Create output directory
    VIZ_DIR.mkdir(parents=True, exist_ok=True)

    # Generate layout visualizations for all years and configurations
    print("Generating individual layout visualizations...")
    for year in YEARS:
        print(f"\nYear {year} Layouts:")
        for f in [2, 3, 4, 5]:
            try:
                create_layout_visualization_yearly(year, f, show_flows=True, flow_threshold=500)
            except Exception as e:
                print(f"  Error creating Year {year}, f={f} visualization: {e}")

    # Generate comparison visualizations
    print("\nGenerating comparison visualizations...")
    try:
        create_comparison_visualization()
        create_yearly_equipment_comparison()
    except Exception as e:
        print(f"  Error creating comparison visualizations: {e}")

    print("\n" + "="*80)
    print("Visualization Generation Complete!")
    print("="*80 + "\n")

    print("Generated visualizations:")
    print("+- Individual Layouts:")
    for year in YEARS:
        for f in [2, 3, 4, 5]:
            print(f"|   +- Year{year}_Fractal_f{f}_Layout.png")
    print("+- Comparison Charts:")
    print("|   +- Fractal_Scaling_Comparison.png")
    print("|   +- Fractal_Yearly_Equipment_Comparison.png")

    print("\nVisualization files saved to:")
    print(f"  {VIZ_DIR}")


if __name__ == "__main__":
    main()