# Fractal Organization Strategy - Methodology & Design Approach

## Overview
A **Fractal Organization** is a factory organized as a network of `f` fractal centers, where each center is capable of making **all products** with approximately `1/f` of the overall demand satisfaction capacity.

## Key Concept

### What is a Fractal Center?
- A self-similar, self-contained production unit that can manufacture **all products** (A1, A2, A3, B1, B2)
- Each fractal center is a "mini-factory" with all necessary processes (A through M)
- Load is distributed evenly: each center handles ~1/f of total demand
- All centers are identical in capability but may differ in scale

### Mathematical Foundation

```
Number of Fractal Centers: f (design parameter, typically 2-5)
Capacity per Center: 1/f of total factory capacity
Demand per Center: 1/f of total weekly demand

Each center must have:
- All 13 processes (A, B, C, D, E, F, G, H, I, J, K, L, M)
- Equipment scaled to handle 1/f of total workload
- Capability to produce all 5 products
- Capability to manufacture all 20 parts
```

## Design Methodology

### Step 1: Determine Number of Fractal Centers (f)

Consider:
- **f = 2**: Two identical centers, each handling 50% of demand
- **f = 3**: Three identical centers, each handling 33.3% of demand
- **f = 4**: Four identical centers, each handling 25% of demand
- **f = 5**: Five identical centers, each handling 20% of demand

Selection criteria:
1. **Load balancing**: Easier with more centers
2. **Redundancy**: More centers = better fault tolerance
3. **Layout efficiency**: Fewer centers = less duplication overhead
4. **Flexibility**: More centers = easier to handle demand fluctuations

### Step 2: Calculate Equipment Requirements per Center

For each process (A through M) and each fractal center:

```python
# From parts-based analysis, we know total weekly workload
Total_Workload[process] = sum of (Weekly_Part_Demand × Process_Time) for all parts

# Divide by number of fractal centers
Workload_per_Center[process] = Total_Workload[process] / f

# Calculate equipment needed per center
Equipment_per_Center[process] = ceil(Workload_per_Center[process] / Capacity_per_Equipment)

# Total equipment needed across all centers
Total_Equipment[process] = Equipment_per_Center[process] × f
```

**Key Insight**: Total equipment may be slightly higher than centralized design due to rounding up at each center.

### Step 3: Create Flow Matrix per Center

Each fractal center has its own internal flow matrix showing part movements between processes:

```python
# Each center handles 1/f of the demand for each part
Part_Demand_per_Center[part] = Total_Weekly_Part_Demand[part] / f

# Flow between processes i and j in one center
Flow[i][j] = sum of (Part_Demand_per_Center[part]) 
             for all parts that transition from process i to j
```

### Step 4: Aggregate Flow Matrix (Factory Level)

Total flow across all fractal centers:
```python
Total_Flow[i][j] = Flow_per_Center[i][j] × f
```

This should equal the flow matrix from the parts-based design.

### Step 5: Layout Considerations

**Within Each Fractal Center**:
- Arrange processes to minimize material handling
- Use flow matrix to optimize process adjacency
- Include local storage for WIP (work-in-process)

**Between Fractal Centers**:
- Option A: Centralized receiving/shipping for all centers
- Option B: Each center has its own receiving/shipping
- Option C: Hybrid approach

## Advantages of Fractal Organization

1. **Scalability**: Easy to add/remove centers based on demand
2. **Fault Tolerance**: If one center fails, others continue operating
3. **Load Balancing**: Distribute work evenly across centers
4. **Flexibility**: Each center can adapt independently
5. **Learning**: Knowledge transfers between similar centers
6. **Modularity**: Standardized design replicates across centers

## Disadvantages

1. **Equipment Duplication**: May need more total equipment than functional design
2. **Space Requirements**: Multiple sets of all processes
3. **Complexity**: Coordinating multiple centers
4. **Setup Costs**: Higher initial investment

## Recommended Values for f

Based on the FeMoaSa case:
- **f = 2**: Good for redundancy, simple coordination
- **f = 3**: Balanced approach, good fault tolerance
- **f = 4**: High flexibility, quarter-capacity modules

We'll analyze multiple scenarios (f = 2, 3, 4) to determine optimal configuration.

## Storage Organization Options

### Option 1: Centralized Storage
- Single receiving area serves all fractal centers
- Central raw material warehouse
- Central finished goods warehouse
- Single shipping area

**Pros**: Efficient storage utilization, simplified inventory management
**Cons**: Increased material handling between storage and centers

### Option 2: Distributed Storage
- Each fractal center has its own receiving/shipping
- Each center manages its own raw materials
- Each center stores its finished goods

**Pros**: Reduced material handling, faster response
**Cons**: Higher storage overhead, complex inventory tracking

### Option 3: Hybrid (Recommended)
- Centralized receiving (bulk deliveries)
- Distributed WIP storage within each center
- Centralized finished goods warehouse
- Centralized shipping

**Pros**: Balances efficiency and flexibility
**Cons**: Moderate complexity

## Output Files to Generate

1. **Equipment Requirements by Center**: Shows equipment count per process per center
2. **Flow Matrix per Center**: Internal flows within each fractal center
3. **Aggregate Flow Matrix**: Total flows across all centers
4. **Capacity Utilization Report**: How efficiently each center operates
5. **Layout Visualization Data**: Coordinates and connections for drawing
6. **Comparative Analysis**: Fractal vs. Functional vs. Parts-based designs

## Implementation Strategy

We'll create Python scripts that:
1. Load demand and process data (reuse existing data loading)
2. Accept parameter `f` (number of fractal centers)
3. Calculate equipment needs per center
4. Generate flow matrices at center and factory levels
5. Produce layout-ready outputs (CSV with process locations, flows)
6. Create comparison metrics vs. other designs

## Next Steps

1. Create `fractal_design_main.py`: Core calculation engine
2. Create `fractal_flow_matrix.py`: Flow analysis per center
3. Create `fractal_equipment_requirements.py`: Equipment allocation
4. Create `fractal_layout_optimizer.py`: Process placement within centers
5. Create `fractal_comparison_analysis.py`: Compare scenarios (f=2,3,4)
