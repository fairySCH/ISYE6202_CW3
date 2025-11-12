"""
Generate Equipment Summary Table as Image
Similar to the user's provided table format
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np

# Data - Updated with actual layout dimensions (Width x Height)
data = [
    ["B1", "14", "36", "1", "ABCD", "196", "7056", "50", "110", "9×4"],
    ["A", "14", "8", "1", "ABCD", "196", "1568", "14", "110", "8×1"],
    ["B2", "14", "36", "1", "ABCD", "196", "7056", "50", "110", "9×4"],
    ["C", "14", "4", "1", "ABCD", "196", "784", "14", "50", "4×1"],
    ["D", "14", "18", "1", "ABCD", "196", "3528", "26", "110", "9×2"],
    ["I", "9", "9", "1", "HIJ", "504", "4536", "42", "108", "3×3"],
    ["J", "8", "18", "1", "HIJ", "504", "9072", "84", "108", "3×6"],
]

headers = [
    "Process",
    "Equipment\n_per_Center",
    "Total_Equi\npment",
    "Utilization_per_\nCenter",
    "",
    "Area per\neqp ft2",
    "Total area of each\neqp centre ft2",
    "L",
    "W",
    "Config"
]

# Color coding based on total area (similar to user's image)
def get_color(process, area):
    area_val = int(area)
    if process in ["B1", "B2"]:
        return '#90EE90'  # Light green
    elif process == "J":
        return '#90EE90'  # Light green
    elif process in ["A", "C"]:
        return '#FFB6C1'  # Light red/pink
    elif process == "D":
        return '#FFD580'  # Light orange
    elif process == "I":
        return '#FFFFE0'  # Light yellow
    return 'white'

def get_equip_color(equip):
    if equip == "14":
        return '#90EE90'  # Green
    elif equip == "9":
        return '#FFB6C1'  # Red/pink
    elif equip == "8":
        return '#FFB6C1'  # Red/pink
    return 'white'

# Create figure
fig, ax = plt.subplots(figsize=(14, 6))
ax.axis('off')

# Table dimensions
n_rows = len(data) + 2  # +1 for header, +1 for total
n_cols = len(headers)
cell_height = 0.12
cell_widths = [0.08, 0.12, 0.10, 0.14, 0.08, 0.10, 0.14, 0.06, 0.08, 0.08]

# Draw header
y_pos = 0.95
for col, (header, width) in enumerate(zip(headers, cell_widths)):
    x_pos = sum(cell_widths[:col])
    
    # Header cell
    rect = Rectangle((x_pos, y_pos - cell_height), width, cell_height,
                     linewidth=1.5, edgecolor='black', facecolor='lightgray')
    ax.add_patch(rect)
    
    ax.text(x_pos + width/2, y_pos - cell_height/2, header,
           ha='center', va='center', fontsize=9, fontweight='bold')

# Draw data rows
y_pos -= cell_height
for row_idx, row_data in enumerate(data):
    for col_idx, (cell, width) in enumerate(zip(row_data, cell_widths)):
        x_pos = sum(cell_widths[:col_idx])
        
        # Determine cell color
        if col_idx == 1:  # Equipment_per_Center
            color = get_equip_color(cell)
        elif col_idx == 6:  # Total area
            color = get_color(row_data[0], cell)
        else:
            color = 'white'
        
        # Draw cell
        rect = Rectangle((x_pos, y_pos - cell_height), width, cell_height,
                        linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        
        # Add text
        ax.text(x_pos + width/2, y_pos - cell_height/2, cell,
               ha='center', va='center', fontsize=10)
    
    y_pos -= cell_height

# Draw total row
y_pos -= cell_height * 0.3  # Small gap
x_pos = 0
total_width = sum(cell_widths[:2])
rect = Rectangle((x_pos, y_pos - cell_height), total_width, cell_height,
                linewidth=1.5, edgecolor='black', facecolor='white')
ax.add_patch(rect)
ax.text(x_pos + total_width/2, y_pos - cell_height/2, "Total Machines",
       ha='center', va='center', fontsize=10, fontweight='bold')

x_pos = sum(cell_widths[:2])
width = cell_widths[2]
rect = Rectangle((x_pos, y_pos - cell_height), width, cell_height,
                linewidth=1.5, edgecolor='black', facecolor='lightgreen')
ax.add_patch(rect)
ax.text(x_pos + width/2, y_pos - cell_height/2, "129",
       ha='center', va='center', fontsize=11, fontweight='bold')

# Add empty box next to total
x_pos = sum(cell_widths[:3])
width = cell_widths[3]
rect = Rectangle((x_pos, y_pos - cell_height), width, cell_height,
                linewidth=1.5, edgecolor='black', facecolor='lightcyan')
ax.add_patch(rect)

# Set axis limits
ax.set_xlim(0, sum(cell_widths))
ax.set_ylim(y_pos - cell_height - 0.05, 1.0)

plt.tight_layout()

# Save
from pathlib import Path
output_path = Path(__file__).parent / 'Equipment_Summary_Table.png'
fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Table image saved to: {output_path}")
plt.close()
