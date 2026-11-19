#!/usr/bin/env python3
"""Print Supplementary Tables S1 and S3 from their data files (the source of the tables in the appendix docx).

S1: data/tableS1_direct_ras_inhibitors.csv  (one row per agent; status as of 18 November 2026)
S3: data/tableS3_resistance_mechanisms.csv  (frequencies from Awad et al. NEJM 2021 and Zhao et al. Nature 2021)
Bracketed numbers refer to the main-text reference list.
"""
import csv, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
for name in ('tableS1_direct_ras_inhibitors.csv', 'tableS3_resistance_mechanisms.csv'):
    rows = list(csv.DictReader(open(os.path.join(D, name), encoding='utf-8')))
    print(f'== {name}: {len(rows)} rows')
    for r in rows:
        print('  ' + ' | '.join(v for v in r.values() if v)[:200])
