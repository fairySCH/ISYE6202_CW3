"""
Update layout generator AREAS dictionaries for all years
"""
from pathlib import Path
import re

# Machine counts for each year using Approach 1
YEAR_CONFIGS = {
    'Year1': {'B1': 12, 'A': 5, 'B2': 12, 'C': 3, 'D': 12, 'I': 6, 'J': 12},
    'Year2': {'B1': 14, 'A': 6, 'B2': 14, 'C': 3, 'D': 14, 'I': 7, 'J': 14},
    'Year3': {'B1': 15, 'A': 6, 'B2': 15, 'C': 3, 'D': 15, 'I': 8, 'J': 15},
    'Year4': {'B1': 15, 'A': 6, 'B2': 15, 'C': 3, 'D': 15, 'I': 8, 'J': 15},
    'Year5': {'B1': 16, 'A': 7, 'B2': 16, 'C': 4, 'D': 16, 'I': 8, 'J': 16},
}

#Calculate optimal grid dimensions for each process
def calculate_grid(count, block_type):
    """Calculate optimal rows x cols grid for given machine count"""
    if block_type == 'ABCD':
        # ABCD blocks: 14x14, prefer vertical arrangement
        if count <= 5:
            return count, 1  # vertical line
        elif count <= 12:
            return (count + 2) // 3, 3  # 3 columns
        else:
            cols = 3 if count <= 15 else 4
            rows = (count + cols - 1) // cols
            return rows, cols
    else:  # HIJ
        # HIJ blocks: 14x36, prefer horizontal arrangement
        if count <= 8:
            rows = 2
            cols = (count + 1) // 2
        else:
            rows = 3
            cols = (count + 2) // 3
        return rows, cols

def calculate_effective_dimensions(rows, cols, block_type):
    """Calculate effective width and height considering overlaps"""
    if block_type == 'ABCD':
        # ABCD: 14x14 blocks with 2ft overlap on 3 sides
        eff_w = cols * 14 - (cols - 1) * 2
        eff_h = rows * 14 - (rows - 1) * 2
    else:  # HIJ
        # HIJ: 14x36 blocks with NO overlap
        eff_w = cols * 36
        eff_h = rows * 14
    return eff_w, eff_h

def update_layout_file(year_path, config):
    """Update the AREAS dictionary in optimized_layout_generator.py"""
    layout_file = year_path / "optimized_layout_generator.py"
    
    if not layout_file.exists():
        print(f"  ⚠ Warning: {layout_file} not found, skipping")
        return
    
    # Read the file
    with open(layout_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build new AREAS dictionary
    areas_lines = ["AREAS = {"]
    
    for proc in ['B1', 'A', 'B2', 'C', 'D', 'I', 'J']:
        count = config[proc]
        block_type = 'ABCD' if proc in ['B1', 'A', 'B2', 'C', 'D'] else 'HIJ'
        rows, cols = calculate_grid(count, block_type)
        eff_w, eff_h = calculate_effective_dimensions(rows, cols, block_type)
        
        areas_lines.append(f'    "{proc}": {{"group": "{block_type}", "count": {count:2d}, "rows": {rows}, "cols": {cols}, "eff_w": {eff_w}, "eff_h": {eff_h}}},')
    
    areas_lines.append("}")
    new_areas = "\n".join(areas_lines)
    
    # Find the AREAS dict more carefully - find first occurrence only
    import re
    # Match AREAS = { ... } but stop at first complete dict
    pattern = r'AREAS\s*=\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
    
    # Check if there are multiple AREAS definitions (malformed file)
    matches = list(re.finditer(pattern, content))
    if len(matches) > 1:
        # File has multiple AREAS dicts, need to clean up
        # Find the first one and replace, delete the rest
        first_match = matches[0]
        updated_content = content[:first_match.start()] + new_areas + content[first_match.end():]
        
        # Now remove any subsequent AREAS definitions
        for match in matches[1:]:
            # Adjust indices after previous replacements
            pattern2 = r',\s*"[A-Z]":\s*\{[^}]*\},'
            updated_content = re.sub(pattern2, '', updated_content, count=10)
    else:
        updated_content = re.sub(pattern, new_areas, content, count=1)
    
    # Write back
    with open(layout_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"  ✓ Layout updated: {layout_file.name}")

# Update files
base_path = Path(__file__).parent / "results" / "task4" / "part" / "Jatin"

for year, config in YEAR_CONFIGS.items():
    print(f"\n{year}:")
    
    if year == 'Year1':
        year_path = Path(__file__).parent / "results" / "Task3" / "Part" / "Jatin"
    else:
        year_path = base_path / year
    
    update_layout_file(year_path, config)

print("\n" + "=" * 70)
print("All layout files updated successfully!")
print("\nSummary:")
for year, config in YEAR_CONFIGS.items():
    total = sum(config.values())
    print(f"{year}: {total} machines - B1={config['B1']}, A={config['A']}, B2={config['B2']}, C={config['C']}, D={config['D']}, I={config['I']}, J={config['J']}")
