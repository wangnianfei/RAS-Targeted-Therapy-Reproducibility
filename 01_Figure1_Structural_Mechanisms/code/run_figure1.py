#!/usr/bin/env python3
"""Figure 1 (revised): experimental structures of the two inhibitor classes.
Step 1 (PyMOL):  pymol -cq code/render_figure1_pymol.py   -> data/_fig1a_6OIM.png, data/_fig1b_9BG6.png
Step 2 (this):   python code/run_figure1.py               -> figures/Fig1.{pdf,png,tif}
a: KRAS(G12C)-GDP-sotorasib, PDB 6OIM.  b: daraxonrasib-cyclophilin A-KRAS(G12V)-GMPPNP tri-complex, PDB 9BG6.
"""
import os, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', 'data'); F = os.path.join(HERE, '..', 'figures'); os.makedirs(F, exist_ok=True)
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
                     'pdf.fonttype': 42, 'font.size': 7})
for fn in ('_fig1a_6OIM.png', '_fig1b_9BG6.png'):
    subprocess.run(['magick', os.path.join(D, fn), '-trim', '-bordercolor', 'white', '-border', '20', os.path.join(D, 'trim' + fn)], check=True)
fig = plt.figure(figsize=(180 / 25.4, 98 / 25.4))
for k, (fn, tag, title) in enumerate([
        ('_fig1a_6OIM.png', 'a', 'KRAS(G12C)–GDP with sotorasib in the switch-II pocket (PDB 6OIM)'),
        ('_fig1b_9BG6.png', 'b', 'Daraxonrasib–cyclophilin A–KRAS(G12V)–GMPPNP tri-complex (PDB 9BG6)')]):
    ax = fig.add_axes([0.005 + k * 0.5, 0.15, 0.49, 0.78]); ax.imshow(plt.imread(os.path.join(D, 'trim' + fn))); ax.axis('off')
    fig.text(0.01 + k * 0.5, 0.97, tag, fontsize=10, fontweight='bold', va='top')
    fig.text(0.035 + k * 0.5, 0.965, title, fontsize=6.8, va='top')
key = [('#1F3A5F', 'P-loop (residues 10–17)'), ('#E89E33', 'Switch I (30–38)'), ('#C73845', 'Switch II (60–76)'),
       ('#DBE0E6', 'KRAS G domain'), ('#94339E', 'Inhibitor (sotorasib / daraxonrasib)'), ('#4D6B8C', 'Nucleotide (GDP / GMPPNP)'),
       ('#F2CC26', 'Cys12 (panel a)'), ('#808080', 'H95, Y96, Q99 side chains (panel a)'), ('#52A094', 'Cyclophilin A (panel b)'), ('#7FE01A', r'Mg$^{2+}$ ion')]
fig.legend(handles=[Patch(facecolor=c, edgecolor='#888888', lw=0.3, label=l) for c, l in key], loc='lower center',
           ncol=5, frameon=False, fontsize=6.3, bbox_to_anchor=(0.5, 0.0), handlelength=1.2, columnspacing=1.4)
for ext in ('pdf', 'png'):
    fig.savefig(os.path.join(F, f'Fig1.{ext}'), dpi=500)
subprocess.run(['magick', os.path.join(F, 'Fig1.png'), '-density', '500', '-units', 'PixelsPerInch', '-compress', 'LZW',
                os.path.join(F, 'Fig1.tif')], check=True)
print('Figure 1 written')
