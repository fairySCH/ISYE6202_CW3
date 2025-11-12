import math

processes = [
    ('B1', 16, 'ABCD'),
    ('A', 7, 'ABCD'),
    ('B2', 16, 'ABCD'),
    ('C', 4, 'ABCD'),
    ('D', 16, 'ABCD'),
    ('I', 8, 'HIJ'),
    ('J', 16, 'HIJ')
]

print("=" * 80)
print("CURRENT: 580 ft × 56 ft (left-to-right)")
print("=" * 80)

for name, count, group in processes:
    unit_w, unit_h, overlap = (14, 14, 2) if group == 'ABCD' else (36, 14, 0)
    
    print(f"\n{name} ({count} machines, {group}):")
    
    configs = []
    for r in range(1, count + 1):
        c = math.ceil(count / r)
        if r * c >= count:
            eff_w = c * unit_w - (c - 1) * overlap if overlap > 0 else c * unit_w
            eff_h = r * unit_h - (r - 1) * overlap if overlap > 0 else r * unit_h
            configs.append((r, c, eff_w, eff_h))
    
    # Show top 6 options
    for r, c, w, h in configs[:6]:
        marker = " ← CURRENT" if (name in ['B1', 'B2', 'D', 'J'] and r == 4 and c == 4) or \
                                 (name == 'A' and r == 1 and c == 7) or \
                                 (name == 'C' and r == 2 and c == 2) or \
                                 (name == 'I' and r == 2 and c == 4) else ""
        print(f"  {r}×{c}: {w:3d}ft × {h:3d}ft{marker}")

print("\n" + "=" * 80)
print("RECOMMENDATIONS FOR MORE COMPACT (taller, shorter):")
print("=" * 80)

recommendations = {
    'B1': (8, 2, "More vertical, reduces width from 50ft to 26ft"),
    'A': (4, 2, "Stacks vertically, reduces width from 86ft to 26ft"),  
    'B2': (8, 2, "More vertical, reduces width from 50ft to 26ft"),
    'C': (4, 1, "Already tall, keep as is or go 4×1 (14ft wide)"),
    'D': (8, 2, "More vertical, reduces width from 50ft to 26ft"),
    'I': (4, 2, "Stacks vertically, reduces width from 144ft to 72ft"),
    'J': (8, 2, "More vertical, reduces width from 144ft to 72ft")
}

total_width_old = 0
total_width_new = 0
max_height_old = 56
max_height_new = 0

print("\nProcess | Current Grid | Current W×H | New Grid | New W×H | Savings")
print("-" * 80)

for name, count, group in processes:
    unit_w, unit_h, overlap = (14, 14, 2) if group == 'ABCD' else (36, 14, 0)
    
    # Current config
    if name in ['B1', 'B2', 'D', 'J']:
        curr_r, curr_c = 4, 4
    elif name == 'A':
        curr_r, curr_c = 1, 7
    elif name == 'C':
        curr_r, curr_c = 2, 2
    else:  # I
        curr_r, curr_c = 2, 4
    
    curr_w = curr_c * unit_w - (curr_c - 1) * overlap if overlap > 0 else curr_c * unit_w
    curr_h = curr_r * unit_h - (curr_r - 1) * overlap if overlap > 0 else curr_r * unit_h
    
    # New config
    new_r, new_c, reason = recommendations[name]
    new_w = new_c * unit_w - (new_c - 1) * overlap if overlap > 0 else new_c * unit_w
    new_h = new_r * unit_h - (new_r - 1) * overlap if overlap > 0 else new_r * unit_h
    
    total_width_old += curr_w
    total_width_new += new_w
    max_height_new = max(max_height_new, new_h)
    
    savings = curr_w - new_w
    print(f"{name:7s} | {curr_r}×{curr_c:2d} ({curr_c*curr_r:2d}) | {curr_w:3d}×{curr_h:2d} | {new_r}×{new_c} ({new_r*new_c:2d}) | {new_w:3d}×{new_h:3d} | -{savings:3d}ft")

total_width_old += 6 * 5  # gaps
total_width_new += 6 * 5  # gaps

print("-" * 80)
print(f"Total layout (with gaps):")
print(f"  Current: {total_width_old}ft × {max_height_old}ft = {total_width_old * max_height_old:,} sq ft")
print(f"  Compact: {total_width_new}ft × {max_height_new}ft = {total_width_new * max_height_new:,} sq ft")
print(f"  Width reduction: {total_width_old - total_width_new}ft ({100*(total_width_old - total_width_new)/total_width_old:.1f}%)")
print(f"  Height increase: {max_height_new - max_height_old}ft")
