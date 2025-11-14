"""
Plot flow lines between handmade centroids.
Saves: results/task3/Fractal/fractal_distance/Handmade_210x195_Flow_Lines.png
Also prints top 10 pairs by flow_x_distance.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE = Path(__file__).parent.parent.parent.parent
in_dir = BASE / 'results' / 'task3' / 'Fractal' / 'fractal_distance'
centroids_file = in_dir / 'Handmade_210x195_Block_Centroids.csv'
pairwise_file = in_dir / 'Handmade_210x195_Flow_Distances_With_Distance_Travelled.csv'

out_file = in_dir / 'Handmade_210x195_Flow_Lines.png'

cent = pd.read_csv(centroids_file)
df = pd.read_csv(pairwise_file)

# Keep only positive flows
df_pos = df[df['flow'] > 0].copy()

# Merge centroid coordinates for from/to
cent_map = {row['process']:(row['centroid_x'], row['centroid_y']) for _, row in cent.iterrows()}

# Filter pairs where both centroids exist
valid_pairs = []
for _, r in df_pos.iterrows():
    f = str(r['from'])
    t = str(r['to'])
    if f in cent_map and t in cent_map:
        valid_pairs.append(r)

if len(valid_pairs) == 0:
    print('No valid flow pairs with centroids found.')
    raise SystemExit(0)

df_plot = pd.DataFrame(valid_pairs)

# Normalize linewidth by flow (map 1st-99th percentile to 0.8-8 px)
flows = df_plot['flow'].values
p1, p99 = np.percentile(flows, [1, 99])

def scale_width(v, lo=p1, hi=p99, minw=0.8, maxw=8.0):
    if v <= lo:
        return minw
    if v >= hi:
        return maxw
    return minw + (maxw-minw)*((v-lo)/(hi-lo))

# Prepare plot
fig, ax = plt.subplots(figsize=(10,8))
ax.set_facecolor('#0f0f0f')

# Plot lines
for _, r in df_plot.iterrows():
    f = str(r['from']); t = str(r['to'])
    x1,y1 = cent_map[f]
    x2,y2 = cent_map[t]
    dist = r['distance_ft']
    ft = r['flow']
    w = scale_width(ft)
    alpha = min(0.9, 0.2 + 0.8*(ft/flows.max()))

    ax.plot([x1,x2],[y1,y2], color='cyan', linewidth=w, alpha=alpha, solid_capstyle='round')

# Draw nodes and labels
for _, row in cent.iterrows():
    p = row['process']
    x = row['centroid_x']; y = row['centroid_y']
    ax.scatter(x,y, s=200, color='white', edgecolor='k', zorder=5)
    ax.text(x, y, str(p), color='black', fontsize=14, fontweight='bold',
            ha='center', va='center', zorder=6)

# Plot formatting
ax.set_xlim(0, 210)
ax.set_ylim(0, 195)
ax.set_xlabel('X (ft)')
ax.set_ylabel('Y (ft)')
ax.set_title('Handmade 210×195 Flow Lines (thicker = larger flow)')
ax.set_aspect('equal')
ax.grid(True, color='#222222')

plt.tight_layout()
plt.savefig(out_file, dpi=300)
plt.close()

# Print top 10 pairs by flow_x_distance
top10 = df_plot.sort_values('flow_x_distance', ascending=False).head(10)
print('\nTop 10 process pairs by flow × distance:')
print(top10[['from','to','flow','distance_ft','flow_x_distance']].to_string(index=False))
print(f"\nSaved flow lines image: {out_file}")
