"""
Add 'distance_travelled' metric and aggregate totals.
Reads: Handmade_210x195_Flow_Distances.csv
Writes: Updated CSV + aggregates and summary
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent.parent.parent.parent
in_file = BASE / "results" / "task4" / "Fractal" / "Fractal_Layout" / "Handmade_210x195_Flow_Distances.csv"
out_dir = BASE / "results" / "task4" / "Fractal" / "Fractal_Layout"
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(in_file)

# Add distance_travelled_ft (same as flow_x_distance) and a km column
if 'flow_x_distance' in df.columns:
    df['distance_travelled_ft'] = df['flow_x_distance']
else:
    df['distance_travelled_ft'] = df['flow'] * df['distance_ft']

# Add kilometers for convenience
df['distance_travelled_km'] = (df['distance_travelled_ft'] / 3.28084).round(3)

# Save updated pairwise CSV
updated_file = out_dir / 'Handmade_210x195_Flow_Distances_With_Distance_Travelled.csv'
df.to_csv(updated_file, index=False)

# Aggregate totals by origin (from) and destination (to)
agg_from = df.groupby('from').agg(
    total_flow=('flow','sum'),
    total_distance_travelled_ft=('distance_travelled_ft','sum')
).reset_index()
agg_from['total_distance_travelled_km'] = (agg_from['total_distance_travelled_ft'] / 3.28084).round(3)

agg_to = df.groupby('to').agg(
    total_flow=('flow','sum'),
    total_distance_travelled_ft=('distance_travelled_ft','sum')
).reset_index()
agg_to['total_distance_travelled_km'] = (agg_to['total_distance_travelled_ft'] / 3.28084).round(3)

agg_from_file = out_dir / 'Handmade_210x195_Distance_By_From_Process.csv'
agg_to_file = out_dir / 'Handmade_210x195_Distance_By_To_Process.csv'
agg_from.to_csv(agg_from_file, index=False)
agg_to.to_csv(agg_to_file, index=False)

# Summary
summary_file = out_dir / 'Handmade_210x195_Distance_Summary.txt'
with open(summary_file, 'w') as f:
    total_flow = df['flow'].sum()
    total_distance_ft = df['distance_travelled_ft'].sum()
    avg_distance_per_flow = total_distance_ft / total_flow if total_flow != 0 else 0
    f.write(f"Total flow: {total_flow:,.2f}\n")
    f.write(f"Total distance travelled (ft): {total_distance_ft:,.2f}\n")
    f.write(f"Total distance travelled (km): {total_distance_ft/3.28084:,.2f}\n")
    f.write(f"Average distance per unit flow (ft): {avg_distance_per_flow:.4f}\n")

print("Saved:", updated_file)
print("Saved:", agg_from_file)
print("Saved:", agg_to_file)
print("Saved summary:", summary_file)
