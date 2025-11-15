# ISyE 6202 Casework 3 - FeMoaSa Facility Organization Testbed

## 📊 Project Overview

This repository contains a comprehensive analysis of manufacturing facility design alternatives for **FeMoaSa's new client-dedicated production facility**. The project analyzes multiple factory organization strategies (Functional, Part-Based, Fractal) across a 5-year timeline, evaluating capacity planning, storage requirements, material flow, and cost optimization.

**Course**: ISyE 6202, Fall 2025  
**Team**: Minjae Kim, Dominic Hose, Adarsh Uday, Jatin Patel, Benoit Morvan, Shankar Subramanian  
**Instructor**: Georgia Institute of Technology

---

## 🎯 Quick Start

### Final Deliverable
**[📄 Final Report](Docs/final_report.md)** - Complete thesis-level analysis with strategic recommendations

### Key Results
- **Task 1 Results**: [Demand Fulfillment Capacity Plan](results/task12/Task1_Demand_Fulfillment_Capacity_Plan.csv)
- **Task 2 Results**: [Storage Capacity Plan](results/task12/Task2_Finished_Storage_Capacity_Plan.csv)
- **Task 3 Results**: Layout comparisons in `results/Task3/`
- **Task 4 Results**: 5-year evolution plans in `results/task4/`

---

## 📁 Repository Structure

```
ISYE6202_CW3/
│
├── README.md                          # This file - Project documentation
│
├── data/                              # 📥 INPUT DATA
│   └── csv_outputs/                   # CSV files extracted from project PDF
│       ├── +1 Year Product Demand.csv
│       ├── +1 Year Parts per Product.csv
│       ├── +2 to +5 Year Product Demand.csv
│       ├── +2 to +5 Year Parts per Product.csv
│       ├── Parts Specs.csv            # Part dimensions & specifications
│       ├── Parts_Step_Time.csv        # Process times for each part
│       └── Equip+Operator Specs.csv   # Equipment specifications
│
├── src/                               # 💻 SOURCE CODE
│   ├── task12/                        # Task 1 & 2 implementations
│   │   └── task1_task2_complete_v2.py # Year +1 capacity & storage analysis
│   │
│   ├── Task3/                         # Task 3: Layout Alternatives (Year +1)
│   │   ├── Functional/                # Functional (Job-Shop) layout
│   │   │   ├── Functional_Capacity.py
│   │   │   ├── Functional_Flow_matrix.py
│   │   │   ├── Functional_Cost_Analysis.py
│   │   │   └── Functional_Visualization.py
│   │   │
│   │   ├── Fractal/                   # Fractal (Modular) layout
│   │   │   ├── Fractal_Design.py
│   │   │   ├── Fractal_Flow_Matrix.py
│   │   │   ├── Fractal_Cost_Analysis.py
│   │   │   ├── Fractal_Comparison_Analysis.py
│   │   │   └── Fractal_Visualization.py
│   │   │
│   │   └── Part/                      # Part-Based (Cellular) layout
│   │       ├── Part_Step_Capacity.py
│   │       ├── Part_Flow_Matrix.py
│   │       ├── Part_Cost_Analysis.py
│   │       ├── Part_Visualization.py
│   │       ├── optimize_grid_layouts.py
│   │       └── [20+ analysis scripts]
│   │
│   └── task4/                         # Task 4: 5-Year Evolution (Years +2 to +5)
│       ├── task4_generation_storage_plan.py  # Main storage & capacity script
│       ├── Functional/                # Functional layout scaling
│       ├── Fractal/                   # Fractal layout scaling
│       └── Part/                      # Part-based layout scaling
│           ├── create_task4_visualizations.py
│           ├── Part_Visualization_per_year.py
│           └── [Year-specific analysis scripts]
│
├── results/                           # 📊 OUTPUT RESULTS
│   ├── task12/                        # Year +1 baseline results
│   │   ├── Task1_Demand_Fulfillment_Capacity_Plan.csv
│   │   └── Task2_Finished_Storage_Capacity_Plan.csv
│   │
│   ├── Task3/                         # Layout comparison results (Year +1)
│   │   ├── Functional/
│   │   │   ├── Flow_Matrix_Summary.csv
│   │   │   ├── Functional_Flow_Matrix.csv
│   │   │   ├── Capacity/              # Equipment requirements
│   │   │   ├── Cost_Analysis/         # Capital & operating costs
│   │   │   └── Visuals/               # Charts & heatmaps
│   │   │
│   │   ├── Fractal/
│   │   │   ├── Organization_Design_Comparison.csv  # Key comparison table
│   │   │   ├── Fractal_Radar_Chart_Data.csv
│   │   │   ├── Fractal_Design/        # Equipment per fractal scenario (f=2,3,4,5)
│   │   │   ├── Cost_Analysis/         # Detailed cost breakdowns
│   │   │   ├── fractal_distance/      # Material travel distances
│   │   │   ├── Fractal_Flowmatrix/    # Flow matrices per scenario
│   │   │   └── Fractal_Visuals/       # Layout diagrams & comparisons
│   │   │
│   │   └── Part/
│   │       ├── Part_Based_Process_Part_Matrix.csv
│   │       ├── Analysis_Reports/      # Text summaries
│   │       ├── Capacity/              # Machine utilization
│   │       ├── Cost_Analysis/         # Cost comparisons
│   │       ├── Visuals/               # Layout visualizations
│   │       └── Documentation/         # Design decisions
│   │
│   └── task4/                         # 5-year evolution results
│       ├── Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv
│       ├── Task4_Storage_Allocation_by_year_and_part.csv
│       ├── Task4_storage_summary_by_year.csv
│       │
│       ├── Functional/
│       │   ├── AllYears_Flow_Matrix_Summary.csv
│       │   ├── per_year/              # Year-by-year breakdowns
│       │   ├── Capacity/
│       │   ├── Cost_Analysis/
│       │   └── Visuals/
│       │
│       ├── Fractal/
│       │   ├── Fractal_Design/        # Equipment scaling paths
│       │   ├── Fractal_Distance/      # Flow distance evolution
│       │   ├── Fractal_Flowmatrix/    # Flow matrices Years 2-5
│       │   ├── Fractal_Layout/        # Layout diagrams per year
│       │   ├── Cost_Analysis/         # Long-term cost projections
│       │   └── Fractal_Visuals/       # Scaling comparison charts
│       │
│       └── part/
│           ├── MASTER_INDEX.md        # Complete index of all Part-based results
│           ├── Year2/, Year3/, Year4/, Year5/  # Year-specific analyses
│           │   ├── Equipment_Summary_Table.csv
│           │   ├── Part_Based_Year*_All_Parts_Flow_Analysis.csv
│           │   ├── Optimized_Compact_Layout_Summary.csv
│           │   └── [Detailed breakdowns]
│           └── INDEX.txt
│
├── logics/                            # 📚 DOCUMENTATION & METHODOLOGY
│   ├── task12/
│   │   ├── SOLUTION_GUIDE_ENGLISH.md  # Detailed solution methodology
│   │   └── SOLUTION_GUIDE_KOREAN.md   # Korean version
│   │
│   ├── task3/
│   │   ├── TASK3_COMPLETE_SUMMARY.md  # Overview of all Task 3 work
│   │   ├── FRACTAL_ORGANIZATION_STRATEGY.md
│   │   ├── FRACTAL_IMPLEMENTATION_SUMMARY.md
│   │   ├── FRACTAL_QUICK_START.md
│   │   ├── TASK3_PARTS_BASED_STRATEGY.md
│   │   └── HYBRID_PARTS_GROUP_EXPLANATION.md
│   │
│   └── task4/
│       ├── COMPLETE_RECALCULATION_SUMMARY.md
│       └── task4_deemand_alloc.md
│
├── Docs/                              # 📄 REPORTS & DOCUMENTATION
│   ├── final_report.md                # 🎯 MAIN DELIVERABLE - Comprehensive report
│   ├── final_report_backup.md         # Backup version
│   ├── TASK4_FRACTAL_COMPREHENSIVE_REPORT.md
│   └── pdf_extracted_text.txt         # Original project requirements
│
├── extract_pdf.py                     # Utility to extract text from project PDF
├── Task1_Demand_Fulfillment_Capacity_Plan.csv  # Top-level results (Year +1)
└── Task2_Finished_Storage_Capacity_Plan.csv    # Top-level results (Year +1)
```

---

## 🔧 Project Tasks Breakdown

### Task 1: Demand Fulfillment Capacity Plan (Year +1)

**Objective**: Calculate equipment requirements to meet forecasted demand for Year +1.

**Key Script**: `src/task12/task1_task2_complete_v2.py`

**Process**:
1. Load product demand from `+1 Year Product Demand.csv`
2. Convert product demand to part demand using BOM (`+1 Year Parts per Product.csv`)
3. Calculate process workloads using `Parts_Step_Time.csv`
4. Determine equipment requirements per process (A-M) based on:
   - Operating schedule: 5 days/week, 2 shifts/day, 8 hours/shift
   - Equipment effectiveness: 88.2% (90% efficiency × 98% reliability)
   - Target utilization: Near 100%

**Key Outputs**:
- `results/task12/Task1_Demand_Fulfillment_Capacity_Plan.csv`
- **Total equipment needed**: 394 units across 13 processes
- **Bottleneck processes**: D (51 units), J (49 units), M (45 units)

**Key Findings**:
- Total annual demand: 10,270,000 units (197,500 units/week)
- Critical processes identified for capacity management
- Equipment distribution optimized for 2-shift operation

---

### Task 2: Finished Storage Capacity Plan (Year +1)

**Objective**: Design inventory strategy and calculate warehouse space requirements.

**Key Script**: `src/task12/task1_task2_complete_v2.py` (integrated with Task 1)

**Inventory Strategy** (Three-tier system):
1. **Safety Stock** (Factory): Protection against demand variability
   - Formula: `Z-score (2.576) × √(Lead Time) × StdDev(Demand)`
   - Service level: 99.5% OTIF

2. **Cycle Stock** (Factory): Operational inventory between production runs
   - Formula: `0.5 × Weekly Demand`

3. **Buffer Stock** (Near-client warehouses):
   - **Client A**: 4-hour buffer (90 miles North)
   - **Client B**: 12-hour buffer (110 miles South)

**Space Calculation**:
- Uses part dimensions from `Parts Specs.csv`
- Assumes 20-foot warehouse height
- 70% space utilization factor
- Converts volume to floor area requirements

**Key Outputs**:
- `results/task12/Task2_Finished_Storage_Capacity_Plan.csv`
- **Total units stored**: 178,365 units
  - Factory: 161,105 units
  - Warehouse A: 6,183 units
  - Warehouse B: 11,077 units
- **Total investment**: $13,624 for near-client warehouses

---

### Task 3: Alternative Factory Organization Design (Year +1)

**Objective**: Compare different factory layout strategies and recommend the optimal design.

**Three Main Approaches Analyzed**:

#### 3.1 Functional (Job-Shop) Layout

**Location**: `src/Task3/Functional/` → `results/Task3/Functional/`

**Concept**: Traditional layout grouping similar processes together (all 'A' machines in one area, all 'B' machines in another, etc.)

**Key Scripts**:
- `Functional_Capacity.py`: Equipment requirements
- `Functional_Flow_matrix.py`: Material flow between departments
- `Functional_Cost_Analysis.py`: Capital & operating costs
- `Functional_Visualization.py`: Layout heatmaps

**Key Outputs**:
- `Flow_Matrix_Summary.csv`: High inter-departmental flow (1,250,000 km/yr)
- `Functional_Flow_Matrix.csv`: Detailed flow matrix
- `Visuals/Functional_Flow_Matrix_Heatmap.png`: Visual "spaghetti diagram"

**Visualizations** (`Visuals/` folder):
- `Functional_Flow_Matrix_Heatmap.png`: Heat map showing complex inter-departmental material flow
- `Functional_Equipment_Summary.png`: Bar chart of equipment distribution across processes
- `Functional_Layout_Comprehensive_Analysis.png`: Multi-panel dashboard with KPIs
- `Functional_Layout_Cost_Analysis.png`: Cost breakdown by process and category
- `Functional_Layout_Cost_KPI_Dashboard.png`: Summary of key cost metrics
- `Functional_Layout_Cost_Efficiency_Matrix.png`: Cost-efficiency comparison matrix
- `Functional_Layout_Process_Cost_Comparison.png`: Process-level cost comparison
- `Functional_Layout_ROI_Analysis.png`: Return on investment analysis
- `Functional_Layout_Investment_Timeline_Analysis.png`: Investment timeline projection

**Characteristics**:
- ✅ Low initial investment (baseline)
- ✅ High equipment utilization
- ❌ Complex material flow
- ❌ High material handling costs
- ❌ Difficult to scale

---

#### 3.2 Fractal (Modular) Layout ⭐ RECOMMENDED

**Location**: `src/Task3/Fractal/` → `results/Task3/Fractal/`

**Concept**: Factory organized as `f` identical, self-contained "mini-factories" (fractal centers), each capable of producing all products with 1/f of total capacity.

**Key Scripts**:
- `Fractal_Design.py`: Equipment distribution across fractal centers
- `Fractal_Flow_Matrix.py`: Material flow within/between centers
- `Fractal_Cost_Analysis.py`: Cost analysis for f=2,3,4,5 scenarios
- `Fractal_Comparison_Analysis.py`: Multi-criteria comparison
- `Fractal_Visualization.py`: Layout diagrams

**Fractal Scenarios Evaluated**:
- **f=2**: Two centers, each handling 50% of demand
- **f=3**: Three centers, each handling 33.3% of demand
- **f=4**: Four centers, each handling 25% of demand ⭐ OPTIMAL
- **f=5**: Five centers, each handling 20% of demand

**Key Outputs**:
- `Organization_Design_Comparison.csv`: Comprehensive comparison table
- `Fractal_Design/Fractal_f*_Equipment_Requirements.csv`: Equipment per scenario
- `Cost_Analysis/Fractal_All_Scenarios_Cost_KPIs.csv`: Cost metrics
- `fractal_distance/`: Material travel distance analysis
- `Fractal_Visuals/Fractal_Layout_Scenario_Comparison.png`

**Visualizations** (`Fractal_Visuals/` folder):
- `Fractal_Layout_f2.png`, `f3.png`, `f4.png`: Physical layout diagrams for each fractal scenario
- `Fractal_Flow_Matrix_f2.png`, `f3.png`, `f4.png`: Flow matrices showing material movement patterns
- `Fractal_Layout_Scenario_Comparison.png`: Multi-criteria comparison across all scenarios
- `Fractal_Equipment_Comparison.png`: Equipment requirements comparison (f=2 to f=5)
- `Fractal_Layout_Equipment_Distribution.png`: Equipment allocation across fractal centers
- `Fractal_Layout_Efficiency_Frontier.png`: Efficiency frontier analysis
- `Fractal_Layout_Process_Cost_Breakdown.png`: Detailed cost breakdown by process

**Strategic Advantages**:
- ✅ **90% reduction** in material travel distance vs. Functional
- ✅ **$600,000 annual savings** in operating costs
- ✅ Modular, scalable design ("copy-paste" expansion)
- ✅ High redundancy and flexibility
- ✅ Simplified material flow (self-contained cells)
- ⚠️ Slightly higher initial investment (+1.6% to +4.9%)

---

#### 3.3 Part-Based (Cellular) Layout

**Location**: `src/Task3/Part/` → `results/Task3/Part/`

**Concept**: Dedicate production lines to specific part families, creating specialized cells.

**Key Scripts**:
- `Part_Step_Capacity.py`: Capacity per part line
- `Part_Flow_Matrix.py`: Material flow analysis
- `Part_Cost_Analysis.py`: Cost breakdowns
- `Part_Based_All_Parts_Metrics.py`: Aggregate metrics
- `optimize_grid_layouts.py`: Layout optimization
- `Part_Visualization.py`: Cell layout diagrams

**Hybrid Approach** (Recommended variant):
- **Group 1**: A-B-C-D Heavy Parts (P1-P6) - Complex routing
- **Group 2**: E-F-G Heavy Parts (P7-P16) - Secondary operations
- **Group 3**: K-L-M Light Parts (P17-P20) - Simple operations
- **Group 4**: Centralized support functions

**Key Outputs**:
- `Part_Based_Process_Part_Matrix.csv`: Process-part relationships
- `Cost_Analysis/Part_Based_Cost_KPIs.csv`: Cost summary
- `Capacity/`: Machine utilization per part
- `Visuals/`: Layout diagrams per part family
- `Documentation/README.md`: Design rationale

**Visualizations** (`Visuals/` folder):
- `Part_Based_Year1_Compact_Layout.png`: Optimized compact layout for Year 1
- `Year1_Part_Based_Layout_Schematic.png`: Detailed schematic with equipment placement
- `Year1_Part_Based_Comprehensive_Dashboard.png`: Multi-panel dashboard with metrics
- `Year1_Part_Based_Top10_Analysis.png`: Analysis of top 10 parts by volume
- `Part_Based_Analysis_Dashboard.png`: Overall analysis dashboard
- `Part_Based_Layout_Cost_Analysis.png`: Cost breakdown by part family
- `Part_Based_Layout_Cost_KPI_Dashboard.png`: Cost KPI summary

**Characteristics**:
- ✅ Reduced equipment duplication vs. pure part-based
- ✅ Simplified scheduling within groups
- ✅ Balanced flow efficiency
- ⚠️ Moderate complexity
- ⚠️ Less flexible than Fractal

---

### Task 4: Facility Evolution Plan (Years +2 to +5)

**Objective**: Project how each layout strategy scales over a 5-year growth period with new products (A4, B3, B4).

**Key Script**: `src/task4/task4_generation_storage_plan.py`

**Growth Scenario**:
- **Year 1**: 5 products (A1, A2, A3, B1, B2)
- **Year 2**: +1 product (A4) → 6 products
- **Year 3**: +1 product (B3) → 7 products
- **Year 4**: +1 product (B4) → 8 products
- **Year 5**: All 8 products at mature volumes

**Analysis Per Layout Type**:

#### 4.1 Functional Layout Evolution
**Location**: `src/task4/Functional/` → `results/task4/functional/`

**Scaling Strategy**: Add machines to existing departments as demand grows

**Key Outputs**:
- `per_year/Year*_Functional_Equipment_Summary.csv`
- `AllYears_Flow_Matrix_Summary.csv`: Flow complexity over time
- `Visuals/Functional_Utilization_Comparison_By_Year.png`

**Visualizations** (`functional/Visuals/` folder):
- `Functional_Utilization_Comparison_By_Year.png`: Equipment utilization trends Year 1-5
- `Functional_Equipment_Comparison_By_Process.png`: Process-level equipment growth
- `Functional_Layout_Summary_Dashboard.png`: Overall summary dashboard
- `Functional_Cost_Analysis_Overview.png`: 5-year cost projection

**Finding**: Material flow complexity increases dramatically with scale (❌ Poor scalability)

---

#### 4.2 Fractal Layout Evolution ⭐ BEST SCALING
**Location**: `src/task4/Fractal/` → `results/task4/Fractal/`

**Scaling Strategy**: Add identical fractal cells as demand grows

**Key Scripts**:
- Multiple fractal scenario analyzers for Years 2-5
- Cost and flow analysis per year
- Visualization generators

**Key Outputs**:
- `Fractal_Design/`: Equipment requirements per year & scenario
- `Fractal_Visuals/Fractal_Scaling_Comparison.png`: Clear scaling advantage
- `Fractal_Visuals/Fractal_Capital_Investment_Comparison.png`: Cost efficiency
- `Cost_Analysis/`: Long-term ROI analysis

**Visualizations** (`Fractal/Fractal_Visuals/` folder):
- `Fractal_Scaling_Comparison.png`: **KEY CHART** - Shows how Fractal scales linearly vs. Functional
- `Fractal_Capital_Investment_Comparison.png`: Capital investment trends Years 1-5
- `Fractal_Operating_Cost_Comparison.png`: Operating cost comparison across scenarios
- `Fractal_Cost_Efficiency_Analysis.png`: Cost-efficiency metrics over time
- `Fractal_Yearly_Equipment_Comparison.png`: Year-over-year equipment growth
- `Year2_Fractal_f2/f3/f4/f5_Layout.png`: Layout diagrams for Year 2 (all scenarios)
- `Year3_Fractal_f2/f3/f4/f5_Layout.png`: Layout diagrams for Year 3
- `Year4_Fractal_f2/f3/f4/f5_Layout.png`: Layout diagrams for Year 4
- `Year5_Fractal_f2/f3/f4/f5_Layout.png`: Layout diagrams for Year 5

**Finding**: Linear, predictable scaling with minimal disruption (✅ Excellent scalability)

---

#### 4.3 Part-Based Layout Evolution
**Location**: `src/task4/Part/` → `results/task4/part/`

**Scaling Strategy**: Expand part-family cells + add new cells for new products

**Key Outputs** (organized by year):
- `Year2/`, `Year3/`, `Year4/`, `Year5/` subdirectories
- Each year contains:
  - `Equipment_Summary_Table.csv`
  - `Part_Based_Year*_All_Parts_Flow_Analysis.csv`
  - `Part_Based_Year*_All_Parts_Layout_Summary.csv`
  - `Optimized_Compact_Layout_Summary.csv`
  - `region_block_counts.csv`
- `MASTER_INDEX.md`: Complete index of all Part-based results

**Key Visualizations**:
- Year-by-year layout evolution
- Flow distance breakdowns
- Machine usage patterns

**Finding**: Moderate scalability, balanced approach

---

## 🔍 Key Files & Their Interconnections

### Data Flow Diagram

```
[PDF Project Requirements]
        ↓
   [extract_pdf.py]
        ↓
[Docs/pdf_extracted_text.txt]
        ↓
   [Manual extraction]
        ↓
[data/csv_outputs/*.csv] ← INPUT DATA
        ↓
        ├─→ [src/task12/task1_task2_complete_v2.py]
        │           ↓
        │   [results/task12/Task1*.csv, Task2*.csv]
        │
        ├─→ [src/Task3/Functional/*.py]
        │           ↓
        │   [results/Task3/Functional/...]
        │
        ├─→ [src/Task3/Fractal/*.py]
        │           ↓
        │   [results/Task3/Fractal/...]
        │
        ├─→ [src/Task3/Part/*.py]
        │           ↓
        │   [results/Task3/Part/...]
        │
        └─→ [src/task4/task4_generation_storage_plan.py]
                    ↓
            [results/task4/Task4_*.csv]
                    ↓
            [src/task4/{Functional,Fractal,Part}/*.py]
                    ↓
            [results/task4/{functional,Fractal,part}/...]
                    ↓
                    ↓
        [All results feed into]
                    ↓
        [Docs/final_report.md] ← FINAL DELIVERABLE
```

### Critical File Dependencies

1. **Input Data** (`data/csv_outputs/`) - Source of truth for all calculations
   - Product demand → Drives capacity calculations
   - Parts per Product (BOM) → Translates product to part demand
   - Parts_Step_Time.csv → Defines process sequences
   - Parts Specs.csv → Enables volume/space calculations

2. **Base Calculations** (`src/task12/`)
   - Foundation for all layout comparisons
   - Establishes baseline equipment needs
   - Defines inventory strategy

3. **Layout Implementations** (`src/Task3/`)
   - Each layout type has parallel script structure
   - Common methodology, different organization logic
   - Results feed into comparative analysis

4. **Evolution Projections** (`src/task4/`)
   - Builds on Task 3 layouts
   - Tests scalability of each approach
   - Generates 5-year scenarios

5. **Methodology Documentation** (`logics/`)
   - Explains decision rationale
   - Provides calculation methodologies
   - Links theory to implementation

6. **Final Synthesis** (`Docs/final_report.md`)
   - Integrates all results
   - Provides strategic recommendations
   - Includes visualizations from `results/*/Visuals/`

---

## 🎓 Understanding the Analysis Approach

### Manufacturing Facility Design Problem

**Given**:
- 5 products (A1, A2, A3, B1, B2) growing to 8 products
- 20 unique parts (P1-P20)
- 13 manufacturing processes (A-M)
- Demand forecasts for 5 years
- Client service level requirements (99.5% OTIF)

**Question**: How should we organize the factory?

### Three Competing Philosophies

1. **Functional**: "Group similar machines together"
   - Pro: Efficient use of expensive equipment
   - Con: Parts travel long distances through the factory

2. **Part-Based**: "Create dedicated lines per part family"
   - Pro: Simplified flow for specific parts
   - Con: Equipment duplication, less flexible

3. **Fractal**: "Build identical mini-factories"
   - Pro: Scalable, flexible, simple material flow
   - Con: Some equipment redundancy

### Analysis Framework

Each layout is evaluated on:
- **Capital Investment**: Equipment & facility costs
- **Operating Costs**: Labor, material handling, maintenance
- **Material Flow**: Distance traveled, complexity
- **Flexibility**: Ability to handle demand changes
- **Scalability**: Ease of expansion

### Key Innovation: Fractal Design

The **Fractal** approach emerged as the winner because:
1. Each fractal center is self-contained → minimal inter-center flow
2. Scaling is simple → just add another identical center
3. Redundancy is built-in → if one center has issues, others compensate
4. Balance of efficiency and flexibility

---

## 📈 Key Results Summary

### Recommended Strategy: Fractal Organization (f=4)

**Year +1 (Initial)**:
- Equipment: 400 units across 4 fractal centers
- Investment: $86.3M (vs. $86.5M Functional)
- Operating Cost: $24.5M/year (vs. $25.1M Functional)
- Material Travel: 150,000 km/year (vs. 1,250,000 km Functional)

**Year +5 (Mature)**:
- Add 1-2 fractal centers as needed
- Linear cost scaling
- Predictable ROI

**Strategic Benefits**:
- $600,000 annual operating cost savings
- 90% reduction in material handling
- Superior scalability for growth
- Higher operational resilience

---

## 🛠️ How to Use This Repository

### For Team Members

1. **Understanding the Big Picture**:
   - Start with `Docs/final_report.md`
   - Review `logics/task*/` for methodology

2. **Reviewing Specific Tasks**:
   - Task 1/2: Check `src/task12/` and `results/task12/`
   - Task 3: Review layout-specific folders in `src/Task3/` and `results/Task3/`
   - Task 4: Examine `src/task4/` and `results/task4/`

3. **Finding Specific Results**:
   - All CSV outputs are in `results/`
   - Visualizations are in `results/*/Visuals/`
   - Cost analyses are in `results/*/Cost_Analysis/`

4. **Understanding Calculations**:
   - Python scripts in `src/` contain all calculation logic
   - Scripts are documented with comments
   - Cross-reference with `logics/` documentation

### For Instructors/Reviewers

1. **Quick Assessment**: Read `Docs/final_report.md`
2. **Methodology Verification**: Check scripts in `src/`
3. **Result Validation**: Review CSV files in `results/`
4. **Visual Evidence**: View charts in `results/*/Visuals/`

---

## 🔬 Technical Details

### Operating Parameters

- **Schedule**: 5 days/week, 2 shifts/day, 8 hours/shift (4,800 min/week)
- **Efficiency**: 90%
- **Reliability**: 98%
- **Effective Availability**: 88.2%
- **Service Level**: 99.5% (Z = 2.576)

### Calculation Formulas

**Equipment Requirements**:
```
Required_Units = ⌈Total_Weekly_Minutes / (4800 × 0.882)⌉
```

**Safety Stock**:
```
Safety_Stock = Z × √(Lead_Time) × StdDev(Weekly_Demand)
```

**Cycle Stock**:
```
Cycle_Stock = 0.5 × Weekly_Demand
```

**Buffer Stock**:
```
Buffer_Stock = (Buffer_Hours / Hours_per_Week) × Weekly_Demand
```

**Floor Space**:
```
Floor_Area = Total_Volume / (Height × Utilization_Factor)
```

---

## 📚 Documentation Guide

### Primary Documentation

1. **`Docs/final_report.md`**: Complete analysis report
   - Executive summary
   - Detailed task breakdowns
   - Strategic recommendations
   - Visualizations embedded

2. **`logics/task12/SOLUTION_GUIDE_ENGLISH.md`**: Detailed methodology
   - Step-by-step calculations
   - Formula derivations
   - Decision criteria

3. **`logics/task3/TASK3_COMPLETE_SUMMARY.md`**: Task 3 overview
   - Layout strategy explanations
   - Equipment requirements
   - Comparative analysis

4. **`logics/task3/FRACTAL_ORGANIZATION_STRATEGY.md`**: Fractal methodology
   - Mathematical foundation
   - Design principles
   - Implementation guide

5. **`logics/task4/COMPLETE_RECALCULATION_SUMMARY.md`**: Task 4 evolution
   - Year-by-year projections
   - Scaling strategies
   - Machine requirements

### Result-Specific Documentation

- **Part-Based**: `results/Task3/Part/Documentation/README.md`
- **Part-Based Index**: `results/task4/part/MASTER_INDEX.md`
- **Fractal Report**: `Docs/TASK4_FRACTAL_COMPREHENSIVE_REPORT.md`

---

## 🏆 Key Contributions by Task

### Task 1 & 2: Foundation
- Established baseline equipment requirements
- Defined inventory strategy
- Calculated warehouse space needs
- **Output**: 394 equipment units, 3-tier inventory system

### Task 3: Layout Comparison
- Implemented 3 layout strategies
- Conducted multi-criteria analysis
- Generated comparative visualizations
- **Output**: Fractal f=4 recommended as optimal

### Task 4: Future Planning
- Projected 5-year growth scenarios
- Tested scalability of each layout
- Validated Fractal superiority long-term
- **Output**: Clear scaling roadmap

---

## 🎯 Final Recommendation

**Adopt Fractal Organization (f=4) for FeMoaSa's new facility.**

This recommendation is based on:
- Quantitative analysis of costs, flow, and capacity
- Qualitative assessment of flexibility and risk
- Long-term strategic value for the business

The Fractal design provides the optimal balance of:
- ✅ Operational efficiency
- ✅ Capital efficiency
- ✅ Scalability
- ✅ Resilience
- ✅ Future-proofing

---

## 📜 License & Usage

This repository contains academic work for ISyE 6202. All analysis, code, and documentation are the intellectual property of the team members and Georgia Institute of Technology.

**For Academic Use**: Please cite appropriately if referencing this work.

---

**Last Updated**: November 14, 2025  
**Repository Status**: Complete - Final Submission Ready

---

## 🚀 Next Steps for Users

1. **Read the Final Report**: Start with [`Docs/final_report.md`](Docs/final_report.md)
2. **Explore Visualizations**: Browse `results/*/Visuals/` folders
3. **Review Calculations**: Examine Python scripts in `src/`
4. **Understand Methodology**: Read documentation in `logics/`
5. **Validate Results**: Cross-check CSV outputs in `results/`

**Questions?** Review the methodology documents in `logics/` or examine the source code with inline comments.
