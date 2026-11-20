# Figure 1 — Experimental structures of the two principal classes of direct KRAS inhibitors

**a,** KRAS(G12C) covalently bound to sotorasib in the switch-II pocket (PDB 6OIM; Canon et al., *Nature* 2019, reference 21 of the manuscript). Switch II is coloured and labelled as residues 60–76, as in the text. **b,** Tri-complex of daraxonrasib (RMC-6236), cyclophilin A and GMPPNP-bound KRAS(G12V) (PDB 9BG6). KRAS in **b** is superposed onto KRAS in **a**.

| File | Role |
|:---|:---|
| `data/6OIM.pdb`, `data/9BG6.cif` | RCSB PDB coordinates |
| `code/render_figure1_pymol.py` | PyMOL renders → `data/_fig1a_6OIM.png`, `data/_fig1b_9BG6.png` (9BG6 chains B and D removed; KRAS chain A superposed on 6OIM) |
| `code/run_figure1.py` | Trims renders (ImageMagick) and composes the figure (matplotlib) → `figures/Fig1.{pdf,png,tif}` |

```bash
cd 01_Figure1_Structural_Mechanisms
pymol -cq code/render_figure1_pymol.py
python3 code/run_figure1.py
```

**中文：** 图 1 为两类直接 KRAS 抑制剂的晶体结构：a 为 sotorasib 共价结合 KRAS(G12C) 开关 II 口袋（6OIM），b 为 daraxonrasib–亲环素 A–KRAS(G12V) 三元复合物（9BG6）。先运行 PyMOL 渲染，再运行拼图脚本。
