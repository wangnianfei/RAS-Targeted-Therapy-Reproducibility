#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 5 - Resistance Mechanism x Combination Logic Decision Matrix.

Redesigned with ESMO Open / Nature Reviews jewel-tone aesthetics and high precision:
- Panel a: Strategy decision matrix mapping 9 acquired resistance mechanisms across 3 functional classes against 5 clinical combination logics.
- Panel b: Clinical detection rates of acquired resistance alterations in paired plasma vs. tissue cohorts.

Usage:
  python3 run_figure5.py
Outputs:
  ../vector_figures/Figure5_resistance_combination.pdf
  ../vector_figures/Figure5_resistance_combination.svg
  ../vector_figures/Figure5_resistance_combination.png
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'vector_figures'))
os.makedirs(FIG, exist_ok=True)

# Layout constants
MM = 1 / 25.4
W = 180.0  # Double column width (mm)
H = 152.0  # Height (mm)
T = 7.2    # Primary text size (pt)
T_SM = 6.2 # Secondary text size (pt)
T_XS = 5.3 # Micro text size (pt)
PN = 9.5   # Panel identifier (pt, bold)

CANVAS_BG = '#FFFFFF'
INK = '#0F172A'
INK_MUTED = '#475569'
GREY = '#64748B'

# Unified Jewel-Tone Group Palette (Harmonized with Fig 1 & Fig 4)
GRP_COLORS = {
    'genetic': {
        'main': '#1F3A5F',       # Deep Prussian Navy (Fig 4 Primary Anchor)
        'light': '#F1F5F9',
        'border': '#CBD5E1',
        'label': 'GENOMIC ALTERATIONS'
    },
    'nongenetic': {
        'main': '#A63A2E',       # Deep Brick Ruby Crimson (Fig 4 Secondary Anchor)
        'light': '#FFF1F2',
        'border': '#FECDD3',
        'label': 'PHENOTYPIC & LINEAGE PLASTICITY'
    },
    'carrier': {
        'main': '#2A6F6F',       # Oceanic Deep Teal (Fig 4 Biomarker & Fig 1 PI3K)
        'light': '#F0FDFA',
        'border': '#99F6E4',
        'label': 'ORGANELLE & METABOLIC REWIRING'
    }
}

LOGICS = [
    {
        'num': '1',
        'title': 'Vertical',
        'subtitle': 'Same pathway clamp',
        'metric': 'ORR 71% (1L)',
        'source': 'Zhong 2026',
        'color': '#2563EB',      # Cobalt Royal Blue (Fig 1 MAPK)
        'bg': '#EFF6FF'
    },
    {
        'num': '2',
        'title': 'Horizontal',
        'subtitle': 'Parallel bypass switch',
        'metric': 'PFS 5.6 vs 2.2 mo',
        'source': 'Fakih 2023',
        'color': '#0D9488',      # Teal Emerald (Fig 1 PI3K)
        'bg': '#F0FDFA'
    },
    {
        'num': '3',
        'title': 'Immunotherapy',
        'subtitle': 'Effector engagement',
        'metric': 'Durability, not ORR',
        'source': 'Chour 2023',
        'color': '#E11D48',      # Crimson Accent (Fig 1 Immune)
        'bg': '#FFF1F2'
    },
    {
        'num': '4',
        'title': 'State & Stress',
        'subtitle': 'Survival switch',
        'metric': 'ORR 82% (n=33)',
        'source': 'Song 2026',
        'color': '#7C3AED',      # Deep Violet (Fig 1 Apoptosis)
        'bg': '#F5F3FF'
    },
    {
        'num': '5',
        'title': 'Cytotoxic',
        'subtitle': 'Off-axis cell kill',
        'metric': 'ORR 88.9%',
        'source': 'Akamatsu 2025',
        'color': '#D97706',      # Warm Golden Amber (Fig 1/4)
        'bg': '#FFFBEB'
    }
]

ROWS = [
    ('genetic', 'Receptor-level bypass', 'MET ampl.; NRAS/BRAF/RET mut.; fusions',
     {1: ('direct', 'SOS1'), 2: ('direct', 'EGFR (CRC)')}),
    ('genetic', 'Downstream MAPK nodes', 'BRAF, MAP2K1, NRAS reactivate ERK',
     {1: ('direct', 'ERK')}),
    ('genetic', 'Parallel chains', 'PI3K-AKT-mTOR & YAP1/TAZ bypass',
     {2: ('partial', 'PI3K-AKT')}),
    ('nongenetic', 'Cell state plasticity', 'Epithelial state; transcriptional reprogramming',
     {4: ('direct', 'cell state → GPX4')}),
    ('nongenetic', 'Lineage exit', 'Adeno-to-squamous transition; Paneth-like state',
     {4: ('direct', 'lineage programme')}),
    ('carrier', 'Proteostasis stress', 'Heat-shock & IRE1α reactivation',
     {4: ('direct', 'IRE1α')}),
    ('carrier', 'Polarity & cytoskeleton', 'YAP-MRAS axis & actin remodeling',
     {4: ('direct', 'YAP-MRAS')}),
    ('carrier', 'Signalling condensates', 'ARAF-RAS condensates defeat NF1',
     {4: ('direct', 'ARAF condensates')}),
    ('carrier', 'Metabolic rewiring', 'Mevalonate membrane tether & OXPHOS/ZBTB11',
     {4: ('direct', 'mevalonate, ZBTB11')}),
]

plt.rcParams.update({
    'font.family': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
})

def draw_pill(ax, x, y, w, h, bg, border, lw=0.6, r=1.4):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       facecolor=bg, edgecolor=border, linewidth=lw, zorder=3)
    ax.add_patch(p)
    return p

def main():
    fig = plt.figure(figsize=(W * MM, H * MM), facecolor=CANVAS_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis('off')

    # Top title
    y_top = H - 5.0
    ax.text(3.5, y_top, 'a', fontsize=PN, fontweight='bold', color=INK, va='top', ha='left')
    ax.text(8.0, y_top - 0.2, 'Resistance Mechanism × Combination Logic Decision Matrix',
            fontsize=T + 1.2, fontweight='bold', color=INK, va='top', ha='left')

    X_ROW_LABEL = 3.5
    X_MATRIX_START = 58.5
    W_MATRIX = W - X_MATRIX_START - 3.5
    CW = W_MATRIX / 5.0
    GAP = 1.0

    # Column Headers (Centered, symmetrical cards)
    y_header_top = y_top - 6.5
    h_header = 16.5
    y_header_bot = y_header_top - h_header

    for i, log in enumerate(LOGICS):
        cx = X_MATRIX_START + i * CW
        # Outer Card
        draw_pill(ax, cx + GAP/2, y_header_bot, CW - GAP, h_header,
                  bg=log['bg'], border=log['color'], lw=0.7, r=1.8)
        
        # Pill badge on top: e.g. "Logic 1"
        draw_pill(ax, cx + CW/2 - 6.5, y_header_top - 3.8, 13.0, 3.0,
                  bg=log['color'], border='none', lw=0, r=1.0)
        ax.text(cx + CW/2, y_header_top - 2.3, f"Logic {log['num']}",
                fontsize=T_XS, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
        
        # Title (Centered)
        ax.text(cx + CW/2, y_header_top - 6.0, log['title'],
                fontsize=T - 0.2, fontweight='bold', color=INK, ha='center', va='center', zorder=5)
        
        # Subtitle (Centered)
        ax.text(cx + CW/2, y_header_top - 8.8, log['subtitle'],
                fontsize=T_XS, color=INK_MUTED, ha='center', va='center', zorder=5)
        
        # Metric pill (Centered)
        draw_pill(ax, cx + GAP/2 + 1.2, y_header_bot + 1.4, CW - GAP - 2.4, 3.8,
                  bg='#FFFFFF', border='#CBD5E1', lw=0.45, r=1.0)
        ax.text(cx + CW/2, y_header_bot + 3.3, log['metric'],
                fontsize=T_SM, fontweight='bold', color=log['color'], ha='center', va='center', zorder=5)

    # Matrix rows
    y_curr = y_header_bot - 3.2
    row_height = 5.6
    group_bar_h = 4.0
    group_spacing = 2.0

    curr_group = None
    for r_idx, (grp, title, detail, matches) in enumerate(ROWS):
        g_info = GRP_COLORS[grp]
        
        if grp != curr_group:
            curr_group = grp
            y_curr -= (group_spacing if r_idx > 0 else 0.5)
            # Group banner
            draw_pill(ax, X_ROW_LABEL, y_curr - group_bar_h, W - X_ROW_LABEL - 3.5, group_bar_h,
                      bg=g_info['light'], border=g_info['border'], lw=0.6, r=1.2)
            draw_pill(ax, X_ROW_LABEL, y_curr - group_bar_h, 2.5, group_bar_h,
                      bg=g_info['main'], border=g_info['main'], lw=0.0, r=0.8)
            
            ax.text(X_ROW_LABEL + 4.5, y_curr - group_bar_h/2,
                    grp.capitalize() + ' mechanisms (' + g_info['label'] + ')',
                    fontsize=T - 0.2, fontweight='bold', color=g_info['main'], va='center', ha='left', zorder=5)
            
            y_curr -= group_bar_h + 1.0

        y_box = y_curr - row_height
        
        # Left title & detail
        ax.text(X_ROW_LABEL + 1.5, y_box + row_height*0.64, title,
                fontsize=T, fontweight='bold', color=INK, va='center', ha='left')
        ax.text(X_ROW_LABEL + 1.5, y_box + row_height*0.22, detail,
                fontsize=T_XS, color=INK_MUTED, va='center', ha='left')

        # Cells
        for c_idx in range(1, 6):
            cx = X_MATRIX_START + (c_idx - 1) * CW
            cw_cell = CW - GAP
            
            if c_idx in matches:
                level, node_text = matches[c_idx]
                if level == 'direct':
                    draw_pill(ax, cx + GAP/2, y_box + 0.5, cw_cell, row_height - 1.0,
                              bg=g_info['main'], border=g_info['main'], lw=0.0, r=1.2)
                    ax.text(cx + CW/2, y_box + row_height/2, node_text,
                            fontsize=T_SM, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
                elif level == 'partial':
                    draw_pill(ax, cx + GAP/2, y_box + 0.5, cw_cell, row_height - 1.0,
                              bg=g_info['light'], border=g_info['main'], lw=0.8, r=1.2)
                    ax.text(cx + CW/2, y_box + row_height/2, node_text,
                            fontsize=T_SM, fontweight='bold', color=g_info['main'], ha='center', va='center', zorder=5)
            else:
                draw_pill(ax, cx + GAP/2, y_box + 0.5, cw_cell, row_height - 1.0,
                          bg='#FAFBFD', border='#E2E8F0', lw=0.4, r=1.2)
                ax.plot(cx + CW/2, y_box + row_height/2, marker='o', markersize=1.8,
                        color='#CBD5E1', zorder=4)

        y_curr -= row_height

    # Divider & Legend
    y_curr -= 2.5
    ax.plot([X_ROW_LABEL, W - 3.5], [y_curr, y_curr], color='#E2E8F0', linewidth=0.6)
    
    y_curr -= 4.2
    ax.text(X_ROW_LABEL, y_curr, 'Evidence Mapping:', fontsize=T, fontweight='bold', color=INK, va='center')
    
    # Direct
    draw_pill(ax, X_ROW_LABEL + 27.0, y_curr - 1.8, 3.8, 3.6, bg=GRP_COLORS['genetic']['main'], border='none', lw=0, r=0.8)
    ax.text(X_ROW_LABEL + 32.0, y_curr, 'Direct mechanism engagement', fontsize=T, color=INK, va='center')
    
    # Partial
    draw_pill(ax, X_ROW_LABEL + 78.0, y_curr - 1.8, 3.8, 3.6, bg='#F1F5F9', border=GRP_COLORS['genetic']['main'], lw=0.8, r=0.8)
    ax.text(X_ROW_LABEL + 83.0, y_curr, 'Partial / Secondary bypass', fontsize=T, color=INK, va='center')
    
    # Not answered
    draw_pill(ax, X_ROW_LABEL + 126.0, y_curr - 1.8, 3.8, 3.6, bg='#FAFBFD', border='#CBD5E1', lw=0.5, r=0.8)
    ax.plot(X_ROW_LABEL + 127.9, y_curr, marker='o', markersize=1.6, color='#CBD5E1')
    ax.text(X_ROW_LABEL + 131.5, y_curr, 'Not addressed (Strategic gap)', fontsize=T, color=INK_MUTED, va='center')

    # Panel b: Detection Rates
    y_b_top = y_curr - 8.5
    ax.text(3.5, y_b_top, 'b', fontsize=PN, fontweight='bold', color=INK, va='top', ha='left')
    ax.text(8.0, y_b_top - 0.2, 'Clinical Detection of Acquired Resistance Alterations',
            fontsize=T + 0.8, fontweight='bold', color=INK, va='top', ha='left')
    
    X_DET_START = 72.0
    W_DET_BAR = W - X_DET_START - 24.0
    y_det_row1 = y_b_top - 8.2
    y_det_row2 = y_det_row1 - 8.0
    bar_h = 4.0
    
    # Item 1: CRC paired plasma
    ax.text(X_DET_START - 2.5, y_det_row1 + bar_h*0.7, 'Paired plasma ctDNA (CRC)',
            fontsize=T_SM, fontweight='bold', color=INK, va='center', ha='right')
    ax.text(X_DET_START - 2.5, y_det_row1 + bar_h*0.2, 'adagrasib + cetuximab (Yaeger 2024)',
            fontsize=T_XS, color=INK_MUTED, va='center', ha='right')
    draw_pill(ax, X_DET_START, y_det_row1, W_DET_BAR, bar_h, bg='#F1F5F9', border='none', lw=0, r=1.0)
    w1 = W_DET_BAR * 0.74
    draw_pill(ax, X_DET_START, y_det_row1, w1, bar_h, bg='#1F3A5F', border='none', lw=0, r=1.0)
    ax.text(X_DET_START + w1 + 2.0, y_det_row1 + bar_h/2, '74% (25 / 34)',
            fontsize=T_SM, fontweight='bold', color='#1F3A5F', va='center', ha='left')

    # Item 2: NSCLC tissue/plasma
    ax.text(X_DET_START - 2.5, y_det_row2 + bar_h*0.7, 'Tissue or plasma (mostly NSCLC)',
            fontsize=T_SM, fontweight='bold', color=INK, va='center', ha='right')
    ax.text(X_DET_START - 2.5, y_det_row2 + bar_h*0.2, 'adagrasib monotherapy (Awad 2021)',
            fontsize=T_XS, color=INK_MUTED, va='center', ha='right')
    draw_pill(ax, X_DET_START, y_det_row2, W_DET_BAR, bar_h, bg='#F1F5F9', border='none', lw=0, r=1.0)
    w2 = W_DET_BAR * 0.45
    draw_pill(ax, X_DET_START, y_det_row2, w2, bar_h, bg='#2A6F6F', border='none', lw=0, r=1.0)
    ax.text(X_DET_START + w2 + 2.0, y_det_row2 + bar_h/2, '45% (17 / 38)',
            fontsize=T_SM, fontweight='bold', color='#2A6F6F', va='center', ha='left')

    # X axis
    y_axis = y_det_row2 - 2.8
    ax.plot([X_DET_START, X_DET_START + W_DET_BAR], [y_axis, y_axis], color='#334155', linewidth=0.6)
    for tick in [0, 25, 50, 75, 100]:
        tx = X_DET_START + W_DET_BAR * (tick / 100.0)
        ax.plot([tx, tx], [y_axis, y_axis - 0.8], color='#334155', linewidth=0.6)
        ax.text(tx, y_axis - 1.8, f"{tick}%", fontsize=T_XS, color=INK_MUTED, ha='center', va='top')
    
    ax.text(X_DET_START + W_DET_BAR/2, y_axis - 4.5,
            'Acquired alteration detected (%; two cohorts with distinct clinical denominators)',
            fontsize=T_XS, color=INK_MUTED, ha='center', va='top')

    stem = 'Figure5_resistance_combination'
    pdf_out = os.path.join(FIG, stem + '.pdf')
    svg_out = os.path.join(FIG, stem + '.svg')
    png_out = os.path.join(FIG, stem + '.png')

    fig.savefig(pdf_out, format='pdf', dpi=400)
    fig.savefig(svg_out, format='svg')
    fig.savefig(png_out, format='png', dpi=400)
    plt.close(fig)
    print("Figure 5 successfully generated at 400 DPI:")
    print("  ->", pdf_out)
    print("  ->", svg_out)
    print("  ->", png_out)

if __name__ == '__main__':
    main()
