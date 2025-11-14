"""
Fractal Distance Metrics - Consolidated Pipeline

Computes pairwise Euclidean distances between centroids, weighted flow distances,
and generates flow line visualizations for fractal layouts.

Supports both Y1F4 and Y5F4 layouts with appropriate output directories.

author: machas^2 team
"""

from pathlib import Path
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def compute_flow_distances_from_centroids(centroids_path, flow_path, output_dir, prefix):
    """
    Compute pairwise Euclidean distances between centroids and weighted flow distances
    """
    # Load data
    cent = pd.read_csv(centroids_path)
    flow = pd.read_csv(flow_path, index_col=0)

    # Transform coordinates: origin at top-left, y increases downwards
    if 'Y1_F4' in prefix or 'Y1F4' in prefix:
        # Y1F4 layout: 210x195 ft, y=0 at top, y=195 at bottom
        max_y = 195
    elif 'Y5_F4' in prefix or 'Y5F4' in prefix:
        # Y5F4 layout: 298x292 ft, y=0 at top, y=292 at bottom
        max_y = 292
    else:
        max_y = 300  # default

    # Flip y-coordinates so origin is at top-left
    cent['centroid_y'] = max_y - cent['centroid_y']

    # Validate processes
    processes_cent = list(cent['process'].astype(str))
    processes_flow = list(flow.index.astype(str))

    rows = []
    total_flow = 0.0
    total_weighted_distance = 0.0

    for from_proc in flow.index:
        for to_proc in flow.columns:
            try:
                flow_val = float(flow.at[from_proc, to_proc])
            except Exception:
                flow_val = float(flow.loc[str(from_proc), str(to_proc)])

            # find centroids; if missing, skip
            f = str(from_proc)
            t = str(to_proc)
            if f not in processes_cent or t not in processes_cent:
                continue

            c_from = cent[cent['process'] == f].iloc[0]
            c_to = cent[cent['process'] == t].iloc[0]

            x1, y1 = float(c_from['centroid_x']), float(c_from['centroid_y'])
            x2, y2 = float(c_to['centroid_x']), float(c_to['centroid_y'])

            dist = math.hypot(x2 - x1, y2 - y1)
            flow_x_dist = flow_val * dist

            rows.append({
                'from': f,
                'to': t,
                'flow': flow_val,
                'distance_ft': round(dist, 3),
                'flow_x_distance': round(flow_x_dist, 3)
            })

            total_flow += flow_val
            total_weighted_distance += flow_x_dist

    # Save dataframe
    df_out = pd.DataFrame(rows)
    df_out.sort_values(by='flow_x_distance', ascending=False, inplace=True)

    pairwise_file = output_dir / f'{prefix}_Flow_Distances.csv'
    df_out.to_csv(pairwise_file, index=False)

    return df_out, total_flow, total_weighted_distance

def add_distance_travelled_metric(df_pairs, output_dir, prefix):
    """
    Add distance travelled metric and create aggregates
    """
    # Add distance travelled metrics
    df_pairs['distance_travelled_ft'] = df_pairs['flow_x_distance']
    df_pairs['distance_travelled_km'] = (df_pairs['distance_travelled_ft'] / 3.28084).round(3)

    # Save updated pairwise CSV
    pairwise_with_dist_file = output_dir / f'{prefix}_Flow_Distances_With_Distance_Travelled.csv'
    df_pairs.to_csv(pairwise_with_dist_file, index=False)

    # Aggregate totals by origin (from) and destination (to)
    agg_from = df_pairs.groupby('from').agg(
        total_flow=('flow', 'sum'),
        total_distance_travelled_ft=('distance_travelled_ft', 'sum')
    ).reset_index()
    agg_from['total_distance_travelled_km'] = (agg_from['total_distance_travelled_ft'] / 3.28084).round(3)

    agg_to = df_pairs.groupby('to').agg(
        total_flow=('flow', 'sum'),
        total_distance_travelled_ft=('distance_travelled_ft', 'sum')
    ).reset_index()
    agg_to['total_distance_travelled_km'] = (agg_to['total_distance_travelled_ft'] / 3.28084).round(3)

    # Save aggregates
    agg_from_file = output_dir / f'{prefix}_Distance_By_From_Process.csv'
    agg_to_file = output_dir / f'{prefix}_Distance_By_To_Process.csv'
    agg_from.to_csv(agg_from_file, index=False)
    agg_to.to_csv(agg_to_file, index=False)

    return df_pairs

def plot_flow_lines(centroids_path, df_pairs, output_dir, prefix):
    """
    Plot flow lines between centroids
    """
    cent = pd.read_csv(centroids_path)

    # Transform coordinates: origin at top-left, y increases downwards
    if 'Y1_F4' in prefix or 'Y1F4' in prefix:
        # Y1F4 layout: 210x195 ft, y=0 at top, y=195 at bottom
        max_y = 195
    elif 'Y5_F4' in prefix or 'Y5F4' in prefix:
        # Y5F4 layout: 298x292 ft, y=0 at top, y=292 at bottom
        max_y = 292
    else:
        max_y = 300  # default

    # Flip y-coordinates so origin is at top-left
    cent['centroid_y'] = max_y - cent['centroid_y']

    # Create centroid mapping
    cent_map = {row['process']: (row['centroid_x'], row['centroid_y']) for _, row in cent.iterrows()}

    # Keep only positive flows
    df_plot = df_pairs[df_pairs['flow'] > 0].copy()

    # Normalize linewidth by flow (map 1st-99th percentile to 0.8-8 px)
    flows = df_plot['flow'].values
    if len(flows) > 0:
        p1, p99 = np.percentile(flows, [1, 99])
    else:
        p1 = p99 = 0

    def scale_width(v, lo=p1, hi=p99, minw=0.8, maxw=8.0):
        if lo == hi:
            return (minw + maxw) / 2
        if v <= lo:
            return minw
        if v >= hi:
            return maxw
        return minw + (maxw - minw) * ((v - lo) / (hi - lo))

    # Prepare plot
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#0f0f0f')

    # Plot lines
    for _, r in df_plot.iterrows():
        f = str(r['from'])
        t = str(r['to'])
        x1, y1 = cent_map[f]
        x2, y2 = cent_map[t]
        ft = r['flow']
        w = scale_width(ft)
        alpha = min(0.9, 0.2 + 0.8 * (ft / flows.max())) if len(flows) > 0 else 0.6

        ax.plot([x1, x2], [y1, y2], color='cyan', linewidth=w, alpha=alpha, solid_capstyle='round')

    # Draw nodes and labels
    for _, row in cent.iterrows():
        p = row['process']
        x = row['centroid_x']
        y = row['centroid_y']
        ax.scatter(x, y, s=200, color='white', edgecolor='k', zorder=5)
        ax.text(x, y, str(p), color='black', fontsize=12, fontweight='bold',
                ha='center', va='center', zorder=6)

    # Plot formatting
    if 'Y1_F4' in prefix or 'Y1F4' in prefix:
        # Y1F4 layout: 210x195 ft area
        xlim_max = 220
        ylim_max = 200
        x_mark = 210
        y_mark = 195
    elif 'Y5_F4' in prefix or 'Y5F4' in prefix:
        # Y5F4 layout: 298x292 ft area
        xlim_max = 300
        ylim_max = 300
        x_mark = 298
        y_mark = 292
    else:
        # Default
        xlim_max = 240
        ylim_max = 300
        x_mark = None
        y_mark = None

    ax.set_xlim(0, xlim_max)
    ax.set_ylim(0, ylim_max)
    ax.set_xlabel('X (ft)')
    ax.set_ylabel('Y (ft)')
    ax.set_title(f'{prefix} Flow Lines (thicker = larger flow)')
    ax.set_aspect('equal')
    ax.grid(True, color='#222222')

    # Add layout area markers
    if x_mark is not None:
        ax.axvline(x=x_mark, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(x_mark, ylim_max * 0.02, f'{x_mark}ft', color='red', fontsize=10,
                ha='center', va='bottom', fontweight='bold')
    if y_mark is not None:
        ax.axhline(y=y_mark, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(xlim_max * 0.02, y_mark, f'{y_mark}ft', color='red', fontsize=10,
                ha='left', va='center', fontweight='bold')

    plt.tight_layout()
    plot_file = output_dir / f'{prefix}_Flow_Lines.png'
    plt.savefig(plot_file, dpi=300)
    plt.close()

    return plot_file

def create_summary_report(total_flow, total_weighted_distance, output_dir, prefix):
    """
    Create summary report
    """
    avg_distance_per_flow = total_weighted_distance / total_flow if total_flow != 0 else None

    summary_file = output_dir / f'{prefix}_Distance_Summary.txt'
    with open(summary_file, 'w') as f:
        f.write(f'Total flow: {total_flow:,.2f}\n')
        f.write(f'Total weighted distance (flow x ft): {total_weighted_distance:,.2f}\n')
        if avg_distance_per_flow is not None:
            f.write(f'Average distance per unit flow (ft per flow unit): {avg_distance_per_flow:.4f}\n')

    return summary_file

def run_distance_pipeline(centroids_path, flow_path, output_dir, prefix):
    """
    Run complete distance + plotting pipeline
    """
    print(f"Processing {prefix}...")

    # Step 1: Compute flow distances
    df_pairs, total_flow, total_weighted_distance = compute_flow_distances_from_centroids(
        centroids_path, flow_path, output_dir, prefix
    )

    # Step 2: Add distance travelled metrics and aggregates
    df_pairs = add_distance_travelled_metric(df_pairs, output_dir, prefix)

    # Step 3: Create summary report
    summary_file = create_summary_report(total_flow, total_weighted_distance, output_dir, prefix)

    # Step 4: Plot flow lines
    plot_file = plot_flow_lines(centroids_path, df_pairs, output_dir, prefix)

    # Print results
    print(f"Saved files to {output_dir}")
    print(f"Total flow: {total_flow:,.2f}")
    print(f"Total weighted distance: {total_weighted_distance:,.2f}")
    print(f"Top 10 process pairs by flow × distance:")
    top10 = df_pairs.sort_values('flow_x_distance', ascending=False).head(10)
    print(top10[['from', 'to', 'flow', 'distance_ft', 'flow_x_distance']].to_string(index=False))

    return {
        'pairwise_file': output_dir / f'{prefix}_Flow_Distances.csv',
        'pairwise_with_dist_file': output_dir / f'{prefix}_Flow_Distances_With_Distance_Travelled.csv',
        'agg_from_file': output_dir / f'{prefix}_Distance_By_From_Process.csv',
        'agg_to_file': output_dir / f'{prefix}_Distance_By_To_Process.csv',
        'summary_file': summary_file,
        'plot_file': plot_file
    }

def main():
    """
    Main function to process both Y1F4 and Y5F4 layouts
    """
    BASE = Path(__file__).parent.parent.parent.parent

    # Y1F4 configuration
    centroids_y1f4 = BASE / 'results' / 'Task3' / 'Fractal' / 'Fractal_Distance' / 'Distance_Layout_Flow_Y1_F4_Block_Centroids.csv'
    flow_path = BASE / 'results' / 'Task3' / 'Fractal' / 'Fractal_Flowmatrix' / 'f4_centers' / 'Single_Center_Flow_Matrix.csv'
    output_dir_y1f4 = BASE / 'results' / 'Task3' / 'Fractal' / 'Fractal_Distance'
    prefix_y1f4 = 'Distance_Layout_Flow_Y1_F4'

    # Y5F4 configuration
    centroids_y5f4 = BASE / 'results' / 'task4' / 'Fractal' / 'Fractal_Distance' / 'Distance_Layout_Flow_Y5_F4_Block_Centroids.csv'
    output_dir_y5f4 = BASE / 'results' / 'task4' / 'Fractal' / 'Fractal_Distance'
    prefix_y5f4 = 'Distance_Layout_Flow_Y5_F4'

    print("=" * 80)
    print("FRACTAL DISTANCE METRICS - CONSOLIDATED PIPELINE")
    print("=" * 80)

    # Process Y1F4
    if centroids_y1f4.exists():
        print(f"\nProcessing Y1F4 layout...")
        run_distance_pipeline(centroids_y1f4, flow_path, output_dir_y1f4, prefix_y1f4)
    else:
        print(f"Y1F4 centroids file not found: {centroids_y1f4}")

    # Process Y5F4
    if centroids_y5f4.exists():
        print(f"\nProcessing Y5F4 layout...")
        run_distance_pipeline(centroids_y5f4, flow_path, output_dir_y5f4, prefix_y5f4)
    else:
        print(f"Y5F4 centroids file not found: {centroids_y5f4}")

    print("\n" + "=" * 80)
    print("FRACTAL DISTANCE METRICS PIPELINE COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    main()