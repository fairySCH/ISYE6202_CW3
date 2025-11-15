"""
Task 3 Part-Based Analysis - Comprehensive Visualizations
Creates visual dashboards for Year 1 part-based layout analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import os

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Base path
base_path = r"c:\Users\jatin\OneDrive\Desktop\Georgia Tech\Coursework\6202 Benoit\Case Work\Case Study 3\ISYE6202_CW3"
results_path = f"{base_path}\\results\\Task3\\Part\\Capacity"
output_path = f"{base_path}\\results\\Task3\\Part\\Visuals"

# Create output directory
os.makedirs(output_path, exist_ok=True)

# Read data files
layout_df = pd.read_csv(f"{results_path}\\Part_Based_All_Parts_Layout_Summary.csv")
flow_df = pd.read_csv(f"{results_path}\\Part_Based_All_Parts_Flow_Analysis.csv")
machine_df = pd.read_csv(f"{results_path}\\Part_Based_All_Parts_Machine_Usage.csv")

print("="*80)
print("TASK 3 PART-BASED VISUALIZATIONS - YEAR 1")
print("="*80)

# ============================================================================
# VISUALIZATION 1: COMPREHENSIVE DASHBOARD
# ============================================================================
print("\n1. Creating comprehensive dashboard...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Title
fig.suptitle('Task 3: Part-Based Layout Analysis - Year 1 (All 20 Parts)', 
             fontsize=20, fontweight='bold', y=0.98)

# 1. Area Requirements by Part
ax1 = fig.add_subplot(gs[0, :2])
parts = layout_df['Part']
areas = layout_df['Total_Area_sq_ft']
colors = plt.cm.viridis(np.linspace(0, 1, len(parts)))

bars1 = ax1.bar(parts, areas, color=colors, edgecolor='black', linewidth=0.5)
ax1.set_xlabel('Part Number', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Area (sq ft)', fontsize=12, fontweight='bold')
ax1.set_title('Area Requirements by Part', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontsize=8)

# 2. Summary Statistics Box
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
total_machines = layout_df['Total_Machines_Per_Part'].sum()
total_area = layout_df['Total_Area_sq_ft'].sum()
avg_area = layout_df['Total_Area_sq_ft'].mean()
total_flow = flow_df['Total_Weekly_Flow_ft'].sum()

summary_text = f"""
YEAR 1 SUMMARY METRICS

Total Parts: {len(layout_df)}

Total Machines: {total_machines:,}

Total Area: {total_area:,.0f} sq ft

Average Area/Part: {avg_area:,.0f} sq ft

Total Weekly Flow: {total_flow:,.0f} ft

Max Area Part: {layout_df.loc[layout_df['Total_Area_sq_ft'].idxmax(), 'Part']}
({layout_df['Total_Area_sq_ft'].max():,.0f} sq ft)

Min Area Part: {layout_df.loc[layout_df['Total_Area_sq_ft'].idxmin(), 'Part']}
({layout_df['Total_Area_sq_ft'].min():,.0f} sq ft)
"""

ax2.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
         verticalalignment='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 3. Machine Count by Part
ax3 = fig.add_subplot(gs[1, :2])
machine_counts = layout_df['Total_Machines_Per_Part']
bars2 = ax3.bar(parts, machine_counts, color=colors, edgecolor='black', linewidth=0.5)
ax3.set_xlabel('Part Number', fontsize=12, fontweight='bold')
ax3.set_ylabel('Number of Machines', fontsize=12, fontweight='bold')
ax3.set_title('Machine Requirements by Part', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
ax3.tick_params(axis='x', rotation=45)

# Add value labels
for bar in bars2:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=8)

# 4. Flow Distance Analysis
ax4 = fig.add_subplot(gs[1, 2])
flow_distances = flow_df['Distance_Per_Unit_ft']
ax4.scatter(range(len(flow_distances)), flow_distances, 
           c=colors, s=200, edgecolors='black', linewidth=1.5, alpha=0.7)
ax4.set_xlabel('Part Index', fontsize=12, fontweight='bold')
ax4.set_ylabel('Distance per Unit (ft)', fontsize=12, fontweight='bold')
ax4.set_title('Flow Distance per Part', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)

# Add average line
avg_distance = flow_distances.mean()
ax4.axhline(y=avg_distance, color='red', linestyle='--', linewidth=2, label=f'Average: {avg_distance:.1f} ft')
ax4.legend()

# 5. Process Distribution Heatmap
ax5 = fig.add_subplot(gs[2, :])
process_cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
process_data = machine_df[process_cols].fillna(0)

# Create heatmap
im = ax5.imshow(process_data.T, aspect='auto', cmap='YlOrRd', interpolation='nearest')
ax5.set_xlabel('Part Number', fontsize=12, fontweight='bold')
ax5.set_ylabel('Process Type', fontsize=12, fontweight='bold')
ax5.set_title('Machine Distribution by Process and Part (Heatmap)', fontsize=14, fontweight='bold')
ax5.set_xticks(range(len(machine_df)))
ax5.set_xticklabels(machine_df['Part'], rotation=45)
ax5.set_yticks(range(len(process_cols)))
ax5.set_yticklabels(process_cols)

# Add colorbar
cbar = plt.colorbar(im, ax=ax5, orientation='horizontal', pad=0.1, aspect=30)
cbar.set_label('Number of Machines', fontsize=10, fontweight='bold')

# Add text annotations for non-zero values
for i in range(len(process_cols)):
    for j in range(len(machine_df)):
        value = process_data.iloc[j, i]
        if value > 0:
            text = ax5.text(j, i, f'{int(value)}',
                           ha="center", va="center", color="black", fontsize=7, fontweight='bold')

plt.savefig(f"{output_path}\\Task3_Part_Based_Comprehensive_Dashboard.png", 
            dpi=300, bbox_inches='tight')
print(f"✓ Saved: Task3_Part_Based_Comprehensive_Dashboard.png")

# ============================================================================
# VISUALIZATION 2: TOP 10 PARTS ANALYSIS
# ============================================================================
print("\n2. Creating top 10 parts analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Task 3: Top 10 Parts Analysis - Year 1', fontsize=18, fontweight='bold')

# Sort by area
top10_area = layout_df.nlargest(10, 'Total_Area_sq_ft')

# Top 10 by Area
ax = axes[0, 0]
bars = ax.barh(top10_area['Part'], top10_area['Total_Area_sq_ft'], 
               color=plt.cm.Reds(np.linspace(0.4, 0.9, 10)), edgecolor='black')
ax.set_xlabel('Total Area (sq ft)', fontsize=12, fontweight='bold')
ax.set_ylabel('Part Number', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Parts by Area', fontsize=14, fontweight='bold')
ax.invert_yaxis()
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'{int(width):,}', ha='left', va='center', fontsize=10, fontweight='bold')

# Top 10 by Machine Count
top10_machines = layout_df.nlargest(10, 'Total_Machines_Per_Part')
ax = axes[0, 1]
bars = ax.barh(top10_machines['Part'], top10_machines['Total_Machines_Per_Part'],
               color=plt.cm.Blues(np.linspace(0.4, 0.9, 10)), edgecolor='black')
ax.set_xlabel('Number of Machines', fontsize=12, fontweight='bold')
ax.set_ylabel('Part Number', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Parts by Machine Count', fontsize=14, fontweight='bold')
ax.invert_yaxis()
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'{int(width)}', ha='left', va='center', fontsize=10, fontweight='bold')

# Top 10 by Flow Distance
top10_flow = flow_df.nlargest(10, 'Total_Weekly_Flow_ft')
ax = axes[1, 0]
bars = ax.barh(top10_flow['Part'], top10_flow['Total_Weekly_Flow_ft'],
               color=plt.cm.Greens(np.linspace(0.4, 0.9, 10)), edgecolor='black')
ax.set_xlabel('Total Weekly Flow (ft)', fontsize=12, fontweight='bold')
ax.set_ylabel('Part Number', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Parts by Weekly Flow', fontsize=14, fontweight='bold')
ax.invert_yaxis()
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'{int(width):,}', ha='left', va='center', fontsize=9, fontweight='bold')

# Area vs Machine Count Scatter
ax = axes[1, 1]
scatter = ax.scatter(layout_df['Total_Machines_Per_Part'], 
                    layout_df['Total_Area_sq_ft'],
                    c=range(len(layout_df)), cmap='viridis', 
                    s=300, edgecolors='black', linewidth=1.5, alpha=0.7)
ax.set_xlabel('Total Machines', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Area (sq ft)', fontsize=12, fontweight='bold')
ax.set_title('Area vs Machine Count Correlation', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# Add part labels
for idx, row in layout_df.iterrows():
    ax.annotate(row['Part'], 
               (row['Total_Machines_Per_Part'], row['Total_Area_sq_ft']),
               fontsize=8, ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f"{output_path}\\Task3_Part_Based_Top10_Analysis.png", 
            dpi=300, bbox_inches='tight')
print(f"✓ Saved: Task3_Part_Based_Top10_Analysis.png")

# ============================================================================
# VISUALIZATION 3: PROCESS-SPECIFIC ANALYSIS
# ============================================================================
print("\n3. Creating process-specific analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Task 3: Process-Specific Machine Distribution - Year 1', 
             fontsize=18, fontweight='bold')

# Total machines by process type
ax = axes[0, 0]
process_totals = machine_df[process_cols].sum().sort_values(ascending=False)
bars = ax.bar(process_totals.index, process_totals.values,
              color=plt.cm.Set3(np.linspace(0, 1, len(process_totals))),
              edgecolor='black', linewidth=1.5)
ax.set_xlabel('Process Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Machines', fontsize=12, fontweight='bold')
ax.set_title('Total Machine Count by Process Type', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Process diversity (number of different processes per part)
ax = axes[0, 1]
process_diversity = (machine_df[process_cols] > 0).sum(axis=1)
merged_diversity = pd.merge(layout_df[['Part']], 
                            pd.DataFrame({'Part': machine_df['Part'], 'Diversity': process_diversity}),
                            on='Part')
bars = ax.bar(merged_diversity['Part'], merged_diversity['Diversity'],
              color=plt.cm.plasma(np.linspace(0, 1, len(merged_diversity))),
              edgecolor='black', linewidth=1)
ax.set_xlabel('Part Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Different Processes', fontsize=12, fontweight='bold')
ax.set_title('Process Diversity by Part', fontsize=14, fontweight='bold')
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', alpha=0.3)

# Most common processes (parts using each process)
ax = axes[1, 0]
parts_per_process = (machine_df[process_cols] > 0).sum().sort_values(ascending=False)
bars = ax.barh(parts_per_process.index, parts_per_process.values,
               color=plt.cm.coolwarm(np.linspace(0, 1, len(parts_per_process))),
               edgecolor='black', linewidth=1.5)
ax.set_xlabel('Number of Parts Using Process', fontsize=12, fontweight='bold')
ax.set_ylabel('Process Type', fontsize=12, fontweight='bold')
ax.set_title('Process Utilization Across Parts', fontsize=14, fontweight='bold')
ax.invert_yaxis()
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2.,
            f'{int(width)}', ha='left', va='center', fontsize=10, fontweight='bold')

# Average machines per process (when used)
ax = axes[1, 1]
avg_machines = []
for col in process_cols:
    non_zero = machine_df[machine_df[col] > 0][col]
    avg_machines.append(non_zero.mean() if len(non_zero) > 0 else 0)

avg_df = pd.DataFrame({'Process': process_cols, 'Avg_Machines': avg_machines}).sort_values('Avg_Machines', ascending=False)
bars = ax.bar(avg_df['Process'], avg_df['Avg_Machines'],
              color=plt.cm.viridis(np.linspace(0, 1, len(avg_df))),
              edgecolor='black', linewidth=1.5)
ax.set_xlabel('Process Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Machines (when used)', fontsize=12, fontweight='bold')
ax.set_title('Average Machine Count per Process', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    if height > 0:
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(f"{output_path}\\Task3_Part_Based_Process_Analysis.png", 
            dpi=300, bbox_inches='tight')
print(f"✓ Saved: Task3_Part_Based_Process_Analysis.png")

# ============================================================================
# VISUALIZATION 4: LAYOUT SCHEMATIC (Conceptual)
# ============================================================================
print("\n4. Creating layout schematic...")

fig, ax = plt.subplots(figsize=(18, 10))
fig.suptitle('Task 3: Conceptual Layout Schematic - All 20 Parts (Year 1)', 
             fontsize=18, fontweight='bold')

# Arrange parts in grid layout
n_cols = 5
n_rows = int(np.ceil(len(layout_df) / n_cols))

x_spacing = 1.5
y_spacing = 1.2

for idx, row in layout_df.iterrows():
    col = idx % n_cols
    row_num = idx // n_cols
    
    x = col * x_spacing
    y = (n_rows - row_num - 1) * y_spacing
    
    # Normalize area for visualization (0.2 to 1.0)
    area_normalized = 0.2 + (row['Total_Area_sq_ft'] - layout_df['Total_Area_sq_ft'].min()) / \
                      (layout_df['Total_Area_sq_ft'].max() - layout_df['Total_Area_sq_ft'].min()) * 0.8
    
    # Draw rectangle
    rect = Rectangle((x - area_normalized/2, y - area_normalized/2), 
                     area_normalized, area_normalized,
                     facecolor=plt.cm.viridis(idx / len(layout_df)),
                     edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(rect)
    
    # Add part label
    ax.text(x, y, row['Part'], 
           ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    
    # Add area below
    ax.text(x, y - area_normalized/2 - 0.15, 
           f"{int(row['Total_Area_sq_ft']):,} sq ft\n{int(row['Total_Machines_Per_Part'])} machines",
           ha='center', va='top', fontsize=8)

ax.set_xlim(-0.5, n_cols * x_spacing - 0.5)
ax.set_ylim(-0.5, n_rows * y_spacing - 0.5)
ax.set_aspect('equal')
ax.axis('off')

# Add legend
legend_text = f"""
Layout Key:
• Size: Proportional to area
• Color: Part sequence
• Total Area: {total_area:,.0f} sq ft
• Total Machines: {total_machines:,}
• Layout: Compact grid arrangement
"""
ax.text(0.02, 0.98, legend_text, transform=ax.transAxes,
       fontsize=11, verticalalignment='top',
       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

plt.savefig(f"{output_path}\\Task3_Part_Based_Layout_Schematic.png", 
            dpi=300, bbox_inches='tight')
print(f"✓ Saved: Task3_Part_Based_Layout_Schematic.png")

plt.close('all')

print("\n" + "="*80)
print("TASK 3 VISUALIZATIONS COMPLETE!")
print("="*80)
print(f"\nFiles created in: {output_path}")
print("\n✓ Task3_Part_Based_Comprehensive_Dashboard.png")
print("✓ Task3_Part_Based_Top10_Analysis.png")
print("✓ Task3_Part_Based_Process_Analysis.png")
print("✓ Task3_Part_Based_Layout_Schematic.png")
print("\n" + "="*80)
