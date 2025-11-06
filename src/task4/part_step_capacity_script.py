# -*- coding: utf-8 -*-
"""
Calcul des besoins machine par pièce/étape/opération et par ANNEE,
pour 1 shift et 2 shifts, à partir de:
../results/Task4_Demand_Fulfilment_Capacity_Plan_by_year.csv

Sorties par année dans: ../results/by_year/<Year N>/...
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path

# =========================
# Paramètres & Données fixes
# =========================
# Gammes d'opérations par pièce
process_operations = {
    'P1':  ['B', 'A', 'B', 'C', 'D', 'I', 'J'],
    'P2':  ['A', 'C', 'D', 'H', 'J'],
    'P3':  ['B', 'D', 'C', 'I', 'J'],
    'P4':  ['A', 'B', 'D', 'G', 'H'],
    'P5':  ['B', 'C', 'D', 'I'],
    'P6':  ['A', 'B', 'C', 'D', 'H', 'I', 'J'],
    'P7':  ['E', 'F', 'C', 'D', 'I', 'J'],
    'P8':  ['E', 'H', 'J', 'I'],
    'P9':  ['F', 'G', 'E', 'G', 'I', 'J'],
    'P10': ['E', 'F', 'I', 'J'],
    'P11': ['E', 'G', 'E', 'G', 'I'],
    'P12': ['E', 'G', 'F', 'I', 'J'],
    'P13': ['E', 'F', 'G', 'F', 'G', 'H', 'I'],
    'P14': ['E', 'F', 'G', 'H'],
    'P15': ['E', 'G', 'F', 'H', 'J'],
    'P16': ['F', 'H', 'I', 'J'],
    'P17': ['K', 'L', 'M'],
    'P18': ['K', 'L', 'K', 'M'],
    'P19': ['L', 'M', 'L', 'M'],
    'P20': ['L', 'K', 'M']
}

# Temps de chaque étape (min)
process_times = {
    'P1':  [2.5, 1.0, 2.5, 0.5, 2.5, 1.25, 2.5],
    'P2':  [1.25, 0.5, 2.5, 1.0, 2.5],
    'P3':  [1.75, 3.0, 0.75, 1.5, 2.5],
    'P4':  [1.0, 2.0, 3.0, 0.25, 1.25],
    'P5':  [1.5, 0.75, 3.5, 1.75],
    'P6':  [0.75, 1.25, 0.5, 3.0, 1.0, 1.25, 2.75],
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
    'P18': [0.75, 1.25, 0.5, 3.75],
    'P19': [2.25, 2.5, 2.0, 3.75],
    'P20': [2.0, 0.75, 3.0],
}

# Paramètres communs
HOURS_PER_SHIFT = 8
DAYS_PER_WEEK = 5
EFFICIENCY = 0.90
RELIABILITY = 0.98
EFFECTIVE_AVAILABILITY = EFFICIENCY * RELIABILITY  # 0.882

# =========================
# Fonctions utilitaires
# =========================
def minutes_per_machine_per_week(shifts_per_day: int) -> float:
    hours_per_week = shifts_per_day * HOURS_PER_SHIFT * DAYS_PER_WEEK
    return hours_per_week * 60 * EFFECTIVE_AVAILABILITY

def validate_routings(parts):
    for p in parts:
        ops = process_operations.get(p)
        tms = process_times.get(p)
        if ops is None or tms is None:
            raise ValueError(f"Pièce {p}: gamme/temps manquants dans les dictionnaires.")
        if len(ops) != len(tms):
            raise ValueError(f"Pièce {p}: longueur mismatch entre opérations ({len(ops)}) et temps ({len(tms)}).")

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

# =========================
# Calcul pour une année donnée
# =========================
def calculate_for_shifts_and_year(year_label: str, weekly_demand: dict, shifts_per_day: int, outdir: str):
    """
    Calcule les machines pour une année donnée et un nombre de shifts/jour.
    Génère les CSV détaillés + résumés dans outdir.
    Retourne le DataFrame 'total_machines_per_operation' pour comparaison 1 vs 2 shifts.
    """
    validate_routings(weekly_demand.keys())

    m_per_week = minutes_per_machine_per_week(shifts_per_day)

    # Table détaillée par étape
    data_rows = []
    for part, demand in weekly_demand.items():
        ops = process_operations[part]
        tms = process_times[part]
        for step_num, (op, time_min) in enumerate(zip(ops, tms), start=1):
            data_rows.append({
                'Year': year_label,
                'Part': part,
                'Step': step_num,
                'Operation': op,
                'Weekly_Demand_Units': float(demand),
                'Time_per_Unit_Min': float(time_min),
                'Time_Required_Min_Week': float(demand) * float(time_min),
            })
    df = pd.DataFrame(data_rows)

    # Machines dédiées par (Part, Operation)
    part_op = df.groupby(['Part', 'Operation'], as_index=False)['Time_Required_Min_Week'].sum()
    part_op['Number_of_Machines'] = np.ceil(part_op['Time_Required_Min_Week'] / m_per_week).astype(int)

    # Join vers le détail
    df = df.merge(part_op[['Part', 'Operation', 'Number_of_Machines']], on=['Part', 'Operation'], how='left')

    # Écritures
    detail_csv = os.path.join(outdir, f'Part_Step_Process_Capacity_Requirements_{shifts_per_day}_shifts.csv')
    df.to_csv(detail_csv, index=False)

    # Résumé "Step_Info" (pivot pièce × rang d’étape)
    df['Step_Info'] = df['Operation'] + ': ' + df['Number_of_Machines'].astype(int).astype(str)
    step_summary = df.pivot(index='Part', columns='Step', values='Step_Info').fillna('')
    step_summary_csv = os.path.join(outdir, f'Part_Step_Machines_Summary_{shifts_per_day}_shifts.csv')
    step_summary.to_csv(step_summary_csv)

    # Totaux
    total_by_op = part_op.groupby('Operation', as_index=False)['Number_of_Machines'].sum()
    total_by_op = total_by_op.rename(columns={'Number_of_Machines': 'Total_Machines_Across_Parts'})
    total_by_op_csv = os.path.join(outdir, f'Total_Machines_per_Operation_{shifts_per_day}_shifts.csv')
    total_by_op.to_csv(total_by_op_csv, index=False)

    total_by_part = part_op.groupby('Part', as_index=False)['Number_of_Machines'].sum()
    total_by_part = total_by_part.rename(columns={'Number_of_Machines': 'Total_Machines_for_Part'})
    total_by_part_csv = os.path.join(outdir, f'Total_Machines_per_Part_{shifts_per_day}_shifts.csv')
    total_by_part.to_csv(total_by_part_csv, index=False)

    print(f"[{year_label}] {shifts_per_day} shift(s) → fichiers écrits dans {outdir}")
    return total_by_op

# =========================
# Programme principal
# =========================
def main():
    # 1) Lecture du CSV multi-années
    input_csv = r"results\task4\Task4_Demand_Fulfillment_Capacity_Plan_by_year.csv"
    df_all = pd.read_csv(input_csv)

    # 2) Liste des années (chaînes du type 'Year 1', 'Year 2', ...)
    years = sorted(df_all['Year'].unique(), key=lambda s: (int(''.join([c for c in s if c.isdigit()]) or 0), s))

    for year in years:
        df_y = df_all[df_all['Year'] == year].copy()

        # Dictionnaire demande hebdo pour l'année
        weekly_demand_year = dict(zip(df_y['Part'], df_y['Weekly_Demand_Units']))

        # Répertoire de sortie par année
        year_sanitized = year.replace(' ', '_')
        base_dir = Path('..') / 'results' / 'task4' / 'by_year'
        outdir = base_dir / year_sanitized
        outdir.mkdir(parents=True, exist_ok=True)

        # 3) Calculs pour 1 shift et 2 shifts
        res_1 = calculate_for_shifts_and_year(year, weekly_demand_year, shifts_per_day=1, outdir=outdir)
        res_2 = calculate_for_shifts_and_year(year, weekly_demand_year, shifts_per_day=2, outdir=outdir)

        # 4) Comparaison 1 vs 2 shifts par opération (pour l'année)
        comparison = pd.merge(res_1, res_2, on='Operation', suffixes=('_1_shift', '_2_shifts'))
        comp_csv = os.path.join(outdir, 'Machine_Comparison_1_vs_2_shifts.csv')
        comparison.to_csv(comp_csv, index=False)

        print(f"[{year}] Comparaison écrite → {comp_csv}")

if __name__ == '__main__':
    main()
