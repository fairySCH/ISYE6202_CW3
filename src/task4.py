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
print(f"\n{'='*80}")
print("DATA LOADING COMPLETE - All data loaded from CSV files")
print(f"{'='*80}\n")

 # ============================================================================
# TASK 4: DEMAND FULFILLMENT CAPACITY PLAN
# ============================================================================

print("="*80)
print("TASK 1: DEMAND FULFILLMENT CAPACITY PLAN (Year +1)")
print("="*80)

print("\n--- Step 1: Calculate Parts Demand from Products ---\n")

# print("="*80)
# print("INPUT DATA: Product Demand")
# print("="*80)
# print(f"{'Product':<10} {'Annual (units)':<18} {'Weekly (units)':<18} {'CV':<8} {'Weekly Std Dev':<18}")
# print("-" * 80)
# for product in products:
#     print(f"{product:<10} {annual_demand[product]:>16,.0f}  {weekly_demand[product]:>16,.2f}  {cv_weekly[product]:>6.2f}  {weekly_std_dev[product]:>16,.2f}")

# print("\n" + "="*80)
# print("CALCULATION METHODOLOGY: Parts Demand Aggregation")
# print("="*80)
# print("""
# Each part is used in multiple products according to the BOM (Bill of Materials).
# To calculate part demand, we aggregate across all products that use each part.

# Formula for each part P:
#   Annual Demand(P) = SUM [BOM(P, Product_i) x Annual Demand(Product_i)]
#   Weekly Demand(P) = SUM [BOM(P, Product_i) x Weekly Demand(Product_i)]
  
# For variance (since product demands are independent):
#   Variance(P) = SUM [BOM(P, Product_i)^2 x Variance(Product_i)]
#   Std Dev(P) = SQRT(Variance(P))
  
# where:
#   - BOM(P, Product_i) = quantity of part P required per unit of Product_i
#   - Variance(Product_i) = (Weekly Std Dev of Product_i)^2
# """)

# # Calculate parts demand WITH DETAILED BREAKDOWN
# parts_annual_demand = {}
# parts_weekly_demand = {}
# parts_weekly_variance = {}

# print("\n" + "="*80)
# print("DETAILED CALCULATION for EACH PART")
# print("="*80)

# for part in parts:
#     annual = 0
#     weekly = 0
#     variance = 0
    
#     print(f"\n{part}: Calculation Breakdown")
#     print("-" * 80)
    
#     for product in products:
#         qty = bom[part].get(product, 0)
#         if qty > 0:
#             prod_annual = qty * annual_demand[product]
#             prod_weekly = qty * weekly_demand[product]
#             prod_variance = (qty * weekly_std_dev[product]) ** 2
            
#             annual += prod_annual
#             weekly += prod_weekly
#             variance += prod_variance
            
#             print(f"  {product}: {qty} parts/unit x {annual_demand[product]:>7,.0f} units/year = {prod_annual:>8,.0f} parts/year")
#             print(f"       {qty} parts/unit x {weekly_demand[product]:>8,.2f} units/week = {prod_weekly:>8,.2f} parts/week")
#             print(f"       Variance contribution: ({qty} x {weekly_std_dev[product]:>7,.2f})^2 = {prod_variance:>10,.2f}")
    
#     parts_annual_demand[part] = annual
#     parts_weekly_demand[part] = weekly
#     parts_weekly_variance[part] = variance
    
#     std_dev = np.sqrt(variance)
#     print(f"  {'-'*60}")
#     print(f"  TOTAL {part}: Annual = {annual:>8,.0f}, Weekly = {weekly:>8,.2f}, Std Dev = {std_dev:>8,.2f}")

# parts_weekly_std_dev = {p: np.sqrt(parts_weekly_variance[p]) for p in parts}

# print("\n\n" + "="*80)
# print("SUMMARY: Parts Demand Results")
# print("="*80)
# print(f"{'Part':<6} {'Annual Demand':<18} {'Weekly Demand':<18} {'Weekly Std Dev':<18}")
# print("-" * 70)
# for part in parts:
#     print(f"{part:<6} {parts_annual_demand[part]:>16,.0f}  {parts_weekly_demand[part]:>16,.2f}  {parts_weekly_std_dev[part]:>16,.2f}")

# # ============================================================================
# # Step 2: Calculate Production Capacity Requirements
# # ============================================================================

# print("\n--- Step 2: Production Capacity Requirements ---\n")

# # Operating parameters
# SHIFTS_PER_DAY = 2
# HOURS_PER_SHIFT = 8
# DAYS_PER_WEEK = 5
# WEEKS_PER_YEAR = 52
# EFFICIENCY = 0.90
# RELIABILITY = 0.98
# EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY

# hours_per_week = SHIFTS_PER_DAY * HOURS_PER_SHIFT * DAYS_PER_WEEK
# minutes_per_week = hours_per_week * 60

# print(f"Operating Schedule:")
# print(f"  - {SHIFTS_PER_DAY} shifts/day x {HOURS_PER_SHIFT} hours/shift x {DAYS_PER_WEEK} days/week")
# print(f"  - Available: {hours_per_week} hours/week = {minutes_per_week} minutes/week")
# print(f"  - Efficiency: {EFFICIENCY:.0%}, Reliability: {RELIABILITY:.0%}")
# print(f"  - Effective availability: {EFFECTIVE_AVAILABILITY:.2%}\n")

# # Calculate total process time per part
# total_process_time = {p: sum(process_times[p]) for p in parts}

# print("Total Process Time per Part:")
# for part in parts:
#     print(f"  {part}: {total_process_time[part]:>6.2f} minutes/unit")

# # Calculate required capacity
# print("\n\nRequired Production Capacity:")
# print(f"{'Part':<6} {'Weekly Demand':<16} {'Time/Unit':<12} {'Total Min/Week':<18} {'w/ Availability':<20}")
# print("-" * 90)

# required_capacity_minutes = {}
# for part in parts:
#     demand = parts_weekly_demand[part]
#     time_unit = total_process_time[part]
#     total_min = demand * time_unit
#     effective_min = total_min / EFFECTIVE_AVAILABILITY
#     required_capacity_minutes[part] = effective_min
    
#     print(f"{part:<6} {demand:>14,.2f}  {time_unit:>10,.2f}  {total_min:>16,.2f}  {effective_min:>18,.2f}")

# # ============================================================================
# # Step 3: Equipment Requirements by Process
# # ============================================================================

# print("\n--- Step 3: Equipment Requirements by Process ---\n")

# # Aggregate by process type
# process_requirements = {}

# for part in parts:
#     demand = parts_weekly_demand[part]
#     operations = process_operations[part]
#     times = process_times[part]
    
#     for operation, time in zip(operations, times):
#         if operation not in process_requirements:
#             process_requirements[operation] = 0
        
#         total_time = demand * time
#         effective_time = total_time / EFFECTIVE_AVAILABILITY
#         process_requirements[operation] += effective_time

# print("Process Requirements:")
# print(f"{'Process':<10} {'Required Min/Week':<20} {'Required Hours':<18} {'# Equipment Needed':<20}")
# print("-" * 80)

# equipment_needed = {}
# for process in sorted(process_requirements.keys()):
#     req_min = process_requirements[process]
#     req_hours = req_min / 60
#     num_equip = req_min / minutes_per_week
#     equipment_needed[process] = np.ceil(num_equip)
    
#     print(f"{process:<10} {req_min:>18,.2f}  {req_hours:>16,.2f}  {num_equip:>18,.3f} -> {int(np.ceil(num_equip))}")

# # ============================================================================
# # Step 4: Safety Stock Calculations
# # ============================================================================

# print("\n--- Step 4: Safety Stock for 99.5% Service Level ---\n")

# SERVICE_LEVEL = 0.995
# Z_SCORE = stats.norm.ppf(SERVICE_LEVEL)

# print(f"Target Service Level: {SERVICE_LEVEL:.1%}")
# print(f"Z-score: {Z_SCORE:.3f}\n")

# safety_stock = {p: Z_SCORE * parts_weekly_std_dev[p] for p in parts}

# print("Safety Stock Requirements:")
# print(f"{'Part':<6} {'Weekly Demand':<18} {'Weekly Std Dev':<18} {'Safety Stock':<18}")
# print("-" * 70)
# for part in parts:
#     print(f"{part:<6} {parts_weekly_demand[part]:>16,.2f}  {parts_weekly_std_dev[part]:>16,.2f}  {safety_stock[part]:>16,.2f}")

# # ============================================================================
# # Save Task 1 Results
# # ============================================================================

# task1_df = pd.DataFrame({
#     'Part': parts,
#     'Annual_Demand_Units': [parts_annual_demand[p] for p in parts],
#     'Weekly_Demand_Units': [parts_weekly_demand[p] for p in parts],
#     'Weekly_StdDev_Units': [parts_weekly_std_dev[p] for p in parts],
#     'Total_Process_Time_Min': [total_process_time[p] for p in parts],
#     'Required_Capacity_Min_Week': [required_capacity_minutes[p] for p in parts],
#     'Safety_Stock_Units': [safety_stock[p] for p in parts]
# })

# task1_df.to_csv('Task1_Demand_Fulfillment_Capacity_Plan.csv', index=False)
# print("\n[OK] Task 1 results saved to: Task1_Demand_Fulfillment_Capacity_Plan.csv")

# # ============================================================================
# # TASK 2: FINISHED STORAGE CAPACITY PLAN
# # ============================================================================

# print("\n\n" + "="*80)
# print("TASK 2: FINISHED STORAGE CAPACITY PLAN (Year +1)")
# print("="*80)

# print("\n--- Step 1: Storage Requirements Analysis ---\n")

# # Client requirements
# CLIENT_A_BUFFER_HOURS = 4
# CLIENT_B_BUFFER_HOURS = 12
# OPERATING_HOURS_PER_WEEK = hours_per_week

# print(f"Client A: {CLIENT_A_BUFFER_HOURS}-hour buffer autonomy (99% service)")
# print(f"Client B: {CLIENT_B_BUFFER_HOURS}-hour buffer autonomy (99% service)")
# print(f"Operating hours: {OPERATING_HOURS_PER_WEEK} hours/week\n")

# # Calculate client-specific demand
# client_a_products = ['A1', 'A2', 'A3']
# client_b_products = ['B1', 'B2']

# parts_demand_a_hourly = {}
# parts_demand_b_hourly = {}

# for part in parts:
#     demand_a = sum(bom[part].get(prod, 0) * weekly_demand[prod] for prod in client_a_products)
#     demand_b = sum(bom[part].get(prod, 0) * weekly_demand[prod] for prod in client_b_products)
    
#     parts_demand_a_hourly[part] = demand_a / OPERATING_HOURS_PER_WEEK
#     parts_demand_b_hourly[part] = demand_b / OPERATING_HOURS_PER_WEEK

# # Buffer stock at client sites
# buffer_stock_a = {p: parts_demand_a_hourly[p] * CLIENT_A_BUFFER_HOURS for p in parts}
# buffer_stock_b = {p: parts_demand_b_hourly[p] * CLIENT_B_BUFFER_HOURS for p in parts}

# print("Client-Specific Hourly Demand and Buffer Stock:")
# print(f"{'Part':<6} {'A Hourly':<16} {'A Buffer':<16} {'B Hourly':<16} {'B Buffer':<16}")
# print("-" * 75)
# for part in parts:
#     print(f"{part:<6} {parts_demand_a_hourly[part]:>14,.4f}  {buffer_stock_a[part]:>14,.2f}  "
#           f"{parts_demand_b_hourly[part]:>14,.4f}  {buffer_stock_b[part]:>14,.2f}")

# # ============================================================================
# # Step 2: Total Storage Allocation
# # ============================================================================

# print("\n--- Step 2: Storage Allocation Plan ---\n")

# # Cycle stock (average inventory between production runs)
# # Assuming weekly production batches
# cycle_stock = {p: parts_weekly_demand[p] / 2 for p in parts}

# # Factory storage = Safety stock + Cycle stock
# factory_storage = {p: safety_stock[p] + cycle_stock[p] for p in parts}

# print("Storage Allocation:")
# print(f"{'Part':<6} {'Safety Stock':<16} {'Cycle Stock':<16} {'Factory Total':<18} {'Warehouse A':<16} {'Warehouse B':<16}")
# print("-" * 105)
# for part in parts:
#     print(f"{part:<6} {safety_stock[part]:>14,.2f}  {cycle_stock[part]:>14,.2f}  {factory_storage[part]:>16,.2f}  "
#           f"{buffer_stock_a[part]:>14,.2f}  {buffer_stock_b[part]:>14,.2f}")

# # ============================================================================
# # Step 3: Physical Storage Space Requirements
# # ============================================================================

# print("\n--- Step 3: Physical Storage Space Requirements ---\n")

# # Calculate volumes
# part_volumes_cuft = {}
# for part in parts:
#     x, y, z = part_dimensions[part]['X'], part_dimensions[part]['Y'], part_dimensions[part]['Z']
#     volume_cuin = x * y * z
#     volume_cuft = volume_cuin / (12**3)  # Convert to cubic feet
#     part_volumes_cuft[part] = volume_cuft

# # Total volumes
# factory_volume = sum(factory_storage[p] * part_volumes_cuft[p] for p in parts)
# warehouse_a_volume = sum(buffer_stock_a[p] * part_volumes_cuft[p] for p in parts)
# warehouse_b_volume = sum(buffer_stock_b[p] * part_volumes_cuft[p] for p in parts)

# # Floor space (20 ft height, 70% utilization)
# WAREHOUSE_HEIGHT = 20
# STORAGE_UTILIZATION = 0.70

# factory_floor_sqft = factory_volume / (WAREHOUSE_HEIGHT * STORAGE_UTILIZATION)
# warehouse_a_floor_sqft = warehouse_a_volume / (WAREHOUSE_HEIGHT * STORAGE_UTILIZATION)
# warehouse_b_floor_sqft = warehouse_b_volume / (WAREHOUSE_HEIGHT * STORAGE_UTILIZATION)

# print(f"Storage Volumes:")
# print(f"  Factory:     {factory_volume:>12,.2f} cubic feet")
# print(f"  Warehouse A: {warehouse_a_volume:>12,.2f} cubic feet")
# print(f"  Warehouse B: {warehouse_b_volume:>12,.2f} cubic feet")
# print(f"\nFloor Space (20 ft height, 70% utilization):")
# print(f"  Factory:     {factory_floor_sqft:>12,.2f} sq ft")
# print(f"  Warehouse A: {warehouse_a_floor_sqft:>12,.2f} sq ft")
# print(f"  Warehouse B: {warehouse_b_floor_sqft:>12,.2f} sq ft")

# # ============================================================================
# # Step 4: Storage Costs
# # ============================================================================

# print("\n--- Step 4: Storage Investment ---\n")

# WAREHOUSE_COST_PER_SQFT = 200

# warehouse_a_cost = warehouse_a_floor_sqft * WAREHOUSE_COST_PER_SQFT
# warehouse_b_cost = warehouse_b_floor_sqft * WAREHOUSE_COST_PER_SQFT

# print(f"Warehouse Building Costs:")
# print(f"  Warehouse A: {warehouse_a_floor_sqft:>10,.2f} sq ft x ${WAREHOUSE_COST_PER_SQFT}/sq ft = ${warehouse_a_cost:>15,.2f}")
# print(f"  Warehouse B: {warehouse_b_floor_sqft:>10,.2f} sq ft x ${WAREHOUSE_COST_PER_SQFT}/sq ft = ${warehouse_b_cost:>15,.2f}")
# print(f"  Total Investment:                                         ${warehouse_a_cost + warehouse_b_cost:>15,.2f}")

# # ============================================================================
# # Save Task 2 Results
# # ============================================================================

# task2_df = pd.DataFrame({
#     'Part': parts,
#     'Safety_Stock_Units': [safety_stock[p] for p in parts],
#     'Cycle_Stock_Units': [cycle_stock[p] for p in parts],
#     'Factory_Storage_Units': [factory_storage[p] for p in parts],
#     'Warehouse_A_Units': [buffer_stock_a[p] for p in parts],
#     'Warehouse_B_Units': [buffer_stock_b[p] for p in parts],
#     'Part_Volume_CuFt': [part_volumes_cuft[p] for p in parts]
# })

# task2_df.to_csv('Task2_Finished_Storage_Capacity_Plan.csv', index=False)
# print("\n[OK] Task 2 results saved to: Task2_Finished_Storage_Capacity_Plan.csv")

# # ============================================================================
# # COMPREHENSIVE SUMMARY
# # ============================================================================

# print("\n\n" + "="*80)
# print("COMPREHENSIVE SUMMARY - TASKS 1 & 2")
# print("="*80)

# print("\n--- TASK 1 SUMMARY ---")
# print(f"\nTotal Annual Parts Demand: {sum(parts_annual_demand.values()):>15,.0f} units")
# print(f"Total Weekly Parts Demand: {sum(parts_weekly_demand.values()):>15,.2f} units")
# print(f"\nEquipment Requirements:")
# for process in sorted(equipment_needed.keys()):
#     print(f"  Process {process}: {int(equipment_needed[process])} units")
# total_equipment = sum(equipment_needed.values())
# print(f"  TOTAL: {int(total_equipment)} equipment units")

# print("\n--- TASK 2 SUMMARY ---")
# print(f"\nFactory Outbound Storage:")
# print(f"  Total Units:    {sum(factory_storage.values()):>12,.2f}")
# print(f"  Floor Space:    {factory_floor_sqft:>12,.2f} sq ft")
# print(f"\nWarehouse A (Client A - 90 miles North):")
# print(f"  Total Units:    {sum(buffer_stock_a.values()):>12,.2f}")
# print(f"  Floor Space:    {warehouse_a_floor_sqft:>12,.2f} sq ft")
# print(f"  Building Cost:  ${warehouse_a_cost:>12,.2f}")
# print(f"\nWarehouse B (Client B - 110 miles South):")
# print(f"  Total Units:    {sum(buffer_stock_b.values()):>12,.2f}")
# print(f"  Floor Space:    {warehouse_b_floor_sqft:>12,.2f} sq ft")
# print(f"  Building Cost:  ${warehouse_b_cost:>12,.2f}")
# print(f"\nTotal Warehouse Investment: ${warehouse_a_cost + warehouse_b_cost:>15,.2f}")

# print("\n" + "="*80)
# print("[OK] ANALYSIS COMPLETE")
# print("="*80)
# print("\nOutput Files:")
# print("  1. Task1_Demand_Fulfillment_Capacity_Plan.csv")
# print("  2. Task2_Finished_Storage_Capacity_Plan.csv")
# print("\n[OK] All calculations verified - data loaded from CSV files")
# print("="*80)
