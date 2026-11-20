#!/usr/bin/env python3
"""Supplementary Figure S1 (revised).

a, Qualitative matrix linking the seven acquired-resistance classes of Supplementary Table S3 (rows)
   to six combination or switching strategies (columns). Filled cells reproduce the strategy listed for
   each class in Table S3 ("primary"); hatched cells mark strategies discussed for that class in main-text
   Section 5.3 ("secondary"). The matrix is a summary of the review, not new data.
b, Frequency of putative resistance mechanisms after adagrasib monotherapy in the cohort of
   Awad et al., N Engl J Med 2021;384:2382-93 (doi:10.1056/NEJMoa2105281): 17/38 patients with >=1
   mechanism; 7/38 with multiple coincident mechanisms; histologic (squamous) transformation in 2 of the
   10 patients with a repeat tissue biopsy at progression (9 NSCLC, 1 colorectal cancer).
Outputs: ../figures/FigS1.{pdf,png,tif}
"""
import os, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.abspath(os.path.join(HERE, '..', 'figures')); os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
                     'pdf.fonttype': 42, 'ps.fonttype': 42, 'font.size': 6.5})

ROWS = ['On-target KRAS\nalterations', 'Upstream reactivation\n(MET, EGFR, fusions, NF1)',
        'SHP2/SOS1-mediated\nnucleotide exchange', 'Downstream MAPK bypass\n(NRAS, BRAF, MAP2K1)',
        'PI3K-AKT bypass\n(PTEN loss of function)', 'STK11 / KEAP1\nco-mutation (baseline)',
        'Lineage plasticity\n(squamous transformation)']
COLS = ['Switch to a\nRAS(ON) inhibitor', 'RTK antibody\nor TKI', 'SHP2 or SOS1\ninhibitor',
        'RAF, MEK or ERK\ninhibitor', 'PI3K, AKT or\nmTOR inhibitor', 'Immunotherapy and/or\nchemotherapy']
# In-cell notes so that each filled cell reads exactly as the strategy in Supplementary Table S3 (round 20)
NOTES = {(5, 5): 'with a direct\nRAS inhibitor', (6, 5): 'histology-\ndirected'}
# One palette for both panels, shared with Supplementary Figure S2: navy = filled cells and bars
NAVY, LIGHT, EMPTY = '#1F3F73', '#C6D7EE', '#F1F3F6'
PRIMARY = {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 5)}
SECONDARY = {(1, 2)}

fig = plt.figure(figsize=(180 / 25.4, 105 / 25.4))
ax = fig.add_axes([0.25, 0.30, 0.73, 0.55])
nr, nc = len(ROWS), len(COLS)
for i in range(nr):
    for j in range(nc):
        y = nr - 1 - i
        if (i, j) in PRIMARY:
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor=NAVY, edgecolor='white', lw=1.2))
            if (i, j) in NOTES:
                ax.text(j + 0.5, y + 0.5, NOTES[(i, j)], ha='center', va='center', fontsize=5.8, color='white', linespacing=1.1)
        elif (i, j) in SECONDARY:
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor=LIGHT, edgecolor='white', lw=1.2, hatch='////'))
        else:
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor=EMPTY, edgecolor='white', lw=1.2))
ax.set_xlim(0, nc); ax.set_ylim(0, nr)
ax.set_xticks([j + 0.5 for j in range(nc)]); ax.set_xticklabels(COLS, fontsize=6.2)
ax.xaxis.tick_top()
ax.set_yticks([nr - 1 - i + 0.5 for i in range(nr)]); ax.set_yticklabels(ROWS, fontsize=6.2)
ax.tick_params(length=0)
for s in ax.spines.values(): s.set_visible(False)
fig.text(0.01, 0.97, 'a', fontsize=9, fontweight='bold', va='top')
lg = fig.add_axes([0.25, 0.235, 0.73, 0.04]); lg.axis('off')
lg.add_patch(Rectangle((0.0, 0.1), 0.025, 0.8, facecolor=NAVY, transform=lg.transAxes))
lg.text(0.033, 0.5, 'Strategy listed for this class in Supplementary Table S3', va='center', fontsize=6, transform=lg.transAxes)
lg.add_patch(Rectangle((0.52, 0.1), 0.025, 0.8, facecolor=LIGHT, hatch='////', transform=lg.transAxes))
lg.text(0.553, 0.5, 'Additional strategy discussed in Section 5.3', va='center', fontsize=6, transform=lg.transAxes)

bx = fig.add_axes([0.25, 0.075, 0.47, 0.13])
labels = ['≥1 putative mechanism (17/38)', 'Multiple coincident mechanisms (7/38)',
          'Squamous transformation\n(2/10 repeat tissue biopsies)']
vals = [17 / 38 * 100, 7 / 38 * 100, 2 / 10 * 100]
bx.barh(range(3)[::-1], vals, color=NAVY, height=0.6)
for k, v in enumerate(vals): bx.text(v + 1, 2 - k, f'{v:.0f}%', va='center', fontsize=6)
bx.set_yticks(range(3)[::-1]); bx.set_yticklabels(labels, fontsize=6)
bx.set_xlim(0, 60); bx.set_xlabel('Patients (%)', fontsize=6.2)
for s in ('top', 'right'): bx.spines[s].set_visible(False)
bx.tick_params(labelsize=6)
fig.text(0.01, 0.21, 'b', fontsize=9, fontweight='bold', va='top')
fig.text(0.75, 0.14, 'Adagrasib monotherapy\n(27 NSCLC, 10 CRC,\n1 appendiceal cancer;\nAwad et al. 2021)', fontsize=5.8, va='center', color='#333333')

for ext in ('pdf', 'png'):
    fig.savefig(os.path.join(FIG, f'FigS1.{ext}'), dpi=500)
subprocess.run(['magick', os.path.join(FIG, 'FigS1.png'), '-units', 'PixelsPerInch', '-density', '500',
                '-compress', 'LZW', os.path.join(FIG, 'FigS1.tif')], check=True)
print('Figure S1 written to', FIG)
