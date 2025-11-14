"""
Scan results/Task3/Part for redundant/useless data in CSV files.
Generates a summary CSV and a human-readable report.
"""
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).parent.parent.parent.parent
results_dir = BASE / 'results' / 'Task3' / 'Part'
output_dir = results_dir

summary_rows = []

for csv_path in results_dir.rglob('*.csv'):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        summary_rows.append({
            'file': str(csv_path.relative_to(BASE)),
            'status': f'ERROR_READING: {e}',
            'rows': None,
            'cols': None,
            'percent_rows_all_zero_or_nan': None,
            'num_constant_columns': None,
            'num_all_zero_columns': None,
            'num_duplicate_rows': None,
            'percent_missing_cells': None
        })
        continue

    rows, cols = df.shape

    # percent rows where all values are zero or NaN (for numeric cols)
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] > 0:
        all_zero_or_nan = numeric_df.replace(0, np.nan).isna().all(axis=1)
        percent_rows_all_zero_or_nan = 100.0 * all_zero_or_nan.sum() / rows if rows>0 else 0
    else:
        percent_rows_all_zero_or_nan = 0.0

    # constant columns (all values equal or all NaN)
    num_constant_columns = 0
    num_all_zero_columns = 0
    for col in df.columns:
        col_vals = df[col].dropna()
        if col_vals.empty:
            num_constant_columns += 1
            continue
        if col_vals.nunique() == 1:
            num_constant_columns += 1
            # check if the constant is zero
            try:
                if pd.to_numeric(col_vals, errors='coerce').fillna(0).eq(0).all():
                    num_all_zero_columns += 1
            except Exception:
                pass

    # duplicate rows
    num_duplicate_rows = rows - df.drop_duplicates().shape[0]

    # percent missing cells
    total_cells = rows * cols
    missing_cells = int(df.isna().sum().sum())
    percent_missing_cells = 100.0 * missing_cells / total_cells if total_cells>0 else 0

    summary_rows.append({
        'file': str(csv_path.relative_to(BASE)),
        'status': 'OK',
        'rows': int(rows),
        'cols': int(cols),
        'percent_rows_all_zero_or_nan': round(percent_rows_all_zero_or_nan,2),
        'num_constant_columns': int(num_constant_columns),
        'num_all_zero_columns': int(num_all_zero_columns),
        'num_duplicate_rows': int(num_duplicate_rows),
        'percent_missing_cells': round(percent_missing_cells,2)
    })

# Save summary
summary_df = pd.DataFrame(summary_rows)
summary_file = output_dir / 'PART_RESULTS_SCAN_SUMMARY.csv'
summary_df.to_csv(summary_file, index=False)

# Human readable report
report_file = output_dir / 'PART_RESULTS_SCAN_REPORT.txt'
with open(report_file, 'w') as f:
    f.write('PART RESULTS SCAN REPORT\n')
    f.write('='*60 + '\n\n')
    for _, row in summary_df.iterrows():
        f.write(f"File: {row['file']}\n")
        f.write(f"  Status: {row['status']}\n")
        if row['status']=='OK':
            f.write(f"  Rows: {row['rows']}, Cols: {row['cols']}\n")
            f.write(f"  % rows all-zero-or-NaN (numeric cols): {row['percent_rows_all_zero_or_nan']}%\n")
            f.write(f"  Constant columns: {row['num_constant_columns']} (all-zero columns: {row['num_all_zero_columns']})\n")
            f.write(f"  Duplicate rows: {row['num_duplicate_rows']}\n")
            f.write(f"  % missing cells: {row['percent_missing_cells']}%\n")
        f.write('\n')

print('Saved summary:', summary_file)
print('Saved report:', report_file)
