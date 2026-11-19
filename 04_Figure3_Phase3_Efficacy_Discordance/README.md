# Figure 3: Phase III RCT Efficacy Synthesis & Crossover Meta-Regression

[English](./README.md) | [中文说明](#中文说明)

---

## English Summary

**Manuscript Reference:** Figure 3 (Main Text, Section 4)  
**Figure Title:** *Efficacy synthesis and endpoint discordance across pivotal phase III randomised controlled trials.*  
**Production Artwork:** `figures/Figure3_Phase3_RCT_Efficacy_and_Crossover_Regression.{tif,pdf,png,eps}` (and `figures/Fig3.*`)  
**Print Specifications:** Standard double-column width (180.0 mm), height 145.0 mm, 500 DPI LZW TIFF, Vector Cairo PDF, Vector EPS.

### Panels:
- **Panel A (Progression-Free Survival Forest Plot):** Synthesis of hazard ratios and 95% confidence intervals across all 7 pivotal phase III RCTs. All direct RAS inhibitor regimens demonstrate statistically significant PFS prolongations (HR range 0.42 to 0.66).
- **Panel B (Overall Survival Forest Plot):** Striking divergence in OS outcomes. Second-line NSCLC monotherapies show hazard ratios clustered near unity (1.01 and 0.98), whereas RASolute 302 in PDAC exhibits an unconfounded OS benefit (HR 0.40, 95% CI 0.31–0.52, p < 0.0001).
- **Panel C (Crossover Confounding Meta-Regression):** Linear regression correlating control-arm effective crossover rate to observed OS hazard ratio across direct RAS trials ($R^2 = 0.88, p = 0.005$). Trials with restricted crossover (<5%, RASolute 302, Krascendo 1) achieved clean OS benefit, while trials with high crossover (30%–35%, CodeBreaK 200, KRYSTAL-12) diluted the observed OS HR toward 1.0.

### Data Sources & Methodology:
- **Data Source:** Primary efficacy endpoints from the 7 pivotal phase III RCTs database:
  - Blinded Independent Central Review (BICR) PFS hazard ratios, 95% confidence intervals, and p-values
  - Overall survival hazard ratios and 95% confidence intervals
  - Post-progression effective crossover percentages (%) to direct RAS or targeted therapies in the control arm
  - Weighted least squares (WLS) linear meta-regression model ($R^2 = 0.88, p = 0.005$) quantifying crossover dilution.
- **Data Cutoff Date:** 18 November 2026.
- **Software & Packages Used:**
  - **R (>= 4.3.0 / 4.4.0):**
    - `ggplot2` (>= 3.5.0): Multi-tier forest plot and scatterplot regression visualization
    - `patchwork` (>= 1.2.0): Alignment of Forest plots (Panels A & B) with meta-regression (Panel C)
    - `ggrepel` (>= 0.9.5): Repulsive label positioning ensuring zero trial label overlap
    - `scales` (>= 1.3.0): Logarithmic transformation for Hazard Ratios and percentage scaling
    - `dplyr` (>= 1.1.4): Statistical calculation of confidence limits and error bars
  - **Python (>= 3.10):** `scipy.stats` (>= 1.12.0) for independent verification of weighted linear regression coefficients.

### Data Files (`data/`):
- `phase3_rct_outcomes_crossover.csv` (Trial IDs, hazard ratios, 95% CIs, p-values, crossover percentages)

### How to Reproduce:
```bash
Rscript code/run_figure3_forest_regression.R
```

---

## 中文说明

**论文对应编号：** 图 3（正文第四节）  
**图件标题：** 关键III期随机对照试验的疗效综合分析与交叉用药元回归  
**高清印刷文件：** `figures/Figure3_Phase3_RCT_Efficacy_and_Crossover_Regression.{tif,pdf,png,eps}`（提交简名 `figures/Fig3.*`）  

### 图件核心方法学与科学价值：
1. **A 与 B 面板森林图：** 对比全部 7 项 III 期 RCT 的无进展生存期（PFS）与总生存期（OS）风险比（HR）。直观展示靶向治疗普遍带来稳健的疾病控制与 PFS 获益，但在 OS 上呈现显著异质性。
2. **C 面板元回归模型：** 创新性地建立对照组交叉用药率与所观察到的 OS HR 之间的定量线性回归模型。量化证明对照组高交叉率（30%–35%）如何显著延长对照组后线生存，从而在数学上将 OS HR 压缩并稀释至 1.0 附近，解释了 FDA 审评中的核心争议。
