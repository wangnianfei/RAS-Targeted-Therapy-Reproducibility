#!/usr/bin/env python3
"""Figure 5 (revised): acquired resistance to KRAS G12C inhibitors and corresponding strategies.
Drawn programmatically (no generative-AI imagery). Alterations are those reported by
Awad et al., N Engl J Med 2021;384:2382-93 (adagrasib monotherapy, n = 38); adaptive EGFR feedback in
colorectal cancer from Amodio et al., Cancer Discov 2020;10:1129-39. Strategies are those discussed in
Section 5.3 of the review. Output: ../figures/Fig5.{pdf,png,tif}
"""
import os, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, '..', 'figures'); os.makedirs(F, exist_ok=True)
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
                     'pdf.fonttype': 42, 'font.size': 6.5})
W, H = 180, 120
fig = plt.figure(figsize=(W / 25.4, H / 25.4)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
NODE, NODE_E = '#E8EDF2', '#1F3A5F'
RES, RES_E = '#FBEAEA', '#A63A2E'
STR, STR_E = '#E6F2EF', '#2A6F6F'

def box(x, y, w, h, text, fc, ec, fs=6.5, bold=False, ha='center'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=1.5', fc=fc, ec=ec, lw=0.7))
    tx = x + w / 2 if ha == 'center' else x + 1.8
    ax.text(tx, y + h / 2, text, ha=ha, va='center', fontsize=fs, fontweight='bold' if bold else 'normal', color='#111111', linespacing=1.25)
def arrow(x1, y1, x2, y2, c='#333333', style='-|>', ls='-'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=7, color=c, lw=0.8, linestyle=ls))
def blunt(x1, y1, x2, y2, c):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-[', mutation_scale=4, color=c, lw=0.8))

# pathway (centre column)
cx, bw, bh = 74, 32, 8
ys = {'RTK': 104, 'SHP2': 90, 'KRAS': 72, 'RAF': 54, 'MEK': 42, 'ERK': 30}
box(cx, ys['RTK'], bw, bh, 'RTKs (EGFR, MET, FGFR)', NODE, NODE_E, bold=True)
box(cx, ys['SHP2'], bw, bh, 'SHP2 → SOS1 (GEF)', NODE, NODE_E, bold=True)
box(cx - 4, ys['KRAS'], bw + 8, 11, 'KRAS G12C\nOFF (GDP) / ON (GTP)', NODE, NODE_E, bold=True)
box(cx, ys['RAF'], bw, bh, 'RAF', NODE, NODE_E, bold=True)
box(cx, ys['MEK'], bw, bh, 'MEK', NODE, NODE_E, bold=True)
box(cx, ys['ERK'], bw, bh, 'ERK → proliferation', NODE, NODE_E, bold=True)
box(cx + 36, ys["RAF"] - 6, 18, 14, 'PI3K → AKT\n→ mTOR', NODE, NODE_E, bold=True)
for a, b in [('RTK', 'SHP2')]:
    arrow(cx + bw / 2, ys[a], cx + bw / 2, ys[b] + bh)
arrow(cx + bw / 2, ys['SHP2'], cx + bw / 2, ys['KRAS'] + 11)
arrow(cx + bw / 2, ys['KRAS'], cx + bw / 2, ys['RAF'] + bh)
arrow(cx + bw / 2, ys['RAF'], cx + bw / 2, ys['MEK'] + bh)
arrow(cx + bw / 2, ys['MEK'], cx + bw / 2, ys['ERK'] + bh)
arrow(cx + bw + 4, ys["KRAS"] + 2, cx + 45, ys["RAF"] + 8)
# ERK negative feedback to RTK/SOS1 (dashed)
ax.add_patch(FancyArrowPatch((cx, ys['ERK'] + 4), (cx, ys['RTK'] + 4), connectionstyle='arc3,rad=-0.35',
             arrowstyle='-[', mutation_scale=4, color='#7F8C8D', lw=0.7, linestyle='--'))
ax.text(cx - 12, 24, 'ERK negative feedback\n(relieved by KRAS\ninhibition)', fontsize=5.6, color='#555555', ha='center', va='center')

# drug on KRAS
box(cx + 9, ys['KRAS'] - 9, 14, 6, 'G12C inhibitor', '#F3E8F5', '#7B2D8E', fs=5.8)
blunt(cx + 16, ys['KRAS'] - 3, cx + 16, ys['KRAS'] + 0.5, '#7B2D8E')

# resistance boxes (right column)
rx, rw = 132, 46
box(rx, 96, rw, 17, 'Upstream reactivation\n• MET amplification\n• Adaptive EGFR feedback (CRC)\n• Oncogenic fusions (ALK, RET, FGFR3)', RES, RES_E, fs=5.7, ha='left')
box(rx, 66, rw, 26, 'On-target KRAS alterations\n• Switch-II pocket: R68S, H95D/Q/R, Y96C\n• Second-site activating: G12D/R/V/W,\n   G13D, Q61H\n• KRAS G12C amplification', RES, RES_E, fs=5.7, ha='left')
box(rx, 38, rw, 22, 'Downstream / parallel bypass\n• NRAS, BRAF, MAP2K1 mutations\n• BRAF, RAF1 fusions\n• NF1, PTEN loss-of-function', RES, RES_E, fs=5.7, ha='left')
box(rx, 14, rw, 18, 'Histological transformation\n• Adenocarcinoma → squamous\n   cell carcinoma (2/9 paired\n   lung biopsies)', RES, RES_E, fs=5.7, ha='left')
arrow(rx, 104.5, cx + bw + 1, 108, c=RES_E)
arrow(rx, 79, cx + bw + 5, 77.5, c=RES_E)
arrow(rx, 52, cx + 54.5, 55, c=RES_E)
arrow(rx, 44, cx + bw + 1, 46, c=RES_E)
ax.text(rx + rw / 2, 117, 'Acquired resistance (Awad et al. 2021)', ha='center', fontsize=6.8, fontweight='bold', color=RES_E)

# strategy boxes (left column)
lx, lw_ = 3, 46
box(lx, 96, lw_, 14, 'Anti-EGFR antibody (CRC), MET TKI', STR, STR_E, fs=5.9)
box(lx, 80, lw_, 11, 'SHP2 or SOS1 inhibitor', STR, STR_E, fs=5.9)
box(lx, 62, lw_, 13, 'RAS(ON) multi-selective or\npan-RAS inhibitor', STR, STR_E, fs=5.9)
box(lx, 44, lw_, 13, 'RAF / MEK inhibitor', STR, STR_E, fs=5.9)
for y, ty in [(103, ys['RTK'] + 4), (85.5, ys['SHP2'] + 4), (68.5, ys['KRAS'] + 5.5), (50.5, ys['RAF'] + 2)]:
    blunt(lx + lw_, y, cx - (4 if ty == ys['KRAS'] + 5.5 else 0) - 0.5, ty, STR_E)
ax.text(lx + lw_ / 2, 117, 'Strategies discussed (Section 5.3)', ha='center', fontsize=6.8, fontweight='bold', color=STR_E)
ax.text(lx, 6, 'Arrows, activation; blunt ends, inhibition; dashed line, physiological ERK negative feedback.', fontsize=5.6, color='#444444')

for ext in ('pdf', 'png'):
    fig.savefig(os.path.join(F, f'Fig5.{ext}'), dpi=500)
subprocess.run(['magick', os.path.join(F, 'Fig5.png'), '-density', '500', '-units', 'PixelsPerInch', '-compress', 'LZW',
                os.path.join(F, 'Fig5.tif')], check=True)
print('Figure 5 written')
