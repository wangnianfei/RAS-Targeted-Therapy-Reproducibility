#!/usr/bin/env python3
"""Derive Figure 2 plotting tables directly from the MSK-IMPACT 2017 cBioPortal download
(Zehir et al., Nat Med 2017; PMID 28481359; 10,945 samples).

Inputs : data/cbioportal_mutations.json                   {gene: [mutation records]}
         data/cbioportal_sample_cancertype.json           {sample_id: cancer type}
         data/cbioportal_sample_cancertype_detailed.json  {sample_id: detailed cancer type}
Outputs: data/pancancer_isoform_frequencies.csv  % of samples with >=1 missense mutation per gene
         data/kras_allele_frequencies.csv        share of KRAS missense mutations by allele
         data/cohort_ras_rates.csv               cohort-wide % of samples with a RAS missense mutation
Only missense mutations are counted (activating RAS alterations are missense).
Pancreatic cancer is restricted to the detailed type 'Pancreatic Adenocarcinoma' (384 of the
502 pancreatic samples); the broader 'Pancreatic Cancer' group also contains neuroendocrine,
acinar-cell and other non-ductal tumours, which lowers the apparent KRAS rate (73.5%).
"""
import csv, json, os, collections as C
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
mut = json.load(open(os.path.join(D, 'cbioportal_mutations.json')))
ctype = json.load(open(os.path.join(D, 'cbioportal_sample_cancertype.json')))
detailed = json.load(open(os.path.join(D, 'cbioportal_sample_cancertype_detailed.json')))
# relabel pancreatic adenocarcinoma so that the PDAC rows use ductal adenocarcinoma only
group = {k: ('PDAC' if detailed.get(k) == 'Pancreatic Adenocarcinoma' else v) for k, v in ctype.items()}

TYPES = [('PDAC', 'Pancreatic (PDAC)'), ('Colorectal Cancer', 'Colorectal (CRC)'),
         ('Non-Small Cell Lung Cancer', 'NSCLC'), ('Endometrial Cancer', 'Endometrial'),
         ('Melanoma', 'Melanoma'), ('Thyroid Cancer', 'Thyroid'), ('Bladder Cancer', 'Bladder')]
mis = {g: [r for r in v if r['type'] == 'Missense_Mutation'] for g, v in mut.items()}
mutated = {g: {r['sample'] for r in v} for g, v in mis.items()}

with open(os.path.join(D, 'pancancer_isoform_frequencies.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cancer_type', 'n_samples', 'KRAS', 'NRAS', 'HRAS'])
    for src, lab in TYPES:
        s = {k for k, v in group.items() if v == src}
        w.writerow([lab, len(s)] + [round(100 * len(s & mutated[g]) / len(s), 1) for g in ('KRAS', 'NRAS', 'HRAS')])

def allele(p):
    if p in ('G12C', 'G12D', 'G12V', 'G12R', 'G13D'): return p
    if p.startswith('Q61'): return 'Q61X'
    return 'Other'
with open(os.path.join(D, 'kras_allele_frequencies.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cancer_type', 'n_kras_mutations', 'allele', 'pct'])
    for src, lab in [('PDAC', 'PDAC'), ('Colorectal Cancer', 'CRC'), ('Non-Small Cell Lung Cancer', 'NSCLC')]:
        al = C.Counter(allele(r['protein']) for r in mis['KRAS'] if group.get(r['sample']) == src)
        n = sum(al.values())
        for a in ('G12C', 'G12D', 'G12V', 'G12R', 'G13D', 'Q61X', 'Other'):
            w.writerow([lab, n, a, round(al[a] / n, 4)])
ras = mutated['KRAS'] | mutated['NRAS'] | mutated['HRAS']
with open(os.path.join(D, 'cohort_ras_rates.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['cohort', 'n_samples', 'pct_any_RAS_missense', 'pct_KRAS_missense'])
    w.writerow(['MSK-IMPACT 2017 (all tumour types)', len(ctype), round(100 * len(ras) / len(ctype), 1),
                round(100 * len(mutated['KRAS']) / len(ctype), 1)])
print(open(os.path.join(D, 'pancancer_isoform_frequencies.csv')).read())
print(open(os.path.join(D, 'cohort_ras_rates.csv')).read())
print(open(os.path.join(D, 'kras_allele_frequencies.csv')).read())
