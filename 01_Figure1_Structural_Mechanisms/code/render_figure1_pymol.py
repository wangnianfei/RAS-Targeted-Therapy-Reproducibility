"""Render the two structural panels of Figure 1 with PyMOL (run from 01_Figure1_Structural_Mechanisms/: pymol -cq code/render_figure1_pymol.py).
a: KRAS(G12C)-GDP covalently bound to sotorasib, PDB 6OIM (Canon et al., Nature 2019).
b: Tri-complex of daraxonrasib (RMC-6236), KRAS(G12V)-GMPPNP and cyclophilin A, PDB 9BG6 (Cregg et al., J Med Chem 2025).
KRAS in b is superposed onto KRAS in a so both panels share one orientation."""
import os
from pymol import cmd
# run from the figure directory: pymol -cq code/render_figure1_pymol.py
D = OUT = os.path.join(os.getcwd(), 'data')
cmd.reinitialize()
cmd.set('ray_opaque_background', 0); cmd.bg_color('white')
cmd.set('cartoon_fancy_helices', 1); cmd.set('ray_trace_mode', 1); cmd.set('ray_trace_gain', 0.08)
cmd.set('antialias', 2); cmd.set('ambient', 0.45); cmd.set('specular', 0.15); cmd.set('stick_radius', 0.28)
cmd.set_color('c_core', [0.86, 0.88, 0.90]); cmd.set_color('c_ploop', [0.12, 0.23, 0.37])
cmd.set_color('c_sw1', [0.91, 0.62, 0.20]); cmd.set_color('c_sw2', [0.78, 0.22, 0.27])
cmd.set_color('c_drug', [0.58, 0.20, 0.62]); cmd.set_color('c_nuc', [0.30, 0.42, 0.55])
cmd.set_color('c_cypa', [0.32, 0.62, 0.58]); cmd.set_color('c_cys', [0.95, 0.80, 0.15])

def style_kras(sel):
    cmd.show('cartoon', sel); cmd.color('c_core', sel)
    cmd.color('c_ploop', f'{sel} and resi 10-17'); cmd.color('c_sw1', f'{sel} and resi 30-38')
    cmd.color('c_sw2', f'{sel} and resi 60-76')   # switch II as in the main text (Cox et al. 2014)

cmd.load(os.path.join(D, '6OIM.pdb'), 's6oim'); cmd.remove('s6oim and (solvent or hydro)')
cmd.load(os.path.join(D, '9BG6.cif'), 's9bg6'); cmd.remove('s9bg6 and (solvent or hydro)')
# The asymmetric unit holds two tri-complexes: KRAS A + CypA/drug D and KRAS B + CypA/drug C
# (drug contacts KRAS switch I P34-I36 and switch II A59-M67; A-C and B-D are crystal contacts).
cmd.remove('s9bg6 and chain B+C')   # keep one functional tri-complex: KRAS chain A + CypA chain D
cmd.super('s9bg6 and chain A and name CA and resi 1-166', 's6oim and name CA and resi 1-166')
cmd.hide('everything')

# panel a
style_kras('s6oim and polymer')
cmd.show('sticks', 's6oim and resn MOV'); cmd.color('c_drug', 's6oim and resn MOV and elem C')
cmd.show('sticks', 's6oim and resn GDP'); cmd.color('c_nuc', 's6oim and resn GDP and elem C')
cmd.show('sticks', 's6oim and resi 12 and not name N+C+O'); cmd.color('c_cys', 's6oim and resi 12 and elem C')
cmd.show('sticks', 's6oim and resi 95+96+99 and not name N+C+O'); cmd.color('grey50', 's6oim and resi 95+96+99 and elem C')
cmd.show('spheres', 's6oim and resn MG'); cmd.set('sphere_scale', 0.35)
cmd.util.cnc('s6oim')
cmd.orient('s6oim and polymer'); cmd.turn('y', 90); cmd.zoom('s6oim', 2)
v = cmd.get_view()
cmd.disable('s9bg6'); cmd.ray(1500, 1500); cmd.png(os.path.join(OUT, '_fig1a_6OIM.png'), dpi=500)

# panel b (same view)
cmd.disable('s6oim'); cmd.enable('s9bg6'); cmd.hide('everything', 's9bg6')
style_kras('s9bg6 and chain A and polymer')
cmd.show('cartoon', 's9bg6 and chain D and polymer'); cmd.color('c_cypa', 's9bg6 and chain D and polymer')
cmd.show('surface', 's9bg6 and chain D and polymer'); cmd.set('transparency', 0.82); cmd.set('surface_color', 'c_cypa')
cmd.show('sticks', 's9bg6 and resn A1AHB'); cmd.set('stick_radius', 0.34, 's9bg6 and resn A1AHB'); cmd.set('stick_transparency', 0); cmd.color('c_drug', 's9bg6 and resn A1AHB and elem C')
cmd.show('sticks', 's9bg6 and resn GNP'); cmd.color('c_nuc', 's9bg6 and resn GNP and elem C')
cmd.show('spheres', 's9bg6 and resn MG'); cmd.util.cnc('s9bg6')
cmd.set_view(v); cmd.zoom('s9bg6', 0)
cmd.ray(1500, 1500); cmd.png(os.path.join(OUT, '_fig1b_9BG6.png'), dpi=500)
print('rendered')
