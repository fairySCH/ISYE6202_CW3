# Task 3: Parts-Based Design - Strategy & Analysis Summary

## Overview
This document outlines the strategy and results for Task 3c: Parts-Based Organization design for the FeMoaSa manufacturing facility.

## Strategy for Parts-Based Design

### Concept
In a **parts-based organization**, the factory is organized as a network of part-dedicated centers, where:
- Each part (P1 through P20) has its own dedicated production cell
- Each cell contains all the equipment and processes needed to manufacture that specific part
- Material flows are simplified as each cell is self-contained
- Receiving, storage, and shipping can be included in each cell or centralized

### Calculation Methodology

#### Step 1: Calculate Weekly Part Demand
For each part P1-P20, we calculate weekly demand using:
```
Weekly_Part_Demand = Σ (Weekly_Product_Demand[product] × BOM[part][product])
                     for all products
```

Where:
- Weekly product demand comes from the Year +1 forecast (A1, A2, A3, B1, B2)
- BOM (Bill of Materials) specifies how many of each part goes into each product

#### Step 2: Identify Process Requirements
For each part, we identify:
- **Process sequence**: The ordered steps (e.g., P1: B→A→B→C→D→I→J)
- **Process times**: Minutes per unit at each step
- **Total workload**: Weekly_Part_Demand × Process_Time_Per_Unit

#### Step 3: Aggregate by Process Type
We calculate how many operations of each process (A through M) occur weekly:
```
Process_Frequency[process] = Σ Weekly_Part_Demand[part]
                             for all parts using that process

Process_Workload[process] = Σ (Weekly_Part_Demand[part] × Process_Time[part, step])
                            for all parts and steps using that process
```

#### Step 4: Calculate Equipment Requirements
Available capacity per equipment unit:
```
Capacity = Days/Week × Shifts/Day × Hours/Shift × 60 × Efficiency × Reliability
         = 5 × Shifts × 8 × 60 × 0.90 × 0.98
         = 2,116.8 minutes/week (1 shift)
         = 4,233.6 minutes/week (2 shifts)
```

Equipment needed:
```
Equipment_Required = CEILING(Process_Workload / Capacity_Per_Unit)
Utilization = Process_Workload / (Equipment_Required × Capacity_Per_Unit)
```

## Key Results

### Weekly Operations Summary
| Metric | Value |
|--------|-------|
| Total parts manufactured | 20 |
| Total active processes | 13 (A-M) |
| Total operations per week | 952,500 |
| Total weekly part demand | 197,076 units |

### Equipment Requirements (2-Shift Operation Recommended)

| Process Group | Processes | Equipment Units | Weekly Hours |
|---------------|-----------|-----------------|--------------|
| **A-B-C-D** (Primary) | A, B, C, D | 108 units | 7,436 hrs |
| **E-F-G** (Secondary) | E, F, G | 60 units | 3,845 hrs |
| **H-I-J** (Finishing) | H, I, J | 120 units | 8,411 hrs |
| **K-L-M** (Light) | K, L, M | 98 units | 6,765 hrs |
| **TOTAL** | | **386 units** | **26,457 hrs** |

### Top 5 Bottleneck Processes
1. **Process J**: 55 units @ 99.0% utilization (3,844 hrs/week)
2. **Process M**: 55 units @ 99.5% utilization (3,861 hrs/week)
3. **Process D**: 50 units @ 99.8% utilization (3,521 hrs/week)
4. **Process B**: 36 units @ 98.1% utilization (2,491 hrs/week)
5. **Process L**: 35 units @ 97.5% utilization (2,409 hrs/week)

### High-Demand Parts
| Part | Weekly Demand | Process Sequence | Total Steps |
|------|---------------|------------------|-------------|
| P1 | 20,962 units | B→A→B→C→D→I→J | 7 steps |
| P19 | 20,000 units | L→M→L→M | 4 steps |
| P14 | 18,077 units | E→F→G→H | 4 steps |
| P20 | 14,808 units | L→K→M | 3 steps |
| P7 | 13,846 units | E→F→C→D→I→J | 6 steps |

## Parts-Based Design Implementation

### Option 1: Pure Parts Cells (20 Dedicated Cells)
**Advantages:**
- Complete isolation of material flows per part
- Simplified scheduling (each cell manages its own part)
- Easy to track WIP and quality by part
- Scalable (can add/remove part cells independently)

**Disadvantages:**
- Equipment duplication (386 total units distributed across 20 cells)
- Some cells will have very low utilization for certain processes
- Higher capital investment
- More floor space required

### Option 2: Hybrid Parts-Process Centers
**Recommended Approach:**

Create 4 part groups based on process similarity:

#### Group 1: A-B-C-D Heavy Parts (P1-P6)
- Parts: P1, P2, P3, P4, P5, P6
- Total weekly demand: 58,462 units
- Shared processes: A(12), B(18), C(10), D(25)
- Dedicated area with A-B-C-D equipment cluster

#### Group 2: E-F-G Heavy Parts (P7-P16)
- Parts: P7, P8, P9, P10, P11, P12, P13, P14, P15, P16
- Total weekly demand: 89,231 units
- Shared processes: E(23), F(27), G(10), plus H(17), I(15), J(28)
- Largest group - consider 2 sub-cells

#### Group 3: K-L-M Parts (P17-P20)
- Parts: P17, P18, P19, P20
- Total weekly demand: 51,731 units
- Shared processes: K(8), L(35), M(55)
- Compact group with similar lightweight operations

#### Group 4: Complex Multi-Process Parts
- Parts requiring processes across multiple groups
- Hybrid routing through group centers

### Space and Layout Considerations

**Equipment Footprints** (from PDF specs):
- A-B-C-D category: 14'×14' each (196 sq ft per unit)
- E-F-G category: 14'×14' each (196 sq ft per unit)
- H-I-J category: 14'×36' or 22'×15' (varies, ~330-504 sq ft per unit)
- K-L-M category: 7'×8' each (56 sq ft per unit)

**Estimated Total Floor Space** (2-shift operation):
- Equipment footprint: ~80,000 sq ft
- Aisles and material handling (2×): ~160,000 sq ft
- Storage, receiving, shipping: ~40,000 sq ft
- **Total factory floor**: ~280,000 sq ft

### Material Flow Design

**Centralized Support Functions:**
- **Receiving Center**: Weekly material kits for all parts
- **Materials Storage**: 2-week inventory (99.9% service level)
- **Finished Goods**: Outbound staging before shipping to clients A & B
- **Shipping**: Hourly to Client A, every 4 hours to Client B

**Cell-Level:**
- Each cell receives weekly material kit deliveries
- WIP storage within cell (minimal)
- Completed parts to finished goods staging

## Process Frequency Analysis

### Most Frequent Processes
| Process | Operations/Week | % of Total | Primary Parts |
|---------|-----------------|------------|---------------|
| I | 105,000 | 11.0% | P1, P3, P5, P6, P7, P8, P9, P10, P11, P12, P13, P16 |
| J | 98,462 | 10.3% | P1, P2, P3, P6, P7, P8, P9, P10, P12, P15, P16 |
| E | 83,462 | 8.8% | P7, P8, P9, P10, P11, P11, P12, P13, P14, P15 |
| G | 83,462 | 8.8% | P4, P9, P11, P11, P12, P13, P13, P14, P15 |
| L | 71,731 | 7.5% | P17, P18, P19, P19, P20 |

### Process-Part Incidence Matrix
Shows which processes are used by which parts:
- **Most versatile processes**: I (12 parts), J (11 parts)
- **Most complex part**: P6 (uses 7 different processes)
- **Simplest parts**: P19 (2 processes), P11, P17 (3 processes each)

## Strategic Recommendations

### 1. Shift Strategy
**Recommend 2-SHIFT operation:**
- Reduces equipment count from 763 to 386 units (49% reduction)
- Average utilization: 96.0%
- Saves significant capital investment
- Allows flexibility for maintenance during off-shifts

### 2. Organization Type
**Recommend Hybrid Parts-Group Design** (not pure parts-based):
- Group similar parts to share equipment
- Reduces duplication while maintaining flow benefits
- 3-4 major group centers instead of 20 individual cells
- Balance between equipment efficiency and material flow simplicity

### 3. Equipment Flexibility
**Consider multi-process equipment where available:**
- ABCD combo equipment (reduce from 108 to ~30 units)
- EFG combo equipment (reduce from 60 to ~20 units)
- IJ combo equipment (reduce from 86 to ~40 units)
- KLM combo equipment (reduce from 98 to ~20 units)
- **Potential reduction to ~200 total units** with 40% cost savings

### 4. Capacity Management
**Focus areas:**
- Processes D, J, M are critical bottlenecks (>99% utilization)
- Plan preventive maintenance carefully
- Consider 10% capacity buffer for critical processes
- Monitor parts P1, P19, P14 (highest demand)

### 5. Scalability
**Design for Year +2 to +5 expansion:**
- Modular cell design allows adding capacity
- Reserve floor space for additional equipment
- Plan electrical and utility infrastructure for growth

## Next Steps for Full Task 3 Design

1. **Layout Design**: Create detailed floor plans for each center
2. **Material Handling**: Design AGV/conveyor systems between centers  
3. **Operator Planning**: Calculate staffing requirements (C1, C2, C3 operators)
4. **Cost Analysis**: Total capital investment and operating costs
5. **Performance Metrics**: Calculate lead times, WIP, throughput
6. **Comparison**: Benchmark against function-based and other designs

## Files Generated

1. `Task3_Parts_Based_Equipment_Requirements.csv` - Detailed equipment needs
2. `Task3_Weekly_Part_Demand.csv` - Demand for each part
3. `Task3_Process_Frequency.csv` - Operations count by process
4. `Task3_Process_Workload_Breakdown.csv` - Detailed workload by part & process
5. `Task3_Process_Part_Matrix.csv` - Incidence matrix
6. `Task3_Parts_Based_Summary_Report.txt` - Executive summary
7. `Task3_Parts_Based_Analysis_Dashboard.png` - Visualizations

---

**Document prepared for:** FeMoaSa Manufacturing Facility Design  
**Course:** ISyE 6202 Supply Chain Facilities  
**Analysis Date:** November 2025
