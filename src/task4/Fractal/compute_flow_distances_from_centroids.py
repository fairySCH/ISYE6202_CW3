"""
Compute pairwise Euclidean distances between handmade centroids and weighted flow distances
Saves: results/task4/Fractal/Fractal_Layout/Handmade_210x195_Flow_Distances.csv
"""
from pathlib import Path
import pandas as pd
import numpy as np
import math

BASE = Path(__file__).parent.parent.parent.parent
centroids_path = BASE / "results" / "task4" / "Fractal" / "Fractal_Layout" / "Handmade_210x195_Block_Centroids.csv"
flow_path = BASE / "results" / "Task3" / "Fractal" / "Fractal_Flowmatrix" / "f4_centers" / "Single_Center_Flow_Matrix.csv"

out_dir = BASE / "results" / "task4" / "Fractal" / "Fractal_Layout"
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "Handmade_210x195_Flow_Distances.csv"

# Load
cent = pd.read_csv(centroids_path)
flow = pd.read_csv(flow_path, index_col=0)

# Validate processes
processes_cent = list(cent['process'].astype(str))
processes_flow = list(flow.index.astype(str))

# Ensure same ordering or map by name
# We'll compute for all pairs present in the flow matrix and centroids
rows = []

total_flow = 0.0
total_weighted_distance = 0.0

for from_proc in flow.index:
    for to_proc in flow.columns:
        try:
            flow_val = float(flow.at[from_proc, to_proc])
        except Exception:
            # if indexing by label mismatches, try str
            flow_val = float(flow.loc[str(from_proc), str(to_proc)])

        if flow_val == 0:
            # still record zero flows for completeness
            # but we won't add to totals
            pass

        # find centroids; if missing, skip
        if str(from_proc) not in processes_cent or str(to_proc) not in processes_cent:
            # try uppercase
            f = str(from_proc)
            t = str(to_proc)
            if f not in processes_cent or t not in processes_cent:
                # skip pairs where centroid missing
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

# Save dataframe
df_out = pd.DataFrame(rows)
# Save sorted by flow_x_distance desc
df_out.sort_values(by='flow_x_distance', ascending=False, inplace=True)
df_out.to_csv(out_file, index=False)

# Compute average distance per unit flow
avg_distance_per_flow = total_weighted_distance / total_flow if total_flow != 0 else None

print("Saved:", out_file)
print(f"Total flow: {total_flow:,.2f}")
print(f"Total weighted distance (flow x ft): {total_weighted_distance:,.2f}")
if avg_distance_per_flow is not None:
    print(f"Average distance per unit flow (ft per flow unit): {avg_distance_per_flow:.4f}")
else:
    print("No flow present to compute average distance.")

# Also save a small summary file
summary_file = out_dir / "Handmade_210x195_Flow_Distances_Summary.txt"
with open(summary_file, 'w') as f:
    f.write(f"Total flow: {total_flow:,.2f}\n")
    f.write(f"Total weighted distance (flow x ft): {total_weighted_distance:,.2f}\n")
    if avg_distance_per_flow is not None:
        f.write(f"Average distance per unit flow (ft per flow unit): {avg_distance_per_flow:.4f}\n")

print("Summary saved:", summary_file)
