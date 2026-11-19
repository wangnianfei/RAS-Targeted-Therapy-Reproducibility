#!/usr/bin/env python3
"""TCGA PanCancer Atlas RAS mutation rate quoted in Section 2.2 (10.7% of 10,967 samples).

Queries the public cBioPortal API (needs internet; not run by reproduce_all.sh) for all
32 *_tcga_pan_can_atlas_2018 studies and counts samples with any KRAS, NRAS or HRAS mutation.
Denominator: all samples in each study ('_all' sample list), as shown by cBioPortal.
Output: data/tcga_pancan_ras_rate.csv (the committed copy was produced on 20 November 2026).
"""
import csv, json, os, urllib.request
B = 'https://www.cbioportal.org/api/'
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def get(u, data=None):
    req = urllib.request.Request(B + u, data=json.dumps(data).encode() if data else None,
                                 headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=120))

studies = [s['studyId'] for s in get('studies?keyword=pan_can_atlas_2018&pageSize=100')
           if s['studyId'].endswith('_tcga_pan_can_atlas_2018')]
n_all = n_seq = 0; mut = set(); mis = set()
for s in studies:
    n_all += len(get(f'sample-lists/{s}_all')['sampleIds'])
    n_seq += len(get(f'sample-lists/{s}_sequenced')['sampleIds'])
    for m in get(f'molecular-profiles/{s}_mutations/mutations/fetch?projection=SUMMARY',
                 {'entrezGeneIds': [3845, 4893, 3265], 'sampleListId': f'{s}_sequenced'}):
        mut.add(m['sampleId'])
        if m['mutationType'] == 'Missense_Mutation': mis.add(m['sampleId'])
with open(os.path.join(D, 'tcga_pancan_ras_rate.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['studies', 'samples_all', 'samples_sequenced', 'samples_any_RAS_mutation', 'pct_of_all', 'samples_RAS_missense', 'pct_missense_of_all'])
    w.writerow([len(studies), n_all, n_seq, len(mut), round(100 * len(mut) / n_all, 1), len(mis), round(100 * len(mis) / n_all, 1)])
print(open(os.path.join(D, 'tcga_pancan_ras_rate.csv')).read())
