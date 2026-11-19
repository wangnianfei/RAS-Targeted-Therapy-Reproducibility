#!/usr/bin/env python3
"""Second, record-level review of the machine classification in data/trials_1182.csv.

Input   data/trials_1182.csv                 output of curate_trials.py (left unchanged)
        data/classification_corrections.csv  one row per verified correction, with reason
Output  data/trials_curated.csv              analysis corpus used for Figure 4 and Section 5.1
        data/trials_excluded_on_review.csv   records removed from the corpus, with reason

Why a second step: curate_trials.py flags a trial as RAS-targeted when a RAS-directed
agent name or token appears anywhere in the record, including keywords, conditions and
eligibility criteria, and it recognises RAS-directed agents only from a name list.
Checking every RAS-targeted trial whose interventions did not themselves name a listed
agent, and every non-targeted trial whose title or interventions suggested a RAS-directed
agent, against the registry intervention descriptions (and, where these were silent,
sponsor or NCI Drug Dictionary descriptions; 20 November 2026) found:
  * trials of non-RAS agents (MEK, RAF, EGFR/PI3K, BET/PARP inhibitors) counted as RAS-targeted;
  * trials of RAS-directed agents with unlisted code names (KRAS inhibitors, KRAS-specific
    TCR-T cells, vaccines and a T-cell engager) counted as biomarker-selected;
  * pharmacology studies in healthy volunteers or participants with organ impairment, and
    non-oncology studies, that had passed the oncology filter through text outside the
    condition list.
An agent with an undisclosed mechanism is counted as RAS-directed only if its first-in-human
trial is restricted to a single KRAS allele; otherwise it stays in its machine-assigned tier.

The tumour-type buckets are also re-derived from the condition list, because the original
patterns missed common spellings ("Carcinoma, Non-Small-Cell Lung", "PDAC",
"Colon Adenocarcinoma", "Malignant Solid Neoplasm").

Usage: python3 apply_classification_corrections.py
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
SRC = os.path.join(DATA, 'trials_1182.csv')
CORR = os.path.join(DATA, 'classification_corrections.csv')
OUT = os.path.join(DATA, 'trials_curated.csv')
EXCL = os.path.join(DATA, 'trials_excluded_on_review.csv')

TUMOUR_BUCKETS = [
    ('Non-small cell lung cancer', r'non.?small.?cell|nsclc|lung adenocarcinom'),
    ('Small cell lung cancer', r'(?<!non-)(?<!non )small.?cell lung|\bsclc\b'),
    ('Colorectal cancer', r'colorect|colon (cancer|adenocarcinom|carcinom)|rectal (cancer|adenocarcinom|carcinom)|mcrc|\bcrc\b'),
    ('Pancreatic cancer', r'pancrea|\bpdac\b'),
    ('Biliary tract / hepatobiliary', r'cholangio|biliary|gallbladder|hepatocellular|liver cancer'),
    ('Melanoma / skin', r'melanom|cutaneous squamous|basal cell|skin cancer'),
    ('Head and neck', r'head and neck|hnscc|oral cavity|nasopharyn|laryng|salivary|thyroid'),
    ('Haematologic malignancy', r'leukaem|leukem|lymphom|myelom|myelodysplas|myeloprolifer|myelofibros|polycythemia|thrombocythemia|cmml|\baml\b|\bcml\b|histiocyt'),
    ('Gynaecologic', r'ovarian|endometri|cervic|uterin'),
    ('Gastro-oesophageal', r'gastric|oesophag|esophag|stomach|gastroesophageal'),
    ('Genitourinary', r'prostate|bladder|urothelial|renal cell|kidney cancer|testic'),
    ('Breast', r'breast'),
    ('CNS', r'gliom|glioblast|medulloblast|brain|\bcns\b'),
    ('Advanced solid tumours (histology-agnostic)',
     r'solid (tumo|neoplasm|cancer|malignan)|advanced (cancer|malignan)|metastatic cancer|'
     r'malignant (tumo|neoplasm)|neoplasm malignant|^neoplasms?$|^cancer$'),
]


def buckets(conditions):
    conds = conditions.split('; ')
    out = [b for b, rx in TUMOUR_BUCKETS if any(re.search(rx, c, re.I) for c in conds)]
    return '; '.join(out) if out else 'Other / unspecified'


with open(SRC, newline='', encoding='utf-8') as f:
    rd = csv.DictReader(f); cols = rd.fieldnames; rows = list(rd)
by_id = {r['nct_id']: r for r in rows}

excluded = {}
for c in csv.DictReader(open(CORR, newline='', encoding='utf-8')):
    r = by_id.get(c['nct_id'])
    if r is None:
        sys.exit('Unknown trial in corrections file: ' + c['nct_id'])
    if c['field'] == 'exclude':
        excluded[c['nct_id']] = c['reason']
        continue
    if r[c['field']] != c['old_value']:
        sys.exit('Unexpected %s for %s: %r (expected %r)' % (c['field'], c['nct_id'], r[c['field']], c['old_value']))
    r[c['field']] = c['new_value']

for r in rows:
    r['tumour_group'] = buckets(r['conditions'])

kept = [r for r in rows if r['nct_id'] not in excluded]
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(kept)
with open(EXCL, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['nct_id', 'brief_title', 'conditions', 'ras_tier_machine', 'exclusion_reason'])
    w.writeheader()
    for r in rows:
        if r['nct_id'] in excluded:
            w.writerow({'nct_id': r['nct_id'], 'brief_title': r['brief_title'], 'conditions': r['conditions'],
                        'ras_tier_machine': r['ras_tier'], 'exclusion_reason': excluded[r['nct_id']]})
print('input %d records; excluded %d; curated corpus %d' % (len(rows), len(excluded), len(kept)))
