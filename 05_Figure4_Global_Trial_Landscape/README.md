# Figure 4: Global Landscape of 1,182 RAS-Related Oncology Clinical Trials

[English](./README.md) | [中文说明](#中文说明)

---

## English Summary

**Manuscript Reference:** Figure 4 (Main Text, Section 5)  
**Figure Title:** *Global landscape and geographic distribution of 1,182 RAS-related oncology clinical trials.*  
**Production Artwork:** `figures/Figure4_Global_Clinical_Trial_Atlas_and_Geography.{tif,pdf,png,eps}` (and `figures/Fig4.*`)  
**Print Specifications:** Standard double-column width (180.0 mm), height 125.0 mm, 500 DPI LZW TIFF, Vector Cairo PDF, Vector EPS.

### Panels:
- **Panel A (Clinical Phase Distribution):** Stratification of active RAS trials showing early-phase concentration: Phase 1 (132 trials, 35.8%), Phase 1/2 (124 trials, 33.6%), Phase 2 (78 trials, 21.1%), and Phase 3 (35 trials, 9.5%), demonstrating the clinical translation bottleneck.
- **Panel B (Drug Modalities & Regimen Strategy):** Comparison of direct G12C inhibitors (192 trials), G12D inhibitors (68 trials), multi-RAS(ON) / pan-RAS inhibitors (54 trials), indirect pathway modulators (SOS1/SHP2, 72 trials), and RAS vaccines/TCR-T therapies (42 trials), highlighting the pronounced shift from monotherapy to rational combination regimens (>60% in development).
- **Panel C (Geographic Distribution & Strategic Focus):** Analysis of global trial registrations across North America (198 trials), East Asia (162 trials), Europe (78 trials), and Multinational consortia (54 trials), defining their regional specialization.

### Data Sources & Methodology:
- **Data Source:** ClinicalTrials.gov REST API v2 (`/api/v2/studies`).
  - Search query retrieved 3,210 initial interventional oncology trial records.
  - Two-round independent manual double-blind curation excluded 2,028 non-qualifying records (1,907 renin-angiotensin cardiovascular studies, 38 non-malignant indications, 19 non-malignant RASopathies, 54 non-evaluable phases, 10 Phase IV post-marketing studies).
  - 1,182 unique interventional trials met all inclusion criteria across 72 countries.
- **Data Cutoff Date:** 18 November 2026 snapshot.
- **Software & Packages Used:**
  - **Python (>= 3.10):** `requests` (>= 2.31.0) for API JSON payload retrieval; `collections` & `csv` for multi-tier qualification pipelines (`code/fig2_fetch_ctgov.py`, `code/fig2_curate.py`).
  - **R (>= 4.3.0 / 4.4.0):**
    - `ggplot2` (>= 3.5.0): Primary plotting system for funnels, modality breakdowns, and bar charts
    - `patchwork` (>= 1.2.0): 4-panel comprehensive figure composition
    - `dplyr` (>= 1.1.4): Cross-tabulation of phases, drug targets, and countries
    - `scales` (>= 1.3.0): Logarithmic and integer trial count axes
    - `cowplot` (>= 1.1.3): Complex graphical composition with geographic insets
    - `readr` (>= 2.1.5): Tabular parsing of trial metadata

### Data Files (`data/`):
- `trials_1182.csv` (Complete ClinicalTrials.gov dataset, frozen 18 November 2026)
- `trial_geographic_summary.csv` (Regional breakdown)

### How to Reproduce:
```bash
Rscript code/run_figure4_trial_landscape.R
```

---

## 中文说明

**论文对应编号：** 图 4（正文第五节）  
**图件标题：** 1,182项全球RAS相关肿瘤临床试验全景图谱与地理分布  
**高清印刷文件：** `figures/Figure4_Global_Clinical_Trial_Atlas_and_Geography.{tif,pdf,png,eps}`（提交简名 `figures/Fig4.*`）  

### 图件核心数据与趋势：
1. **A 面板试验分期：** 揭示研发管线极度倾斜于早期阶段，I 期与 I/II 期合计占 69.4%，而进入确证性 III 期试验的仅占 9.5%。
2. **B 面板分子类型与联合用药：** 靶向 G12C 的试验依然最多（192 项），但 G12D 与多靶点 pan-RAS 药物迅速崛起；联合用药方案占比已超过 60%，单药时代加速过渡为联合时代。
3. **C 面板全球地理格局：** 北美（198 项）以 First-in-class 分子胶与早期探索为主，东亚（中日韩，162 项）在新型 G12D 与快速跟进方面展现极高临床效率，欧洲（78 项）则聚焦于生物标志物驱动的转化研究。
