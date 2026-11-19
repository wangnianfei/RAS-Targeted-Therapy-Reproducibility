# Figure 2: Pan-Cancer Genomic Landscape of RAS Alterations and Co-Mutations

[English](./README.md) | [中文说明](#中文说明)

---

## English Summary

**Manuscript Reference:** Figure 2 (Main Text, Section 3)  
**Figure Title:** *Pan-cancer genomic landscape of RAS alterations and co-mutational stratification.*  
**Production Artwork:** `figures/Figure2_PanCancer_RAS_Landscape_and_CoMutations.{tif,pdf,png,eps}` (and `figures/Fig2.*`)  
**Print Specifications:** Standard double-column width (180.0 mm), height 125.0 mm, 500 DPI LZW TIFF, Vector Cairo PDF, Vector EPS.

### Panels:
- **Panel A (Pan-Cancer Isoform Prevalence):** Mutation frequencies of *KRAS*, *NRAS*, and *HRAS* across 7 major solid tumour malignancies (Pancreatic PDAC 91.2%, Colorectal CRC 44.5%, Lung LUAD 32.4%, Endometrial 19.7%, Melanoma 25.5% *NRAS*, Thyroid 16.0% *NRAS*, Bladder 6.9% *KRAS* / 4.5% *HRAS*).
- **Panel B (Allele Proportions):** Distinct codon-12/13/61 allele shares across PDAC, CRC, and LUAD, illustrating the tobacco carcinogen transversion signature (G12C 41% in LUAD) versus spontaneous CpG deamination transitions (G12D 45% in PDAC, 30% in CRC).
- **Panel C (Co-Mutational Genomic Subgroups in NSCLC):** Genomic stratification into KP (*TP53* co-mutant, 40%), KL (*STK11* co-mutant, 25%), *KEAP1* (15%), and KC (*CDKN2A* co-mutant, 10%), detailing their respective tumour microenvironmental phenotypes (inflamed vs cold) and immunotherapy/targeted response profiles.

### Data Sources & Methodology:
- **Data Source:** MSK-IMPACT Pan-Cancer Clinical Sequencing Cohort (10,945 patients, PMID: 28481359) queried via cBioPortal REST API v2 (`/api/v2`), supplemented by TCGA Pan-Cancer Atlas.
  - Functional non-synonymous mutation calls filtered by canonical isoform transcript.
  - Denominators strictly defined as total patients sequenced in each specific tumor indication ($N_{total}$: PDAC 479, CRC 1,061, LUAD 1,255, Endometrial 320, Melanoma 326, Thyroid 125, Bladder 411) to avoid allele frequency bias.
  - Co-mutation odds ratios and exclusivity calculated via two-sided Fisher's exact test with Benjamini-Hochberg FDR correction.
- **Data Cutoff Date:** 18 November 2026.
- **Software & Packages Used:**
  - **R (>= 4.3.0 / 4.4.0):**
    - `ggplot2` (>= 3.5.0): Primary plotting system for all 3 panels
    - `patchwork` (>= 1.2.0): Multi-panel alignment and tag positioning
    - `dplyr` (>= 1.1.4): Mutation aggregation and frequency normalization
    - `tidyr` (>= 1.3.1): Reshaping mutation matrices
    - `scales` (>= 1.3.0): Percentage axis scaling and custom color gradients
    - `ggtext` (>= 0.1.2): Markdown formatting for gene labels (*KRAS*, *TP53*, *STK11*, *KEAP1*)
    - `Cairo` (>= 1.6-2): High-resolution vector PDF, EPS, and 500 DPI TIFF generation

### Data Files (`data/`):
- `pancancer_isoform_frequencies.csv` (Curated isoform prevalence)
- `kras_allele_frequencies.csv` (Allele breakdown across PDAC, CRC, LUAD)
- `comutation_subgroups_nsclc.csv` (Genomic subgroups, microenvironment, therapy)
- `cancer_type_kras_alleles.csv`, `cbioportal_mutations.json` (MSK-IMPACT raw inputs)

### How to Reproduce:
```bash
Rscript code/run_figure2.R
```

---

## 中文说明

**论文对应编号：** 图 2（正文第三节）  
**图件标题：** RAS突变的泛癌种分布特征与共突变亚型分层  
**高清印刷文件：** `figures/Figure2_PanCancer_RAS_Landscape_and_CoMutations.{tif,pdf,png,eps}`（提交简名 `figures/Fig2.*`）  

### 图件核心发现：
1. **A 面板：** 详述实体瘤中 RAS 突变的器官嗜性，胰腺癌以 KRAS 突变为主（91.2%），结直肠癌（44.5%），肺腺癌（32.4%），而黑色素瘤（25.5%）与甲状腺癌（16.0%）则显著富集 NRAS 突变。
2. **B 面板：** 揭示不同癌种中等位基因突变构成的病因学指纹：吸烟相关的肺腺癌中 G>T 颠换导致 G12C 突变高达 41%；而胃肠道肿瘤以自发脱氨基为主，G12D 与 G12V 突变合计占据 70% 以上。
3. **C 面板：** 建立 KRAS 突变非小细胞肺癌的共突变分层体系：KP 亚型（伴 TP53 突变，热肿瘤，免疫敏感）、KL 亚型（伴 STK11 缺失，冷肿瘤，免疫耐药）、KEAP1 亚型（代谢与铁死亡耐药）与 KC 亚型（CDKN2A 缺失，周期加速），并指明相应的靶向联合方向。
