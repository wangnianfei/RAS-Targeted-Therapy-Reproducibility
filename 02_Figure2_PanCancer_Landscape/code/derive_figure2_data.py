#!/usr/bin/env python3
"""Derive Figure 2 plotting tables directly from the MSK-IMPACT 2017 cBioPortal download
(Zehir et al., Nat Med 2017; PMID 28481359; 10,945 samples).

Inputs : data/cbioportal_mutations.json          {gene: [mutation records]}
         data/cbioportal_sample_cancertype.json  {sample_id: cancer type}
Outputs: data/pancancer_isoform_frequencies.csv  % of samples with >=1 missense mutation per gene
         data/kras_allele_frequencies.csv        share of KRAS missense mutations by allele
Only missense mutations are counted (activating RAS alterations are missense).
"""
import csv, json, os, collections as C
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
mut = json.load(open(os.path.join(D, 'cbioportal_mutations.json')))
ctype = json.load(open(os.path.join(D, 'cbioportal_sample_cancertype.json')))

TYPES = [('Pancreatic Cancer', 'Pancreatic (PDAC)'), ('Colorectal Cancer', 'Colorectal (CRC)'),
         ('Non-Small Cell Lung Cancer', 'NSCLC'), ('Endometrial Cancer', 'Endometrial'),
         ('Melanoma', 'Melanoma'), ('Thyroid Cancer', 'Thyroid'), ('Bladder Cancer', 'Bladder')]
mis = {g: [r for r in v if r['type'] == 'Missense_Mutation'] for g, v in mut.items()}
mutated = {g: {r['sample'] for r in v} for g, v in mis.items()}

with open(os.path.join(D, 'pancancer_isoform_frequencies.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cancer_type', 'n_samples', 'KRAS', 'NRAS', 'HRAS'])
    for src, lab in TYPES:
        s = {k for k, v in ctype.items() if v == src}
        w.writerow([lab, len(s)] + [round(100 * len(s & mutated[g]) / len(s), 1) for g in ('KRAS', 'NRAS', 'HRAS')])

def allele(p):
    if p in ('G12C', 'G12D', 'G12V', 'G12R', 'G13D'): return p
    if p.startswith('Q61'): return 'Q61X'
    return 'Other'
with open(os.path.join(D, 'kras_allele_frequencies.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cancer_type', 'n_kras_mutations', 'allele', 'pct'])
    for src, lab in [('Pancreatic Cancer', 'PDAC'), ('Colorectal Cancer', 'CRC'), ('Non-Small Cell Lung Cancer', 'NSCLC')]:
        al = C.Counter(allele(r['protein']) for r in mis['KRAS'] if ctype.get(r['sample']) == src)
        n = sum(al.values())
        for a in ('G12C', 'G12D', 'G12V', 'G12R', 'G13D', 'Q61X', 'Other'):
            w.writerow([lab, n, a, round(al[a] / n, 4)])
print(open(os.path.join(D, 'pancancer_isoform_frequencies.csv')).read())
print(open(os.path.join(D, 'kras_allele_frequencies.csv')).read())
