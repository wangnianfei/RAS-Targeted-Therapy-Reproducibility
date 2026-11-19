# Figure 5: Comprehensive Molecular Networks of Acquired Resistance and Multimodal Combinations

[English](./README.md) | [中文说明](#中文说明)

---

## English Summary

**Manuscript Reference:** Figure 5 (Main Text, Section 6)  
**Figure Title:** *Comprehensive molecular networks of acquired resistance and multimodal combination strategies.*  
**Production Artwork:** `figures/Figure5_Acquired_Resistance_Networks_and_Rational_Combinations.{tif,pdf,png}` (and `figures/Fig5.*`)  
**Print Specifications:** Standard double-column width (180.0 mm), 500 DPI LZW TIFF, Vector Cairo PDF, intact extracellular receptor domains (MET, AXL, EGFR, HER2).

### Molecular Resistance Networks:
1. **On-Target Switch-II Secondary Mutations (15%–25%):** Emergence of Y96C/D, H95D/Q/R, R68S, and A59S/T perturbing covalent inhibitor binding geometry. Asymmetric binding permits sequential inhibitor switching (adagrasib to sotorasib for H95 mutations).
2. **Upstream RTK Feedback Reactivation (10%–15%):** Loss of ERK-mediated negative feedback leading to focal *MET* amplification, *HER2* amplification, and upregulation of *AXL* and *EGFR*. Overcome by vertical receptor co-inhibition.
3. **Signaling Hub Hyperactivation (15%–20%):** SHP2 (*PTPN11*) and SOS1 functional upregulation sustaining nucleotide exchange across wild-type and mutant RAS.
4. **Downstream MAPK Pathway Bypass (8%–12%):** *BRAF* V600E/non-V600 mutations, *CRAF* fusions, *NRAS* Q61K, and *MAP2K1* (MEK1) mutations restoring ERK phosphorylation independently of RAS.
5. **Parallel Survival Activation (5%–10%):** *PIK3CA* oncogenic mutations and *PTEN* loss restoring PI3K/AKT survival signaling.
6. **Phenotypic Lineage Plasticity (3%–5%):** Small-cell neuroendocrine histological transformation and epithelial-to-mesenchymal transition (EMT) with biallelic *TP53*/*RB1* co-inactivation, requiring chemo-immunotherapy rescue.
7. **ctDNA Kinetics:** Early molecular clearance at C2D1 as an actionable surrogate marker (ORR ~80% vs <10%, HR < 0.35), providing a 2–4 month lead time prior to radiographic progression.

### Data Sources & Methodology:
- **Data Source:** High-impact peer-reviewed resistance cohorts and translational genomics studies:
  - Awad MM et al. *N Engl J Med* 2021;384:2382-2393 (KRAS G12C resistance spectrum)
  - Yaeger R et al. *Nature* 2023;616:783-794 (CRC acquired resistance and polyclonal dynamics)
  - Bekaii-Saab TS et al. *ESMO GI* 2024/2025 (KRYSTAL-10 resistance profiles)
  - Negrao MV et al. *Clin Cancer Res* 2025;31:1069-1081 (Transcriptional and co-mutational resistance in NSCLC)
  - Dy GK et al. *J Clin Oncol* 2023;41:3311-3317 (CodeBreaK 100 2-year ctDNA molecular correlates).
- **Data Cutoff Date:** 18 November 2026.
- **Software & Packages Used:**
  - **Python (>= 3.10):** `matplotlib` (>= 3.8.0), `numpy` (>= 1.26.0), `pillow` (>= 10.0.0)
  - **ImageMagick (>= 7.1.1):** Lanczos resampling filter, 500 DPI LZW TIFF packaging, color space preservation
  - **Vector Pipeline:** Intact extracellular receptor domains (MET, AXL, EGFR, HER2) rendered in scalable vector geometry.

### Data Files (`data/`):
- `resistance_alterations_pathways.csv` (Curated alteration classes and frequencies)
- `resistance_combination_targets.csv` (Targeted rescue combination partners)

### How to Validate:
```bash
python3 code/run_figure5.py
```

---

## 中文说明

**论文对应编号：** 图 5（正文第六节）  
**图件标题：** 获得性耐药分子网络与多维度联合应对策略全景  
**高清印刷文件：** `figures/Figure5_Acquired_Resistance_Networks_and_Rational_Combinations.{tif,pdf,png}`（提交简名 `figures/Fig5.*`）  

### 图件核心科学内容：
1. **靶内继发突变：** 详解 Switch-II 口袋残基突变（Y96、H95、R68、A59）对共价结合的立体位阻与口袋重塑，阐明 H95 突变保留对索托拉西布敏感性的分子机制。
2. **上游受体反馈：** 阐明 ERK 负反馈解除后引发的 MET、HER2 扩增及 AXL/EGFR 代偿性激活，建立垂直阻断的临床必要性。
3. **下游通路旁路：** 揭示 BRAF、CRAF、NRAS 及 MEK1 突变如何绕过 RAS 直接激活 MAPK 级联。
4. **组织表型可塑性：** 总结小细胞神经内分泌转化与 EMT 的分子特征（常伴 TP53/RB1 双等位基因缺失）。
5. **液体活检 ctDNA 监测：** 强调早期（C2D1）ctDNA 清除对长期生存的预测价值，以及 ctDNA 较影像学提前 2–4 个月捕捉继发耐药突变的临床干预窗口。
