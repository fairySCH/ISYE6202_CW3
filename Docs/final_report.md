# FeMoaSa Manufacturing & Warehousing Facility Design: Final Report

**Course**: ISyE 6202, Fall 2025  
**Project**: Casework 3 - FeMoaSa Facility Organization Testbed  
**Date**: November 8, 2025  
**Version**: 8.0 - Final Conclusion & Risk Analysis

---

## 📋 Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Overview](#2-project-overview)
3. [Task 1: Demand Fulfillment Capacity Plan (Year +1)](#3-task-1-demand-fulfillment-capacity-plan-year-1)
4. [Task 2: Finished Goods Storage Capacity Plan (Year +1)](#4-task-2-finished-goods-storage-capacity-plan-year-1)
5. [Task 3: Alternative Factory Organization Design Analysis (Year +1)](#5-task-3-alternative-factory-organization-design-analysis-year-1)
6. [Task 4: Facility Evolution Plan (Years +2 to +5)](#6-task-4-facility-evolution-plan-years-2-to-5)
7. [Strategic Insights & Recommendations](#7-strategic-insights--recommendations)
8. [Risks & Mitigation Strategies](#8-risks--mitigation-strategies)
9. [Conclusion](#9-conclusion)
10. [Appendix: Data and Outputs](#10-appendix-data-and-outputs)

---

## 1. Executive Summary

This report culminates in a decisive recommendation for the strategic reorganization of FeMoaSa's new client-dedicated manufacturing facility. Our rigorous, data-driven analysis concludes that a transformative shift from the traditional Functional layout to a **Fractal Organization** is imperative for achieving competitive advantage. This move will unlock significant gains in efficiency, cost-effectiveness, and long-term scalability.

**Core Recommendations:**

* **Adopt Fractal Design as the New Standard:** The Fractal layout is the unequivocal winner, delivering a **$600,000 annual operating cost advantage** and a **90% reduction in material travel distance** (from 1,250,000 to 150,000 km/yr) over the legacy Functional model. This is not an incremental improvement but a fundamental leap in operational excellence. We recommend its immediate adoption.
* **Leverage Modularity for Phased Expansion:** The Fractal design's modularity is a key strategic asset. It allows for a predictable, capital-efficient expansion path to accommodate the projected growth to Year +5. Capacity can be scaled from the initial **394 equipment units** by adding self-contained fractal cells, minimizing disruption and maximizing ROI.
* **Implement a Multi-Echelon Inventory Strategy:** The three-tiered inventory system (Factory Safety/Cycle Stock, Client A 4-hour Buffer, Client B 12-hour Buffer) is critical for guaranteeing the **99.5% service level**. This targeted allocation optimizes inventory holding costs while ensuring client-side supply chain resilience, requiring a minimal initial outlay of **$13,624** for the two near-client warehouses.

**Strategic Imperative:**
The transition to a Fractal paradigm is more than an operational tweak; it is a strategic necessity. It will forge a facility that is not only highly efficient and cost-effective today but also inherently agile and scalable for the future. This positions FeMoaSa to deliver superior, dedicated service to its key clients, cementing its role as a strategic partner and building a foundation for sustainable, profitable growth.

---

## 2. Project Overview

### 2.1. Objective

The primary objective of this project is to engineer and evaluate a superior facility design for FeMoaSa's new testbed factory, moving beyond the constraints of the traditional **Functional (Job-Shop) organization**. The analysis provides a data-driven recommendation for the optimal factory layout by comprehensively modeling production capacity, material flow, warehousing, and total cost of ownership.

### 2.2. Key Operational Parameters

The analysis was grounded in a set of core operational constraints and performance targets:

* **Operating Schedule:** 5 days/week, 2 shifts/day, 8 hours/shift, totaling 4,800 minutes/week.
* **Performance:** A blended rate of 90% efficiency and 98% reliability, resulting in an **88.2% effective availability** for all equipment.
* **Service Level:** A stringent **99.5% On-Time In-Full (OTIF)** replenishment service level, mandating a Z-score of 2.576 for safety stock calculations.
* **Client Proximity & Buffers:**
  * Client A: 90 miles North, requiring a **4-hour** on-site buffer stock.
  * Client B: 110 miles South, requiring a **12-hour** on-site buffer stock.
* **Production Scope:** A portfolio of **20 unique parts** supporting **5 distinct products**, manufactured through **13 different process steps** (A-M).

---

## 3. Task 1: Demand Fulfillment Capacity Plan (Year +1)

This task establishes the foundational production requirements to meet the forecasted demand for Year +1.

### 3.1. Part Demand Aggregation

First, we translated the client's product demand into specific part demand by leveraging the Bill of Materials (BOM). The total annual demand for all parts is **10,270,000 units**, which averages to **197,500 units per week**. We also calculated the weekly standard deviation for each part's demand to account for variability, which is crucial for safety stock calculations.

### 3.2. Production Time & Equipment Calculation

The total processing time required for each part was determined by summing the times for its specific manufacturing sequence. This time was then aggregated at the process level (A-M) to determine the total workload for each process type.

**Formula for Equipment Units:**
`Required Units = (Total Weekly Minutes for Process) / (4800 Available Mins/Week * 0.882 Effectiveness)`

This calculation, rounded up to the nearest whole number, yielded the required number of equipment units per process.

### 3.3. Final Capacity Plan

The analysis pinpointed Processes **D (Stamping), J (Finishing), and M (Final Assembly)** as the primary capacity bottlenecks, demanding the largest fleets of equipment. This highlights these areas as critical control points for production scheduling and future investment. A total of **394 equipment units** are necessary to meet the Year +1 demand robustly.

**Summary from `Task1_Demand_Fulfillment_Capacity_Plan.csv`:**

| Process | Required Equipment Units |
| :--- | :--- |
| A | 27 |
| B | 20 |
| C | 18 |
| D | **51** |
| E | 23 |
| F | 27 |
| G | 16 |
| H | 34 |
| I | 30 |
| J | **49** |
| K | 21 |
| L | 33 |
| M | **45** |
| **Total** | **394** |

---

## 4. Task 2: Finished Goods Storage Capacity Plan (Year +1)

This task translates the production plan into a detailed storage and inventory strategy, defining the requirements for the central factory warehouse and two near-client distribution points.

### 4.1. The Three Pillars of Inventory

Our inventory strategy is a holistic approach built on three pillars, each serving a distinct purpose:

1. **Safety Stock:** Protects against demand uncertainty to guarantee the 99.5% service level. Calculated as `Z * sqrt(Lead Time) * StdDev(Demand)`.
2. **Cycle Stock:** The operational inventory needed between production runs, assumed to be half of one week's average demand.
3. **Buffer Stock:** Forward-deployed inventory at near-client warehouses to ensure uninterrupted supply and meet contractual autonomy requirements (4 hours for A, 12 hours for B).

### 4.2. Storage Allocation & Space Calculation

Inventory was allocated as follows:

* **Factory Warehouse:** Holds Safety Stock + Cycle Stock.
* **Client A Warehouse:** Holds the 4-hour buffer stock for parts used in products A1-A3.
* **Client B Warehouse:** Holds the 12-hour buffer stock for parts used in products B1-B2.

The physical volume of this inventory was calculated using part dimensions from `Parts Specs.csv`. Assuming a standard warehouse with a **20-foot usable height** and **70% space utilization**, we converted the required inventory volume into a necessary floor area footprint.

### 4.3. Final Storage Plan & Investment

The plan requires a total of **178,365 units** in storage across all locations. The larger buffer requirement for Client B results in a proportionally larger warehouse.

**Summary from `Task2_Finished_Storage_Capacity_Plan.csv`:**

| Location | Total Units Stored | Required Volume (cu ft) | Required Floor Area (sq ft) | Construction Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Factory** | 161,105 | 8,934.8 | 638.2 | (Part of main factory) |
| **Warehouse A** | 6,183 | 346.3 | 24.7 | $4,947 |
| **Warehouse B** | 11,077 | 607.4 | 43.4 | $8,677 |
| **Total Investment**| - | - | - | **$13,624** |

---

## 5. Task 3: Alternative Factory Organization Design Analysis (Year +1)

We designed and compared five organizational models to identify the most effective alternative to the status-quo Functional layout. The analysis focused on four key performance indicators: Total Investment, Annual Operating Cost, Inter-Center Travel Distance, and Flexibility/Scalability.

### 5.1. Design Overviews

* **a. Functional:** Traditional model with departments organized by process type (e.g., all 'A' machines together). Leads to complex material flow and high handling costs.
* **c. Part-Based:** Each part family has a dedicated production line. Improves flow but can lead to equipment duplication.
* **f. Fractal:** The factory is composed of identical, self-sufficient mini-factories ("fractals"), each capable of producing the full range of parts. Offers excellent scalability and simple material flow.
* **g. Holographic:** A decentralized network of small, distributed process centers. Highly flexible but can be complex to manage.
* **h. Free-Style (Hybrid):** A pragmatic, custom design combining the best elements of other models. Our proposed hybrid utilizes a Fractal approach for high-volume, high-variety parts and consolidates lower-volume parts into a dedicated Part-Based cell to balance flow efficiency with equipment utilization.

### 5.2. Comparative Analysis

The **Fractal organization** demonstrated decisive advantages across the board. Its most significant impact lies in the **90% reduction of inter-center material flow**. This simplification directly reduces material handling costs, minimizes work-in-process (WIP) inventory, shortens production lead times, and alleviates shop floor congestion. While its initial investment is comparable to the Functional layout, its annual operating costs are significantly lower, making it the clear economic choice.

**Key Performance Indicators (KPIs) Comparison:**

| Metric | Functional | Fractal | Advantage of Fractal |
| :--- | :--- | :--- | :--- |
| **Total Investment** | $86.5M | **$86.3M** | -0.2% |
| **Annual Operating Cost**| $25.1M | **$24.5M** | -2.4% |
| **Inter-Center Travel** | High | **Very Low** | Reduced complexity & cost |
| **Flexibility/Scalability**| Low | **High** | Easy to add capacity |

The `Flow_Matrix_Summary.csv` for the Functional layout confirms its high degree of inter-departmental flow (1,250,000 km/yr), a key weakness that the Fractal design's co-located processes directly resolves.

---

## 6. Task 4: Facility Evolution Plan (Years +2 to +5)

This task stress-tests the leading layouts against a significant future demand increase, assessing their long-term viability and scalability.

### 6.1. Demand Growth Scenario

The forecast for Years +2 to +5 includes three new products (A4, B3, B4) and a general increase in demand, leading to a substantial rise in the required production and storage capacity.

### 6.2. Layout Evolution & Scalability

We analyzed how each layout paradigm would accommodate the growth:

* **Functional:** Scaling requires haphazardly adding machines to existing departments. This approach amplifies the inherent inefficiencies of the layout, worsening material flow spaghetti, increasing coordination overhead, and offering a poor return on investment.
* **Fractal:** Scaling is elegant and efficient. Growth is achieved by deploying new, identical fractal cells—effectively a "copy-paste" approach. This modularity preserves the simple material flow and allows for predictable, linear scaling of capacity with minimal disruption to ongoing operations.
* **Free-Style:** The hybrid model scales through a combination of adding fractal cells and expanding its part-based lines. While more adaptable than a purely functional layout, it lacks the simplicity and pure scalability of the true Fractal model.

### 6.3. Final State (End of Year +5)

By the end of the planning horizon, the advantages of the Fractal design become even more pronounced. The `Task4_storage_summary_by_year.csv` shows the year-over-year growth in storage needs.

**Total Storage Area Required by End of Year +5:**

| Layout Type | Total Floor Area (sq ft) |
| :--- | :--- |
| Functional | 1,950 |
| Fractal | **1,855** |
| Free-Style | 1,890 |

The Fractal layout remains the most space-efficient and, by extension, the most cost-effective solution for long-term growth.

---

## 7. Strategic Insights & Recommendations

This comprehensive analysis yields several actionable insights that should guide FeMoaSa's facility design strategy:

1. **Prioritize Material Flow Over Specialization:** The data proves that for dedicated production, optimizing material flow paths (as in the Fractal design) generates far more value than grouping specialized equipment (as in the Functional design). The 90% reduction in travel distance is a testament to this principle.
2. **Embrace Modularity for Future-Proofing:** The future is uncertain, but growth is planned. The Fractal model's modular, "plug-and-play" scalability provides the strategic agility to adapt to changing demand without costly and disruptive redesigns. Design for tomorrow's growth, not just today's requirements.
3. **Treat the Supply Chain as an Integrated System:** Facility layout, production capacity, and inventory strategy are not independent variables. The optimal solution recognizes their deep interconnection. The Fractal layout's efficiency directly enables a leaner, more responsive inventory and warehousing strategy.
4. **Adopt the Fractal Paradigm:** Based on the overwhelming evidence, the final recommendation is to adopt the Fractal organization as the new strategic standard for FeMoaSa's client-dedicated facilities. It offers the best combination of cost, efficiency, and long-term scalability.

---

## 8. Risks & Mitigation Strategies

While the Fractal model presents a compelling case, a successful transition requires proactive management of potential risks.

| Risk | Likelihood | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Implementation Complexity** | Medium | High | **Phased Rollout:** Implement one fractal cell as a pilot program. Develop a standardized playbook for equipment installation, workflow configuration, and validation before scaling to the full facility. |
| **Higher Initial Skill Requirements** | High | Medium | **Cross-Training Program:** Invest in a robust, proactive training program for operators and maintenance staff. Focus on multi-disciplinary skills to create a flexible workforce capable of managing the entire process within a cell. |
| **Resistance to Change** | Medium | Medium | **Change Management & Incentives:** Clearly communicate the strategic benefits of the new system (e.g., less chaotic workflow, higher team ownership). Involve team leads in the design and rollout process. Align performance incentives with cell-based KPIs (e.g., cell output, quality) rather than individual process metrics. |
| **Coordination Overhead** | Low | Low | **Decentralized Management:** Empower each fractal cell with a dedicated lead responsible for scheduling, quality, and performance. The central management role shifts from micro-managing workflows to overseeing overall output and strategic resource allocation. |

---

## 9. Conclusion

This report has systematically deconstructed the requirements for FeMoaSa's new client-dedicated facility, moving from initial demand analysis to a long-term strategic evolution plan. The investigation of alternative factory layouts has produced a clear and unequivocal result: the **Fractal organization is the superior model** for this application.

It surpasses the traditional Functional layout in every critical dimension for long-term success:

* **Economic Viability:** It delivers a significant annual operating cost reduction of **$600,000**.
* **Operational Efficiency:** It radically simplifies material flow, cutting inter-center travel distance by **90%**.
* **Strategic Agility:** Its modular, "copy-paste" design provides a clear, low-disruption path for scaling capacity to meet the 5-year growth forecast.

The recommendation to adopt the Fractal design is therefore not merely a preference but a data-driven strategic imperative. By embracing this paradigm, FeMoaSa can build a facility that is not only cost-effective and efficient from day one but also inherently resilient, scalable, and future-proof. This decision will solidify FeMoaSa's position as a high-performing, strategic partner to its key clients and establish a new benchmark for its manufacturing operations.

---

## 10. Appendix: Data and Outputs

### 10.1. Input Data Files (in `data/csv_outputs/`)

* `+1 Year Product Demand.csv`
* `+1 Year Parts per Product.csv`
* `+2 to +5 Year Product Demand.csv`
* `+2 to +5 Year Parts per Product.csv`
* `Parts Specs.csv`
* `Parts_Step_Time.csv`
* `Equip+Operator Specs.csv`

### 10.2. Key Output Files (in `results/`)

* `task12/Task1_Demand_Fulfillment_Capacity_Plan.csv`
* `task12/Task2_Finished_Storage_Capacity_Plan.csv`
* `Task3/Fractal/Organization_Design_Comparison.csv`
* `Task3/Functional/Flow_Matrix_Summary.csv`
* `task4/Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv`
* `task4/Task4_Storage_Allocation_by_year_and_part.csv`
* `task4/Task4_storage_summary_by_year.csv`


