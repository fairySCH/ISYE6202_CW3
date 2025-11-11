## 6. Task 4: Facility Evolution Plan (Years +2 to +5)

This task stress-tests the leading layouts against a significant future demand increase, assessing their long-term viability and scalability.

### 6.1. Demand Growth Scenario

Approach (same as Task 1 & 2). We mirror the Task-1/Task-2 workflow: product-level forecast (including new A4, B3, B4 from Year+1 to Year+5) are translated to part demand via the BOM, weekly viariability is carried through to part-level standard deviations, and we size capacity minutes using each part's total process time adjusted by the same 88.2% effective availability (90% efficiency x 98% reliability). Safety stocj is computed at a 99.5% service level (Z=2.576) with one week of lead time, identical assumptions to earlier tasks.

* **Weekly demand** rises from 197,500 units (Year 1) to 394,200 units (Year 5), so 2x.
* **Required capacity** incresases from 1.92M to 3.62M min/week, so +88%. 
* **Total safety stock** grows from 62.4k to 105.8k units, so 70%.

**Year-5 drivers (parts)**.
* **Highest weekly demand**: P19  (31.5k/wk), P1 (29.8k), P12 (29.8k), P11 (27.8k), P3 (26.9k)
* **Largest capacity minutes**: P1 (430.8k), P19 (375.0k), P3 (289.7k), P20 (233.1k), P12 (202.7k)
* **Largest safety stock**: P11 (9.3k), P12 (8.3k), P19 (7.5k), P1 (7.4k), P16 (6.8k)

Fastest-growing parts (weekly demand, Y5 vs Y1)
* P8 (4.33x), P15 (4.29x), P3 (3.37x), P17 (2.72x), P11 (2.44x) lead the acceleration.

| Year | Total Weekly Demand (units) |Required Capacity (min/ wk) | Total Safety Stocks (units) |
| :--- | :--- | :--- | :--- |
| **Year 1** | 197,500 | 1,924,876 | 62,355 |
| **Year 2**| 290,500 | 2,748,583 | 75,220 |
| **Year 3** | 321,600 | 3,012,783 | 82,109 |
| **Year 4**| 352,700 | 3,276,984 | 90,884 |
| **Year 5**| 394,200| 3,621,003 | 105,751 |

Demand roughly doubles over five years, and capacity minutes scale slightly less than linearly beacause the mix shifts toward parts with different process-time profiles. 

We keep the same three-tier inventory structure: (i) **Safety** stock sized to a 99.5% service level, (ii) **Cycle stock** = 1/2 of one week's average part demand, held centrally, and (iii) **client buffers** foward deployed at Warehouse A (4-hour autonomy) and Warehouse B (12-hour autonomy). In code, cycle stock is weekly_demand/2, factory storage is safety + cycle, and client buffers are computed from BOM-based hourly part demand multiplied by the autonomy hours. Physical space uses part cube (cu ft), then concerts to floor area with 20 ft ckear height, and 70% utilization; warehouse building vost is $200/sq ft.

| Year | Total Weekly Units (all locations) | Factory floor (sq ft) | WH-A floor (sq ft) | WH-B floor (sq ft) |
| :--- | :--- | :--- | :--- |:--- |
| **Year 1** | 178,365 | 657 | 25.5 | 44.4 |
| **Year 2**| 247,875 | 901 | 34.1 | 75.3 |
| **Year 3** | 275,089 | 1,000 | 34.3| 94.8 |
| **Year 4**| 304,189 | 1,105 | 34.5 | 114.4 |
| **Year 5**| 345,351 | 1,258 | 36.4 | 135.1 |

* The factory footprint grows +91% (656 -> 1,258 sq ft) as safety + cycle stock scale with demand.
* Client buffers rise steadily, with Warehouse B growing the most (94.8 -> 135.1 sq ft, +43% from Y3 -> Y5) due to the longue 12-hour autonomy requirement.

The storage plan scales predictably with demand: factory holdinfs (safety + cycle) drive most of the footprint growth, while foward buffers, especially at B, expand with the mix that feeds B-side products. 

