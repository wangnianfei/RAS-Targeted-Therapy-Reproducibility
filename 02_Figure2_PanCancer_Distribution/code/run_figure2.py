#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 2 - Pan-cancer distribution of KRAS, NRAS, and HRAS mutations.

Harmonized with ESMO Open / Nature Reviews jewel-tone color scheme:
- Panel a: Pan-cancer KRAS mutation frequencies and allele shares (G12D/V/C/R, G13D, Q61X, Other) across 16 major solid tumor types.
- Panel b: Pan-cancer NRAS mutation frequencies across 10 tumor types.
- Panel c: Pan-cancer HRAS mutation frequencies across 10 tumor types.

Data:
  MSK-IMPACT clinical sequencing cohort (10,945 sequenced samples; Zehir et al., Nat Med 2017).
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
W2 = 180.0  # Standard double-column width (mm)
T = 7.5     # Regular text size (pt)
T_SM = 6.5  # Small metadata text size (pt)
PN = 9.5    # Panel identifier size (pt, bold)

# Canvas & Typography Colors
CANVAS_BG = '#FFFFFF'
INK_DARK = '#0F172A'
INK_MUTED = '#475569'
AXIS_COLOR = '#334155'
GRID_COLOR = '#F1F5F9'

# Unified Jewel-Tone Allele Palette (Harmonized with Figure 1 & Figure 4)
KEYS = ['G12D', 'G12V', 'G12C', 'G12R', 'G13D', 'Q61X', 'Other']
PAL = [
    '#E11D48',  # G12D: Ruby Crimson (Primary oncogenic driver, Fig 1 active accent)
    '#1F3A5F',  # G12V: Deep Prussian Navy (Fig 4 primary anchor, high contrast next to G12D)
    '#0D9488',  # G12C: Emerald Teal (Covalent landmark, Fig 1 PI3K/GEF & Fig 4 biomarker)
    '#D97706',  # G12R: Golden Amber (PDAC specific, Fig 4 amber & Fig 1 RAC1)
    '#6366F1',  # G13D: Royal Indigo (CRC EGFR-resistance differentiator)
    '#0284C7',  # Q61X: Azure Sky Blue (Fig 1 RAL cascade)
    '#94A3B8',  # Other: Slate Silver Grey (Neutral background alleles)
]

# Panel b & c dedicated harmonious anchors:
COLOR_NRAS = '#1F3A5F'  # Deep Prussian Navy (Consistent with RAS-targeted anchor)
COLOR_HRAS = '#2A6F6F'  # Oceanic Deep Teal (Consistent with Biomarker anchor)

plt.rcParams.update({
    'font.family': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
    'axes.linewidth': 0.65,
    'xtick.major.width': 0.65,
    'ytick.major.width': 0.65,
    'xtick.major.size': 2.2,
    'ytick.major.size': 2.2,
    'xtick.labelsize': T,
    'ytick.labelsize': T,
    'axes.labelsize': T,
    'font.size': T,
    'text.color': INK_DARK,
    'axes.labelcolor': INK_DARK,
    'xtick.color': INK_DARK,
    'ytick.color': INK_DARK,
    'mathtext.fontset': 'custom',
    'mathtext.rm': 'Arial',
    'mathtext.it': 'Arial:italic',
    'mathtext.bf': 'Arial:bold',
})

def figure(h_mm, w_mm=W2):
    fig = plt.figure(figsize=(w_mm * MM, h_mm * MM), facecolor=CANVAS_BG)
    fig._mm = (w_mm, h_mm)
    return fig

def axes(fig, x_mm, y_mm, w_mm, h_mm):
    W, H = fig._mm
    ax = fig.add_axes([x_mm / W, y_mm / H, w_mm / W, h_mm / H])
    ax.set_facecolor(CANVAS_BG)
    return ax

def GI(gene):
    return r'$\it{' + gene + '}$'

def main():
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

    # Layout geometry specifications
    NA, NB, PITCH, BAR = 16, 10, 4.1, 2.9
    BOT = 2.5        # Bottom margin (mm)
    XAX = 9.5        # Height allocated for x-axis ticks and labels (mm)
    GAP = 11.5       # Gap between panel a and panels b/c (mm)
    TOP = 4.5        # Top margin (mm)
    LEGH = 7.5       # Legend height (mm)
    HA, HB = NA * PITCH, NB * PITCH
    H = BOT + XAX + HB + GAP + XAX + HA + LEGH + TOP

    fig = figure(H)
    rend = fig.canvas.get_renderer()

    def text_mm(labels):
        w = 0.0
        for t in labels:
            o = fig.text(0, 0, t, fontsize=T)
            w = max(w, o.get_window_extent(rend).width / fig.dpi / MM)
            o.remove()
        return w

    def style(ax, n, labels, xlab):
        ax.set_yticks(range(n))
        ax.set_yticklabels(labels, fontsize=T, color=INK_DARK)
        ax.set_ylim(-0.5, n - 0.5)
        ax.set_xlabel(xlab, fontsize=T, labelpad=3.2, fontweight='bold', color=INK_DARK)
        ax.tick_params(axis='y', length=0, pad=2.5)
        ax.tick_params(axis='x', labelsize=T, pad=1.8, colors=INK_DARK)
        for s_ in ('top', 'right', 'left'):
            ax.spines[s_].set_visible(False)
        ax.spines['bottom'].set_color(AXIS_COLOR)
        ax.spines['bottom'].set_linewidth(0.65)
        ax.grid(axis='x', color=GRID_COLOR, linewidth=0.5, zorder=0)

    def lab(r):
        return '%.0f%% (%s/%s)' % (float(r['freq_pct']), r['n_mut_samples'], r['n_samples'])

    OFF = 1.3  # Text offset from bar end in mm

    def fit_xlim(rows, w_mm):
        return max(float(r['freq_pct']) * w_mm / (w_mm - OFF - text_mm([lab(r)]) - 2.0) for r in rows)

    def value(ax, x_val, y_pos, r, X_limit, w_mm):
        ax.text(x_val + OFF * X_limit / w_mm, y_pos, lab(r),
                va='center', fontsize=T, color=INK_DARK)

    def ticks(ax, X_limit, step):
        last = int(X_limit // step) * step
        ax.set_xlim(0, X_limit)
        ax.set_xticks(range(0, last + 1, step))
        ax.spines['bottom'].set_bounds(0, last)

    # -------------------------------------------------------------
    # Panel a: Pan-cancer KRAS mutation frequencies and allele shares
    # -------------------------------------------------------------
    LEFT = 4.5
    PADL = 2.0
    ks = sorted([r for r in BYCT if r['gene'] == 'KRAS'],
                key=lambda r: -float(r['freq_pct']))[:NA][::-1]
    labA = [r['cancer_type'] for r in ks]
    xa = LEFT + text_mm(labA) + PADL
    ya = BOT + XAX + HB + GAP + XAX
    RM = 3.0  # Right margin (mm)
    wa = W2 - RM - xa
    axA = axes(fig, xa, ya, wa, HA)
    XMAX_A = fit_xlim(ks, wa)

    for i, r in enumerate(ks):
        f = float(r['freq_pct'])
        cc = comp[r['cancer_type']]
        tot = sum(cc.values()) or 1
        left = 0.0
        for k, col in zip(KEYS, PAL):
            w = f * cc[k] / tot
            if w > 0:
                axA.barh(i, w, left=left, color=col, height=BAR / PITCH,
                         ec='#FFFFFF', lw=0.45, zorder=3)
            left += w
        value(axA, f, i, r, XMAX_A, wa)

    ticks(axA, XMAX_A, 10)
    style(axA, NA, labA, GI('KRAS') + '-mutant samples (%)')

    # Panel a Legend with refined jewel-tone chips
    legend_handles = [
        Rectangle((0, 0), 1, 1, fc=c, ec='#475569', lw=0.4, label=k)
        for k, c in zip(KEYS, PAL)
    ]
    lg = fig.legend(
        handles=legend_handles,
        loc='lower left',
        ncol=len(KEYS),
        fontsize=T,
        borderpad=0,
        handlelength=1.2,
        handleheight=0.85,
        columnspacing=1.0,
        frameon=False,
        bbox_to_anchor=((xa + 13.0) / W2, (ya + HA + 1.2) / H)
    )

    fig.text(xa / W2, (ya + HA + 2.0) / H, 'Allele:',
             fontsize=T, ha='left', va='center', fontweight='bold', color=INK_DARK)
    
    fig.text(LEFT / W2, (ya + HA + LEGH + 1.0) / H, 'a', fontsize=PN,
             fontweight='bold', ha='left', va='bottom', color=INK_DARK)
    
    # Cohort annotation on top-right
    fig.text((W2 - RM) / W2, (ya + HA + 2.0) / H, 'MSK-IMPACT cohort (n = 10,945)',
             fontsize=T_SM, ha='right', va='center', fontstyle='italic', color=INK_MUTED)

    # -------------------------------------------------------------
    # Panels b & c: NRAS and HRAS
    # Separate horizontally with dedicated gutters
    # -------------------------------------------------------------
    nras_rows = sorted([r for r in BYCT if r['gene'] == 'NRAS'],
                       key=lambda r: -float(r['freq_pct']))[:NB][::-1]
    hras_rows = sorted([r for r in BYCT if r['gene'] == 'HRAS'],
                       key=lambda r: -float(r['freq_pct']))[:NB][::-1]

    lab_nras = [r['cancer_type'] for r in nras_rows]
    lab_hras = [r['cancer_type'] for r in hras_rows]

    w_label_b = text_mm(lab_nras)
    w_label_c = text_mm(lab_hras)

    GUTTER = 10.0   # Clear physical separation between Panel B and C
    TOTAL_PLOT_W = W2 - LEFT - RM - GUTTER - w_label_b - w_label_c - (PADL * 2)
    wb = TOTAL_PLOT_W / 2.0

    xb_b = LEFT + w_label_b + PADL
    x0_c = xb_b + wb + GUTTER
    xb_c = x0_c + w_label_c + PADL

    # Panel b: NRAS (Deep Prussian Navy)
    axB = axes(fig, xb_b, BOT + XAX, wb, HB)
    X_B = fit_xlim(nras_rows, wb)
    axB.barh(range(NB), [float(r['freq_pct']) for r in nras_rows],
             color=COLOR_NRAS, height=BAR / PITCH, ec='#0F172A', lw=0.4, zorder=3)
    for i, r in enumerate(nras_rows):
        value(axB, float(r['freq_pct']), i, r, X_B, wb)
    ticks(axB, X_B, 5)
    style(axB, NB, lab_nras, GI('NRAS') + '-mutant samples (%)')
    fig.text(LEFT / W2, (BOT + XAX + HB + 2.5) / H, 'b', fontsize=PN,
             fontweight='bold', ha='left', va='bottom', color=INK_DARK)

    # Panel c: HRAS (Oceanic Deep Teal)
    axC = axes(fig, xb_c, BOT + XAX, wb, HB)
    X_C = fit_xlim(hras_rows, wb)
    axC.barh(range(NB), [float(r['freq_pct']) for r in hras_rows],
             color=COLOR_HRAS, height=BAR / PITCH, ec='#0F172A', lw=0.4, zorder=3)
    for i, r in enumerate(hras_rows):
        value(axC, float(r['freq_pct']), i, r, X_C, wb)
    ticks(axC, X_C, 1)
    style(axC, NB, lab_hras, GI('HRAS') + '-mutant samples (%)')
    fig.text(x0_c / W2, (BOT + XAX + HB + 2.5) / H, 'c', fontsize=PN,
             fontweight='bold', ha='left', va='bottom', color=INK_DARK)

    stem = 'Figure2_cancer_type_distribution'
    pdf_out = os.path.join(FIG, stem + '.pdf')
    svg_out = os.path.join(FIG, stem + '.svg')
    png_out = os.path.join(FIG, stem + '.png')

    fig.savefig(pdf_out, format='pdf', dpi=400)
    fig.savefig(svg_out, format='svg')
    fig.savefig(png_out, format='png', dpi=400)
    plt.close(fig)
    print("Figure 2 successfully generated at 400 DPI:")
    print("  ->", pdf_out)
    print("  ->", svg_out)
    print("  ->", png_out)

if __name__ == '__main__':
    main()
