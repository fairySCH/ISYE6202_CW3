"""
Run distance + plotting pipeline for a given centroids file and flow matrix.
Saves outputs into specified output directory with given prefix.
"""
from pathlib import Path
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).parent.parent.parent.parent

# Parameters (editable)
centroids_path = BASE / 'results' / 'task3' / 'Fractal' / 'fractal_distance' / 'Distance_Layout_Flow_Y5_F4_Block_Centroids.csv'
flow_path = BASE / 'results' / 'Task3' / 'Fractal' / 'Fractal_Flowmatrix' / 'f4_centers' / 'Single_Center_Flow_Matrix.csv'
output_dir = BASE / 'results' / 'task3' / 'Fractal' / 'distance_Y5_F4'
output_dir.mkdir(parents=True, exist_ok=True)

prefix = 'Distance_Layout_Flow_Y5_F4'

# Load
cent = pd.read_csv(centroids_path)
flow = pd.read_csv(flow_path, index_col=0)

# Compute pairwise distances and flow_x_distance
rows = []
total_flow = 0.0
total_weighted_distance = 0.0

for from_proc in flow.index:
    for to_proc in flow.columns:
        flow_val = float(flow.at[from_proc, to_proc])
        # find centroids
        if str(from_proc) not in list(cent['process'].astype(str)) or str(to_proc) not in list(cent['process'].astype(str)):
            continue
        c_from = cent[cent['process'] == str(from_proc)].iloc[0]
        c_to = cent[cent['process'] == str(to_proc)].iloc[0]
        x1, y1 = float(c_from['centroid_x']), float(c_from['centroid_y'])
        x2, y2 = float(c_to['centroid_x']), float(c_to['centroid_y'])
        dist = math.hypot(x2 - x1, y2 - y1)
        flow_x_dist = flow_val * dist
        rows.append({
            'from': str(from_proc),
            'to': str(to_proc),
            'flow': flow_val,
            'distance_ft': round(dist,3),
            'flow_x_distance': round(flow_x_dist,3)
        })
        total_flow += flow_val
        total_weighted_distance += flow_x_dist

# Save pairwise
df_pairs = pd.DataFrame(rows)
df_pairs.sort_values(by='flow_x_distance', ascending=False, inplace=True)
pairwise_file = output_dir / f'{prefix}_Flow_Distances.csv'
df_pairs.to_csv(pairwise_file, index=False)

# Add distance_travelled metric
df_pairs['distance_travelled_ft'] = df_pairs['flow_x_distance']
df_pairs['distance_travelled_km'] = (df_pairs['distance_travelled_ft'] / 3.28084).round(3)
pairwise_with_dist_file = output_dir / f'{prefix}_Flow_Distances_With_Distance_Travelled.csv'
df_pairs.to_csv(pairwise_with_dist_file, index=False)

# Aggregates
agg_from = df_pairs.groupby('from').agg(total_flow=('flow','sum'), total_distance_travelled_ft=('distance_travelled_ft','sum')).reset_index()
agg_from['total_distance_travelled_km'] = (agg_from['total_distance_travelled_ft'] / 3.28084).round(3)
agg_to = df_pairs.groupby('to').agg(total_flow=('flow','sum'), total_distance_travelled_ft=('distance_travelled_ft','sum')).reset_index()
agg_to['total_distance_travelled_km'] = (agg_to['total_distance_travelled_ft'] / 3.28084).round(3)
agg_from.to_csv(output_dir / f'{prefix}_Distance_By_From_Process.csv', index=False)
agg_to.to_csv(output_dir / f'{prefix}_Distance_By_To_Process.csv', index=False)

# Summary
avg_distance_per_flow = total_weighted_distance / total_flow if total_flow != 0 else None
summary_file = output_dir / f'{prefix}_Distance_Summary.txt'
with open(summary_file, 'w') as f:
    f.write(f'Total flow: {total_flow:,.2f}\n')
    f.write(f'Total weighted distance (flow x ft): {total_weighted_distance:,.2f}\n')
    if avg_distance_per_flow is not None:
        f.write(f'Average distance per unit flow (ft per flow unit): {avg_distance_per_flow:.4f}\n')

# Plot flow lines
cent_map = {row['process']:(row['centroid_x'], row['centroid_y']) for _, row in cent.iterrows()}

# Keep only positive flows
df_plot = df_pairs[df_pairs['flow'] > 0].copy()

# Normalize linewidth
flows = df_plot['flow'].values
if len(flows) > 0:
    p1, p99 = np.percentile(flows, [1,99])
else:
    p1 = p99 = 0

def scale_width(v, lo=p1, hi=p99, minw=0.8, maxw=8.0):
    if lo == hi:
        return (minw + maxw)/2
    if v <= lo:
        return minw
    if v >= hi:
        return maxw
    return minw + (maxw-minw)*((v-lo)/(hi-lo))

fig, ax = plt.subplots(figsize=(10,8))
ax.set_facecolor('#0f0f0f')
for _, r in df_plot.iterrows():
    fproc = r['from']; tproc = r['to']
    x1,y1 = cent_map[fproc]; x2,y2 = cent_map[tproc]
    ft = r['flow']
    w = scale_width(ft)
    alpha = min(0.9, 0.2 + 0.8*(ft/flows.max())) if len(flows)>0 else 0.6
    ax.plot([x1,x2],[y1,y2], color='cyan', linewidth=w, alpha=alpha, solid_capstyle='round')

for _, row in cent.iterrows():
    p = row['process']
    x = row['centroid_x']; y = row['centroid_y']
    ax.scatter(x,y, s=200, color='white', edgecolor='k', zorder=5)
    ax.text(x, y, str(p), color='black', fontsize=12, fontweight='bold', ha='center', va='center', zorder=6)

ax.set_xlim(0, 240)
ax.set_ylim(0, 300)
ax.set_xlabel('X (ft)')
ax.set_ylabel('Y (ft)')
ax.set_title(f'{prefix} Flow Lines')
ax.set_aspect('equal')
ax.grid(True, color='#222222')
plt.tight_layout()
plot_file = output_dir / f'{prefix}_Flow_Lines.png'
plt.savefig(plot_file, dpi=300)
plt.close()

print('Saved files to', output_dir)
print('Top 10 process pairs by flow x distance:')
print(df_pairs[['from','to','flow','distance_ft','flow_x_distance']].sort_values('flow_x_distance', ascending=False).head(10).to_string(index=False))
print('Done')
