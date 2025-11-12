# Jatin Folder - Year-by-Year Layout Analysis

This folder contains optimized facility layouts organized by year, focusing on Part 1 production.

## Folder Structure

```
Jatin/
├── Block_Specs.csv          # Shared block specifications (ABCD, HIJ, EFG, KLM)
├── README.md                # This file
├── Year4/                   # Year 4 Part 1 layout (77 machines)
│   ├── Block_Specs.csv
│   ├── calculate_PART1_ONLY.py
│   ├── Equipment_Summary_Table.csv
│   ├── Equipment_Summary_Table.png
│   ├── generate_equipment_table.py
│   ├── Layout_Summary_Report.txt
│   ├── optimized_layout_generator.py
│   ├── Optimized_Layout_Summary.csv
│   ├── Optimized_Layout_with_Overlaps.png
│   ├── README_PART1_ONLY.md
│   └── Year4_Part1_ONLY_Machine_Requirements.txt
└── Year5/                   # Year 5 Part 1 layout (129 machines)
    ├── Block_Specs.csv
    ├── Equipment_Summary_Table.csv
    ├── Equipment_Summary_Table.png
    ├── generate_equipment_table.py
    ├── Layout_Summary_Report.txt
    ├── optimized_layout_generator.py
    ├── Optimized_Layout_Summary.csv
    ├── Optimized_Layout_with_Overlaps.png
    └── region_block_counts.csv
```

## Quick Comparison

| Metric | Year 4 Part 1 | Year 5 Part 1 |
|--------|---------------|---------------|
| **Demand** | 28,500 units/week | 29,800 units/week |
| **Machines** | 77 (2-shift) | 129 (1-shift data) |
| **Layout Size** | 298 × 108 ft | 310 × 110 ft |
| **Footprint** | 32,184 ft² | 34,100 ft² |
| **Efficiency** | 68.9% | 98.5% |
| **Process Flow** | B1→A→B2→C→D→I→J | B1→A→B2→C→D→I→J |
| **Block Types** | ABCD, HIJ | ABCD, HIJ |

## Design Principles

All layouts follow these principles:
1. **Vertical Stacking** - Areas configured tall/narrow to minimize width
2. **Left-to-Right Flow** - Process order: B1 → A → B2 → C → D → I → J
3. **Center Alignment** - All areas vertically centered for straight material flow
4. **Clear Separation** - 5 ft gaps between process areas
5. **Overlap Zones** - 2 ft sharing within ABCD blocks only (visualized in red)

## Block Specifications

### ABCD Blocks (14×14 ft, 196 ft²)
- Used for: B1, A, B2, C, D processes
- Share 2 ft on front/left/right sides within same area
- Effective dimensions account for sharing

### HIJ Blocks (14×36 ft, 504 ft²)
- Used for: I, J processes  
- No internal sharing
- Larger footprint for complex equipment

## Key Files in Each Year Folder

1. **optimized_layout_generator.py** - Main layout generation script
2. **Optimized_Layout_with_Overlaps.png** - Visual layout diagram (300 DPI)
3. **Equipment_Summary_Table.png** - Equipment counts and specs
4. **Layout_Summary_Report.txt** - Comprehensive documentation
5. **Optimized_Layout_Summary.csv** - Area positions and dimensions

## Usage

To regenerate layouts:
```bash
cd Year4  # or Year5
python optimized_layout_generator.py
python generate_equipment_table.py
```

## Notes

- **Year 4** uses 2-shift equipment data (4800 min/week per machine)
- **Year 5** original data uses 1-shift counts (2400 min/week per machine)
- Both layouts focus on **Part 1 (P1) ONLY**, not all parts
- Layouts optimized for space efficiency and material flow

---

**Last Updated**: November 11, 2025  
**Organization**: Organized by year for clarity and comparison
