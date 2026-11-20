#!/usr/bin/env python3
"""Print every number reported in Section 5.1, the Supplementary Methods and the Supplementary Figure S2 legend.

Usage: python3 summarise_trials.py [csv] [--all-targeted]
  default csv: ../data/trials_curated.csv
  The analysis set is the RAS-targeted trials, excluding trials that enrol only
  patients with haematological malignancies (the review covers solid tumours);
  --all-targeted keeps them (used to check the legacy counts).
"""
import csv, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
path = args[0] if args else os.path.join(HERE, '..', 'data', 'trials_curated.csv')
rows = list(csv.DictReader(open(path, newline='', encoding='utf-8')))
P = lambda a, b: '%d (%.1f%%)' % (a, 100 * a / b)

print('corpus records:', len(rows), '| first posted', min(r['first_posted_year'] for r in rows), '-', max(r['first_posted_year'] for r in rows))
tiers = Counter(r['ras_tier'] for r in rows)
for k, v in tiers.most_common(): print('  tier', k, P(v, len(rows)))
targ = [r for r in rows if r['ras_tier'] == 'RAS-targeted']
haem = [r for r in targ if r['tumour_group'] == 'Haematologic malignancy']
print('RAS-targeted:', len(targ), '| haematological-only:', [r['nct_id'] for r in haem])
T = targ if '--all-targeted' in sys.argv else [r for r in targ if r not in haem]
n = len(T); print('ANALYSIS SET n =', n)

ph = Counter()
for r in T:
    p = r['phase']
    ph['Phase 1' if p in ('Phase 1', 'Early Phase 1') else 'Phase 1/2' if p == 'Phase 1/Phase 2' else
       'Phase 2' if p == 'Phase 2' else 'Phase 2/3 or 3' if p in ('Phase 2/Phase 3', 'Phase 3') else p] += 1
for k in ['Phase 1', 'Phase 1/2', 'Phase 2', 'Phase 2/3 or 3']: print('  ', k, P(ph[k], n))
print('   early phase 1:', sum(r['phase'] == 'Early Phase 1' for r in T), '| phase 2/3:', sum(r['phase'] == 'Phase 2/Phase 3' for r in T))

def cls(tc):
    for k, lab in [('KRAS G12C', 'G12C'), ('KRAS G12D', 'G12D'), ('pan-RAS / multi-selective', 'multi/pan'), ('vaccine', 'vaccine/TCR-T')]:
        if k in tc: return lab
    return 'other/unspecified'
cc = Counter(cls(r['target_class']) for r in T)
print('  classes:', dict(cc))
multi = Counter(cls(r['target_class']) for r in T if '|' in r['interventions'])
print('  >1 registered intervention by class:', dict(multi), '| total', P(sum(multi.values()), n))

has = lambda r, c: c in r['countries'].split('; ')
print('  US >=1 site', P(sum(has(r, 'United States') for r in T), n), '| China >=1 site', P(sum(has(r, 'China') for r in T), n))
print('  US only', sum(r['countries'] == 'United States' for r in T), '| China only', sum(r['countries'] == 'China' for r in T))
NA = {'United States', 'Canada', 'Puerto Rico'}; EA = {'China', 'Japan', 'South Korea', 'Taiwan', 'Hong Kong'}
EU = {"Spain", "Italy", "France", "Germany", "United Kingdom", "Belgium", "Poland", "Netherlands", "Greece", "Denmark",
      "Switzerland", "Austria", "Hungary", "Portugal", "Romania", "Sweden", "Finland", "Norway", "Ukraine", "Czechia",
      "Ireland", "Bulgaria", "Russia", "Serbia", "Croatia", "Slovakia", "Estonia", "Latvia", "Slovenia", "Iceland",
      "Georgia", "Turkey (Türkiye)"}
reg = Counter(); nmr = 0; nos = 0
for r in T:
    cs = [c for c in r['countries'].split('; ') if c]
    if not cs: nos += 1; continue
    rs = {('North America' if c in NA else 'East Asia' if c in EA else 'Europe' if c in EU else 'Other') for c in cs}
    reg.update(rs); nmr += len(rs) > 1
print('  regions', dict(reg), '| multi-region', nmr, '| no site', nos, '| multinational', P(sum(r['is_multinational'] == 'yes' for r in T), n))
tg = Counter(b for r in T for b in r['tumour_group'].split('; '))
for k in ['Non-small cell lung cancer', 'Advanced solid tumours (histology-agnostic)', 'Pancreatic cancer', 'Colorectal cancer']:
    print('  tumour', k, P(tg[k], n))

def yr(lo, hi):
    a = [r for r in rows if lo <= int(r['first_posted_year']) <= hi]
    t = [r for r in a if r in T]
    return '%d of %d (%.1f%%)' % (len(t), len(a), 100 * len(t) / len(a))
print('  registration: before 2018', yr(0, 2017), '| 2021-2023', yr(2021, 2023), '| 2024-2026', yr(2024, 2026))
print('  targeted first posted >=2021', P(sum(int(r['first_posted_year']) >= 2021 for r in T), n))
ind = [r for r in T if r['lead_sponsor_class'] == 'INDUSTRY']
late = [r for r in T if r['phase'] in ('Phase 2/Phase 3', 'Phase 3')]
print('  industry lead', P(len(ind), n), '| of phase 2/3-3:', sum(r['lead_sponsor_class'] == 'INDUSTRY' for r in late), 'of', len(late))
ac = [r for r in T if r['lead_sponsor_class'] != 'INDUSTRY']
print('  non-industry', P(len(ac), n), '| phase>=2:', sum(r['phase'] not in ('Phase 1', 'Early Phase 1', 'Phase 1/Phase 2') for r in ac),
      '| G12C:', sum('KRAS G12C' in r['target_class'] for r in ac))
