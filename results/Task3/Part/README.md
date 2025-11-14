# Task 3: Part-Based Factory Layout Organization

## Overview

This folder contains the complete **Part-Based Layout Analysis** for ISYE 6202 Case Study 3. This approach assigns each of the 20 parts (P1-P20) its own dedicated manufacturing area, optimizing material flow within each part's production line.

## Key Results Summary

- **Total Machines:** 432 (with 88.2% reliability factor)
- **Total Manufacturing Area:** 265,097 sq ft (6.08 acres)
- **Total Capital Investment:** $171,766,000
- **Annual Operating Cost:** $52,291,200/year
- **Total Operators:** 547.2 FTEs
- **Average Utilization:** 84.4%

## Folder Structure

```
Part/
├── README.md                          # This file
├── Part_Based_Process_Part_Matrix.csv # Process-part relationship matrix
│
├── Analysis_Reports/                  # Analysis outputs and summaries
│   ├── Part_Based_Summary_Report.txt
│   ├── PART_RESULTS_SCAN_REPORT.txt
│   └── PART_RESULTS_SCAN_SUMMARY.csv
│
├── Capacity/                          # Capacity planning and equipment requirements
│   ├── Part_Step_Machines_Summary_1_shifts.csv
│   ├── Part_Step_Machines_Summary_2_shifts.csv
│   ├── Part_Based_Equipment_Requirements.csv
│   ├── Part_Based_Process_Workload_Breakdown.csv
│   ├── Part_Based_All_Parts_Flow_Distance_Breakdown.csv
│   ├── Part_Based_All_Parts_Layout_Summary.csv
│   ├── Part_Based_All_Parts_Flow_Analysis.csv
│   ├── Part_Based_All_Parts_Machine_Usage.csv
│   ├── OPTIMIZED_Equipment_Requirements.csv
│   ├── OPTIMIZED_Utilization_Matrix_2_shifts.csv
│   └── [Additional capacity files]
│
├── Cost_Analysis/                     # Cost breakdowns and financial analysis
│   ├── Part_Based_Capital_Costs_Detailed.csv
│   ├── Part_Based_Operating_Costs_Detailed.csv
│   ├── Part_Based_Depreciation_Analysis.csv
│   ├── Part_Based_Layout_Cost_Analysis_Report.txt
│   └── REGENERATION_SUMMARY.txt
│
├── Documentation/                     # Project documentation and summaries
│   ├── README.md                      # Detailed project documentation
│   ├── BRIEF_SUMMARY_FOR_SHARING.txt  # Executive summary
│   ├── CLEANUP_SUMMARY.txt            # File cleanup history
│   ├── RESTRUCTURING_SUMMARY.txt      # Folder reorganization history
│   └── Part_Based_Year1_Documentation.txt
│
├── Scripts/                           # Python calculation and generation scripts
│   ├── Part_Based_Year1_P1_Capacity_Calculator.py
│   ├── Part_Based_Year1_All_Processes_Calculator.py
│   ├── Part_Based_Year1_Layout_Generator.py
│   └── Part_Based_Year1_Metrics_Calculator.py
│
├── Visuals/                          # Charts, dashboards, and layout visualizations
│   ├── Part_Based_Analysis_Dashboard.png
│   ├── Part_Based_Year1_Compact_Layout.png
│   ├── Part_Based_Layout_Cost_Analysis.png
│   ├── Part_Based_Layout_Cost_KPI_Dashboard.png
│   ├── Year1_Dashboard.png
│   ├── Year1_Part_Based_Comprehensive_Dashboard.png
│   └── [Additional visualization files]
│
├── originals_backup_20251114_1200/   # Backup of original files before cleaning
│   ├── Part_Based_All_Parts_Flow_Distance_Breakdown.csv
│   ├── Part_Based_Process_Workload_Breakdown.csv
│   ├── Part_Step_Machines_Summary_1_shifts.csv
│   └── Part_Step_Machines_Summary_2_shifts.csv
│
└── summary_archive/                   # Archived summary files
    └── Part_Based_Cost_KPIs.csv
```

## Key Data Files

### Core Analysis
- **Part_Based_Process_Part_Matrix.csv** - Shows which processes (A-M) are used by each part

### Capacity Planning (Capacity/)
- **Part_Step_Machines_Summary_2_shifts.csv** - Machine requirements per part/step (2-shift operation)
- **Part_Based_Equipment_Requirements.csv** - Total equipment needs by process type (432 machines)
- **OPTIMIZED_Equipment_Requirements.csv** - Optimized machine counts (375 machines, 88.9% utilization)
- **Part_Based_All_Parts_Layout_Summary.csv** - Layout dimensions and area for all 20 parts
- **Part_Based_All_Parts_Flow_Distance_Breakdown.csv** - Step-by-step flow distances for each part

### Cost Analysis (Cost_Analysis/)
- **Part_Based_Capital_Costs_Detailed.csv** - $171.8M capital investment breakdown
- **Part_Based_Operating_Costs_Detailed.csv** - $52.3M annual operating costs
- **Part_Based_Depreciation_Analysis.csv** - $12.6M annual depreciation

### Analysis Reports (Analysis_Reports/)
- **Part_Based_Summary_Report.txt** - Comprehensive summary with key insights
- **PART_RESULTS_SCAN_REPORT.txt** - Data quality scan results for all CSV files

## Equipment Specifications

| Group | Processes | Width | Depth | Overlap | Shareable Sides |
|-------|-----------|-------|-------|---------|-----------------|
| ABCD  | A, B, C, D | 14 ft | 14 ft | 2 ft | Front, Left, Right |
| EFG   | E, F, G | 22 ft | 15 ft | 0 ft | None |
| HIJ   | H, I, J | 14 ft | 36 ft | 0 ft | None |
| KLM   | K, L, M | 3 ft | 6 ft | 1 ft | Left, Right |

## Reliability & Capacity Parameters

- **Machine Efficiency:** 90%
- **Reliability:** 98%
- **Effective Availability:** 88.2% (90% × 98%)
- **Working Hours:** 99 hours/week (2 shifts)
- **Effective Capacity:** 4,191.3 minutes/week per machine

## Data Quality

All CSV files in the Capacity/ folder have been cleaned:
- Duplicate rows removed
- Missing numeric values filled with 0
- Original files backed up in `originals_backup_20251114_1200/`

## Quick Start

1. Review **Documentation/BRIEF_SUMMARY_FOR_SHARING.txt** for executive overview
2. Examine **Capacity/Part_Step_Machines_Summary_2_shifts.csv** for machine requirements
3. Check **Cost_Analysis/Part_Based_Layout_Cost_Analysis_Report.txt** for financial analysis
4. View **Visuals/Part_Based_Analysis_Dashboard.png** for visual summary

## Scripts Usage

All Python scripts are in `Scripts/` folder:

```bash
# Calculate Part 1 capacity
python Scripts/Part_Based_Year1_P1_Capacity_Calculator.py

# Calculate all processes capacity
python Scripts/Part_Based_Year1_All_Processes_Calculator.py

# Generate layout visualization
python Scripts/Part_Based_Year1_Layout_Generator.py

# Calculate comprehensive metrics
python Scripts/Part_Based_Year1_Metrics_Calculator.py
```

## Notes

- **Reorganization Date:** November 14, 2025
- **Data Cleaning Date:** November 14, 2025
- **Original Backups:** Stored in `originals_backup_20251114_1200/`
- **Archived Files:** Small summary files moved to `summary_archive/`

For detailed reorganization history, see `Documentation/RESTRUCTURING_SUMMARY.txt` and `Documentation/CLEANUP_SUMMARY.txt`.
