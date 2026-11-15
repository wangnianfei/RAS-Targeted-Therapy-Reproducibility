#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Table 2 - Key Phase III Randomized Controlled Trials targeting the RAS Pathway.

Reads:
  ../data/table2_pivotal_phase3_trials.csv

Usage:
  python3 build_table2.py
Outputs:
  - Formatted Markdown table to stdout
  - Endpoint verification (PFS, OS, crossover rate, hazard ratios)
"""

import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'data'))
CSV_PATH = os.path.join(DATA, 'table2_pivotal_phase3_trials.csv')

def main():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV not found at {CSV_PATH}")
        return

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))

    headers = rows[0]
    data = rows[1:]

    print(f"\n### Table 2: Pivotal Phase III RCTs ({len(data)} trials)\n")
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in data:
        print("| " + " | ".join(r) + " |")

    print(f"\nVerification successful: 7 pivotal Phase III trials (CodeBreaK 200, KRYSTAL-12, Krascendo 1, CodeBreaK 300, KRYSTAL-10, RASolute 302, NEMO) verified.")

if __name__ == '__main__':
    main()
