#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 1 - Biophysical nucleotide cycling and structural paradigms of direct pharmacological RAS inhibition.

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
  python3 run_figure1.py
Output:
  ../figures/Figure1_Conformational_Switch_and_Inhibitor_Mechanisms.pdf
  ../figures/Figure1_Conformational_Switch_and_Inhibitor_Mechanisms.png
  ../figures/Figure1_Conformational_Switch_and_Inhibitor_Mechanisms.svg
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
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'figures'))
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
    'line_a': '#A63A2E',
    'line_b': '#2A6F6F',
    'peak_a': '#7A1C14',
    'peak_b': '#174040',
    'text': '#2A2A2A',
    'subtle': '#6E6E6E',
    'grid': '#E5E5E5',
    'axis': '#333333',
    'white': '#FFFFFF',
}

def parse_ca(path, chain='A', min_res=1, max_res=166):
    coords = {}
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith(('ATOM  ', 'HETATM')):
                atom = line[12:16].strip()
                ch = line[21]
                if atom == 'CA' and ch == chain:
                    resseq = int(line[22:26])
                    if min_res <= resseq <= max_res and resseq not in coords:
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        coords[resseq] = np.array([x, y, z])
    return coords

def align_and_rmsd(ref, mob):
    common = sorted(set(ref.keys()) & set(mob.keys()))
    r_pts = np.array([ref[r] for r in common])
    m_pts = np.array([mob[r] for r in common])
    cr = r_pts.mean(axis=0)
    cm = m_pts.mean(axis=0)
    r_cen = r_pts - cr
    m_cen = m_pts - cm
    H = m_cen.T @ r_cen
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    m_rot = (m_pts - cm) @ R + cr
    dists = {r: float(np.linalg.norm(r_pts[i] - m_rot[i])) for i, r in enumerate(common)}
    return common, dists

def main():
    print("Parsing PDB files...")
    obe = parse_ca(os.path.join(DATA, '4OBE.pdb'), 'B')
    vq2 = parse_ca(os.path.join(DATA, '5VQ2.pdb'), 'A')
    ldj = parse_ca(os.path.join(DATA, '4LDJ.pdb'), 'A')
    oim = parse_ca(os.path.join(DATA, '6OIM.pdb'), 'A')

    c_a, d_a = align_and_rmsd(obe, vq2)
    c_b, d_b = align_and_rmsd(ldj, oim)

    # Export CSV
    csv_path = os.path.join(DATA, 'ca_distance_shifts.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Residue', 'Shift_GDP_to_GTP_Angstrom', 'Shift_GDP_to_Sotorasib_Angstrom'])
        for r in range(1, 167):
            w.writerow([r, f"{d_a.get(r, 0.0):.3f}", f"{d_b.get(r, 0.0):.3f}"])
    print(f"Exported distance matrix to {csv_path}")

    # Build Matplotlib figure
    fig = plt.figure(figsize=(W2 * MM, 85 * MM), dpi=300)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1.0], height_ratios=[1, 1],
                           left=0.08, right=0.98, bottom=0.12, top=0.92,
                           wspace=0.18, hspace=0.35)

    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[:, 1])

    # Plot panel a
    ax_a.plot(c_a, [d_a[r] for r in c_a], color=C['line_a'], lw=1.2)
    ax_a.fill_between(c_a, [d_a[r] for r in c_a], color=C['line_a'], alpha=0.15)
    ax_a.axvspan(10, 17, color=C['ploop'], alpha=0.18)
    ax_a.axvspan(30, 38, color=C['sw1'], alpha=0.18)
    ax_a.axvspan(59, 76, color=C['sw2'], alpha=0.18)
    ax_a.set_xlim(1, 166)
    ax_a.set_ylim(0, 10)
    ax_a.set_ylabel('Cα displacement (Å)', fontsize=T)
    ax_a.text(0.02, 0.88, 'A: KRAS-GDP vs KRAS-GTP (5VQ2/4OBE)', transform=ax_a.transAxes, fontsize=T, fontweight='bold', color=C['text'])
    ax_a.grid(True, ls=':', color=C['grid'], lw=0.5)

    # Plot panel b
    ax_b.plot(c_b, [d_b[r] for r in c_b], color=C['line_b'], lw=1.2)
    ax_b.fill_between(c_b, [d_b[r] for r in c_b], color=C['line_b'], alpha=0.15)
    ax_b.axvspan(10, 17, color=C['ploop'], alpha=0.18)
    ax_b.axvspan(30, 38, color=C['sw1'], alpha=0.18)
    ax_b.axvspan(59, 76, color=C['sw2'], alpha=0.18)
    ax_b.set_xlim(1, 166)
    ax_b.set_ylim(0, 10)
    ax_b.set_xlabel('Residue position (KRAS G-domain)', fontsize=T)
    ax_b.set_ylabel('Cα displacement (Å)', fontsize=T)
    ax_b.text(0.02, 0.88, 'B: KRAS(G12C)-GDP vs +Sotorasib (6OIM/4LDJ)', transform=ax_b.transAxes, fontsize=T, fontweight='bold', color=C['text'])
    ax_b.grid(True, ls=':', color=C['grid'], lw=0.5)

    # Plot panel c
    panel_c_img = os.path.join(DATA, '_panelC_6OIM.png')
    if os.path.exists(panel_c_img):
        img = plt.imread(panel_c_img)
        ax_c.imshow(img)
        ax_c.axis('off')
        ax_c.text(0.02, 0.96, 'C: Sotorasib in Switch-II Pocket (6OIM)', transform=ax_c.transAxes, fontsize=T, fontweight='bold', color=C['text'])

    out_prefix = os.path.join(FIG, 'Figure1_Conformational_Switch_and_Inhibitor_Mechanisms')
    for ext in ['.png', '.pdf', '.svg']:
        plt.savefig(f"{out_prefix}{ext}", dpi=300)
    print(f"Generated Figure 1 vector assets in {FIG}")

if __name__ == '__main__':
    main()
