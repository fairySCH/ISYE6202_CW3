# Fractal Organization Design - Quick Start Guide

## Overview

This guide helps you generate complete fractal organization analysis including equipment requirements, flow matrices, and layout-ready outputs for drawing your factory design.

## What is Fractal Organization?

A **fractal organization** divides the factory into `f` identical self-contained centers, each capable of producing all products with 1/f of total capacity. It's like having multiple mini-factories instead of one large factory.

### Key Characteristics:
- **Self-similar**: Each center is a complete mini-factory
- **Redundant**: If one center fails, others continue operating
- **Scalable**: Easy to add/remove centers based on demand
- **Flexible**: Load can be distributed across centers

## Quick Start (Recommended)

### Option 1: Run Everything at Once

```powershell
cd "d:\Adarsh GATech Files\6335 Benoit SC1\CW3\ISYE6202_CW3\src"
python fractal_run_all.py
```

This will automatically:
1. ✓ Calculate equipment for f=2,3,4,5 configurations
2. ✓ Generate flow matrices for each configuration
3. ✓ Create layout coordinates for drawing
4. ✓ Produce comparison analysis and recommendations

**Total time**: ~2-3 minutes

### Option 2: Run Individual Scripts

If you want to run steps separately:

```powershell
# Step 1: Equipment requirements
python fractal_design_main.py

# Step 2: Flow matrices
python fractal_flow_matrix.py

# Step 3: Layout generation
python fractal_layout_generator.py

# Step 4: Comparison analysis
python fractal_comparison_analysis.py
```

## Understanding the Output Files

### 1. Equipment Requirements

**Files**: `Fractal_f{2,3,4,5}_Equipment_Requirements.csv`

Shows for each configuration:
- Process type (A-M)
- Equipment needed per center
- Total equipment across all centers
- Utilization percentage

**Use case**: Determine how many machines you need

### 2. Flow Matrices

**Location**: `results/fractal_flow_matrices/f{X}_centers/`

**Files**:
- `Single_Center_Flow_Matrix.csv` - Material flow within ONE center
- `Aggregate_Factory_Flow_Matrix.csv` - Total flow across ALL centers
- `Flow_Summary.csv` - Flow statistics by process

**Use case**: Understand material movement patterns

### 3. Layout Data (FOR DRAWING!)

**Location**: `results/fractal_layouts/f{X}_layout/`

**Files**:
- `Process_Locations.csv` - X,Y coordinates of each process
- `Flow_Connections.csv` - Start/end points for flow arrows
- `Center_Boundaries.csv` - Fractal center boundaries
- `Layout_Data.json` - Complete layout data

**Use case**: Import into CAD/drawing software

### 4. Comparison & Recommendations

**Files**:
- `Organization_Design_Comparison.csv` - Compare all designs
- `Fractal_Recommendation_Report.txt` - Design recommendations
- `Fractal_Radar_Chart_Data.csv` - Visualization data

**Use case**: Decision making and presentation

## How to Draw the Layout

### Using Excel/Google Sheets:

1. Open `Process_Locations.csv`
2. Create scatter plot with Global_X and Global_Y
3. Label each point with Process name
4. Size by Equipment_Count

5. Open `Flow_Connections.csv`
6. Draw arrows from (From_X, From_Y) to (To_X, To_Y)
7. Make arrow thickness proportional to Flow_Units

8. Open `Center_Boundaries.csv`
9. Draw rectangles using x, y, width, height

### Using CAD Software (AutoCAD, SolidWorks, etc.):

1. Import `Process_Locations.csv`:
   - Create blocks/symbols for each process
   - Place at (Global_X, Global_Y)
   - Scale by Equipment_Count

2. Import `Flow_Connections.csv`:
   - Create polylines/arrows
   - From (From_X, From_Y) to (To_X, To_Y)
   - Line weight = Flow_Units / max(Flow_Units)

3. Import `Center_Boundaries.csv`:
   - Create rectangles for center boundaries
   - Add labels (Center_ID)

### Using Python (Matplotlib):

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
processes = pd.read_csv('results/fractal_layouts/f3_layout/Process_Locations.csv')
flows = pd.read_csv('results/fractal_layouts/f3_layout/Flow_Connections.csv')
centers = pd.read_csv('results/fractal_layouts/f3_layout/Center_Boundaries.csv')

# Create plot
fig, ax = plt.subplots(figsize=(15, 12))

# Draw center boundaries
for _, center in centers.iterrows():
    rect = plt.Rectangle((center['x'] - center['width']/2, 
                          center['y'] - center['height']/2),
                         center['width'], center['height'],
                         fill=False, edgecolor='blue', linewidth=2)
    ax.add_patch(rect)
    ax.text(center['x'], center['y'], f"Center {center['center_id']}", 
            ha='center', fontsize=12, weight='bold')

# Draw flows
for _, flow in flows.iterrows():
    ax.arrow(flow['From_X'], flow['From_Y'],
            flow['To_X'] - flow['From_X'], 
            flow['To_Y'] - flow['From_Y'],
            head_width=2, head_length=2, 
            fc='gray', ec='gray', alpha=0.5)

# Draw processes
for _, proc in processes.iterrows():
    circle = plt.Circle((proc['Global_X'], proc['Global_Y']), 
                        proc['Width']/2, 
                        color='red', alpha=0.7)
    ax.add_patch(circle)
    ax.text(proc['Global_X'], proc['Global_Y'], proc['Process'],
           ha='center', va='center', fontsize=10, weight='bold')

plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.xlabel('X (meters)')
plt.ylabel('Y (meters)')
plt.title('Fractal Organization Layout (f=3)')
plt.tight_layout()
plt.savefig('fractal_layout.png', dpi=300)
plt.show()
```

## Interpreting Results

### Which configuration to choose?

**f=2 (Two Centers)**:
- ✓ Simplest to coordinate
- ✓ Lowest equipment overhead
- ✓ 50% redundancy
- ✗ Less flexibility

**f=3 (Three Centers)** ⭐ RECOMMENDED
- ✓ Good redundancy (66.7%)
- ✓ Balanced cost/benefit
- ✓ Easy maintenance scheduling
- ✓ Good load distribution

**f=4 (Four Centers)**:
- ✓ Excellent flexibility
- ✓ 75% redundancy
- ✗ Higher equipment cost
- ✗ More complex coordination

**f=5 (Five Centers)**:
- ✓ Maximum flexibility
- ✓ 80% redundancy
- ✗ Highest equipment overhead
- ✗ Most complex to manage

### Reading the Recommendation Report

Open `Fractal_Recommendation_Report.txt` to see:
1. Equipment efficiency comparison
2. Redundancy analysis
3. Scenario-based recommendations
4. Implementation considerations
5. Financial impact assessment

## Common Questions

### Q: How does fractal compare to functional design?

**Functional** (baseline): 
- One location per process type (A-M)
- Minimum equipment (386 units)
- No redundancy

**Fractal f=3**:
- Three identical centers
- ~2-3% more equipment
- 66.7% redundancy

### Q: Can I customize the number of fractals?

Yes! Edit `fractal_design_main.py` and modify this line:

```python
for f in [2, 3, 4, 5, 6, 7]:  # Add more values
```

### Q: How do I change the layout algorithm?

In `fractal_layout_generator.py`, change:

```python
generate_complete_layout(f, layout_method='flow_based')
# or
generate_complete_layout(f, layout_method='simple')
```

### Q: What about storage areas?

Storage recommendations are in the report. Three options:
- **Centralized**: One receiving/shipping for all centers
- **Distributed**: Each center has its own
- **Hybrid**: Centralized receiving, distributed WIP (recommended)

## Troubleshooting

### "File not found" errors:
```powershell
# Make sure you're in the right directory
cd "d:\Adarsh GATech Files\6335 Benoit SC1\CW3\ISYE6202_CW3\src"

# Verify data files exist
ls ..\data\csv_outputs\
```

### Missing Task1 results:
The scripts will calculate from source data if Task1 files don't exist.

### Import errors:
```powershell
# Install required packages
pip install pandas numpy matplotlib
```

## Advanced Usage

### Custom fractal configuration:

```python
# In fractal_design_main.py
from fractal_design_main import calculate_fractal_requirements

# Custom analysis for f=6
requirements = calculate_fractal_requirements(
    num_fractals=6,
    process_workload=your_workload_dict,
    num_shifts=2
)
```

### Export to other formats:

```python
# JSON export
import json
df.to_json('output.json', orient='records')

# Excel export
df.to_excel('output.xlsx', index=False)
```

## Summary

1. **Run**: `python fractal_run_all.py`
2. **Review**: `Fractal_Recommendation_Report.txt`
3. **Draw**: Use `Process_Locations.csv` and `Flow_Connections.csv`
4. **Present**: Use comparison data for decision making

## Files Created Summary

```
results/
├── Fractal_f2_Equipment_Requirements.csv
├── Fractal_f3_Equipment_Requirements.csv
├── Fractal_f4_Equipment_Requirements.csv
├── Fractal_f5_Equipment_Requirements.csv
├── Fractal_Comparison_All_Scenarios.csv
├── Organization_Design_Comparison.csv
├── Fractal_Recommendation_Report.txt
├── Fractal_Radar_Chart_Data.csv
├── fractal_flow_matrices/
│   ├── f2_centers/
│   │   ├── Single_Center_Flow_Matrix.csv
│   │   ├── Aggregate_Factory_Flow_Matrix.csv
│   │   ├── Flow_Summary.csv
│   │   └── Center_1_Flow_Matrix.csv, Center_2_Flow_Matrix.csv
│   ├── f3_centers/
│   ├── f4_centers/
│   └── f5_centers/
└── fractal_layouts/
    ├── f2_layout/
    │   ├── Process_Locations.csv ⭐
    │   ├── Flow_Connections.csv ⭐
    │   ├── Center_Boundaries.csv ⭐
    │   ├── Layout_Data.json
    │   └── Layout_Summary.txt
    ├── f3_layout/
    └── f4_layout/
```

⭐ = Essential for drawing layouts

---

**Questions?** Check the detailed methodology in `logics/FRACTAL_ORGANIZATION_STRATEGY.md`
