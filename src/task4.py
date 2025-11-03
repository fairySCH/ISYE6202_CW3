# -*- coding: utf-8 -*-
"""
ISyE 6202 Casework 3 - Task 4
FeMoaSa Manufacturing & Warehousing Facility Design

Task 1: Demand Fulfillment Capacity Plan for each part (Year +1)
Task 2: Finished Storage Capacity Plan for each part (Year +1)

DATA SOURCE: All data loaded from CSV files in data/csv_outputs/
"""

import pandas as pd
import numpy as np
from scipy import stats

# ============================================================================
# DATA LOADING FROM CSV FILES
# ============================================================================


# Load Product Demand (+1 Year)
product_demand_raw = pd.read_csv(r'data\csv_outputs\+2 to +5 Year Product Demand.csv', header=None)
product_demand_raw_yo1 = pd.read_csv(r'data\csv_outputs\+1 Year Product Demand.csv', header=None)


# # Row 2 (index 2) has annual demand: columns 2-6 are A1, A2, A3, B1, B2
annual_demand = product_demand_raw.iloc[2:6, 2:10].astype(float)  # années 2→5, 8 colonnes
cols = ["A1","A2","A3","B1","B2","A4","B3","B4"]
years = [f"Year {i}" for i in range(1, 6)]
annual_demand.columns = cols


# We combined year 1 with year 2, 3, 4, 5
y1_vals = product_demand_raw_yo1.iloc[2, 2:7].astype(float).values  # A1..B2
y1_full = (
    pd.Series(y1_vals, index=cols[:5])   # indexe A1..B2
      .reindex(cols, fill_value=0)       # ajoute A4,B3,B4=0
)


annual_demand_values = pd.concat([y1_full.to_frame().T, annual_demand], ignore_index=True)
annual_demand_values.index = [f"Year {i}" for i in range(1, 6)]
#print(annual_demand_values)  

# # Row 12 (index 12) has weekly demand
weekly_demand = product_demand_raw.iloc[18:22, 2:10].astype(float)
weekly_demand.columns = cols

# We combined year 1 with year 2, 3, 4, 5
w1_vals = product_demand_raw_yo1.iloc[12, 2:7].astype(float).values  # A1..B2
w1_full = (
    pd.Series(w1_vals, index=cols[:5])   # indexe A1..B2
      .reindex(cols, fill_value=0)       # ajoute A4,B3,B4=0
)

weekly_demand_values = pd.concat([w1_full.to_frame().T, weekly_demand], ignore_index=True)
weekly_demand_values.index = [f"Year {i}" for i in range(1, 6)]
#print(weekly_demand_values)



# # Row 16 (index 16) has CV values
cv = product_demand_raw.iloc[26:30, 2:10].astype(float)
cv.columns = cols

# We combined year 1 with year 2, 3, 4, 5
cv1_vals = product_demand_raw_yo1.iloc[16, 2:7].astype(float).values  # A1..B2
cv1_full = (
    pd.Series(cv1_vals, index=cols[:5])   # indexe A1..B2
      .reindex(cols, fill_value=0)       # ajoute A4,B3,B4=0
)

cv_values = pd.concat([cv1_full.to_frame().T, cv], ignore_index=True)
cv_values.index = [f"Year {i}" for i in range(1, 6)]

# print(cv_values['A1']['Year 1'])

weekly_std_dev = cv_values * weekly_demand_values
# print(weekly_std_dev['A1']['Year 1'])

print(f"[OK] Product demand loaded from CSV: {len(cols)} products")

# Load Parts per Product (BOM) - using on_bad_lines='skip' to handle formatting issues
# # First, let's read it line by line to handle the inconsistent column counts

#bom_lines = []
bom_lines = pd.read_csv(r'data\csv_outputs\+2 to +5 Year Parts per Product.csv',  header=1, index_col= 0, usecols=range(1,10), skipinitialspace=True)
#print(bom_lines)

print(f"[OK] BOM matrix loaded from CSV: {len(bom_lines)} parts")

# # Load Parts Specs - Dimensions and Process Operations
parts_specs_raw = pd.read_csv(r'data\csv_outputs\Parts Specs.csv', header=None)

# Dimensions start at row 35 (after "Identifier" header at row 34)
part_dimensions = {}
for i in range(35, 55):  # Rows 35-54 contain P1-P20 dimensions
    part_name = parts_specs_raw.iloc[i, 1]
    part_dimensions[part_name] = {
        'X': float(parts_specs_raw.iloc[i, 2]),
        'Y': float(parts_specs_raw.iloc[i, 3]),
        'Z': float(parts_specs_raw.iloc[i, 4]),
        'Weight': float(parts_specs_raw.iloc[i, 5]),
        'Price': float(parts_specs_raw.iloc[i, 6])
    }

# print(part_dimensions)
print(f"[OK] Part dimensions loaded from CSV: {len(part_dimensions)} parts")

# Process operations start at row 11 (after "Part" header at row 10)
process_operations = {}
for i in range(11, 31):  # Rows 11-30 contain P1-P20 process steps
    part_name = parts_specs_raw.iloc[i, 1]
    operations = []
    for j in range(2, 9):  # Columns 2-8 contain process steps
        op = parts_specs_raw.iloc[i, j]
        if pd.notna(op):
            operations.append(str(op))
    process_operations[part_name] = operations


# print(process_operations)
print(f"[OK] Process operations loaded from CSV: {len(process_operations)} parts")

# Process times (manually entered from PDF - not in CSV)
process_times = {
    'P1':  [1.25, 2.5, 1.0, 2.0, 3.5, 1.0, 1.5],
    'P2':  [2.5, 0.5, 2.5, 1.0, 2.5],
    'P3':  [1.75, 3.0, 0.75, 1.5, 2.5],
    'P4':  [2.5, 1.0, 2.0, 3.0, 0.25, 1.25],
    'P5':  [1.5, 0.75, 3.5, 1.75],
    'P6':  [2.5, 0.75, 1.25, 0.5, 3.0, 1.0, 1.25, 2.75],
    'P7':  [1.0, 1.5, 0.75, 3.5, 1.25, 2.0],
    'P8':  [1.25, 2.0, 0.5, 1.0],
    'P9':  [1.75, 0.75, 1.25, 0.5, 1.25, 3.0],
    'P10': [1.5, 1.75, 1.25, 2.0],
    'P11': [1.25, 0.5, 1.25, 0.25, 0.75],
    'P12': [1.0, 0.5, 1.0, 1.25, 2.25],
    'P13': [1.25, 1.25, 0.5, 1.0, 0.25, 2.0, 1.25],
    'P14': [1.0, 1.5, 0.5, 1.75],
    'P15': [0.75, 0.5, 1.25, 2.5, 2.5],
    'P16': [1.25, 5.0, 1.25, 2.5],
    'P17': [0.75, 3.0, 3.5],
    'P18': [2.0, 0.75, 2.0, 3.0],
    'P19': [2.25, 2.5, 2.0, 3.75],
    'P20': [2.0, 2.25, 0.75, 3.0],
}

print(f"[OK] Process times loaded (manual entry from PDF): {len(process_times)} parts")

 # ============================================================================
# TASK 4: DEMAND FULFILLMENT CAPACITY PLAN
# ============================================================================

print("="*80)
print("TASK 4: DEMAND FULFILLMENT CAPACITY PLAN (Year +5)")
print("="*80)

print("\n--- Step 1: Calculate Parts Demand from Products ---\n")


print("\n" + "="*80)
print("CALCULATION METHODOLOGY: Parts Demand Aggregation")
print("="*80)
print("""
Each part is used in multiple products according to the BOM (Bill of Materials).
To calculate part demand, we aggregate across all products that use each part.

Formula for each part P:
  Annual Demand(P) = SUM [BOM(P, Product_i) x Annual Demand(Product_i)]
  Weekly Demand(P) = SUM [BOM(P, Product_i) x Weekly Demand(Product_i)]
  
For variance (since product demands are independent):
  Variance(P) = SUM [BOM(P, Product_i)^2 x Variance(Product_i)]
  Std Dev(P) = SQRT(Variance(P))
  
where:
  - BOM(P, Product_i) = quantity of part P required per unit of Product_i
  - Variance(Product_i) = (Weekly Std Dev of Product_i)^2
""")

print(bom_lines['A1']['P1'])
parts = bom_lines.index
print(parts[0])

index = pd.Index(parts, name="Part")
dtypes = {
    "parts_annual_demand": "float64",
    "parts_weekly_demand": "float64",
    "parts_weekly_variance": "float64",
    "required_capacity_minutes": "float64",
    "parts_weekly_std_dev": "float64"
}
fillers = {"parts_annual_demand": 0.0, "parts_weekly_demand": 0.0, "parts_weekly_variance": 0.0}

def make_empty():
    return (pd.DataFrame(index=index, columns=list(dtypes))
              .astype(dtypes)
              .fillna(fillers))

parts_demand_Y1 = make_empty()
parts_demand_Y2 = make_empty()
parts_demand_Y3 = make_empty()
parts_demand_Y4 = make_empty()
parts_demand_Y5 = make_empty()

parts_demand = pd.concat(
    {
        "Year 1": parts_demand_Y1,
        "Year 2": parts_demand_Y2,
        "Year 3": parts_demand_Y3,
        "Year 4": parts_demand_Y4,
        "Year 5": parts_demand_Y5,
    },
    names=["year"]  # niveau 0; le niveau 1 garde le nom "Part"
)
# (optionnel) s'assurer des noms des deux niveaux :
parts_demand.index = parts_demand.index.set_names(["year", "Part"])

years = parts_demand.index.unique("year").tolist()


print("\n" + "="*80)
print("DETAILED CALCULATION for EACH PART")
print("="*80)

for year in years:
    #print(f"Calculation {year}")
    for part in parts:
        annual = 0
        weekly = 0
        variance = 0
        
        #print(f"Calculation {part}")
        # print("-" * 80)
        
        for product in cols:
            
            qty = bom_lines.loc[part, product]
            if qty > 0:
                prod_annual = qty * annual_demand_values[product][year]
                prod_weekly = qty * weekly_demand_values[product][year]
                prod_variance = (qty * weekly_std_dev[product][year]) ** 2
                
                annual += prod_annual
                weekly += prod_weekly
                variance += prod_variance
                
                # print(f"  {product}: {qty} parts/unit x {annual_demand_values[product][year]:>7,.0f} units/year = {prod_annual:>8,.0f} parts/year")
                # print(f"       {qty} parts/unit x {weekly_demand_values[product][year]:>8,.2f} units/week = {prod_weekly:>8,.2f} parts/week")
                # print(f"       Variance contribution: ({qty} x {weekly_std_dev[product][year]:>7,.2f})^2 = {prod_variance:>10,.2f}")
        
        parts_demand.loc[(year, part), "parts_annual_demand"] = annual
        parts_demand.loc[(year, part), "parts_weekly_demand"] = weekly
        parts_demand.loc[(year, part), "parts_weekly_variance"] = variance
        parts_demand.loc[(year, part), "parts_weekly_std_dev"] = np.sqrt(variance)

        
        std_dev = np.sqrt(variance)
        #print(f"  {'-'*60}")
        #print(f"  Year {year} TOTAL {part}: Annual = {annual:>8,.0f}, Weekly = {weekly:>8,.2f}, Std Dev = {std_dev:>8,.2f}")


print("\n\n" + "="*80)
print("SUMMARY: Parts Demand Results")
print("="*80)
# print(parts_demand.loc["Year 1"])

# ============================================================================
# Step 2: Calculate Production Capacity Requirements
# ============================================================================

print("\n--- Step 2: Production Capacity Requirements ---\n")

# Operating parameters
SHIFTS_PER_DAY = 2
HOURS_PER_SHIFT = 8
DAYS_PER_WEEK = 5
WEEKS_PER_YEAR = 52
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY

hours_per_week = SHIFTS_PER_DAY * HOURS_PER_SHIFT * DAYS_PER_WEEK
minutes_per_week = hours_per_week * 60

print(f"Operating Schedule:")
print(f"  - {SHIFTS_PER_DAY} shifts/day x {HOURS_PER_SHIFT} hours/shift x {DAYS_PER_WEEK} days/week")
print(f"  - Available: {hours_per_week} hours/week = {minutes_per_week} minutes/week")
print(f"  - Efficiency: {EFFICIENCY:.0%}, Reliability: {RELIABILITY:.0%}")
print(f"  - Effective availability: {EFFECTIVE_AVAILABILITY:.2%}\n")

# Calculate total process time per part
total_process_time = {p: sum(process_times[p]) for p in parts}

print("Total Process Time per Part:")
# for part in parts:
    # print(f"  {part}: {total_process_time[part]:>6.2f} minutes/unit")

# Calculate required capacity

for year in years:
    for part in parts:
        demand = parts_demand.loc[(year,part), "parts_weekly_demand"]
        time_unit = total_process_time[part]
        total_min = demand * time_unit
        effective_min = total_min / EFFECTIVE_AVAILABILITY
        parts_demand.loc[(year,part), "required_capacity_minutes"]= effective_min
        
        # print(f"{part:<6} {demand:>14,.2f}  {time_unit:>10,.2f}  {total_min:>16,.2f}  {effective_min:>18,.2f}")


print("\n\n" + "="*80)
print("SUMMARY: Parts required capacity minutes")
print("="*80)
# print(parts_demand.loc["Year 1"])

# ============================================================================
# Step 3: Equipment Requirements by Process
# ============================================================================
from collections import defaultdict

print("\n--- Step 3: Equipment Requirements by Process ---\n")

# process_requirements[year][operation] = minutes requises / semaine
process_requirements = defaultdict(lambda: defaultdict(float))

for year in years:              # ex. "Year 1", ...
    for part in parts:          # ex. "P1"..."P20"
        demand = parts_demand.loc[(year, part), "parts_weekly_demand"]
        # récupère les opérations et temps de ce part
        operations = process_operations[part]
        times = process_times[part]
        for operation, time in zip(operations, times):
            # charge en minutes sur ce poste/opération pour ce part
            total_time = demand * time
            # ajuste par l’efficacité / fiabilité
            effective_time = total_time / EFFECTIVE_AVAILABILITY
            process_requirements[year][operation] += effective_time

# Affichage + calcul du nombre d’équipements par année
equipment_needed = defaultdict(dict)

for year in years:
    # print(f"\nProcess Requirements — {year}")
    # print(f"{'Process':<18} {'Req Min/Week':>16} {'Req Hours':>14} {'# Equip Needed':>16}")
    # print("-" * 70)

    for operation in sorted(process_requirements[year].keys()):
        req_min = process_requirements[year][operation]             # minutes/semaine
        req_hours = req_min / 60.0
        num_equip = req_min / minutes_per_week                      # minutes dispo/machine/sem.
        equipment_needed[year][operation] = int(np.ceil(num_equip)) # arrondi au dessus
        #print(f"{operation:<18} {req_min:>16,.2f} {req_hours:>14,.2f} {num_equip:>16,.3f} -> {equipment_needed[year][operation]}")


# DF: lignes = années, colonnes = opérations, valeurs = minutes requises / semaine
proc_req_df = pd.DataFrame.from_dict(process_requirements, orient="index").fillna(0.0)
# DF équipements nécessaires (arrondi)
equip_needed_df = np.ceil(proc_req_df / minutes_per_week).astype(int)

print("\nRésumé minutes requises (min/sem) par process et par année :")
print(proc_req_df)

print("\nRésumé équipements nécessaires par process et par année :")
print(equip_needed_df)


# ============================================================================
# Step 4: Safety Stock Calculations
# ============================================================================

print("\n--- Step 4: Safety Stock for 99.5% Service Level ---\n")

SERVICE_LEVEL = 0.995
Z_SCORE = stats.norm.ppf(SERVICE_LEVEL)

LEAD_TIME_WEEKS = 1  
print(f"Target Service Level: {SERVICE_LEVEL:.1%}")
print(f"Z-score: {Z_SCORE:.3f}")
print(f"Lead time (weeks): {LEAD_TIME_WEEKS}\n")


# Safety stock par (year, Part) : Z * sigma * sqrt(L)
parts_demand["safety_stock_99_5"] = (
    Z_SCORE * parts_demand["parts_weekly_std_dev"] * np.sqrt(LEAD_TIME_WEEKS)
)


for year in years:
    # print(f"Safety Stock Requirements — {year}")
    # print(f"{'Part':<6} {'Weekly Demand':>16}  {'Weekly Std Dev':>16}  {'Safety Stock':>16}")
    # print("-" * 70)
    df_y = parts_demand.loc[year, ["parts_weekly_demand", "parts_weekly_std_dev", "safety_stock_99_5"]]
    # garder l'ordre des parts si tu as la liste `parts`
    df_y = df_y.reindex(parts)

    # for part, row in df_y.iterrows():
        # print(f"{part:<6} {row['parts_weekly_demand']:>16,.2f}  "
        #       f"{row['parts_weekly_std_dev']:>16,.2f}  "
        #       f"{row['safety_stock_99_5']:>16,.2f}")
    #print()

# ============================================================================
# Save Task 1 Results
# ============================================================================
from pathlib import Path
task1_df = (
    parts_demand
      .reset_index()  # remet 'year' et 'Part' en colonnes
      .rename(columns={
          "year": "Year",
          "parts_annual_demand": "Annual_Demand_Units",
          "parts_weekly_demand": "Weekly_Demand_Units",
          "parts_weekly_std_dev": "Weekly_StdDev_Units",
          "required_capacity_minutes": "Required_Capacity_Min_Week",
          "safety_stock_99_5": "Safety_Stock_Units",
      })
)

# Ajouter le temps process total (min/unité) par pièce
task1_df["Total_Process_Time_Min"] = task1_df["Part"].map(total_process_time)

# Ordonner les colonnes
task1_df = task1_df[
    ["Year", "Part",
     "Annual_Demand_Units", "Weekly_Demand_Units", "Weekly_StdDev_Units",
     "Total_Process_Time_Min", "Required_Capacity_Min_Week", "Safety_Stock_Units"]
]

# (option) garder l'ordre Year 1..Year 5
task1_df["Year"] = pd.Categorical(task1_df["Year"], categories=[f"Year {i}" for i in range(1,6)], ordered=True)
task1_df = task1_df.sort_values(["Year","Part"])

# --- Export CSV ---
out_dir = Path("results")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv"

task1_df.to_csv(out_file, index=False, encoding="utf-8-sig")
print(f"\n[OK] Task 1 results saved to: {out_file}")

# # ============================================================================
# # TASK 2: FINISHED STORAGE CAPACITY PLAN
# # ============================================================================

print("\n\n" + "="*80)
print("TASK 2: FINISHED STORAGE CAPACITY PLAN (Year +1)")
print("="*80)

print("\n--- Step 1: Storage Requirements Analysis ---\n")

CLIENT_A_BUFFER_HOURS = 4
CLIENT_B_BUFFER_HOURS = 12
OPERATING_HOURS_PER_WEEK = hours_per_week  # 2×8×5 = 80

client_a_products = ['A1', 'A2', 'A3', 'A4']
client_b_products = ['B1', 'B2', 'B3', 'B4']

# DataFrames vides (parts × years) en float
parts_demand_CA_hourly = pd.DataFrame(0.0, index=parts, columns=years)
parts_demand_CB_hourly = pd.DataFrame(0.0, index=parts, columns=years)

# Calcul vectoriel par année
BOM_A = bom_lines[client_a_products].fillna(0)
BOM_B = bom_lines[client_b_products].fillna(0)

for year in years:
    # Demande hebdo (parts) = (parts×products) @ (products)
    a_weekly = BOM_A @ weekly_demand_values.loc[year, client_a_products].fillna(0)
    b_weekly = BOM_B @ weekly_demand_values.loc[year, client_b_products].fillna(0)

    parts_demand_CA_hourly.loc[:, year] = a_weekly / OPERATING_HOURS_PER_WEEK
    parts_demand_CB_hourly.loc[:, year] = b_weekly / OPERATING_HOURS_PER_WEEK

# Buffer stock (unités finies à stocker) pour l’autonomie demandée
buffer_A_units = parts_demand_CA_hourly * CLIENT_A_BUFFER_HOURS
buffer_B_units = parts_demand_CB_hourly * CLIENT_B_BUFFER_HOURS
buffer_total_units = buffer_A_units.add(buffer_B_units, fill_value=0)


print("Client-Specific Hourly Demand and Buffer Stock:")
print(f"{'Part':<6} {'A Hourly':<16} {'A Buffer':<16} {'B Hourly':<16} {'B Buffer':<16}")
print("-" * 75)
# for part in parts:
#     print(
#         f"{part:<6} "
#         f"{parts_demand_CA_hourly.loc[part, 'Year 2']:>14,.1f}  "
#         f"{buffer_A_units.loc[part, 'Year 2']:>14,.1f}  "
#         f"{parts_demand_CB_hourly.loc[part, 'Year 2']:>14,.1f}  "
#         f"{buffer_B_units.loc[part, 'Year 2']:>14,.1f}"
#     )

# ============================================================================
# Step 2: Total Storage Allocation
# ============================================================================

print("\n--- Step 2: Storage Allocation Plan ---\n")


# Cycle stock (average inventory between production runs)
# Assuming weekly production batches
parts_demand["cycle_stock_units"] = parts_demand["parts_weekly_demand"] / 2.0

# Factory storage = Safety stock + Cycle stock
parts_demand["factory_storage_units"] = (
    parts_demand["safety_stock_99_5"] + parts_demand["cycle_stock_units"]
)


for target_year in years:
    print(f"\nStorage Allocation — {target_year}\n")
    print(f"{'Part':<6} {'Safety Stock':>14}  {'Cycle Stock':>14}  {'Factory Total':>16}  {'Warehouse A':>14}  {'Warehouse B':>14}")
    print("-" * 92)
    df_y = parts_demand.loc[target_year, ["safety_stock_99_5", "cycle_stock_units", "factory_storage_units"]].reindex(parts)
    for part in parts:
        ss = df_y.loc[part, "safety_stock_99_5"]
        cs = df_y.loc[part, "cycle_stock_units"]
        ft = df_y.loc[part, "factory_storage_units"]
        wa = float(buffer_A_units.loc[part, target_year])
        wb = float(buffer_B_units.loc[part, target_year])
        print(f"{part:<6} {ss:>14,.2f}  {cs:>14,.2f}  {ft:>16,.2f}  {wa:>14,.2f}  {wb:>14,.2f}")


# ============================================================================
# Step 3: Physical Storage Space Requirements — by year
# ============================================================================

print("\n--- Step 3: Physical Storage Space Requirements (by year) ---\n")

# Calculate volumes
volumes_cuft = pd.Series(
    {p: (part_dimensions[p]['X'] * part_dimensions[p]['Y'] * part_dimensions[p]['Z']) / (12**3)
     for p in parts},
    name="volume_cuft"
).reindex(parts).astype(float)

WAREHOUSE_HEIGHT = 20.0
STORAGE_UTILIZATION = 0.70
DENOM = WAREHOUSE_HEIGHT * STORAGE_UTILIZATION  


buffer_A_df = buffer_A_units   # parts × years
buffer_B_df = buffer_B_units


summary_rows = []

for year in years:
    factory_units  = parts_demand.loc[year, "factory_storage_units"].reindex(parts).fillna(0.0).astype(float)
    wh_a_units     = buffer_A_df.loc[parts, year].fillna(0.0).astype(float)
    wh_b_units     = buffer_B_df.loc[parts, year].fillna(0.0).astype(float)


    factory_volume_cuft    = (factory_units * volumes_cuft).sum()
    warehouse_a_volume_cuft = (wh_a_units * volumes_cuft).sum()
    warehouse_b_volume_cuft = (wh_b_units * volumes_cuft).sum()


    factory_floor_sqft     = factory_volume_cuft / DENOM
    warehouse_a_floor_sqft = warehouse_a_volume_cuft / DENOM
    warehouse_b_floor_sqft = warehouse_b_volume_cuft / DENOM


    print(f"Storage Volumes — {year}:")
    print(f"  Factory:     {factory_volume_cuft:>12,.2f} cubic feet")
    print(f"  Warehouse A: {warehouse_a_volume_cuft:>12,.2f} cubic feet")
    print(f"  Warehouse B: {warehouse_b_volume_cuft:>12,.2f} cubic feet")
    print(f"\nFloor Space (20 ft height, 70% utilization) — {year}:")
    print(f"  Factory:     {factory_floor_sqft:>12,.2f} sq ft")
    print(f"  Warehouse A: {warehouse_a_floor_sqft:>12,.2f} sq ft")
    print(f"  Warehouse B: {warehouse_b_floor_sqft:>12,.2f} sq ft\n")


    WAREHOUSE_COST_PER_SQFT = 200.0
    warehouse_a_cost = warehouse_a_floor_sqft * WAREHOUSE_COST_PER_SQFT
    warehouse_b_cost = warehouse_b_floor_sqft * WAREHOUSE_COST_PER_SQFT
    total_investment = warehouse_a_cost + warehouse_b_cost

    print(f"Warehouse Building Costs — {year}:")
    print(f"  Warehouse A: {warehouse_a_floor_sqft:>10,.2f} sq ft × ${WAREHOUSE_COST_PER_SQFT:.0f}/sq ft = ${warehouse_a_cost:>15,.2f}")
    print(f"  Warehouse B: {warehouse_b_floor_sqft:>10,.2f} sq ft × ${WAREHOUSE_COST_PER_SQFT:.0f}/sq ft = ${warehouse_b_cost:>15,.2f}")
    print(f"  Total Investment:                                            ${total_investment:>15,.2f}\n")

    summary_rows.append({
        "Year": year,
        "Factory_Volume_cuft": factory_volume_cuft,
        "Warehouse_A_Volume_cuft": warehouse_a_volume_cuft,
        "Warehouse_B_Volume_cuft": warehouse_b_volume_cuft,
        "Factory_Floor_sqft": factory_floor_sqft,
        "Warehouse_A_Floor_sqft": warehouse_a_floor_sqft,
        "Warehouse_B_Floor_sqft": warehouse_b_floor_sqft,
        "Warehouse_A_Cost": warehouse_a_cost,
        "Warehouse_B_Cost": warehouse_b_cost,
        "Total_Investment": total_investment,
    })


storage_summary_by_year = pd.DataFrame(summary_rows).set_index("Year")
storage_summary_by_year.to_csv("results/Task4_storage_summary_by_year.csv",
                               encoding="utf-8-sig", float_format="%.2f")




task2_detail_rows = []

for year in years:

    ss  = parts_demand.loc[year, "safety_stock_99_5"].reindex(parts).astype(float)
    cs  = parts_demand.loc[year, "cycle_stock_units"].reindex(parts).astype(float)
    fs  = parts_demand.loc[year, "factory_storage_units"].reindex(parts).astype(float)


    wa = buffer_A_units.loc[parts, year].astype(float)
    wb = buffer_B_units.loc[parts, year].astype(float)


    part_volumes_cuft = pd.Series(
        {p: (part_dimensions[p]['X'] * part_dimensions[p]['Y'] * part_dimensions[p]['Z']) / (12**3) for p in parts},
        index=parts, name="Part_Volume_CuFt"
    ).astype(float)

    detail_y = pd.DataFrame({
        "Safety_Stock_Units":   ss,
        "Cycle_Stock_Units":    cs,
        "Factory_Storage_Units":fs,
        "Warehouse_A_Units":    wa,
        "Warehouse_B_Units":    wb,
        "Part_Volume_CuFt":     part_volumes_cuft,
    })
    detail_y.index.name = "Part"
    detail_y = detail_y.reset_index()
    detail_y.insert(0, "Year", year)  

    task2_detail_rows.extend(detail_y.to_dict(orient="records"))


task2_df = pd.DataFrame(task2_detail_rows)[
    ["Year","Part","Safety_Stock_Units","Cycle_Stock_Units","Factory_Storage_Units",
     "Warehouse_A_Units","Warehouse_B_Units","Part_Volume_CuFt"]
]


out_dir = Path("results")
out_dir.mkdir(parents=True, exist_ok=True)
task2_df.to_csv(out_dir / "Task2_Storage_Allocation_by_year_and_part.csv",
                index=False, encoding="utf-8-sig", float_format="%.2f")

