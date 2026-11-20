# Supplementary Figure S2 — Registered interventional trials of directly RAS-targeted agents

`data/trials_1182.csv` is the rule-based output of `code/curate_trials.py`: 1,182 RAS-related interventional oncology trials from ClinicalTrials.gov (cut-off 18 November 2026), each classified by its relation to RAS. A record-level review (`code/apply_classification_corrections.py`, decisions and reasons in `data/classification_corrections.csv`) removed 31 records that were not oncology trials in patients with cancer and corrected the classification of 57 trials. The resulting `data/trials_curated.csv` holds 1,151 trials: RAS-targeted 369, RAS-regulator-targeted 130 (e.g. SHP2 or SOS1), RAS-biomarker-selected 607 and RAS-mentioned 45. The figure shows the 367 RAS-targeted trials in solid tumours (two trials restricted to haematological malignancies excluded):

- **a,** by phase: phase 1, 133 (incl. four early phase 1); phase 1/2, 103; phase 2, 88; phase 2/3 or 3, 43.
- **b,** by principal drug class (KRAS G12C 201, KRAS G12D 60, vaccine/TCR-T 57, multi-RAS(ON)/pan-RAS 35; 14 other trials not shown), split by whether more than one intervention is registered (registered interventions include control-arm agents).
- **c,** trials with at least one site in each region: North America 210, East Asia 188, Europe 93, other 80 (a trial counts in every region where it has a site).

| File | Role |
|:---|:---|
| `data/trials_1182.csv` | Rule-based trial table (one row per NCT number), unchanged after curation |
| `data/classification_corrections.csv` | Record-level corrections with reasons (exclusions, tier and class changes) |
| `data/trials_curated.csv` | Analysis corpus (1,151 trials) used for Supplementary Figure S2, Section 5.1 and the Supplementary Methods |
| `data/trials_excluded_on_review.csv` | The 31 records removed on review, with reasons |
| `code/apply_classification_corrections.py` | Applies the corrections; re-derives tumour types from the condition list |
| `code/summarise_trials.py` | Prints every number reported in Section 5.1, the Supplementary Methods and the Supplementary Figure S2 legend |
| `code/run_figureS2_trial_landscape.R` | Supplementary Figure S2 → `figures/FigS2.*` and `figures/FigureS2_Global_Clinical_Trial_Atlas_and_Geography.*` |
| `code/fetch_ctgov.py` | Harvest from the ClinicalTrials.gov API v2 (gene/biomarker sweep plus agent sweep) |
| `code/curate_trials.py` | Rule-based inclusion and classification; writes excluded records with reasons |

The harvest and curation scripts were written for the original project layout; the raw API payloads and the rule-based exclusion log are not included here, so the figure is reproduced from `trials_1182.csv` and the corrections file.

**中文：** `curate_trials.py` 按规则得到 1,182 项 RAS 相关干预性肿瘤试验；逐条复核（`classification_corrections.csv` 逐条列出理由）剔除 31 条非肿瘤患者试验（健康受试者或肝肾功能不全药代研究 23 条、非肿瘤研究 8 条），并更正 57 项试验的分类，得到 1,151 项（`trials_curated.csv`）。图 4 展示其中 367 项实体瘤直接靶向 RAS 的试验（分期、药物类别、地区），2 项仅纳入血液肿瘤的试验除外。
