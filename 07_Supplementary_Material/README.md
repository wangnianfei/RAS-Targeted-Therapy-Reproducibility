# Supplementary Material: Figure S1 & Tables S1–S3

[English](./README.md) | [中文说明](#中文说明)

---

## English Summary

**Manuscript Reference:** Supplementary Appendix (4 Pages, ESMO Open Submission)  
**Supplementary Figures:**
- **Supplementary Figure S1:** *Strategy decision matrix mapping 9 acquired resistance mechanisms against 5 clinical combination logics.* (`figures/Supplementary_Figure1_Resistance_Mechanism_Combination_Decision_Matrix.{tif,pdf,png}`, `figures/FigS1.*`)
  - **Panel A:** 9×5 Functional decision matrix across Genomic, Plasticity, and Metabolic alteration classes.
  - **Panel B:** Clinical detection rates in paired plasma (ctDNA) vs tissue cohorts in NSCLC and CRC.

**Supplementary Tables:**
- **Table S1:** Landscape of direct RAS inhibitors across four molecular mechanism classes (Class I covalent OFF, Class II non-covalent OFF, Class III tri-complex ON/OFF, Class IV degraders).
- **Table S2:** Global regulatory approvals, indications, and post-marketing confirmatory trial trajectories (FDA, EMA, NMPA, PMDA, including KRYSTAL-10 withdrawal).
- **Table S3:** Mechanistic matrix of acquired resistance patterns, functional pathways, and rational combination counterstrategies.

**Appendix Document:**
- `RAS_Targeted_Therapy_Review_Supplementary_Appendix.docx`
- `RAS_Targeted_Therapy_Review_Supplementary_Appendix.pdf`
- `RAS_Targeted_Therapy_Review_Supplementary_Appendix.md`

### Data Sources & Methodology:
- **Data Source:** Paired plasma (ctDNA) vs tissue clinical cohorts (Awad 2021, Yaeger 2023, CodeBreaK 100/200, KRYSTAL-1) for Supplementary Figure S1; official regulatory review dossiers from FDA (Orange Book, CDER), EMA (EPAR), NMPA, and PMDA for Supplementary Tables S1–S3.
- **Data Cutoff Date:** 18 November 2026.
- **Software & Packages Used:**
  - **Python (>= 3.10):**
    - `matplotlib` (>= 3.8.0): Figure S1 9x5 matrix visualization and paired detection rate bar charts (`code/run_figureS1_resistance_matrix.py`)
    - `numpy` (>= 1.26.0), `pillow` (>= 10.0.0): 500 DPI TIFF and Cairo PDF export
    - `python-docx` (>= 1.1.2): 4-page Supplementary Appendix document generation
    - `openpyxl` (>= 3.1.2): Programmatic creation of Supplementary Tables S1–S3 Excel workbooks

### How to Reproduce:
```bash
python3 code/run_figureS1_resistance_matrix.py
python3 code/build_supplementary_tables.py
```

---

## 中文说明

**论文对应编号：** 补充附录（4页标准版心，含附图 S1 与附表 S1–S3）  
**附图 S1：** 9 种获得性耐药机制与 5 大临床联合干预逻辑的功能对应决策矩阵，以及外周血 ctDNA 与组织配对检出率。  
**附表 S1：** 四代直接靶向 RAS 抑制剂的化学分类、作用机制、结合构象与研发阶段。  
**附表 S2：** 全球四大监管机构（FDA/EMA/NMPA/PMDA）批准案卷、适应症及上市后确证性试验轨迹（含 KRYSTAL-10 撤销全记录）。  
**附表 S3：** 获得性耐药位点、受累生化通路及前瞻性补救联合治疗方案矩阵。
