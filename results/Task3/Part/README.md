# Task 3: Part-Based Factory Layout Organization

## Overview

This folder contains the complete **Part-Based Layout Analysis** for Case Study 3, implementing a manufacturing organization strategy where **each of the 20 parts (P1-P20) has its own dedicated manufacturing area**. This approach optimizes material flow within each part's production line while maintaining clear separation between different product families.

## Key Features

- **432 Total Machines** across all 20 parts (corrected with 88.2% reliability factor)
- **265,097 sq ft Total Area** (6.08 acres) - sum of all dedicated part areas
- **Compact Vertical Stacking Layout** with GAP=0 for space optimization
- **Center-to-Center Flow Analysis** for material handling efficiency
- **Equipment Specifications** from 4 groups: ABCD (14×14 ft), EFG (22×15 ft), HIJ (14×36 ft), KLM (3×6 ft)

## Critical Parameters

### Reliability Factor Correction
- **Effective Availability:** 88.2% = 90% efficiency × 98% reliability
- **Effective Capacity:** 4,191.3 minutes/week per machine (was 4,752 without reliability)
- **Impact:** Requires 432 machines instead of 366 (+18% increase)

### Equipment Specifications (from Block_Specs.csv)

| Group | Processes | Width | Depth | Overlap | Shareable Sides |
|-------|-----------|-------|-------|---------|-----------------|
| ABCD  | A, B, C, D | 14 ft | 14 ft | 2 ft | Front, Left, Right |
| EFG   | E, F, G | 22 ft | 15 ft | 0 ft | None |
| HIJ   | H, I, J | 14 ft | 36 ft | 0 ft | None |
| KLM   | K, L, M | 3 ft | 6 ft | 1 ft | Left, Right |

### Layout Strategy
- **Compact Grid:** Vertical stacking with preference for taller configurations
- **GAP:** 0 ft (blocks touch directly)
- **Process Order:** Left-to-right flow following production sequence
- **Vertical Alignment:** Center-aligned within maximum height
- **Overlap Calculation:** Reduces effective dimensions when blocks share sides

## Folder Structure

```
Part/
├── README.md                                    # This file
├── Part_Based_Analysis_Summary_Report.txt       # Overall analysis summary
├── Part_Based_Process_Part_Matrix.csv           # Process-part relationship matrix
├── Part_Based_Year1_All_Processes_Calculator.py # All processes capacity calculator
├── Part_Based_Year1_P1_Capacity_Calculator.py   # Part 1 specific calculator
├── Part_Based_Year1_Layout_Generator.py         # Layout generation script
├── Part_Based_All_Parts_Metrics.py              # Comprehensive metrics for all 20 parts
├── CLEANUP_SUMMARY.txt                          # File cleanup documentation
├── RESTRUCTURING_SUMMARY.txt                    # Folder merge documentation
│
├── Capacity/                                    # Capacity planning files (16 files)
│   ├── Part_Step_Machines_Summary_2_shifts.csv  # Machine requirements per part/step
│   ├── Part_Based_Equipment_Requirements.csv    # Total equipment by process (432 machines)
│   ├── Part_Based_Weekly_Part_Demand.csv        # Weekly demand for all 20 parts
│   ├── Part_Based_Process_Workload_Breakdown.csv # Workload analysis by process
│   ├── Part_Based_All_Parts_Layout_Summary.csv  # Layout dimensions for all parts
│   ├── Part_Based_All_Parts_Flow_Analysis.csv   # Flow distances and total flow
│   ├── Part_Based_All_Parts_Machine_Usage.csv   # Machine counts A-M per part
│   ├── Part_Based_All_Parts_Detailed_Report.txt # 1,536-line comprehensive report
│   ├── Part_Based_All_Parts_Executive_Summary.txt # Strategic insights
│   └── [Other capacity analysis files...]
│
├── Cost_Analysis/                               # Cost analysis files (6 files)
│   ├── Part_Based_Capital_Costs_Detailed.csv    # $171.8M investment by process
│   ├── Part_Based_Operating_Costs_Detailed.csv  # $52.3M annual labor costs
│   ├── Part_Based_Depreciation_Analysis.csv     # $12.6M annual depreciation
│   ├── Part_Based_Cost_KPIs.csv                 # Key performance indicators
│   ├── Part_Based_Layout_Cost_Analysis_Report.txt # Comprehensive cost report
│   └── REGENERATION_SUMMARY.txt                 # Cost regeneration notes
│
└── Visuals/                                     # Visualization files (3 files)
    ├── Part_Based_Year1_Compact_Layout.png      # P1 layout visualization (214×98 ft)
    ├── Part_Based_Layout_Cost_Analysis.png      # Cost breakdown charts
    └── Part_Based_Layout_Cost_KPI_Dashboard.png # KPI dashboard
```

## Key Files Description

### Analysis & Calculation Scripts

#### `Part_Based_All_Parts_Metrics.py` ⭐ NEW
Comprehensive metrics calculator for all 20 parts computing:
- **Layout Area:** Grid dimensions, effective width/height with overlaps, total area
- **Flow Distance:** Center-to-center distances between consecutive processes
- **Machine Usage:** Process counts (A-M) with duplicate tracking
- **Output:** 4 files (Layout Summary, Flow Analysis, Machine Usage, Detailed Report)

#### `Part_Based_Year1_P1_Capacity_Calculator.py`
Calculates machine requirements specifically for Part 1 (Year 1):
- Process sequence: B → A → B → C → D → I → J
- Total machines: 68 (with 88.2% reliability)
- Weekly demand: 20,961.54 units

#### `Part_Based_Year1_All_Processes_Calculator.py`
Aggregates machine requirements across all 20 parts:
- Consolidates workload by process type (A-M)
- Computes total equipment needs: 432 machines
- Calculates utilization rates (84.4% average)

#### `Part_Based_Year1_Layout_Generator.py`
Generates compact layout visualization for Part 1:
- Creates 214 ft × 98 ft layout (20,972 sq ft)
- Applies ABCD overlap rules (2 ft) and HIJ spacing (0 ft)
- Outputs PNG visualization with process areas labeled

### Capacity Analysis Files

#### `Part_Step_Machines_Summary_2_shifts.csv` ⭐ CORRECTED
**THE AUTHORITATIVE MACHINE REQUIREMENTS FILE**
```csv
Part,1,2,3,4,5,6,7,Total_Machines
P1,B: 13,A: 6,B: 13,C: 3,D: 13,I: 7,J: 13,68
P19,L: 11,M: 12,L: 10,M: 18,,,,51
P17,K: 1.0,L: 4.0,M: 5.0,,,,,10.0
```
- Corrected with 88.2% reliability factor
- Shows process sequence and machine count per step
- Includes duplicate processes (e.g., P1 has B twice)

#### `Part_Based_Equipment_Requirements.csv` ⭐ REGENERATED
Total equipment requirements by process:
```
Process A: 14 machines (80.4% utilization)
Process B: 39 machines (91.4% utilization)
Process D: 53 machines (95.1% utilization)
Process J: 61 machines (90.2% utilization)
Process M: 57 machines (97.0% utilization)
TOTAL: 432 machines (84.4% average utilization)
```

#### `Part_Based_All_Parts_Layout_Summary.csv` ⭐ NEW
Layout dimensions for all 20 parts:
- **Largest:** P1 (48,384 sq ft), P16 (30,672 sq ft), P7 (28,224 sq ft)
- **Smallest:** P17 (273 sq ft), P20 (390 sq ft), P18 (468 sq ft)
- **Layout dimensions:** Width × Height for each part
- **Complexity:** Number of process steps (3-7 steps)

#### `Part_Based_All_Parts_Flow_Analysis.csv` ⭐ NEW
Flow distance analysis with total weekly flow:
- **Longest Flow:** P1 (229.91 ft/unit → 4.8M unit-ft/week)
- **Shortest Flow:** P20 (11.79 ft/unit → 175K unit-ft/week)
- **Formula Column:** Shows calculation (e.g., "20961.54 × 229.91 ft")

#### `Part_Based_All_Parts_Machine_Usage.csv` ⭐ NEW
Machine counts per part by process type:
```csv
Part,A,B,C,D,E,F,G,H,I,J,K,L,M,Total_Process_Areas
P1,1,2,1,1,0,0,0,0,1,1,0,0,0,7
P17,0,0,0,0,0,0,0,0,0,0,1,1,1,3
P19,0,0,0,0,0,0,0,0,0,0,0,2,2,4
```
- Counts duplicate processes (P1 has B=2, P19 has L=2 and M=2)
- Shows equipment group usage patterns

#### `Part_Based_Weekly_Part_Demand.csv`
Weekly production demand for all 20 parts:
```csv
Part,Weekly_Demand
P1,20961.54
P19,20000.00
P14,18076.92
P20,14807.69
P7,13846.15
```

### Cost Analysis Files

#### `Part_Based_Capital_Costs_Detailed.csv`
Equipment investment costs by process:
- **Total Investment:** $171,766,000
- **Highest Costs:** Process H ($41.8M), J ($36.6M), I ($22.8M), D ($16.4M)
- Based on 432 machines with corrected requirements

#### `Part_Based_Operating_Costs_Detailed.csv`
Annual labor costs by process:
- **Total Annual Cost:** $52,291,200
- **Total Operators:** 547.2 FTEs
- **Highest Costs:** Process J ($10.2M), B ($8.1M), I ($6.3M), H ($6.3M)

#### `Part_Based_Cost_KPIs.csv`
Key performance indicators:
- Cost per Operating Hour: $18.86
- Annual Depreciation: $12,567,083
- Average Utilization: 84.4% (realistic with reliability factor)

### Documentation Files

#### `Part_Based_All_Parts_Detailed_Report.txt` ⭐ NEW
1,536-line comprehensive report with detailed calculations for all 20 parts:
- **Per Part Sections:** Layout calculation, flow distance breakdown, machine usage
- **Grid Configurations:** Rows × cols for each process area
- **Effective Dimensions:** Width/height with overlap calculations
- **Flow Details:** Center coordinates and distances for all transitions
- **Summary:** Total machines (432), total area (265,097 sq ft)

#### `Part_Based_All_Parts_Executive_Summary.txt` ⭐ NEW
Strategic insights and key findings:
- Space efficiency comparison (KLM vs HIJ equipment)
- Flow efficiency analysis
- Equipment group utilization patterns
- Facility planning recommendations

#### `Part_Based_Analysis_Summary_Report.txt`
Original analysis report documenting:
- Part-based organization strategy rationale
- Machine requirements methodology
- Layout design principles

## Key Metrics Summary

### Layout Areas by Part

| Rank | Part | Area (sq ft) | Dimensions | Steps | Machines | Equipment Types |
|------|------|--------------|------------|-------|----------|-----------------|
| 1 | P1 | 48,384 | 224 × 216 | 7 | 68 | ABCD, HIJ |
| 2 | P16 | 30,672 | 142 × 216 | 4 | 31 | EFG, HIJ |
| 3 | P7 | 28,224 | 196 × 144 | 6 | 36 | ABCD, EFG, HIJ |
| ... | ... | ... | ... | ... | ... | ... |
| 18 | P18 | 468 | 18 × 26 | 4 | 20 | KLM only |
| 19 | P20 | 390 | 15 × 26 | 3 | 22 | KLM only |
| 20 | P17 | 273 | 13 × 21 | 3 | 10 | KLM only |

**Insight:** P1 is 177× larger than P17 due to HIJ equipment (14×36 ft) vs KLM (3×6 ft)

### Flow Distance Analysis

| Category | Part | Distance/Unit | Weekly Flow | Weekly Demand |
|----------|------|---------------|-------------|---------------|
| Longest | P1 | 229.91 ft | 4,819,267 unit-ft | 20,961.54 |
| | P16 | 193.34 ft | 2,305,208 unit-ft | 11,923.08 |
| | P7 | 184.92 ft | 2,560,431 unit-ft | 13,846.15 |
| Shortest | P20 | 11.79 ft | 174,583 unit-ft | 14,807.69 |
| | P17 | 11.99 ft | 59,950 unit-ft | 5,000.00 |
| | P18 | 17.73 ft | 211,396 unit-ft | 11,923.08 |

**Insight:** KLM parts achieve ~20× shorter flow distances due to compact equipment

### Equipment Investment Summary

| Process | Machines | Unit Cost | Total Investment | Utilization |
|---------|----------|-----------|------------------|-------------|
| H | 38 | $1,100,000 | $41,800,000 | 90.2% |
| J | 61 | $600,000 | $36,600,000 | 90.2% |
| I | 38 | $600,000 | $22,800,000 | 87.5% |
| D | 53 | $310,000 | $16,430,000 | 95.1% |
| B | 39 | $200,000 | $7,800,000 | 91.4% |
| **Total** | **432** | - | **$171,766,000** | **84.4%** |

## Methodology

### Capacity Calculation
1. **Input Data:** Processing times from `Parts_Step_Time.csv`, demand from weekly demand file
2. **Effective Capacity:** 4,191.3 min/week = 5,280 min/week × 90% efficiency × 98% reliability
3. **Machine Calculation:** `Machines = (Demand × Processing_Time) / Effective_Capacity`
4. **Rounding:** Round up to nearest integer for each process step
5. **Aggregation:** Sum machines by process type across all parts

### Layout Generation
1. **Grid Optimization:** Calculate rows/cols preferring taller grids (more rows)
   - `rows = ceil(sqrt(machine_count × 2))`
   - `cols = ceil(machine_count / rows)`
2. **Effective Dimensions:** Apply overlap rules by equipment group
   - ABCD: `eff_w = 14×cols - 2×(cols-1)`, `eff_h = 14×rows - 2×(rows-1)`
   - EFG: `eff_w = 22×cols`, `eff_h = 15×rows`
   - HIJ: `eff_w = 14×cols`, `eff_h = 36×rows`
   - KLM: `eff_w = 3×cols - 1×(cols-1)`, `eff_h = 6×rows - 1×(rows-1)`
3. **Layout Placement:** Arrange process areas left-to-right with GAP=0
4. **Total Dimensions:** `Width = sum(eff_widths)`, `Height = max(eff_heights)`

### Flow Distance Calculation
1. **Center Positions:** For each process area, calculate center point
   - `center_x = cumulative_width + eff_width/2`
   - `center_y = eff_height/2`
2. **Distance Calculation:** Euclidean distance between consecutive centers
   - `distance = sqrt((x2-x1)² + (y2-y1)²)`
3. **Total Flow:** Multiply distance by weekly demand
   - `total_flow = weekly_demand × total_distance_per_unit`

## Cost Analysis

### Capital Investment: $171,766,000
- Equipment purchase and installation for 432 machines
- Corrected from $150,666,000 (18% increase due to reliability factor)
- Major investments: Process H ($41.8M), J ($36.6M), I ($22.8M)

### Annual Operating Cost: $52,291,200
- Labor costs for 547.2 FTE operators
- Based on $96,000/year average salary (2 shifts)
- Corrected from $46,092,800 (13.4% increase)

### Annual Depreciation: $12,567,083
- Straight-line depreciation over 10-20 year useful life
- Varies by equipment type (Process K: 10 years, Process H: 20 years)

### Key Cost Drivers
1. **Process H (Machining):** $41.8M capital + $6.3M/year labor = Highest total cost
2. **Process J (Assembly):** $36.6M capital + $10.2M/year labor = Most operators (122 FTE)
3. **Process D (Forming):** $16.4M capital but 95.1% utilization = Bottleneck risk

## Change History

### Recent Updates (November 2025)

#### ✅ Reliability Factor Correction
- Applied 88.2% effective availability (was 90% efficiency only)
- Updated all capacity files with corrected machine counts
- Impact: +66 machines (366 → 432, +18% increase)

#### ✅ File Structure Cleanup (28 files removed)
- Removed obsolete flow matrices (20 files)
- Deleted duplicate documentation (3 files)
- Removed outdated cost analysis (5 files based on 366 machines)
- Created `CLEANUP_SUMMARY.txt` documenting changes

#### ✅ Folder Restructuring
- Merged `Jatin/` subfolder into main Part folder
- Applied uniform `Part_Based_*` naming convention to all files
- Renamed 8 files for consistency
- Created `RESTRUCTURING_SUMMARY.txt` with before/after comparison

#### ✅ Cost Analysis Regeneration
- Updated equipment requirements to 432 machines
- Regenerated 5 cost analysis files with corrected data
- Updated 2 visualization files (cost charts and dashboards)
- Investment increased to $171.8M (+$21.1M vs old)
- Operating cost increased to $52.3M/year (+$6.2M vs old)
- Created `REGENERATION_SUMMARY.txt` comparing old vs new

#### ✅ Comprehensive 20-Part Metrics (NEW)
- Created `Part_Based_All_Parts_Metrics.py` calculator
- Generated 4 new analysis files:
  * `Part_Based_All_Parts_Layout_Summary.csv`
  * `Part_Based_All_Parts_Flow_Analysis.csv`
  * `Part_Based_All_Parts_Machine_Usage.csv`
  * `Part_Based_All_Parts_Detailed_Report.txt` (1,536 lines)
- Created `Part_Based_All_Parts_Executive_Summary.txt` with strategic insights
- Validated equipment specifications from `Block_Specs.csv`

## Usage Instructions

### Running Capacity Calculations

```powershell
# Calculate Part 1 capacity only (Year 1)
python src/Task3/Part/Part_Based_Year1_P1_Capacity_Calculator.py

# Calculate all parts aggregated capacity
python src/Task3/Part/Part_Based_Year1_All_Processes_Calculator.py

# Calculate comprehensive metrics for all 20 parts
python src/Task3/Part/Part_Based_All_Parts_Metrics.py
```

### Generating Layout Visualizations

```powershell
# Generate Part 1 layout (214×98 ft compact layout)
python src/Task3/Part/Part_Based_Year1_Layout_Generator.py
```

### Running Cost Analysis

```python
# Located in src/Task3/Part/Part_Cost_Analysis.py
# Reads: Part_Based_Equipment_Requirements.csv
# Outputs: 5 cost files + 2 visualizations
python src/Task3/Part/Part_Cost_Analysis.py
```

### Accessing Results

All output files are saved to:
```
results/Task3/Part/
├── Capacity/          # Capacity and metrics files
├── Cost_Analysis/     # Cost analysis files
└── Visuals/          # Layout visualizations
```

## Validation Checklist

✅ **Total Machine Count:** 432 (matches corrected capacity plan)  
✅ **Reliability Factor:** 88.2% applied to all calculations  
✅ **Equipment Specs:** Verified against Block_Specs.csv  
✅ **Process Sequences:** Match Parts_Step_Time.csv  
✅ **Demand Data:** From Part_Based_Weekly_Part_Demand.csv  
✅ **Overlap Rules:** Correctly applied per equipment group  
✅ **Flow Calculations:** Center-to-center Euclidean distances  
✅ **Duplicate Counting:** Process repetitions tracked (e.g., B twice in P1)  
✅ **Cost Analysis:** Based on 432 machines with 84.4% utilization  
✅ **File Naming:** Uniform Part_Based_* convention throughout  

## Strategic Recommendations

### 1. Space Optimization
- **KLM Equipment Advantage:** Parts P17-P20 achieve 45-60× better space efficiency
- **Recommendation:** Consider redesigning high-volume parts to use KLM processes where feasible
- **Potential Savings:** Significant reduction in facility footprint and rent costs

### 2. Material Handling Efficiency
- **High Flow Parts:** P1, P7, P14, P16 account for 50% of total weekly flow
- **Recommendation:** Prioritize automated material handling (AGVs, conveyors) for these parts
- **Expected Impact:** Reduce labor costs and cycle time

### 3. Capacity Bottlenecks
- **High Utilization Processes:** Process D (95.1%), M (97.0%) approaching capacity
- **Recommendation:** Add buffer capacity (+10-15% machines) for these processes
- **Risk Mitigation:** Prevent production delays due to machine downtime

### 4. Facility Layout Planning
- **Current Analysis:** Assumes each part has dedicated area (265,097 sq ft total)
- **Alternative Approach:** Share common processes (e.g., single B area for P1-P5)
- **Trade-off:** Reduced footprint (potential 30-40% savings) vs increased flow complexity

### 5. Investment Prioritization
- **Highest ROI:** Focus on parts with high demand and high margins
- **Phased Implementation:** Start with P1, P7, P14, P16 (highest volume)
- **Cost Avoidance:** Defer low-volume parts (P15, P17) if capital constrained

## References

### Input Data Files
- `data/csv_outputs/Parts_Step_Time.csv` - Processing times for all 20 parts
- `data/csv_outputs/Equip+Operator Specs.csv` - Equipment costs and operator requirements
- `results/task4/part/Jatin/Block_Specs.csv` - Authoritative equipment dimensions and overlaps

### Related Documentation
- `Logics/task3/TASK3_PARTS_BASED_STRATEGY.md` - Strategic overview
- `Logics/task3/TASK3_COMPLETE_SUMMARY.md` - Complete task 3 summary
- `results/Task3/Functional/` - Alternative functional layout organization
- `results/Task3/Fractal/` - Alternative fractal layout organization

### External Resources
- **Reliability Factor Discussion:** 88.2% = 90% efficiency × 98% reliability × 99% utilization
- **Compact Layout Algorithm:** Vertical stacking with GAP=0 optimization
- **Flow Distance Formula:** Euclidean distance for center-to-center calculation

## Contact & Support

For questions about this analysis or to request additional calculations:
- Review detailed reports in `Capacity/Part_Based_All_Parts_Detailed_Report.txt`
- Check executive summary in `Capacity/Part_Based_All_Parts_Executive_Summary.txt`
- Examine cost analysis in `Cost_Analysis/Part_Based_Layout_Cost_Analysis_Report.txt`

---

**Last Updated:** November 12, 2025  
**Analysis Version:** Year 1 (P1-P20)  
**Reliability Factor:** 88.2% (CORRECTED)  
**Total Machines:** 432  
**Total Investment:** $171,766,000
