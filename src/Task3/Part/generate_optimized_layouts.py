"""
Generate optimized compact layouts for all years using optimal grids
"""

import math
from pathlib import Path

def find_optimal_grid(machine_count):
    """Find most compact grid (rows × cols) for machine count"""
    if machine_count == 0:
        return 0, 0
    
    best_config = None
    best_score = float('inf')
    
    for rows in range(1, machine_count + 1):
        cols = math.ceil(machine_count / rows)
        total_slots = rows * cols
        waste = total_slots - machine_count
        aspect_ratio = max(rows, cols) / min(rows, cols)
        
        # Score: minimize waste first, then aspect ratio
        score = waste * 100 + aspect_ratio
        
        if best_config is None or score < best_score:
            best_config = (rows, cols)
            best_score = score
    
    return best_config

def calc_dimensions(rows, cols, unit_w, unit_h, overlap=0):
    """Calculate effective width and height with overlap"""
    if overlap > 0 and rows > 0 and cols > 0:
        eff_w = cols * unit_w - (cols - 1) * overlap
        eff_h = rows * unit_h - (rows - 1) * overlap
    else:
        eff_w = cols * unit_w if cols > 0 else 0
        eff_h = rows * unit_h if rows > 0 else 0
    return int(eff_w), int(eff_h)

# Machine counts for all years
YEARS = {
    "Year1": {"B1": 12, "A": 5, "B2": 12, "C": 3, "D": 12, "I": 6, "J": 12},
    "Year2": {"B1": 14, "A": 6, "B2": 14, "C": 3, "D": 14, "I": 7, "J": 14},
    "Year3": {"B1": 15, "A": 6, "B2": 15, "C": 3, "D": 15, "I": 8, "J": 15},
    "Year4": {"B1": 15, "A": 6, "B2": 15, "C": 3, "D": 15, "I": 8, "J": 15},
    "Year5": {"B1": 16, "A": 7, "B2": 16, "C": 4, "D": 16, "I": 8, "J": 16},
}

YEAR_DIRS = {
    "Year1": r"results\Task3\Part\Jatin",
    "Year2": r"results\task4\part\Jatin\Year2",
    "Year3": r"results\task4\part\Jatin\Year3",
    "Year4": r"results\task4\part\Jatin\Year4",
    "Year5": r"results\task4\part\Jatin\Year5",
}

print("Generating optimized layout files...")
print("=" * 80)

for year_name, machines in YEARS.items():
    # Calculate optimal grids
    configs = {}
    for process in ["B1", "A", "B2", "C", "D", "I", "J"]:
        count = machines[process]
        
        if process in ["B1", "A", "B2", "C", "D"]:
            unit_w, unit_h, overlap = 14, 14, 2
            group = "ABCD"
        else:
            unit_w, unit_h, overlap = 36, 14, 0
            group = "HIJ"
        
        rows, cols = find_optimal_grid(count)
        eff_w, eff_h = calc_dimensions(rows, cols, unit_w, unit_h, overlap)
        
        configs[process] = {
            "group": group,
            "count": count,
            "rows": rows,
            "cols": cols,
            "eff_w": eff_w,
            "eff_h": eff_h
        }
    
    # Build code string
    code_lines = []
    code_lines.append('"""')
    code_lines.append(f'{year_name} Part 1 - OPTIMIZED Compact Layout Generator')
    code_lines.append('')
    code_lines.append(f'Machine counts for {year_name} Part 1:')
    code_lines.append(f'- B1: {machines["B1"]}, A: {machines["A"]}, B2: {machines["B2"]}, C: {machines["C"]}, D: {machines["D"]}, I: {machines["I"]}, J: {machines["J"]}')
    code_lines.append(f'- Total: {sum(machines.values())} machines')
    code_lines.append('')
    code_lines.append('OPTIMIZED: Zero waste grids + compact 2D arrangement')
    code_lines.append('"""')
    code_lines.append('')
    code_lines.append('from pathlib import Path')
    code_lines.append('import matplotlib.pyplot as plt')
    code_lines.append('from matplotlib.patches import Rectangle')
    code_lines.append('import csv')
    code_lines.append('')
    code_lines.append('# Optimal grid configurations (ZERO WASTE)')
    code_lines.append('AREAS = {')
    
    for process in ["B1", "A", "B2", "C", "D", "I", "J"]:
        cfg = configs[process]
        code_lines.append(f'    "{process}": {{"group": "{cfg["group"]}", "count": {cfg["count"]:2d}, "rows": {cfg["rows"]}, "cols": {cfg["cols"]}, "eff_w": {cfg["eff_w"]:3d}, "eff_h": {cfg["eff_h"]:2d}}},')
    
    code_lines.append('}')
    code_lines.append('')
    code_lines.append('PROCESS_ORDER = ["B1", "A", "B2", "C", "D", "I", "J"]')
    code_lines.append('GAP = 5  # ft between areas')
    code_lines.append('')
    code_lines.append('AREA_COLORS = {')
    code_lines.append('    "B1": \'#4c9aff\',  # Blue')
    code_lines.append('    "A":  \'#ffa726\',  # Orange')
    code_lines.append('    "B2": \'#4c9aff\',  # Blue')
    code_lines.append('    "C":  \'#ab47bc\',  # Purple')
    code_lines.append('    "D":  \'#26c6da\',  # Cyan')
    code_lines.append('    "I":  \'#66bb6a\',  # Green')
    code_lines.append('    "J":  \'#f06292\',  # Pink')
    code_lines.append('}')
    code_lines.append('')
    
    # Add rest of the code (layout generation functions)
    code_lines.extend([
        'def pack_areas_2d():',
        '    """Pack areas in 2-row arrangement: Row1 (ABCD), Row2 (HIJ centered)"""',
        '    positions = {}',
        '    ',
        '    # Row 1: ABCD processes',
        '    row1_processes = ["B1", "A", "B2", "C", "D"]',
        '    x_offset = 0',
        '    row1_height = max([AREAS[p]["eff_h"] for p in row1_processes])',
        '    ',
        '    for process in row1_processes:',
        '        area = AREAS[process]',
        '        positions[process] = {"x": x_offset, "y": 0}',
        '        x_offset += area["eff_w"] + GAP',
        '    ',
        '    row1_width = x_offset - GAP',
        '    ',
        '    # Row 2: HIJ processes (centered below)',
        '    row2_processes = ["I", "J"]',
        '    row2_width = sum([AREAS[p]["eff_w"] for p in row2_processes]) + GAP',
        '    row2_height = max([AREAS[p]["eff_h"] for p in row2_processes])',
        '    ',
        '    x_offset = (row1_width - row2_width) / 2',
        '    y_offset = row1_height + GAP',
        '    ',
        '    for process in row2_processes:',
        '        area = AREAS[process]',
        '        positions[process] = {"x": x_offset, "y": y_offset}',
        '        x_offset += area["eff_w"] + GAP',
        '    ',
        '    total_width = max(row1_width, row2_width)',
        '    total_height = row1_height + GAP + row2_height',
        '    ',
        '    return total_width, total_height, positions',
        '',
        'def draw_area(ax, x0, y0, area_data, process_name):',
        '    """Draw area with blocks and overlaps"""',
        '    rows = area_data["rows"]',
        '    cols = area_data["cols"]',
        '    count = area_data["count"]',
        '    group = area_data["group"]',
        '    ',
        '    if group == "ABCD":',
        '        unit_w, unit_h, overlap = 14, 14, 2',
        '    else:',
        '        unit_w, unit_h, overlap = 36, 14, 0',
        '    ',
        '    # Draw boundary',
        '    boundary = Rectangle((x0, y0), area_data["eff_w"], area_data["eff_h"],',
        '                         facecolor=\'none\', edgecolor=\'black\', linewidth=2,',
        '                         linestyle=\'--\', alpha=0.5)',
        '    ax.add_patch(boundary)',
        '    ',
        '    # Draw blocks',
        '    block_idx = 0',
        '    for r in range(rows):',
        '        for c in range(cols):',
        '            if block_idx >= count:',
        '                break',
        '            ',
        '            if overlap > 0:',
        '                bx = x0 + c * (unit_w - overlap)',
        '                by = y0 + r * (unit_h - overlap)',
        '            else:',
        '                bx = x0 + c * unit_w',
        '                by = y0 + r * unit_h',
        '            ',
        '            block = Rectangle((bx, by), unit_w, unit_h,',
        '                            facecolor=AREA_COLORS[process_name],',
        '                            edgecolor=\'#333\', linewidth=0.5, alpha=0.7)',
        '            ax.add_patch(block)',
        '            ',
        '            # Overlap zones',
        '            if overlap > 0:',
        '                if c < cols - 1:',
        '                    ov = Rectangle((bx + unit_w - overlap, by), overlap, unit_h,',
        '                                 facecolor=\'#ff6b6b\', alpha=0.3)',
        '                    ax.add_patch(ov)',
        '                if r < rows - 1:',
        '                    ov = Rectangle((bx, by + unit_h - overlap), unit_w, overlap,',
        '                                 facecolor=\'#ff6b6b\', alpha=0.3)',
        '                    ax.add_patch(ov)',
        '            ',
        '            block_idx += 1',
        '    ',
        '    # Label',
        '    ax.text(x0 + area_data["eff_w"]/2, y0 + area_data["eff_h"]/2,',
        '           f"{process_name}\\\\n{count}",',
        '           ha=\'center\', va=\'center\', fontsize=10, fontweight=\'bold\',',
        '           color=\'white\', bbox=dict(boxstyle=\'round\', facecolor=\'black\', alpha=0.6))',
        '',
        'def generate_layout():',
        '    """Generate optimized layout"""',
        '    total_w, total_h, positions = pack_areas_2d()',
        '    ',
        '    actual_area = sum(AREAS[p]["eff_w"] * AREAS[p]["eff_h"] for p in PROCESS_ORDER)',
        '    total_area = total_w * total_h',
        '    efficiency = (actual_area / total_area) * 100',
        '    ',
        '    print("Creating OPTIMIZED compact 2-row layout...")',
        '    print("  Row 1: B1 → A → B2 → C → D (ABCD processes)")',
        '    print("  Row 2: I → J (HIJ processes, centered)")',
        '    print(f"\\\\nLayout: {total_w:.0f} ft × {total_h:.0f} ft = {total_area:,.0f} ft²")',
        '    print(f"Actual area: {actual_area:,.0f} ft² (efficiency: {efficiency:.1f}%)")',
        '    ',
        '    fig, ax = plt.subplots(figsize=(16, 10))',
        '    ',
        '    for process in PROCESS_ORDER:',
        '        area = AREAS[process]',
        '        pos = positions[process]',
        '        draw_area(ax, pos["x"], pos["y"], area, process)',
        '    ',
        '    # Draw arrows',
        '    for i in range(len(PROCESS_ORDER) - 1):',
        '        p1, p2 = PROCESS_ORDER[i], PROCESS_ORDER[i + 1]',
        '        x1 = positions[p1]["x"] + AREAS[p1]["eff_w"]',
        '        y1 = positions[p1]["y"] + AREAS[p1]["eff_h"] / 2',
        '        x2 = positions[p2]["x"]',
        '        y2 = positions[p2]["y"] + AREAS[p2]["eff_h"] / 2',
        '        ax.annotate(\'\', xy=(x2, y2), xytext=(x1, y1),',
        '                   arrowprops=dict(arrowstyle=\'->\', lw=2, color=\'red\', alpha=0.6))',
        '    ',
        '    ax.set_xlim(-10, total_w + 10)',
        '    ax.set_ylim(-10, total_h + 10)',
        '    ax.set_aspect(\'equal\')',
        f'    ax.set_title(f\'{year_name} Optimized Compact Layout (Zero Waste) - {{sum([AREAS[p]["count"] for p in PROCESS_ORDER])}} Machines\',',
        '                fontsize=14, fontweight=\'bold\')',
        '    ax.grid(True, alpha=0.3)',
        '    ',
        '    output_dir = Path(__file__).parent',
        '    png_file = output_dir / "Optimized_Compact_Layout.png"',
        '    csv_file = output_dir / "Optimized_Compact_Layout_Summary.csv"',
        '    ',
        '    plt.tight_layout()',
        '    plt.savefig(png_file, dpi=150, bbox_inches=\'tight\')',
        '    print(f"\\\\nSaved: {png_file}")',
        '    ',
        '    with open(csv_file, \'w\', newline=\'\', encoding=\'utf-8\') as f:',
        '        writer = csv.writer(f)',
        '        writer.writerow([\'Area\', \'X_ft\', \'Y_ft\', \'Width_ft\', \'Height_ft\', \'Rows\', \'Cols\', \'Machines\'])',
        '        for process in PROCESS_ORDER:',
        '            area = AREAS[process]',
        '            pos = positions[process]',
        '            writer.writerow([process, f"{pos[\'x\']:.1f}", f"{pos[\'y\']:.1f}",',
        '                           area["eff_w"], area["eff_h"], area["rows"], area["cols"], area["count"]])',
        '    ',
        '    print(f"Saved: {csv_file}")',
        '    plt.close()',
        '',
        'if __name__ == "__main__":',
        '    generate_layout()',
    ])
    
    # Write file
    year_dir = Path(YEAR_DIRS[year_name])
    output_file = year_dir / "optimized_compact_layout_generator.py"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(code_lines))
    
    print(f"✓ {year_name}: {sum(machines.values())} machines, saved to {output_file.name}")

print("\n" + "=" * 80)
print("All files generated! Run them to create optimized layouts.")
