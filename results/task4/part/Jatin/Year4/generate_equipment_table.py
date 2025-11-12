"""
Generate Equipment Summary Table for Year 4 Part 1
Similar format to Year 5
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Equipment data for Year 4 Part 1
equipment_data = [
    {
        'Process': 'B1',
        'Equipment_per_Center': 1,
        'Total_Equipment': 15,
        'Utilization': 99.0,
        'Group': 'ABCD',
        'Area_per_eqp': 196,
        'Total_area': 2940,
        'L': 38,
        'W': 62,
        'Config': '5×3'
    },
    {
        'Process': 'A',
        'Equipment_per_Center': 1,
        'Total_Equipment': 6,
        'Utilization': 99.0,
        'Group': 'ABCD',
        'Area_per_eqp': 196,
        'Total_area': 1176,
        'L': 14,
        'W': 74,
        'Config': '6×1'
    },
    {
        'Process': 'B2',
        'Equipment_per_Center': 1,
        'Total_Equipment': 15,
        'Utilization': 99.0,
        'Group': 'ABCD',
        'Area_per_eqp': 196,
        'Total_area': 2940,
        'L': 38,
        'W': 62,
        'Config': '5×3'
    },
    {
        'Process': 'C',
        'Equipment_per_Center': 1,
        'Total_Equipment': 3,
        'Utilization': 99.0,
        'Group': 'ABCD',
        'Area_per_eqp': 196,
        'Total_area': 588,
        'L': 14,
        'W': 38,
        'Config': '3×1'
    },
    {
        'Process': 'D',
        'Equipment_per_Center': 1,
        'Total_Equipment': 15,
        'Utilization': 99.0,
        'Group': 'ABCD',
        'Area_per_eqp': 196,
        'Total_area': 2940,
        'L': 38,
        'W': 62,
        'Config': '5×3'
    },
    {
        'Process': 'I',
        'Equipment_per_Center': 1,
        'Total_Equipment': 8,
        'Utilization': 92.8,
        'Group': 'HIJ',
        'Area_per_eqp': 504,
        'Total_area': 4032,
        'L': 56,
        'W': 72,
        'Config': '2×4'
    },
    {
        'Process': 'J',
        'Equipment_per_Center': 1,
        'Total_Equipment': 15,
        'Utilization': 99.0,
        'Group': 'HIJ',
        'Area_per_eqp': 504,
        'Total_area': 7560,
        'L': 70,
        'W': 108,
        'Config': '3×5'
    },
]

def create_equipment_table():
    """Create formatted table as image"""
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('off')
    
    # Headers
    headers = ['Process', 'Equipment\nper Center', 'Total\nEquipment', 
               'Utilization\n(%)', 'Group', 'Area per\nEquip (ft²)', 
               'Total\nArea (ft²)', 'L\n(ft)', 'W\n(ft)', 'Config']
    
    # Prepare data rows
    data_rows = []
    for row in equipment_data:
        data_rows.append([
            row['Process'],
            row['Equipment_per_Center'],
            row['Total_Equipment'],
            f"{row['Utilization']:.1f}",
            row['Group'],
            row['Area_per_eqp'],
            f"{row['Total_area']:,}",
            row['L'],
            row['W'],
            row['Config']
        ])
    
    # Color code by utilization
    def get_row_color(util):
        if util >= 95:
            return '#d4edda'  # Green
        elif util >= 85:
            return '#fff3cd'  # Yellow
        else:
            return '#f8d7da'  # Red
    
    row_colors = [get_row_color(row['Utilization']) for row in equipment_data]
    
    # Create table
    table = ax.table(cellText=data_rows,
                     colLabels=headers,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.08, 0.12, 0.1, 0.1, 0.08, 0.12, 0.12, 0.07, 0.07, 0.08])
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    # Style header
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor('#34495e')
        cell.set_text_props(weight='bold', color='white')
    
    # Style data rows with color coding
    for i in range(len(data_rows)):
        for j in range(len(headers)):
            cell = table[(i+1, j)]
            cell.set_facecolor(row_colors[i])
            cell.set_edgecolor('#bdc3c7')
    
    plt.title('Year 4 Part 1 - Equipment Summary Table\n77 Total Machines', 
             fontsize=14, fontweight='bold', pad=20)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(color='#d4edda', label='High Utilization (≥95%)'),
        mpatches.Patch(color='#fff3cd', label='Medium Utilization (85-95%)'),
        mpatches.Patch(color='#f8d7da', label='Low Utilization (<85%)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, -0.05), 
             ncol=3, frameon=False)
    
    # Save
    output_path = Path(__file__).parent / 'Equipment_Summary_Table.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Equipment table saved to: {output_path}")
    
    # Also save as CSV
    csv_path = Path(__file__).parent / 'Equipment_Summary_Table.csv'
    with open(csv_path, 'w') as f:
        f.write(','.join(headers) + '\n')
        for row in data_rows:
            f.write(','.join(str(x) for x in row) + '\n')
    
    print(f"CSV data saved to: {csv_path}")
    
    # Print summary
    total_equipment = sum(row['Total_Equipment'] for row in equipment_data)
    total_area = sum(row['Total_area'] for row in equipment_data)
    
    print(f"\nSummary:")
    print(f"  Total Equipment: {total_equipment}")
    print(f"  Total Area: {total_area:,} ft²")
    print(f"  Average Utilization: {sum(row['Utilization'] for row in equipment_data) / len(equipment_data):.1f}%")

if __name__ == '__main__':
    create_equipment_table()
