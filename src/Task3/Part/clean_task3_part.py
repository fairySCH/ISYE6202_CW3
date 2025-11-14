"""
Clean Task3 Part results: remove exact duplicate rows, fill numeric missing with 0 for selected files,
archive tiny KPI files, and save cleaned outputs to results/Task3/Part/cleaned/.
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent.parent.parent.parent
results_dir = BASE / 'results' / 'Task3' / 'Part'
clean_dir = results_dir / 'cleaned'
archive_dir = results_dir / 'summary_archive'
clean_dir.mkdir(parents=True, exist_ok=True)
archive_dir.mkdir(parents=True, exist_ok=True)

# Files to clean
dup_file = results_dir / 'Capacity' / 'Part_Based_Process_Workload_Breakdown.csv'
missing_fill_files = [
    results_dir / 'Capacity' / 'Part_Based_All_Parts_Flow_Distance_Breakdown.csv',
    results_dir / 'Capacity' / 'Part_Step_Machines_Summary_1_shifts.csv',
    results_dir / 'Capacity' / 'Part_Step_Machines_Summary_2_shifts.csv'
]
# Files to archive if small/single-row
archive_candidates = [results_dir / 'Cost_Analysis' / 'Part_Based_Cost_KPIs.csv']

print('Cleaning Task3 Part results...')

# 1) Remove exact duplicate rows from dup_file
if dup_file.exists():
    df_dup = pd.read_csv(dup_file)
    before = df_dup.shape[0]
    df_clean = df_dup.drop_duplicates()
    after = df_clean.shape[0]
    out_path = clean_dir / dup_file.name.replace('.csv','_CLEANED.csv')
    df_clean.to_csv(out_path, index=False)
    print(f'Removed {before-after} duplicate rows from {dup_file.name} -> {out_path.name}')
else:
    print(f'File not found: {dup_file}')

# 2) Fill numeric missing with 0 for target files and save
for f in missing_fill_files:
    if f.exists():
        df = pd.read_csv(f)
        # fill numeric columns with 0
        num_cols = df.select_dtypes(include=['number']).columns
        df[num_cols] = df[num_cols].fillna(0)
        out_path = clean_dir / f.name.replace('.csv','_CLEANED.csv')
        df.to_csv(out_path, index=False)
        print(f'Filled numeric missing values with 0 in {f.name} -> {out_path.name}')
    else:
        print(f'File not found: {f}')

# 3) Archive small/single-row KPI files
for f in archive_candidates:
    if f.exists():
        df = pd.read_csv(f)
        if df.shape[0] <= 1 or df.shape[1] <= 2:
            dest = archive_dir / f.name
            f.rename(dest)
            print(f'Archived {f.name} -> {dest.relative_to(BASE)}')
        else:
            print(f'Kept {f.name} (not small)')
    else:
        print(f'Archive candidate not found: {f}')

# 4) Save a README in cleaned folder listing files
readme = clean_dir / 'CLEANED_FILES_README.txt'
with open(readme, 'w') as fh:
    fh.write('Cleaned files created by clean_task3_part.py\n')
    fh.write('\n')
    if dup_file.exists():
        fh.write(f'- {dup_file.name} -> {dup_file.name.replace(".csv","_CLEANED.csv")} (duplicates removed)\n')
    for f in missing_fill_files:
        if f.exists():
            fh.write(f'- {f.name} -> {f.name.replace(".csv","_CLEANED.csv")} (numeric NaN -> 0)\n')

print('Cleaning complete. Cleaned files saved to', clean_dir)
