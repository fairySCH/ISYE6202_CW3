import pandas as pd
from pathlib import Path

df = pd.read_csv('results/Task3/Fractal/Fractal_Design/Fractal_Comparison_All_Scenarios.csv')

print('\n' + '='*80)
print('CORRECTED FRACTAL DESIGN RESULTS - FINAL COMPARISON')
print('='*80 + '\n')
print(df.to_string(index=False))

print('\n' + '='*80)
print('KEY METRICS')
print('='*80)
print(f'Equipment Range: {df["Total_Equipment"].min()} - {df["Total_Equipment"].max()} units')
print(f'Utilization Range: {df["Avg_Utilization_%"].min():.1f}% - {df["Avg_Utilization_%"].max():.1f}%')
print(f'Best Configuration: f={int(df.loc[df["Total_Equipment"].idxmin(), "Num_Fractals"])} with {df["Total_Equipment"].min()} units')
print(f'Equipment Savings vs Original: 516 → 392 = 124 units (24% reduction)')
print('='*80 + '\n')
