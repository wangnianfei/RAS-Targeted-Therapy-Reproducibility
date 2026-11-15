#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 3 - Conformational displacement upon nucleotide exchange and drug binding.

Panels:
  a: Cα deviation between KRAS-GDP (4OBE, chain B) and KRAS-GTP (5VQ2, chain A).
  b: Cα deviation between KRAS(G12C)-GDP (4LDJ, chain A) and KRAS(G12C)-sotorasib (6OIM, chain A).
  c: 3D molecular surface view of the switch II pocket in the KRAS(G12C)-sotorasib complex (PDB: 6OIM).

Data:
  Source PDB coordinates in ../data/:
    - 4OBE.pdb (1.24 Å)
    - 5VQ2.pdb
    - 4LDJ.pdb
    - 6OIM.pdb
    - _panelC_6OIM.png (600 dpi ray-traced surface rendering)

Usage:
  python3 run_figure3.py
Output:
  ../vector_figures/Figure3_conformational_switch.pdf
  ../vector_figures/Figure3_conformational_switch.svg
  ../vector_figures/Figure3_conformational_switch.png
  ../data/ca_distance_shifts.csv (exported residue-level displacement matrix)
"""

import csv
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'data'))
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'vector_figures'))
os.makedirs(FIG, exist_ok=True)

MM = 1 / 25.4
W2 = 180.0
T, PN = 7.5, 9.0

# Colors
C = {
    'ploop': '#8CC2BC',
    'sw1': '#A63A2E',
    'sw2': '#2A6F6F',
    'g4': '#C9A227',
    'g5': '#1F3A5F',
    'h': '#2A6F6F',
    'hot': '#A63A2E',
    'ink': '#1A1A1A',
    'grey': '#59656B'
}
REG = [('P-loop', 10, 17, C['ploop']),
       ('switch I', 30, 38, C['sw1']),
       ('switch II', 60, 76, C['sw2'])]

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
})

def figure(h_mm, w_mm=W2):
    fig = plt.figure(figsize=(w_mm * MM, h_mm * MM))
    fig._mm = (w_mm, h_mm)
    return fig

def axes(fig, x_mm, y_mm, w_mm, h_mm):
    W, H = fig._mm
    return fig.add_axes([x_mm / W, y_mm / H, w_mm / W, h_mm / H])

def ca(pdb_path, chain=None):
    xyz = {}
    with open(pdb_path, 'r', encoding='utf-8', errors='ignore') as f:
        for l in f:
            if l.startswith('ATOM') and l[12:16].strip() == 'CA':
                if chain and l[21] != chain:
                    continue
                if l[16] not in (' ', 'A'):
                    continue
                xyz[int(l[22:26])] = (float(l[30:38]), float(l[38:46]), float(l[46:54]))
    return xyz

def kabsch(P, Q):
    cp, cq = P.mean(0), Q.mean(0)
    U, S, Vt = np.linalg.svd((P - cp).T @ (Q - cq))
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    return Vt.T @ np.diag([1, 1, d]) @ U.T, cp, cq

def devcurve(p1_id, c1, p2_id, c2, excl=((25, 45), (55, 76))):
    p1_path = os.path.join(DATA, f'{p1_id}.pdb')
    p2_path = os.path.join(DATA, f'{p2_id}.pdb')
    a = ca(p1_path, c1)
    b = ca(p2_path, c2)
    com = [r for r in sorted(set(a) & set(b)) if r <= 169]
    core = [r for r in com if not any(lo <= r <= hi for lo, hi in excl)]
    P, Q = np.array([a[r] for r in core]), np.array([b[r] for r in core])
    R, cp, cq = kabsch(P, Q)
    A, B = np.array([a[r] for r in com]), np.array([b[r] for r in com])
    d = np.linalg.norm((R @ (A - cp).T).T + cq - B, axis=1)
    rms = float(np.sqrt((np.linalg.norm((R @ (P - cp).T).T + cq - Q, axis=1) ** 2).mean()))
    return com, d, rms

def main():
    LEFT = 0.5
    PH, GAPY, BOT, TOP = 40.0, 10.0, 10.5, 8.0
    H = BOT + 2 * PH + GAPY + TOP
    fig = figure(H)
    XA, WA = 12.5, 85.5
    XC = XA + WA + 6.0
    WC = W2 - XC

    pairs = [
        (('4OBE', 'B'), ('5VQ2', 'A'), 'KRAS–GDP (4OBE) vs KRAS–GTP (5VQ2)', C['h']),
        (('4LDJ', 'A'), ('6OIM', 'A'), 'KRAS(G12C)–GDP (4LDJ) vs KRAS(G12C)–sotorasib (6OIM)', C['sw2'])
    ]

    export_shifts = {}

    for i, (p1, p2, ttl, col) in enumerate(pairs):
        y = H - TOP - (i + 1) * PH - i * GAPY
        ax = axes(fig, XA, y, WA, PH)
        com, d, rms = devcurve(p1[0], p1[1], p2[0], p2[1])
        export_shifts[f"{p1[0]}_vs_{p2[0]}"] = dict(zip(com, d))
        
        ax.fill_between(com, 0, d, color=col, alpha=0.30, lw=0)
        ax.plot(com, d, color=col, lw=1.4)
        for nm, lo, hi, cc in REG:
            ax.axvspan(lo, hi, color=cc, alpha=0.18, zorder=0, lw=0)
            ax.text((lo + hi) / 2, max(d) * 1.17, nm, ha='center',
                    va='bottom', fontsize=T, color=cc)
        ax.set_xlim(1, 170)
        ax.set_ylim(0, max(d) * 1.32)
        ax.set_ylabel('Cα deviation (Å)', fontsize=T, labelpad=2)
        ax.yaxis.set_label_coords(-(XA - LEFT - 0.3) / WA, 0.5)
        ax.yaxis.label.set_va('top')
        ax.text(1.0, 1.03, ttl, transform=ax.transAxes, ha='right',
                va='bottom', fontsize=T, color=C['ink'])
        ax.text(1.0, 0.80, 'Core-region RMSD = %.2f Å' % rms,
                transform=ax.transAxes, ha='right', va='top',
                fontsize=T, color=C['grey'])
        ax.set_xticks([1, 25, 50, 75, 100, 125, 150, 170])
        if i == 1:
            ax.set_xlabel('Residue number', fontsize=T, labelpad=1.5)
        ax.tick_params(labelsize=T, pad=1.5, width=0.6, length=2.2)
        for s_ in ('top', 'right'):
            ax.spines[s_].set_visible(False)
        for s_ in ('left', 'bottom'):
            ax.spines[s_].set_linewidth(0.6)
        fig.text(LEFT / W2, (y + PH + 3.0) / H, 'ab'[i], fontsize=PN,
                 fontweight='bold', ha='left', va='bottom')

    # Export CSV data
    all_res = sorted(set(list(export_shifts["4OBE_vs_5VQ2"].keys()) + list(export_shifts["4LDJ_vs_6OIM"].keys())))
    csv_out = os.path.join(DATA, 'ca_distance_shifts.csv')
    with open(csv_out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Residue', 'Region', 'Dev_4OBE_GDP_vs_5VQ2_GTP_Angstrom', 'Dev_4LDJ_GDP_vs_6OIM_Sotorasib_Angstrom'])
        for r in all_res:
            reg_name = 'Core'
            if 10 <= r <= 17: reg_name = 'P-loop'
            elif 30 <= r <= 38: reg_name = 'switch I'
            elif 60 <= r <= 76: reg_name = 'switch II'
            elif 116 <= r <= 119: reg_name = 'G4'
            elif 145 <= r <= 147: reg_name = 'G5'
            d1 = export_shifts["4OBE_vs_5VQ2"].get(r, '')
            d2 = export_shifts["4LDJ_vs_6OIM"].get(r, '')
            writer.writerow([r, reg_name, f"{d1:.3f}" if d1 != '' else '', f"{d2:.3f}" if d2 != '' else ''])

    # Panel C
    SEGS = [('P-loop', C['ploop']), ('switch I', C['sw1']),
            ('switch II', C['sw2']), ('G4', C['g4']), ('G5', C['g5'])]
    seg_h = [plt.Line2D([], [], color=c, lw=2.6, label=n) for n, c in SEGS]
    lig_h = [plt.Line2D([], [], marker='o', ls='', color='#355070', ms=3.5, label='GDP'),
             plt.Line2D([], [], marker='o', ls='', color=C['sw2'], ms=3.5, label='Sotorasib (AMG 510)'),
             plt.Line2D([], [], marker='o', ls='', color=C['ploop'], ms=4, label='Mg$^{2+}$'),
             plt.Line2D([], [], marker='o', ls='', color=C['hot'], ms=4.5, mec='k', mew=0.3, label='Cys12 (covalent site)')]
    
    render = os.path.join(DATA, '_panelC_6OIM.png')
    LGH = 17.0
    CTOP = H - TOP + 2.0

    if os.path.exists(render):
        img = plt.imread(render)
        if img.ndim == 3 and img.shape[2] == 4:
            a = img[:, :, 3] > 0.02
            rs, cs = np.where(a.any(1))[0], np.where(a.any(0))[0]
            pad = int(0.01 * max(img.shape[:2]))
            img = img[max(rs[0] - pad, 0):rs[-1] + pad, max(cs[0] - pad, 0):cs[-1] + pad]
        ih = min(WC * img.shape[0] / img.shape[1], CTOP - BOT - LGH)
        iw = ih * img.shape[1] / img.shape[0]
        imax = axes(fig, XC + (WC - iw) / 2, CTOP - ih, iw, ih)
        imax.imshow(img, interpolation='antialiased')
        imax.set_axis_off()
        lgax = axes(fig, XC, BOT, WC, LGH)
        lgax.set_axis_off()
        L1 = lgax.legend(handles=seg_h, loc='upper left', fontsize=T,
                         handlelength=1.4, handletextpad=0.5, labelspacing=0.3,
                         borderpad=0, borderaxespad=0, frameon=False,
                         bbox_to_anchor=(0.08, 1.0))
        lgax.add_artist(L1)
        lgax.legend(handles=lig_h, loc='upper left', fontsize=T,
                    handlelength=1.0, handletextpad=0.5, labelspacing=0.3,
                    borderpad=0, borderaxespad=0, frameon=False,
                    bbox_to_anchor=(0.44, 1.0))
        fig.text((XC - 3.5) / W2, (H - TOP + 3.0) / H, 'c', fontsize=PN,
                 fontweight='bold', ha='left', va='bottom')

    stem = 'Figure3_conformational_switch'
    pdf_out = os.path.join(FIG, stem + '.pdf')
    svg_out = os.path.join(FIG, stem + '.svg')
    png_out = os.path.join(FIG, stem + '.png')

    fig.savefig(pdf_out, format='pdf', dpi=300)
    fig.savefig(svg_out, format='svg')
    fig.savefig(png_out, format='png', dpi=300)
    plt.close(fig)
    print("Figure 3 successfully generated:")
    print("  ->", pdf_out)
    print("  ->", svg_out)
    print("  ->", png_out)
    print("  -> ca_distance_shifts.csv exported.")

if __name__ == '__main__':
    main()
