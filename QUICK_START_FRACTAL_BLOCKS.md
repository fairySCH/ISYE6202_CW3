# Quick Reference Guide - Fractal Block Optimization Scripts

## Two-Step Process

### Step 1: Generate Optimal Grid Configurations
```bash
python src\task4\Fractal\Year5_F4_Optimal_Grid_Optimizer.py <year> <num_fractals>
```

**Examples:**
```bash
# Year 5, F4
python src\task4\Fractal\Year5_F4_Optimal_Grid_Optimizer.py 5 4

# Year 1, F4  
python src\task4\Fractal\Year5_F4_Optimal_Grid_Optimizer.py 1 4

# Year 2, F4
python src\task4\Fractal\Year5_F4_Optimal_Grid_Optimizer.py 2 4
```

**Outputs:**
- CSV file with optimal grid configurations

---

### Step 2: Generate Individual Block Images
```bash
python src\task4\Fractal\Fractal_Individual_Block_Visualizer.py <year> <num_fractals>
```

**Examples:**
```bash
# Year 5, F4
python src\task4\Fractal\Fractal_Individual_Block_Visualizer.py 5 4

# Year 1, F4
python src\task4\Fractal\Fractal_Individual_Block_Visualizer.py 1 4

# Year 2, F4
python src\task4\Fractal\Fractal_Individual_Block_Visualizer.py 2 4
```

**Outputs:**
- 13 PNG images: Process_A_Block.png through Process_M_Block.png

---

## Output Locations

All outputs are saved to:
```
results/task4/Fractal/Fractal_Layout/Year{Y}_F{N}_Optimized/
```

Where:
- `{Y}` = year number (1-5)
- `{N}` = number of fractal centers (e.g., 4)

---

## What Gets Generated

### Configuration CSV
Contains for each process (A-M):
- Optimal grid layout (rows × cols)
- Machine dimensions
- Block dimensions (considering overlap)
- Utilization percentage
- Wasted spaces
- Optimization score

### Individual Images (A-M)
Each image shows:
- Parent block boundary
- Child equipment blocks (numbered 1, 2, 3...)
- Shareability zones (red overlay)
- Dimension annotations
- Statistics box

---

## Already Completed

✅ **Year 5 F4** - 13 images + CSV
- Location: `results/task4/Fractal/Fractal_Layout/Year5_F4_Optimized/`
- 184 machines total
- 96.37% average utilization

✅ **Year 1 F4** - 13 images + CSV  
- Location: `results/task4/Fractal/Fractal_Layout/Year1_F4_Optimized/`
- 100 machines total
- 98.49% average utilization

---

## Notes

- Scripts automatically find correct equipment requirements file
- Year 1 uses Task3 folder, Years 2-5 use task4 folder
- No layout generation - only individual blocks
- Images are 300 DPI, publication-ready
- CSV files can be used for further analysis
