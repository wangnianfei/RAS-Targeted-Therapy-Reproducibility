# Figure 3 — PFS and OS hazard ratios in seven phase III trials

Descriptive forest plots (log scale) of PFS (left) and OS (right) hazard ratios with 95% CIs, in one figure without panel letters (each block is headed by its endpoint); each row names its comparator. KRYSTAL-12 OS is shown as immature at the primary report. No pooled estimate or regression is calculated. Layout: one table-forest with PFS and OS side by side; colour = tumour type, filled square = 95% CI excludes 1, open = includes 1, square area proportional to n.

| File | Role |
|:---|:---|
| `data/phase3_rct_outcomes.csv` | HRs, CIs and the source (with DOI) of each row |
| `code/run_figure3_forest.R` | → `figures/Fig3.*` and `figures/Figure3_Phase3_RCT_PFS_OS_Forest.*` |

```bash
Rscript 04_Figure3_Phase3_Efficacy_Discordance/code/run_figure3_forest.R
```

**中文：** 图 3 为七项试验 PFS（左）与 OS（右）风险比的描述性森林图，不分 a/b 面板，各以终点名称标示；不做合并或回归；原版的"交叉用药–OS 回归"面板因样本少、数据无出处已删除。
