"""
Part-Based Visualizations for Task 4 Only
Creates visualizations for Years 2-5
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import os
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

base_path = r"c:\Users\jatin\OneDrive\Desktop\Georgia Tech\Coursework\6202 Benoit\Case Work\Case Study 3\ISYE6202_CW3"

def create_visualizations(year_label, data_path, output_path):
    """Create visualizations for a specific year"""
    
    print(f"\n{'='*80}")
    print(f"{year_label} VISUALIZATIONS")
    print(f"{'='*80}")
    
    os.makedirs(output_path, exist_ok=True)
    
    # Read data
    layout_df = pd.read_csv(f"{data_path}\\Part_Based_{year_label}_All_Parts_Layout_Summary.csv")
    flow_df = pd.read_csv(f"{data_path}\\Part_Based_{year_label}_All_Parts_Flow_Analysis.csv")
    machine_df = pd.read_csv(f"{data_path}\\Part_Based_{year_label}_All_Parts_Machine_Usage.csv")
    
    # Standardize columns
    if 'Total_Area_sqft' in layout_df.columns:
        layout_df['Area'] = layout_df['Total_Area_sqft']
    elif 'Total_Area_sq_ft' in layout_df.columns:
        layout_df['Area'] = layout_df['Total_Area_sq_ft']
    
    if 'Total_Machines' in layout_df.columns:
        layout_df['Machines'] = layout_df['Total_Machines']
    elif 'Total_Machines_Per_Part' in layout_df.columns:
        layout_df['Machines'] = layout_df['Total_Machines_Per_Part']
    
    if 'Total_Weekly_Flow_ft' in flow_df.columns:
        flow_df['Flow'] = flow_df['Total_Weekly_Flow_ft']
    elif 'Total_Weekly_Flow_unit_ft' in flow_df.columns:
        flow_df['Flow'] = flow_df['Total_Weekly_Flow_unit_ft']
    
    print(f"Loaded {len(layout_df)} parts")
    
    # DASHBOARD 1: Overview
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    fig.suptitle(f'{year_label}: Part-Based Layout Analysis - All 20 Parts', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(layout_df)))
    
    # Area bar chart
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.bar(layout_df['Part'], layout_df['Area'], color=colors, edgecolor='black', linewidth=0.5)
    ax1.set_xlabel('Part Number', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Total Area (sq ft)', fontsize=12, fontweight='bold')
    ax1.set_title('Area Requirements by Part', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Summary box
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.axis('off')
    total_machines = layout_df['Machines'].sum()
    total_area = layout_df['Area'].sum()
    avg_area = layout_df['Area'].mean()
    
    summary = f"""
{year_label.upper()} SUMMARY

Parts: {len(layout_df)}
Machines: {total_machines:,}
Total Area: {total_area:,.0f} sq ft
Avg Area: {avg_area:,.0f} sq ft

Largest: {layout_df.loc[layout_df['Area'].idxmax(), 'Part']}
  ({layout_df['Area'].max():,.0f} sq ft)
  
Smallest: {layout_df.loc[layout_df['Area'].idxmin(), 'Part']}
  ({layout_df['Area'].min():,.0f} sq ft)
"""
    ax2.text(0.1, 0.5, summary, fontsize=10, family='monospace',
             verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Machine count
    ax3 = fig.add_subplot(gs[1, :2])
    ax3.bar(layout_df['Part'], layout_df['Machines'], color=colors, edgecolor='black', linewidth=0.5)
    ax3.set_xlabel('Part Number', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Number of Machines', fontsize=12, fontweight='bold')
    ax3.set_title('Machine Requirements by Part', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # Flow scatter
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.scatter(range(len(flow_df)), flow_df['Distance_Per_Unit_ft'], 
               c=colors, s=200, edgecolors='black', linewidth=1.5, alpha=0.7)
    ax4.set_xlabel('Part Index', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Distance per Unit (ft)', fontsize=12, fontweight='bold')
    ax4.set_title('Flow Distance per Part', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    avg_dist = flow_df['Distance_Per_Unit_ft'].mean()
    ax4.axhline(y=avg_dist, color='red', linestyle='--', linewidth=2, label=f'Avg: {avg_dist:.1f} ft')
    ax4.legend()
    
    # Process heatmap
    ax5 = fig.add_subplot(gs[2, :])
    process_cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    process_data = machine_df[[col for col in process_cols if col in machine_df.columns]].fillna(0)
    
    im = ax5.imshow(process_data.T, aspect='auto', cmap='YlOrRd', interpolation='nearest')
    ax5.set_xlabel('Part Number', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Process Type', fontsize=12, fontweight='bold')
    ax5.set_title('Machine Distribution Heatmap', fontsize=14, fontweight='bold')
    ax5.set_xticks(range(len(machine_df)))
    ax5.set_xticklabels(machine_df['Part'], rotation=45)
    ax5.set_yticks(range(len(process_data.columns)))
    ax5.set_yticklabels(process_data.columns)
    
    cbar = plt.colorbar(im, ax=ax5, orientation='horizontal', pad=0.1, aspect=30)
    cbar.set_label('Machines', fontsize=10, fontweight='bold')
    
    for i in range(len(process_data.columns)):
        for j in range(len(machine_df)):
            value = process_data.iloc[j, i]
            if value > 0:
                ax5.text(j, i, f'{int(value)}',
                        ha="center", va="center", color="black", fontsize=7, fontweight='bold')
    
    plt.savefig(f"{output_path}\\{year_label}_Dashboard.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {year_label}_Dashboard.png")
    plt.close()
    
    # DASHBOARD 2: Top 10
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'{year_label}: Top 10 Parts Analysis', fontsize=18, fontweight='bold')
    
    top10_area = layout_df.nlargest(10, 'Area')
    ax = axes[0, 0]
    ax.barh(top10_area['Part'], top10_area['Area'], 
           color=plt.cm.Reds(np.linspace(0.4, 0.9, 10)), edgecolor='black')
    ax.set_xlabel('Area (sq ft)', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 by Area', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    for i, (idx, row) in enumerate(top10_area.iterrows()):
        ax.text(row['Area'], i, f" {int(row['Area']):,}", va='center', fontsize=9, fontweight='bold')
    
    top10_machines = layout_df.nlargest(10, 'Machines')
    ax = axes[0, 1]
    ax.barh(top10_machines['Part'], top10_machines['Machines'],
           color=plt.cm.Blues(np.linspace(0.4, 0.9, 10)), edgecolor='black')
    ax.set_xlabel('Machines', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 by Machines', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    for i, (idx, row) in enumerate(top10_machines.iterrows()):
        ax.text(row['Machines'], i, f" {int(row['Machines'])}", va='center', fontsize=9, fontweight='bold')
    
    top10_flow = flow_df.nlargest(10, 'Flow')
    ax = axes[1, 0]
    ax.barh(top10_flow['Part'], top10_flow['Flow'],
           color=plt.cm.Greens(np.linspace(0.4, 0.9, 10)), edgecolor='black')
    ax.set_xlabel('Weekly Flow (ft)', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 by Flow', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    ax = axes[1, 1]
    ax.scatter(layout_df['Machines'], layout_df['Area'],
              c=range(len(layout_df)), cmap='viridis', 
              s=300, edgecolors='black', linewidth=1.5, alpha=0.7)
    ax.set_xlabel('Machines', fontsize=12, fontweight='bold')
    ax.set_ylabel('Area (sq ft)', fontsize=12, fontweight='bold')
    ax.set_title('Area vs Machines', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_path}\\{year_label}_Top10.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {year_label}_Top10.png")
    plt.close()
    
    # DASHBOARD 3: Layout Schematic
    fig, ax = plt.subplots(figsize=(18, 10))
    fig.suptitle(f'{year_label}: Layout Schematic - All 20 Parts', fontsize=18, fontweight='bold')
    
    n_cols, n_rows = 5, 4
    x_spacing, y_spacing = 1.5, 1.2
    
    for idx, row in layout_df.iterrows():
        col = idx % n_cols
        row_num = idx // n_cols
        x = col * x_spacing
        y = (n_rows - row_num - 1) * y_spacing
        
        area_norm = 0.2 + (row['Area'] - layout_df['Area'].min()) / \
                    (layout_df['Area'].max() - layout_df['Area'].min()) * 0.8
        
        rect = Rectangle((x - area_norm/2, y - area_norm/2), 
                         area_norm, area_norm,
                         facecolor=plt.cm.viridis(idx / len(layout_df)),
                         edgecolor='black', linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        
        ax.text(x, y, row['Part'], 
               ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        ax.text(x, y - area_norm/2 - 0.15, 
               f"{int(row['Area']):,} sq ft\n{int(row['Machines'])} machines",
               ha='center', va='top', fontsize=7)
    
    ax.set_xlim(-0.5, n_cols * x_spacing - 0.5)
    ax.set_ylim(-0.5, n_rows * y_spacing - 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    legend_text = f"""
Layout Key:
Size: Proportional to area
Color: Part sequence
Total: {total_area:,.0f} sq ft
Machines: {total_machines:,}
"""
    ax.text(0.02, 0.98, legend_text, transform=ax.transAxes,
           fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    plt.savefig(f"{output_path}\\{year_label}_Schematic.png", dpi=300, bbox_inches='tight')
    print(f"Saved: {year_label}_Schematic.png")
    plt.close()
    
    print(f"{year_label} complete!")
    return total_machines, total_area

# MAIN
print("="*80)
print("TASK 4 PART-BASED VISUALIZATIONS (Years 2-5)")
print("="*80)

task4_base = f"{base_path}\\results\\task4\\part"
metrics = []

for year in [2, 3, 4, 5]:
    print(f"\nYEAR {year}")
    year_label = f"Year{year}"
    data_path = f"{task4_base}\\{year_label}"
    m, a = create_visualizations(year_label, data_path, data_path)
    metrics.append((year, m, a))

# Multi-year comparison
print("\nMULTI-YEAR COMPARISON")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Multi-Year Capacity Growth (Years 2-5)', fontsize=18, fontweight='bold')

years = [y[0] for y in metrics]
machines = [y[1] for y in metrics]
areas = [y[2] for y in metrics]

ax = axes[0]
ax.bar(years, machines, color=plt.cm.Blues(np.linspace(0.4, 0.9, len(years))),
      edgecolor='black', linewidth=2, width=0.6)
ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Total Machines', fontsize=14, fontweight='bold')
ax.set_title('Machine Growth', fontsize=16, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
ax.set_xticks(years)
for i, (y, m) in enumerate(zip(years, machines)):
    ax.text(y, m, f'{int(m):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax = axes[1]
ax.bar(years, areas, color=plt.cm.Greens(np.linspace(0.4, 0.9, len(years))),
      edgecolor='black', linewidth=2, width=0.6)
ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Total Area (sq ft)', fontsize=14, fontweight='bold')
ax.set_title('Area Growth', fontsize=16, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
ax.set_xticks(years)
for i, (y, a) in enumerate(zip(years, areas)):
    ax.text(y, a, f'{int(a):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(f"{task4_base}\\MultiYear_Comparison.png", dpi=300, bbox_inches='tight')
print(f"Saved: MultiYear_Comparison.png")
plt.close()

print("\n" + "="*80)
print("TASK 4 VISUALIZATIONS COMPLETE!")
print("="*80)
print(f"\nOutput: {task4_base}\\Year[N]\\")
print("\nTotal: 13 files (3 per year x 4 years + 1 comparison)")
print("="*80)
