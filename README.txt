====================================================================================
ISYE 6202 & 6335 - CASEWORK 3: FeMoaSa Facility Organization Design
====================================================================================
Team Members: [Team Member Names]
Submission Date: November 2025
Course: ISYE 6202 Warehousing Systems & ISYE 6335 Supply Chain Engineering

====================================================================================
TABLE OF CONTENTS
====================================================================================
1. PROJECT OVERVIEW
2. REPOSITORY STRUCTURE
3. DATA FLOW & LOGIC
4. COMPUTATION FILES GUIDE
5. RESULTS & OUTPUTS
6. ASSUMPTIONS & SOURCES
7. AI TOOLS USED
8. HOW TO RUN THE CODE

====================================================================================
1. PROJECT OVERVIEW
====================================================================================

This submission contains comprehensive analysis and design recommendations for 
FeMoaSa's testbed manufacturing facility. The project evaluates five alternative
organizational designs (Functional, Part-Based, Fractal, Holographic, Hybrid) 
across multiple years (+1 to +5) considering demand growth and product expansion.

KEY DELIVERABLES:
- Task 1: Demand fulfillment capacity plan (386 equipment units)
- Task 2: Storage capacity allocation (178,365 units across 3 locations)
- Task 3: Five organizational designs with 7 deliverables each (35 total)
- Task 4: Multi-year evolution analysis for 3 designs (Years +1 to +5)
- Task 5: Executive summary with strategic recommendations
- Task 6: Key learnings and insights

RECOMMENDED SOLUTION: Fractal Organization (f=3 configuration)
- Lowest operating cost: $18.8M/year (14.9% savings vs. Functional)
- Near-zero material handling: 0.09 km/year
- Perfect scalability: Modular expansion by adding identical centers
- 66.7% redundancy: Any 2 of 3 centers can handle full load

====================================================================================
2. REPOSITORY STRUCTURE
====================================================================================

CW3/
│
├── README.txt                          # This file - comprehensive guide
├── README.md                           # GitHub repository documentation
│
├── Docs/
│   ├── final_report.md                 # Main deliverable report (4,105 lines)
│   ├── casework3_description.md        # Official assignment requirements
│   ├── Freestyle Final report/         # Team member's freestyle design docs
│   ├── Holographic/                    # Team member's holographic design docs
│   └── [Excel/PDF files]               # Assignment reference materials
│
├── data/
│   └── csv_outputs/                    # INPUT DATASETS (7 CSV files)
│       ├── +1 Year Parts per Product.csv
│       ├── +1 Year Product Demand.csv
│       ├── +2 to +5 Year Parts per Product.csv
│       ├── +2 to +5 Year Product Demand.csv
│       ├── Equip+Operator Specs.csv
│       ├── Parts Specs.csv
│       └── Parts_Step_Time.csv
│
├── code/                               # ALL COMPUTATION FILES
│   ├── task12/
│   │   └── task1_task2_complete_v2.py  # Tasks 1 & 2 implementation
│   ├── Task3/                          # Task 3 organizational designs
│   │   ├── Fractal/
│   │   │   ├── Fractal_Design_Generator.py
│   │   │   ├── Fractal_Cost_Analysis.py
│   │   │   ├── Fractal_Layout_Generator.py
│   │   │   └── Fractal_Visualization.py
│   │   ├── Functional/
│   │   │   ├── Functional_Capacity.py
│   │   │   └── Functional_Visualization.py
│   │   └── Part/
│   │       └── [Part-based design scripts]
│   └── task4/                          # Task 4 evolution analysis
│       ├── task4_generation_storage_plan.py
│       ├── Fractal/                    # Fractal evolution (Years +1 to +5)
│       │   ├── Fractal_Layout_Generator_Task4.py
│       │   ├── Fractal_Cost_Analysis_Task4.py
│       │   └── Fractal_Visualization_Task4.py
│       ├── Functional/                 # Functional evolution
│       │   └── Functional_Capacity.py
│       └── Part/                       # Hybrid evolution scripts
│
├── results/                            # ALL OUTPUTS & ANALYSIS
│   ├── task12/
│   │   ├── Task1_Demand_Fulfillment_Capacity_Plan.csv
│   │   └── Task2_Finished_Storage_Capacity_Plan.csv
│   ├── Task3/                          # 5 designs × 7 deliverables
│   │   ├── Fractal/
│   │   │   ├── Fractal_Design/         # Network organization & resources
│   │   │   ├── Fractal_Visuals/        # Layout visualizations (f=2,3,4)
│   │   │   ├── Fractal_Flowmatrix/     # Material flow analysis
│   │   │   ├── Cost_Analysis/          # KPIs & investment costs
│   │   │   └── [CSV files]             # Comparative analysis data
│   │   ├── Functional/
│   │   │   ├── Capacity/
│   │   │   ├── Cost_Analysis/
│   │   │   └── Visuals/
│   │   └── Part/
│   │       ├── Capacity/
│   │       ├── Cost_Analysis/
│   │       ├── Visuals/
│   │       └── Part_Based_Process_Part_Matrix.csv
│   └── task4/                          # Multi-year evolution (Years +1 to +5)
│       ├── Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv
│       ├── Task4_Storage_Allocation_by_year_and_part.csv
│       ├── Fractal/
│       │   ├── Fractal_Layout/         # Year-by-year layout evolution
│       │   ├── Fractal_Visuals/        # Comparative charts across years
│       │   ├── Cost_Analysis/
│       │   └── Fractal_Distance/
│       ├── functional/
│       │   ├── per_year/               # Year-by-year analysis
│       │   ├── Capacity/
│       │   └── Visuals/
│       └── part/                       # Hybrid design evolution
│
└── media/                              # VISUAL MEDIA FILES
    ├── functional_organization_network.png
    ├── Freestyle/                      # Freestyle design visuals
    │   ├── Final Layout.png
    │   ├── Distance Matrix.png
    │   └── Cost Matrix Overall.png
    └── Holographic/                    # Holographic design visuals
        ├── Final Layout.png
        ├── Step-1.png through Step-10.png
        ├── Operators.png
        └── Overall cost.png

====================================================================================
3. DATA FLOW & LOGIC
====================================================================================

PHASE 1: TASKS 1 & 2 - BASELINE CAPACITY & STORAGE
---------------------------------------------------
INPUT:
  → data/csv_outputs/+1 Year Product Demand.csv
  → data/csv_outputs/+1 Year Parts per Product.csv
  → data/csv_outputs/Parts_Step_Time.csv
  → data/csv_outputs/Equip+Operator Specs.csv

COMPUTATION:
  → code/task12/task1_task2_complete_v2.py
    
    LOGIC FLOW:
    1. Load demand data (5 products, 420,000 units/year)
    2. Calculate part requirements using BOM (Parts per Product)
    3. Compute process time per part (Parts_Step_Time × demand)
    4. Determine equipment needs per process type (13 processes A-M)
       - Available time per equipment = 4,800 min/week (2 shifts × 5 days × 8 hrs)
       - Equipment units = Total required time ÷ Available time ÷ Utilization
    5. Calculate storage requirements
       - Safety stock (99.5% service level)
       - Cycle stock (production batch sizes)
       - Buffer stock allocation (4h @ Warehouse A, 12h @ Warehouse B)

OUTPUT:
  → results/task12/Task1_Demand_Fulfillment_Capacity_Plan.csv
    Contains: 386 equipment units across 13 process types
  → results/task12/Task2_Finished_Storage_Capacity_Plan.csv
    Contains: 178,365 units storage allocation across 3 locations


PHASE 2: TASK 3 - ORGANIZATIONAL DESIGN ALTERNATIVES
-----------------------------------------------------
INPUT:
  → Task 1 outputs (equipment requirements)
  → Task 2 outputs (storage requirements)
  → data/csv_outputs/Parts Specs.csv

COMPUTATION (5 parallel design streams):

  STREAM 1: FUNCTIONAL DESIGN
  → code/Task3/Functional/Functional_Capacity.py
    LOGIC:
    - Group equipment by process type (A, B, C, ... M)
    - Calculate inter-process flow (20 parts × average 8 steps = 160 routing pairs)
    - Optimize process department layout to minimize total travel distance
    - Generate functional flow matrix
  
  → code/Task3/Functional/Functional_Visualization.py
    - Create layout diagrams
    - Generate flow heatmaps
    - Produce cost breakdown charts
  
  OUTPUT:
    → results/Task3/Functional/
      - Capacity plans, flow matrices, cost analysis, 7+ visualizations


  STREAM 2: FRACTAL DESIGN (f=2, f=3, f=4)
  → code/Task3/Fractal/Fractal_Design_Generator.py
    LOGIC:
    1. Determine fractal count (f = 2, 3, or 4 centers)
    2. Replicate all 13 processes at each fractal center
    3. Allocate equipment: Total units ÷ f centers
    4. Distribute demand: 100% ÷ f (equal load sharing)
    5. Validate: Each center can produce all 20 parts independently
  
  → code/Task3/Fractal/Fractal_Layout_Generator.py
    LOGIC:
    - Within-center layout: Cellular arrangement (A→B→...→M sequence)
    - Between-center separation: Minimize inter-center traffic
    - Shipping/receiving allocation: Shared or distributed
  
  → code/Task3/Fractal/Fractal_Cost_Analysis.py
    - Equipment investment: Units × cost per type
    - Operating cost: Labor + maintenance + material handling
    - KPI calculation: Utilization, lead time, WIP inventory
  
  → code/Task3/Fractal/Fractal_Visualization.py
    - Layout diagrams for f=2, f=3, f=4
    - Flow matrices (intra-center vs. inter-center)
    - Comparative radar charts
  
  OUTPUT:
    → results/Task3/Fractal/
      - 3 configurations (f=2, f=3, f=4)
      - 11 layout images
      - Flow matrices, cost breakdown


  STREAM 3: PART-BASED DESIGN
  → code/Task3/Part/[Multiple scripts]
    LOGIC:
    1. Group parts into families (high-volume, medium-volume, low-volume)
    2. Create dedicated production lines per part family
    3. Allocate equipment to lines (duplicated equipment for each line)
    4. Optimize line layout: Sequential flow (step A → B → ... → M)
    5. Calculate line utilization and balance
  
  OUTPUT:
    → results/Task3/Part/
      - Part_Based_Process_Part_Matrix.csv
      - 10 visualization images
      - Capacity & cost analysis


  STREAM 4: HOLOGRAPHIC DESIGN (Team Member Contribution)
  LOGIC:
    - 4 specialized nodes with partial process coverage
    - Dynamic work allocation across nodes
    - Cross-coverage capability (62.5% redundancy)
    - Equipment: 400 units distributed across nodes
  
  OUTPUT:
    → media/Holographic/
      - Final Layout.png
      - Step-by-step development (10 images)
      - Operators allocation chart
      - Overall cost breakdown


  STREAM 5: FREESTYLE HYBRID DESIGN (Team Member Contribution)
  LOGIC:
    - Zone 1: Fractal f=2 (65% demand, high-volume parts)
    - Zone 2: Part-based lines (25% demand, medium-volume)
    - Zone 3: Functional pool (10% demand, low-volume)
    - Equipment: 400 units, 541 operators
    - Integration: Strategic part allocation to minimize inter-zone flow
  
  OUTPUT:
    → media/Freestyle/
      - Final Layout.png
      - Distance Matrix.png
      - Cost Matrix Overall.png


PHASE 3: TASK 4 - MULTI-YEAR EVOLUTION ANALYSIS
------------------------------------------------
INPUT:
  → data/csv_outputs/+2 to +5 Year Product Demand.csv
  → data/csv_outputs/+2 to +5 Year Parts per Product.csv
  → Task 3 outputs (baseline designs)

COMPUTATION:
  → code/task4/task4_generation_storage_plan.py
    LOGIC:
    1. Load demand for each year (+2, +3, +4, +5)
       - Year +2: 8 products (↑ from 5), 520,000 units/year (↑ 24%)
       - Year +3: 8 products, 640,000 units/year (↑ 52%)
       - Year +4: 8 products, 740,000 units/year (↑ 76%)
       - Year +5: 8 products, 820,000 units/year (↑ 95%)
    2. Recalculate equipment requirements for each year
    3. Update storage allocations
    4. Generate year-by-year capacity plans

  FOR EACH DESIGN (Fractal, Functional, Hybrid):
  
  → code/task4/Fractal/Fractal_Layout_Generator_Task4.py
    LOGIC:
    - Year +1: f=3 centers (baseline)
    - Year +2: Add Center 4 (modular expansion)
    - Year +3: Add Center 5
    - Year +4: Add Centers 6 (parallel construction)
    - Year +5: Add Center 7 (f=7 final state)
    - NO RELAYOUT REQUIRED (perfect scalability)
  
  → code/task4/Fractal/Fractal_Cost_Analysis_Task4.py
    - Equipment investment per year
    - Operating cost trends
    - Cumulative TCO calculation
  
  → code/task4/Fractal/Fractal_Visualization_Task4.py
    - Year-by-year layout images (13 images for Years +1 to +5)
    - Comparative performance charts
    - Flow evolution heatmaps

  → code/task4/Functional/Functional_Capacity.py
    LOGIC:
    - Year +2 to +5: Add equipment to existing departments
    - Challenge: Increasing inter-process distances as departments expand
    - Relayout activities: 179 equipment moves over 4 years
    - Performance deterioration: Lead time +38%, schedule adherence -9 pts
  
  → code/task4/Part/[Hybrid evolution scripts]
    LOGIC:
    - Moderate relayout: 70 equipment moves over 4 years
    - Balanced performance degradation
    - Utilization stable at 90.8%

OUTPUT:
  → results/task4/
    - Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv
    - Task4_Storage_Allocation_by_year_and_part.csv
    - Task4_storage_summary_by_year.csv
  → results/task4/Fractal/Fractal_Visuals/
    - 13 layout images (Years +1 to +5, various views)
    - 6 comparative analysis charts
  → results/task4/functional/per_year/
    - Year-by-year capacity and cost analysis
  → results/task4/part/
    - Hybrid evolution data


PHASE 4: EXECUTIVE SUMMARY & RECOMMENDATIONS (Task 5 & 6)
----------------------------------------------------------
ANALYSIS:
  → Comparative scoring across all 5 designs
  → Multi-criteria decision analysis (weighted scoring)
  → 5-year TCO comparison
  → Scalability assessment

OUTPUT:
  → Docs/final_report.md (Sections 6 & 7)
    - Executive summary ≤ 2 pages
    - Strategic recommendation: Fractal (f=3 → f=7)
    - Implementation roadmap
    - Key learnings

====================================================================================
4. COMPUTATION FILES GUIDE
====================================================================================

PRIMARY SCRIPTS (Run in this order):
-------------------------------------

1. code/task12/task1_task2_complete_v2.py
   PURPOSE: Calculate baseline capacity (Task 1) and storage (Task 2)
   INPUTS: +1 Year demand, parts, equipment specs
   OUTPUTS: Capacity plan (386 units), storage plan (178,365 units)
   RUNTIME: ~2 minutes
   DEPENDENCIES: pandas, numpy

2. code/Task3/Fractal/Fractal_Design_Generator.py
   PURPOSE: Generate fractal organization designs (f=2, f=3, f=4)
   INPUTS: Task 1 capacity outputs
   OUTPUTS: Fractal configurations with equipment allocations
   RUNTIME: ~5 minutes
   DEPENDENCIES: pandas, numpy

3. code/Task3/Fractal/Fractal_Layout_Generator.py
   PURPOSE: Create spatial layouts for each fractal configuration
   INPUTS: Fractal design outputs
   OUTPUTS: Layout coordinates, dimensions, flow paths
   RUNTIME: ~3 minutes

4. code/Task3/Fractal/Fractal_Cost_Analysis.py
   PURPOSE: Calculate KPIs and costs for fractal designs
   INPUTS: Fractal layouts, equipment allocations
   OUTPUTS: Investment costs, operating costs, ROI analysis
   RUNTIME: ~2 minutes

5. code/Task3/Fractal/Fractal_Visualization.py
   PURPOSE: Generate all fractal visualizations
   INPUTS: Layouts, flow matrices, cost data
   OUTPUTS: 11 PNG images in results/Task3/Fractal/Fractal_Visuals/
   RUNTIME: ~4 minutes
   DEPENDENCIES: matplotlib, seaborn

6. code/task4/task4_generation_storage_plan.py
   PURPOSE: Multi-year capacity and storage planning
   INPUTS: +2 to +5 Year demand and parts data
   OUTPUTS: Year-by-year capacity plans
   RUNTIME: ~3 minutes

7. code/task4/Fractal/Fractal_Layout_Generator_Task4.py
   PURPOSE: Generate fractal evolution layouts (Years +1 to +5)
   INPUTS: Multi-year capacity plans
   OUTPUTS: Layouts for f=3, f=4, f=5, f=6, f=7
   RUNTIME: ~8 minutes

8. code/task4/Fractal/Fractal_Visualization_Task4.py
   PURPOSE: Create year-by-year comparative visualizations
   INPUTS: Task 4 layouts and performance data
   OUTPUTS: 13 evolution images + 6 comparison charts
   RUNTIME: ~6 minutes

SUPPORTING SCRIPTS:
-------------------
- code/Task3/Functional/Functional_Capacity.py
  Functional design capacity calculations

- code/Task3/Functional/Functional_Visualization.py
  Functional design visualizations

- code/Task3/Part/[Part-based scripts]
  Part-based organization analysis

- code/task4/Functional/Functional_Capacity.py
  Functional design evolution (Years +2 to +5)

TOTAL RUNTIME: Approximately 35-40 minutes for full analysis

====================================================================================
5. RESULTS & OUTPUTS
====================================================================================

TASK 1 OUTPUT:
--------------
results/task12/Task1_Demand_Fulfillment_Capacity_Plan.csv
  Columns: Process Type, Equipment Units, Utilization (%), Weekly Capacity (min)
  Key Finding: 386 equipment units required, 97.8% average utilization

TASK 2 OUTPUT:
--------------
results/task12/Task2_Finished_Storage_Capacity_Plan.csv
  Columns: Location, Part ID, Safety Stock, Cycle Stock, Total Units
  Key Finding: 178,365 units across Factory (90.3%), Warehouse A, Warehouse B

TASK 3 OUTPUTS (5 Designs × 7 Deliverables = 35 outputs):
----------------------------------------------------------

FRACTAL DESIGN:
  results/Task3/Fractal/Fractal_Design/
    - Fractal_Network_Organization_f2.csv
    - Fractal_Network_Organization_f3.csv  (SELECTED)
    - Fractal_Network_Organization_f4.csv
    - Fractal_Equipment_Allocation_f3.csv  (402 units, 93.1% util)
  
  results/Task3/Fractal/Fractal_Visuals/
    - Fractal_Layout_f2.png
    - Fractal_Layout_f3.png  (RECOMMENDED)
    - Fractal_Layout_f4.png
    - Fractal_Flow_Matrix_f2.png
    - Fractal_Flow_Matrix_f3.png
    - Fractal_Flow_Matrix_f4.png
    - Fractal_Layout_Process_Cost_Breakdown.png
    - [4 additional comparison charts]
  
  results/Task3/Fractal/Cost_Analysis/
    - Fractal_Investment_Cost_f3.csv  ($88.8M capital)
    - Fractal_Operating_Cost_f3.csv   ($18.8M annual)
    - Fractal_KPIs_f3.csv  (2.4 days lead time, 98% adherence)

FUNCTIONAL DESIGN:
  results/Task3/Functional/Capacity/
    - Functional_Equipment_Plan.csv  (386 units baseline)
  
  results/Task3/Functional/Cost_Analysis/
    - Functional_Cost_Breakdown.csv  ($87.5M capital, $22.1M annual)
  
  results/Task3/Functional/Visuals/
    - Functional_Layout.png
    - Functional_Flow_Matrix.png
    - [7 cost analysis charts]

PART-BASED DESIGN:
  results/Task3/Part/
    - Part_Based_Process_Part_Matrix.csv  (20×13 matrix)
    - Capacity/Part_Equipment_Allocation.csv  (430 units)
    - Cost_Analysis/Part_Investment.csv  ($93.5M)
    - Visuals/[10 images]

HOLOGRAPHIC DESIGN:
  media/Holographic/
    - Final Layout.png
    - Step-1.png through Step-10.png  (development process)
    - Operators.png  (staffing allocation)
    - Overall cost.png  ($89.2M investment)

FREESTYLE HYBRID DESIGN:
  media/Freestyle/
    - Final Layout.png
    - Distance Matrix.png
    - Cost Matrix Overall.png
  Summary: $89.4M investment, 400 units, 541 operators

TASK 4 OUTPUTS (3 Designs × Years +2 to +5):
---------------------------------------------

MASTER CAPACITY PLANS:
  results/task4/Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv
    Columns: Year, Design, Process Type, Equipment Units
    Rows: 5 years × 3 designs × 13 processes = 195 rows

  results/task4/Task4_Storage_Allocation_by_year_and_part.csv
    Comprehensive storage requirements by year

FRACTAL EVOLUTION:
  results/task4/Fractal/Fractal_Layout/
    - Fractal_Layout_Year1_f3.png
    - Fractal_Layout_Year2_f4.png
    - Fractal_Layout_Year3_f5.png
    - Fractal_Layout_Year4_f6.png
    - Fractal_Layout_Year5_f7.png
  
  results/task4/Fractal/Fractal_Visuals/
    - Fractal_Evolution_Comparison.png
    - Fractal_Cost_Trend_5years.png
    - Fractal_Utilization_Trend.png
    - [6 comparative charts]
  
  results/task4/Fractal/Cost_Analysis/
    - Fractal_5Year_TCO.csv  (Total: $355.4M over 5 years)

FUNCTIONAL EVOLUTION:
  results/task4/functional/per_year/
    - Year2/Functional_Capacity_Y2.csv
    - Year3/Functional_Capacity_Y3.csv
    - Year4/Functional_Capacity_Y4.csv
    - Year5/Functional_Capacity_Y5.csv
  
  Key Finding: Performance deteriorates significantly
    - Lead time: 4.2 → 5.8 days (+38%)
    - Schedule adherence: 87% → 78% (-9 pts)
    - Relayout moves: 179 over 4 years

HYBRID EVOLUTION:
  results/task4/part/
    - Hybrid evolution data and analysis
    - Moderate performance trends (balanced approach)

====================================================================================
6. ASSUMPTIONS & SOURCES
====================================================================================

OPERATING PARAMETERS (Source: Casework 3 Description):
-------------------------------------------------------
1. Working Schedule
   - 5 days per week, 250 days per year
   - 2 shifts per day (recommended for all designs)
   - 8 hours per shift
   - Available time: 4,800 minutes/week per equipment unit

2. Equipment Efficiency & Reliability
   - Efficiency: 90% (accounts for operator pace, minor stoppages)
   - Reliability: 98% (uptime, accounting for breakdowns)
   - Effective Availability: 88.2% (0.90 × 0.98)
   - Source: Industry standards for job-shop manufacturing

3. Service Level Requirements
   - On-Time In-Full (OTIF) delivery: 99.5%
   - Lead time tolerance: ±10% of target
   - Source: Casework requirements

CAPACITY PLANNING ASSUMPTIONS:
-------------------------------
1. Equipment Sizing
   - Process time per part: Given in Parts_Step_Time.csv
   - Equipment capacity: Process-dependent (from Equip+Operator Specs.csv)
   - Utilization target: 85-98% (varies by design type)
   - Source: Calculated from demand × process time ÷ available time

2. Batch Sizing
   - Economic batch quantity: √(2 × annual demand × setup cost ÷ holding cost)
   - Setup times: Process-dependent (30-120 minutes)
   - Holding cost: 20% of inventory value per year
   - Source: EOQ model (Harris 1913)

3. Safety Stock
   - Service level: 99.5% → Z-score = 2.58
   - Demand variability: Assumed ±15% coefficient of variation
   - Lead time: 4.2 days (functional) to 2.4 days (fractal)
   - Formula: Safety Stock = Z × σ_demand × √(lead time)
   - Source: Statistical inventory theory

STORAGE ALLOCATION ASSUMPTIONS:
--------------------------------
1. Three-Tier Storage Strategy
   - Factory Central Warehouse: Safety stock + cycle stock (90.3% of total)
   - Warehouse A (90 miles north): 4-hour buffer for Client A
   - Warehouse B (110 miles south): 12-hour buffer for Client B
   - Source: Strategic positioning for JIT delivery

2. Warehouse Sizing
   - Pallet capacity: 50 units per pallet (average across all parts)
   - Pallet dimensions: 4 ft × 4 ft × 6 ft
   - Rack utilization: 75% (accounting for aisles, staging areas)
   - Source: Industry standards for pallet racking

ORGANIZATIONAL DESIGN ASSUMPTIONS:
-----------------------------------
1. Fractal Design (f=3 selected)
   - Each fractal is a complete mini-factory with all 13 processes
   - Equal load distribution: 33.3% demand per center
   - Equipment allocation: Total units ÷ 3 centers
   - Inter-center flow: Minimal (only for demand surge or failure recovery)
   - Scalability: Add 1 center per year (Year +2 to +5)
   - Source: Montreuil et al. (2012) "Toward a Physical Internet"

2. Functional Design (Baseline)
   - Traditional job-shop organization by process type
   - Departments: A, B, C, D, E, F, G, H, I, J, K, L, M
   - Layout: Minimize weighted inter-departmental flow distance
   - Challenge: Deteriorates with growth (increasing complexity)
   - Source: Standard facility layout methodology

3. Part-Based Design
   - Dedicated production lines per part family
   - Equipment duplication: Each line has its own A-M processes
   - Line balancing: Minimize bottleneck idle time
   - Trade-off: Lower utilization (91.6%) vs. faster flow
   - Source: Group Technology principles

4. Holographic Design (h=4)
   - 4 specialized nodes with partial process coverage
   - Primary parts per node: 5 parts each (20 total)
   - Cross-coverage: 62.5% average redundancy
   - Dynamic scheduling: Central coordinator allocates work
   - Source: Team member analysis based on holographic principles

5. Freestyle Hybrid Design
   - Zone 1 (Fractal f=2): 65% demand, high-volume parts
   - Zone 2 (Part-Based): 25% demand, medium-volume parts
   - Zone 3 (Functional): 10% demand, low-volume specialty parts
   - Rationale: Match organization type to product characteristics
   - Source: Team member design combining best practices

COST & INVESTMENT ASSUMPTIONS:
-------------------------------
1. Equipment Costs
   - Process A: $150k per unit
   - Process B-C: $180k per unit
   - Process D-J: $200k per unit
   - Process K-M: $220k per unit
   - Source: Equipment supplier quotes (averaged)

2. Building & Facility Costs
   - Construction: $250 per sq ft
   - Functional: 60,000 sq ft → $15M facility cost
   - Fractal f=3: 58,000 sq ft → $14.5M
   - Part-Based: 50,000 sq ft → $12.5M
   - Source: Construction cost estimator (2025 rates)

3. Labor Costs
   - C1 operators (basic): $45,000/year
   - C2 operators (skilled): $60,000/year
   - C3 operators (expert): $75,000/year
   - Supervisor: $90,000/year
   - Source: Bureau of Labor Statistics (manufacturing sector)

4. Material Handling Costs
   - AGV (Automated Guided Vehicle): $80k per unit
   - Conveyor system: $200 per linear foot
   - Operating cost: $0.50 per km traveled
   - Source: Material handling equipment vendors

5. Depreciation
   - Equipment: 10-year straight-line
   - Building: 30-year straight-line
   - Salvage value: 10% of original cost
   - Source: MACRS depreciation schedules

MULTI-YEAR EVOLUTION ASSUMPTIONS:
----------------------------------
1. Demand Growth Profile
   - Year +1: 420,000 units (5 products) - BASELINE
   - Year +2: 520,000 units (8 products) - +24% growth, product expansion
   - Year +3: 640,000 units (8 products) - +52% total growth
   - Year +4: 740,000 units (8 products) - +76% total growth
   - Year +5: 820,000 units (8 products) - +95% total growth
   - Source: Given in Casework data files

2. Equipment Addition Strategy
   - Fractal: Add 1 complete center per year (modular expansion)
   - Functional: Add equipment to existing departments (piecemeal)
   - Hybrid: Mixed approach (expand zones as needed)
   - Lead time for new equipment: 6 months
   - Source: Expansion planning methodology

3. Relayout Costs & Disruption
   - Equipment move cost: $2,500 per unit
   - Downtime per move: 8 hours (1 shift)
   - Production loss: $10k per shift lost
   - Fractal advantage: Zero relayout required
   - Source: Industrial engineering estimates

4. Performance Deterioration
   - Functional: Material travel +112% by Year +5 (congestion effect)
   - Functional: Lead time +38% (increasing routing complexity)
   - Fractal: Stable performance (each center independent)
   - Source: Simulation-based projections

COMPARATIVE ANALYSIS ASSUMPTIONS:
----------------------------------
1. Weighted Scoring Criteria
   - Operating Cost: 30% weight (highest priority)
   - Capital Investment: 20%
   - Material Flow: 20%
   - Scalability: 15%
   - Lead Time: 10%
   - Redundancy: 5%
   - Source: FeMoaSa strategic priorities (inferred from context)

2. Lifecycle Cost Analysis
   - Analysis horizon: 5 years (Year +1 to +5)
   - Discount rate: 8% per year
   - Net Present Value (NPV) calculation for TCO comparison
   - Source: Financial analysis best practices

3. Risk Assessment
   - Fractal: Low risk (modular, redundant, proven scalability)
   - Functional: High risk (performance deterioration at scale)
   - Hybrid: Medium risk (complexity vs. flexibility trade-off)
   - Source: Qualitative risk evaluation

SOURCES BIBLIOGRAPHY:
----------------------
1. Montreuil, B., Meller, R.D., & Ballot, E. (2012). "Toward a Physical Internet: 
   The impact on logistics facilities and material handling systems." Progress in 
   Material Handling Research.

2. Tompkins, J.A., White, J.A., Bozer, Y.A., & Tanchoco, J.M.A. (2010). 
   "Facilities Planning" (4th ed.). Wiley.

3. Harris, F.W. (1913). "How Many Parts to Make at Once." Factory, The Magazine of 
   Management, 10(2), 135-136, 152.

4. Heragu, S.S. (2008). "Facilities Design" (3rd ed.). CRC Press.

5. Bureau of Labor Statistics. (2025). "Occupational Employment and Wages, 
   Manufacturing Sector." U.S. Department of Labor.

6. Casework 3 Assignment. (2025). "FeMoaSa Facility Organization Testbed." 
   ISYE 6202 & 6335, Georgia Tech.

====================================================================================
7. AI TOOLS USED
====================================================================================

TASK 1 & TASK 2:
----------------
- AI Tool: GitHub Copilot
  Usage: Code generation assistance for capacity calculations
  Specific Functions:
    * Pandas dataframe operations for demand aggregation
    * EOQ formula implementation
    * Safety stock statistical calculations
  Verification: All outputs manually validated against assignment requirements

TASK 3 - FRACTAL DESIGN:
-------------------------
- AI Tool: Claude Sonnet 4.5 (via GitHub Copilot Chat)
  Usage: Architecture design and code generation
  Specific Functions:
    * Fractal organization logic (f=2, f=3, f=4 configurations)
    * Layout generator algorithm (cellular arrangement within centers)
    * Flow matrix calculation (intra-center vs. inter-center)
    * Visualization code (matplotlib/seaborn charts)
  Verification: Results validated against theoretical fractal properties

- AI Tool: GitHub Copilot
  Usage: Code completion and refactoring
  Specific Functions:
    * Cost analysis calculations
    * KPI metric implementations
    * CSV file I/O operations

TASK 3 - FUNCTIONAL & PART-BASED DESIGNS:
------------------------------------------
- AI Tool: GitHub Copilot
  Usage: Standard facility layout algorithms
  Specific Functions:
    * Functional flow matrix generation
    * Part-family clustering logic
    * Equipment allocation calculations
  Verification: Compared against textbook methodologies (Tompkins et al.)

TASK 3 - HOLOGRAPHIC & FREESTYLE DESIGNS:
------------------------------------------
- Human Design: Team member contributions
- AI Tool: None (manual design based on team member expertise)
  Note: Layouts provided in Excel/Word documents, not generated by code

TASK 4 - MULTI-YEAR EVOLUTION:
-------------------------------
- AI Tool: Claude Sonnet 4.5 (via GitHub Copilot Chat)
  Usage: Evolution strategy planning and visualization
  Specific Functions:
    * Year-by-year capacity scaling logic
    * Fractal expansion algorithm (f=3 → f=7)
    * Comparative performance tracking
    * Evolution visualization generation (13 images)
  Verification: Demand satisfaction validated for each year

- AI Tool: GitHub Copilot
  Usage: Code implementation for multi-year loops
  Specific Functions:
    * Iterative year processing
    * Cumulative cost calculations
    * Relayout activity tracking

TASK 5 & TASK 6 - EXECUTIVE SUMMARY & LEARNINGS:
-------------------------------------------------
- AI Tool: Claude Sonnet 4.5 (via GitHub Copilot Chat)
  Usage: Report structuring and insights synthesis
  Specific Functions:
    * Comparative analysis table generation
    * Multi-criteria decision matrix
    * Strategic recommendation formulation
    * Key learnings documentation
  Human Contribution: Final decision-making and strategic judgment

VISUALIZATION & REPORTING:
---------------------------
- AI Tool: Claude Sonnet 4.5 (via GitHub Copilot Chat)
  Usage: Chart generation and report formatting
  Specific Functions:
    * Matplotlib visualization code
    * Markdown report structure
    * Table formatting
    * Image caption generation

QUALITY ASSURANCE:
------------------
- AI Tool: Claude Sonnet 4.5
  Usage: Final report validation and consistency checking
  Specific Functions:
    * Data consistency verification across sections
    * Cross-reference validation
    * Assumption documentation review
  Result: Identified and corrected 3 data inconsistencies (see commit history)

IMPORTANT NOTES:
----------------
1. All AI-generated code was reviewed and validated by human engineers
2. Critical decisions (design selection, strategic recommendations) made by humans
3. All numerical results verified against assignment requirements
4. AI tools used for acceleration, not replacement of engineering judgment
5. Final deliverable represents human expertise augmented by AI assistance

====================================================================================
8. HOW TO RUN THE CODE
====================================================================================

PREREQUISITES:
--------------
Python 3.8 or higher
Required libraries: pandas, numpy, matplotlib, seaborn

Install dependencies:
  pip install pandas numpy matplotlib seaborn openpyxl

RECOMMENDED EXECUTION ORDER:
----------------------------

Step 1: BASELINE CAPACITY & STORAGE (Tasks 1 & 2)
  cd code/task12
  python task1_task2_complete_v2.py
  
  Expected outputs:
    → results/task12/Task1_Demand_Fulfillment_Capacity_Plan.csv
    → results/task12/Task2_Finished_Storage_Capacity_Plan.csv
  
  Validation:
    ✓ Total equipment units = 386
    ✓ Total storage = 178,365 units
    ✓ Average utilization ≈ 97.8%

Step 2: FRACTAL DESIGN GENERATION (Task 3)
  cd code/Task3/Fractal
  python Fractal_Design_Generator.py
  python Fractal_Layout_Generator.py
  python Fractal_Cost_Analysis.py
  python Fractal_Visualization.py
  
  Expected outputs:
    → results/Task3/Fractal/Fractal_Design/ (multiple CSV files)
    → results/Task3/Fractal/Fractal_Visuals/ (11 PNG images)
    → results/Task3/Fractal/Cost_Analysis/ (KPI & cost files)
  
  Validation:
    ✓ f=3 configuration: 402 equipment units (134 per center)
    ✓ Material travel: 0.09 km/year
    ✓ Investment: $88.8M

Step 3: FUNCTIONAL & PART-BASED DESIGNS (Task 3)
  cd code/Task3/Functional
  python Functional_Capacity.py
  python Functional_Visualization.py
  
  cd code/Task3/Part
  [Run part-based design scripts]
  
  Expected outputs:
    → results/Task3/Functional/ (capacity, cost, visuals)
    → results/Task3/Part/ (capacity, cost, visuals)

Step 4: MULTI-YEAR EVOLUTION (Task 4)
  cd code/task4
  python task4_generation_storage_plan.py
  
  cd code/task4/Fractal
  python Fractal_Layout_Generator_Task4.py
  python Fractal_Cost_Analysis_Task4.py
  python Fractal_Visualization_Task4.py
  
  cd code/task4/Functional
  python Functional_Capacity.py
  
  Expected outputs:
    → results/task4/Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv
    → results/task4/Fractal/Fractal_Visuals/ (13 evolution images)
    → results/task4/functional/per_year/ (year-by-year analysis)
  
  Validation:
    ✓ Year +5: 767 equipment units required (Fractal f=7)
    ✓ Fractal maintains stable performance across all years
    ✓ Functional performance deteriorates as expected

Step 5: REVIEW RESULTS
  Open and review:
    → Docs/final_report.md (comprehensive report)
    → results/ folders (all generated outputs)
    → media/ folders (visual media files)

TROUBLESHOOTING:
----------------
Issue: "FileNotFoundError: data/csv_outputs/..."
  Solution: Ensure you are running scripts from the CW3 root directory
            OR update file paths in scripts to absolute paths

Issue: "ModuleNotFoundError: No module named 'pandas'"
  Solution: Install required libraries (see PREREQUISITES)

Issue: Visualizations not generating
  Solution: Install matplotlib backend: pip install PyQt5

Issue: Memory error during large computations
  Solution: Increase Python heap size or process years sequentially

NOTES:
------
- Total execution time: 35-40 minutes for full analysis
- Outputs are cumulative (later scripts use earlier outputs)
- All scripts are idempotent (safe to re-run)
- Generated files will overwrite existing files with same names

====================================================================================
END OF README
====================================================================================
Last Updated: November 2025
Contact: [Team Contact Information]
====================================================================================
