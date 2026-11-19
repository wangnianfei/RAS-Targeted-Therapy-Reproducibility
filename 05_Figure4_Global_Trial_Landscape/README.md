# Figure 4 — Registered interventional trials of directly RAS-targeted agents

`data/trials_1182.csv` holds 1,182 RAS-related interventional oncology trials from ClinicalTrials.gov (cut-off 18 November 2026), each classified by its relation to RAS: RAS-targeted (358), RAS-regulator-targeted (134, e.g. SHP2 or SOS1), RAS-biomarker-selected (639) and RAS-mentioned (51). The figure shows the 358 RAS-targeted trials:

- **a,** by phase: phase 1, 121 (incl. one early phase 1); phase 1/2, 102; phase 2, 90; phase 2/3 or 3, 45.
- **b,** by principal drug class (KRAS G12C 220, KRAS G12D 52, vaccine/TCR-T 39, multi-RAS(ON)/pan-RAS 33; 14 other trials not shown), split by whether more than one intervention is registered (registered interventions include control-arm agents).
- **c,** trials with at least one site in each region: North America 215, East Asia 166, Europe 92, other 78 (a trial counts in every region where it has a site).

| File | Role |
|:---|:---|
| `data/trials_1182.csv` | Curated trial table (one row per NCT number) |
| `code/run_figure4_trial_landscape.R` | Figure 4 → `figures/Fig4.*` and `figures/Figure4_Global_Clinical_Trial_Atlas_and_Geography.*` |
| `code/fetch_ctgov.py` | Harvest from the ClinicalTrials.gov API v2 (gene/biomarker sweep plus agent sweep) |
| `code/curate_trials.py` | Rule-based inclusion and classification; writes excluded records with reasons |

The harvest and curation scripts were written for the original project layout; the raw API payloads and exclusion log are not included here, so the figure is reproduced from `trials_1182.csv`.

**中文：** 1,182 项 RAS 相关干预性肿瘤试验按与 RAS 的关系分为四类，图 4 只展示其中 358 项直接靶向 RAS 的试验（分期、药物类别、地区）。检索与清洗脚本为规则化流程，原始 API 数据未收录，图由 `trials_1182.csv` 复现。
