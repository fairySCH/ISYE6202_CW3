# Fractal Parent Block Optimization - Summary Report

## Overview

Successfully created **reusable scripts** to generate optimal grid configurations and individual block visualizations for fractal layouts. The scripts work for any year and fractal center configuration.

## Scripts Created

### 1. `Year5_F4_Optimal_Grid_Optimizer.py`
**Purpose:** Generate optimal grid configurations for each process (A-M)

**Features:**
- Reusable for any year/fractal combination
- Considers shareability rules:
  - **ABCD group**: 14×14 ft, 2ft overlap on 3 sides
  - **EFG group**: 22×15 ft, no overlap
  - **HIJ group**: 14×36 ft, no overlap
  - **KLM group**: 14×7 ft, 1ft overlap on 2 sides
- Multi-criteria optimization:
  - Minimizes wasted spaces
  - Optimizes aspect ratio (prefers square-like)
  - Minimizes perimeter
  - Maximizes utilization

**Usage:**
```bash
python Year5_F4_Optimal_Grid_Optimizer.py <year> <num_fractals>
# Examples:
python Year5_F4_Optimal_Grid_Optimizer.py 5 4
python Year5_F4_Optimal_Grid_Optimizer.py 1 4
```

**Output:** 
- CSV with optimal grid configurations

### 2. `Fractal_Individual_Block_Visualizer.py`
**Purpose:** Generate individual images for each process showing parent blocks with child equipment

**Features:**
- One PNG per process (A.png through M.png)
- Shows child equipment blocks inside parent block
- Color-coded by process group
- Displays shareability zones (overlap areas)
- Professional annotations and dimensions
- Information box with key metrics

**Usage:**
```bash
python Fractal_Individual_Block_Visualizer.py <year> <num_fractals>
# Examples:
python Fractal_Individual_Block_Visualizer.py 5 4
python Fractal_Individual_Block_Visualizer.py 1 4
```

**Output:**
- 13 individual PNG images (Process_A_Block.png through Process_M_Block.png)

---

## Results Generated

### Year 5 F4 (4 Fractal Centers)

**Location:** `results/task4/Fractal/Fractal_Layout/Year5_F4_Optimized/`

**Files:**
- `Year5_F4_Optimal_Grid_Configurations.csv` - Configuration data
- `Process_A_Block.png` through `Process_M_Block.png` - 13 individual images

**Key Statistics:**
- Total Equipment: **184 machines**
- Total Block Area: **53,508 sq ft**
- Average Utilization: **96.37%**
- Total Wasted Spaces: **5** (out of 189 total spaces)

**Best Configurations:**
- Process K: 2×2 grid, 378 sq ft, score=43.78
- Process G: 2×3 grid, 1,980 sq ft, score=94.80
- Process L: 4×4 grid, 1,484 sq ft, score=94.84

**Group Breakdown:**
| Group | Processes | Machines | Area (sq ft) | Avg Utilization |
|-------|-----------|----------|--------------|-----------------|
| ABCD  | A,B,C,D   | 47       | 8,032        | 89.58%          |
| EFG   | E,F,G     | 32       | 10,560       | 100.00%         |
| HIJ   | H,I,J     | 60       | 30,744       | 98.15%          |
| KLM   | K,L,M     | 45       | 4,172        | 100.00%         |

---

### Year 1 F4 (4 Fractal Centers)

**Location:** `results/task4/Fractal/Fractal_Layout/Year1_F4_Optimized/`

**Files:**
- `Year1_F4_Optimal_Grid_Configurations.csv` - Configuration data
- `Process_A_Block.png` through `Process_M_Block.png` - 13 individual images

**Key Statistics:**
- Total Equipment: **100 machines**
- Total Block Area: **28,295 sq ft**
- Average Utilization: **98.49%**
- Total Wasted Spaces: **2** (out of 102 total spaces)

**Best Configurations:**
- Process L: 3×3 grid, 840 sq ft, score=68.40
- Process B: 3×3 grid, 1,444 sq ft, score=74.44
- Process K: 1×2 grid, 189 sq ft, score=81.89

**Group Breakdown:**
| Group | Processes | Machines | Area (sq ft) | Avg Utilization |
|-------|-----------|----------|--------------|-----------------|
| ABCD  | A,B,C,D   | 28       | 4,744        | 98.22%          |
| EFG   | E,F,G     | 16       | 5,610        | 95.83%          |
| HIJ   | H,I,J     | 31       | 15,624       | 100.00%         |
| KLM   | K,L,M     | 25       | 2,317        | 100.00%         |

---

## Technical Implementation

### Shareability Calculation

The scripts properly implement shareability rules:

**For ABCD (A, B, C, D):**
- Machine size: 14×14 ft
- Overlap: 2 ft on 3 sides (front, left, right)
- Effective width for n columns: `14 × n - 2 × (n-1)`
- Effective depth for n rows: `14 × n - 2 × (n-1)`

**For KLM (K, L, M):**
- Machine size: 14×7 ft
- Overlap: 1 ft on 2 sides (left, right)
- Effective width for n columns: `14 × n - 1 × (n-1)`
- Effective depth for n rows: `7 × n` (no vertical overlap)

**For EFG and HIJ:**
- No sharing/overlap
- Direct multiplication for dimensions

### Optimization Algorithm

Multi-criteria scoring function:
```
score = waste_penalty + area_factor + aspect_penalty + utilization_bonus + perimeter_penalty

where:
- waste_penalty = (rows × cols - machine_count) × 100
- area_factor = block_area / 100
- aspect_penalty = (aspect_ratio - 1) × 50
- utilization_bonus = (1 - utilization) × 200
- perimeter_penalty = perimeter × 5
```

Lower score = better configuration

---

## Usage for Other Years

The scripts are fully reusable. To generate for any year/fractal combination:

```bash
# For Year 2, F4
python Year5_F4_Optimal_Grid_Optimizer.py 2 4
python Fractal_Individual_Block_Visualizer.py 2 4

# For Year 3, F4
python Year5_F4_Optimal_Grid_Optimizer.py 3 4
python Fractal_Individual_Block_Visualizer.py 3 4

# etc.
```

**Note:** The scripts automatically determine the correct input file path:
- Year 1: Uses `results/Task3/Fractal/Fractal_Design/`
- Years 2-5: Uses `results/task4/Fractal/Fractal_Design/`

---

## Image Outputs

Each process image includes:
- ✓ Parent block boundary (dashed black line)
- ✓ Individual child equipment blocks (numbered)
- ✓ Shareability zones (red overlay where applicable)
- ✓ Dimension annotations (width and depth)
- ✓ Information box with:
  - Group and shareability type
  - Machine size
  - Grid layout
  - Total/wasted spaces
  - Block area
  - Aspect ratio
  - Utilization percentage

The images are publication-ready at 300 DPI with professional styling.

---

## Next Steps

You can now:
1. Use these individual block images for layout planning
2. Arrange them manually in your preferred layout software
3. Run the scripts for other years/fractal combinations as needed
4. Analyze the optimal configurations to understand trade-offs

The configuration CSVs contain all the data needed for further analysis or integration with other tools.
