#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 2 - Pan-cancer distribution of KRAS, NRAS, and HRAS mutations.

Plots:
  Panel a: Pan-cancer KRAS mutation frequencies and allele shares (G12D/V/C/R, G13D, Q61X, Other) across 16 major solid tumor types.
  Panel b: Pan-cancer NRAS mutation frequencies across 10 tumor types.
  Panel c: Pan-cancer HRAS mutation frequencies across 10 tumor types.

Data:
  MSK-IMPACT 2017 clinical sequencing cohort (10,945 sequenced samples; Zehir et al., Nat Med 2017).
  Source files in ../data/:
    - cancer_type_kras_alleles.csv
    - cbioportal_mutations.json
    - cbioportal_sample_cancertype.json
    - codon_share.csv

Usage:
  python3 run_figure2.py
Output:
  ../vector_figures/Figure2_cancer_type_distribution.pdf
  ../vector_figures/Figure2_cancer_type_distribution.svg
  ../vector_figures/Figure2_cancer_type_distribution.png
"""

import collections
import csv
import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'data'))
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'vector_figures'))
os.makedirs(FIG, exist_ok=True)

# Layout constants
MM = 1 / 25.4
W2 = 180.0  # double-column width, mm
T, PN = 7.5, 9.0  # typography
INK, GREY = '#1A1A1A', '#59656B'

plt.rcParams.update({
    'font.family': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 2.0,
    'ytick.major.size': 2.0,
    'xtick.labelsize': T,
    'ytick.labelsize': T,
    'axes.labelsize': T,
    'font.size': T,
    'mathtext.fontset': 'custom',
    'mathtext.rm': 'Arial',
    'mathtext.it': 'Arial:italic',
    'mathtext.bf': 'Arial:bold',
})

def figure(h_mm, w_mm=W2):
    fig = plt.figure(figsize=(w_mm * MM, h_mm * MM))
    fig._mm = (w_mm, h_mm)
    return fig

def axes(fig, x_mm, y_mm, w_mm, h_mm):
    W, H = fig._mm
    return fig.add_axes([x_mm / W, y_mm / H, w_mm / W, h_mm / H])

def GI(gene):
    return '$\it{' + gene + '}$'

def main():
    KEYS = ['G12D', 'G12V', 'G12C', 'G12R', 'G13D', 'Q61X', 'Other']
    PAL = ['#1F3A5F', '#1F3A5F', '#8CC2BC', '#C9A227', '#A63A2E', '#7A8B99', '#DDE3E8']

    muts = json.load(open(os.path.join(DATA, 'cbioportal_mutations.json')))
    ct = json.load(open(os.path.join(DATA, 'cbioportal_sample_cancertype.json')))
    comp = collections.defaultdict(collections.Counter)
    for m in muts['KRAS']:
        if m['sample'] in ct and m['protein']:
            k = m['protein'] if m['protein'] in KEYS[:5] else (
                'Q61X' if str(m['start']) == '61' else 'Other')
            comp[ct[m['sample']]][k] += 1

    byct_path = os.path.join(DATA, 'cancer_type_kras_alleles.csv')
    BYCT = list(csv.DictReader(open(byct_path, encoding='utf-8')))

    NA, NB, PITCH, BAR = 16, 10, 4.1, 2.8
    BOT, XAX, GAP, TOP, LEGH = 1.0, 9.5, 9.0, 4.0, 6.0
    HA, HB = NA * PITCH, NB * PITCH
    H = BOT + XAX + HB + GAP + XAX + HA + LEGH + TOP
    fig = figure(H)
    rend = fig.canvas.get_renderer()

    def text_mm(labels):
        w = 0
        for t in labels:
            o = fig.text(0, 0, t, fontsize=T)
            w = max(w, o.get_window_extent(rend).width / fig.dpi / MM)
            o.remove()
        return w

    def style(ax, n, labels, xlab):
        ax.set_yticks(range(n))
        ax.set_yticklabels(labels, fontsize=T)
        ax.set_ylim(-0.5, n - 0.5)
        ax.set_xlabel(xlab, fontsize=T, labelpad=2)
        ax.tick_params(axis='y', length=0, pad=2)
        ax.tick_params(axis='x', labelsize=T, pad=1.5)
        for s_ in ('top', 'right', 'left'):
            ax.spines[s_].set_visible(False)

    def lab(r):
        return '%.0f%% (%s/%s)' % (float(r['freq_pct']), r['n_mut_samples'], r['n_samples'])

    OFF = 1.0

    def fit_xlim(rows, w):
        return max(float(r['freq_pct']) * w / (w - OFF - text_mm([lab(r)])) for r in rows)

    def value(ax, x, y, r, X, w):
        ax.text(x + OFF * X / w, y, lab(r), va='center', fontsize=T, color='#333333')

    def ticks(ax, X, step):
        last = int(X // step) * step
        ax.set_xlim(0, X)
        ax.set_xticks(range(0, last + 1, step))
        ax.spines['bottom'].set_bounds(0, last)

    LEFT, PADL = 4.0, 1.5
    ks = sorted([r for r in BYCT if r['gene'] == 'KRAS'],
                key=lambda r: -float(r['freq_pct']))[:NA][::-1]
    labA = [r['cancer_type'] for r in ks]
    xa = LEFT + text_mm(labA) + PADL
    ya = BOT + XAX + HB + GAP + XAX
    RM = 0.5
    wa = W2 - RM - xa
    axA = axes(fig, xa, ya, wa, HA)
    XMAX = fit_xlim(ks, wa)
    for i, r in enumerate(ks):
        f = float(r['freq_pct'])
        cc = comp[r['cancer_type']]
        tot = sum(cc.values()) or 1
        left = 0.0
        for k, col in zip(KEYS, PAL):
            w = f * cc[k] / tot
            if w > 0:
                axA.barh(i, w, left=left, color=col, height=BAR / PITCH,
                         ec='white', lw=0.3)
            left += w
        value(axA, f, i, r, XMAX, wa)
    ticks(axA, XMAX, 10)
    style(axA, NA, labA, GI('KRAS') + '-mutant samples (%)')
    fig.legend(handles=[Rectangle((0, 0), 1, 1, fc=c, label=k)
                        for k, c in zip(KEYS, PAL)],
               loc='lower left', ncol=len(KEYS), fontsize=T, borderpad=0,
               handlelength=1.4, handleheight=0.9, columnspacing=1.3,
               title='Allele', title_fontsize=T, alignment='left',
               bbox_to_anchor=(xa / W2, (ya + HA + 0.8) / H))

    lg = fig.legends[-1]
    lg.set_title(None)
    bb = lg.get_window_extent(rend).transformed(fig.transFigure.inverted())
    fig.text(xa / W2 - 0.004, (bb.y0 + bb.y1) / 2, 'Allele',
             fontsize=T, ha='right', va='center', fontweight='bold')
    fig.text(LEFT / W2, (ya + HA + LEGH) / H, 'a', fontsize=PN,
             fontweight='bold', ha='left', va='bottom')

    half = W2 / 2
    labw = text_mm([r['cancer_type'] for r in BYCT if r['gene'] in ('NRAS', 'HRAS')
                    and r in sorted([x for x in BYCT if x['gene'] == r['gene']],
                                    key=lambda x: -float(x['freq_pct']))[:NB]])
    for idx, (g, col, pn) in enumerate((('NRAS', '#2A6F6F', 'b'),
                                        ('HRAS', '#C9A227', 'c'))):
        rs = sorted([r for r in BYCT if r['gene'] == g],
                    key=lambda r: -float(r['freq_pct']))[:NB][::-1]
        labs = [r['cancer_type'] for r in rs]
        x0 = LEFT + idx * half
        xb = x0 + labw + PADL
        wb = half * (idx + 1) - xb - (4.0 if idx == 0 else RM)
        a_ = axes(fig, xb, BOT + XAX, wb, HB)
        X = fit_xlim(rs, wb)
        a_.barh(range(NB), [float(r['freq_pct']) for r in rs], color=col,
                height=BAR / PITCH, ec='none')
        for i, r in enumerate(rs):
            value(a_, float(r['freq_pct']), i, r, X, wb)
        ticks(a_, X, 5 if g == 'NRAS' else 1)
        style(a_, NB, labs, GI(g) + '-mutant samples (%)')
        fig.text(x0 / W2, (BOT + XAX + HB + 2.0) / H, pn, fontsize=PN,
                 fontweight='bold', ha='left', va='bottom')

    stem = 'Figure2_cancer_type_distribution'
    pdf_out = os.path.join(FIG, stem + '.pdf')
    svg_out = os.path.join(FIG, stem + '.svg')
    png_out = os.path.join(FIG, stem + '.png')
    
    fig.savefig(pdf_out, format='pdf', dpi=300)
    fig.savefig(svg_out, format='svg')
    fig.savefig(png_out, format='png', dpi=300)
    plt.close(fig)
    print("Figure 2 successfully generated:")
    print("  ->", pdf_out)
    print("  ->", svg_out)
    print("  ->", png_out)

if __name__ == '__main__':
    main()
