# Figure 1: Biophysical Nucleotide Cycling & Structural Paradigms of Direct Pharmacological RAS Inhibition

[English](./README.md) | [中文说明](#中文说明)

---

## English Summary

**Manuscript Reference:** Figure 1 (Main Text, Section 2)  
**Figure Title:** *Biophysical nucleotide cycling and structural paradigms of direct pharmacological RAS inhibition.*  
**Production Artwork:** `figures/Figure1_Conformational_Switch_and_Inhibitor_Mechanisms.{tif,pdf,png}` (and `figures/Fig1.*`)  
**Print Specifications:** Standard double-column width (180.0 mm), 500 DPI LZW TIFF, Vector Cairo PDF, TrueType Arial typography.

### Structural Panels:
- **Panel A (KRAS-GDP vs KRAS-GTP, PDB 4OBE vs 5VQ2):** Residue-level Cα displacement profile illustrating switch-I (residues 30–38) and switch-II (residues 59–76) dynamic loop movements during nucleotide exchange.
- **Panel B (KRAS(G12C)-GDP vs +Sotorasib, PDB 4LDJ vs 6OIM):** Structural displacement upon covalent engagement of mutant Cys12 in the induced switch-II hydrophobic pocket (S-IIP).
- **Panel C (3D Pocket Architecture, PDB 6OIM):** High-resolution molecular surface view showing sotorasib occupying the switch-II pocket, forming covalent adduct with Cys12 while preserving native GDP binding.
- **Pharmacological Classes:** Class I (covalent OFF-state inhibitors; sotorasib, adagrasib, divarasib, glecirasib, fulzerasib), Class II (non-covalent OFF-state inhibitors; MRTX1133), Class III (tri-complex ON/OFF inhibitors recruiting cyclophilin A; daraxonrasib RMC-6236), Class IV (targeted degraders; ASP3082).

### Data Files (`data/`):
- `4OBE.pdb` (KRAS wild-type GDP-bound, 1.24 Å)
- `5VQ2.pdb` (KRAS wild-type GTP-bound)
- `4LDJ.pdb` (KRAS G12C GDP-bound apo)
- `6OIM.pdb` (KRAS G12C bound to sotorasib)
- `ca_distance_shifts.csv` (Calculated Cα displacement matrix across 166 residues)
- `_panelC_6OIM.png` (600 DPI ray-traced molecular surface)

### How to Reproduce:
```bash
python3 code/run_figure1.py
```

---

## 中文说明

**论文对应编号：** 图 1（正文第二节）  
**图件标题：** RAS蛋白核苷酸循环生物物理机制与直接靶向抑制剂的结构模式  
**高清印刷文件：** `figures/Figure1_Conformational_Switch_and_Inhibitor_Mechanisms.{tif,pdf,png}`（提交简名 `figures/Fig1.*`）  
**印刷规格：** 180.0 mm 标准通栏版心，500 DPI LZW TIFF 与矢量 Cairo PDF，无文字碰撞。

### 图件核心内容：
1. **A 面板：** 基于 PDB 4OBE 与 5VQ2 晶体坐标，精确计算 GDP 与 GTP 结合态之间 166 个氨基酸残基的 Cα 骨架位移曲线，展示 Switch-I（30–38 位）与 Switch-II（59–76 位）的功能性位移。
2. **B 面板：** 基于 PDB 4LDJ 与 6OIM 晶体坐标，计算共价抑制剂（索托拉西布）结合前后的残基位移，揭示 Switch-II 口袋（S-IIP）的诱导性开辟。
3. **C 面板：** 600 DPI 光线追踪分子表面图，清晰展示索托拉西布与突变型 Cys12 形成不可逆共价加合物的空间取向。
4. **四大抑制剂代际：** 汇总第一类（OFF态共价）、第二类（OFF态非共价）、第三类（ON/OFF三元复合物分子胶）、第四类（PROTAC靶向降解剂）的作用机制与代表化合物。
