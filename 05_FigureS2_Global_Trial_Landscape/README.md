# Supplementary Figure S2 — Registered interventional trials of directly RAS-targeted agents

`data/trials_1182.csv` is the rule-based output of `code/curate_trials.py`: 1,182 RAS-related interventional oncology trials from ClinicalTrials.gov (cut-off 18 November 2026), each classified by its relation to RAS. A record-level review in two rounds (`code/apply_classification_corrections.py`, decisions and reasons in `data/classification_corrections.csv`) removed 31 records that were not oncology trials in patients with cancer and corrected the classification of 80 trials. The second round checked the mechanism of every agent in the RAS-targeted tier against registry, sponsor or NCI Drug Dictionary descriptions and swept the other tiers for unlisted RAS inhibitors:

- **Counted as RAS-targeted:** a registered intervention acts on the RAS protein or its transcript (allele-selective, multi-selective or pan-RAS inhibitors and degraders, RAS-directed conjugates, RAS siRNA, vaccines, TCR-T cells or T-cell engagers against mutant RAS).
- **Not counted:** inhibitors acting upstream (SHP2, SOS1, farnesyltransferase) or downstream (RAF, MEK, ERK) of RAS unless combined with a direct RAS inhibitor; multi-antigen vaccine regimens in which RAS is one of several antigens and patients are not RAS-selected (17 NANT trials); trials in haematological malignancies.
- **Round-2 changes:** four pan-KRAS/pan-RAS inhibitor trials added (KST-6051, JYP0015, PF-07985045, PF-07934040); ZG2001 (a SOS1 inhibitor) moved to the regulator tier; the 17 NANT multi-antigen trials moved out; salirasib relabelled.

The resulting `data/trials_curated.csv` holds 1,151 trials: RAS-targeted 355, RAS-regulator-targeted 129 (SHP2, SOS1 or farnesyltransferase), RAS-biomarker-selected 605 and RAS-mentioned 62. The figure shows the 353 RAS-targeted trials in solid tumours (the two trials in haematological malignancies excluded; no RAS-targeted trial enrolled both):

- **a,** by phase: phase 1, 136 (incl. four early phase 1); phase 1/2, 88; phase 2, 86; phase 2/3 or 3, 43.
- **b,** by principal drug class (KRAS G12C 201, KRAS G12D 60, vaccine/TCR-T 40, multi-RAS(ON)/pan-RAS 39; 13 other trials not shown), split by whether more than one intervention is registered (registered interventions include control-arm agents).
- **c,** world map of trials with at least one site in each country or region (65 countries and regions; a trial counts once in every country with a site; map polygons from the R `maps` package) with the 12 countries and regions with most trials, and regional totals: North America 202, East Asia 188, Europe 93, other 80 (a trial counts in every region where it has a site).

Panel letters are lower case (a, b, c), as in all figures and legends of the manuscript. All three panels use one blue scale: the map and the top-12 bars continue the phase colours of panel a (darker = more trials), and Supplementary Figure S1 uses the same navy. The panel b legend follows the stacking order of the bars, and the top-12 bars label China as "Mainland China", as in the text (Taiwan and Hong Kong are counted separately).

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

**中文：** `curate_trials.py` 按规则得到 1,182 项 RAS 相关干预性肿瘤试验；两轮逐条复核（`classification_corrections.csv` 逐条列出理由）剔除 31 条非肿瘤患者试验（健康受试者或肝肾功能不全药代研究 23 条、非肿瘤研究 8 条），并更正 80 项试验的分类，得到 1,151 项（`trials_curated.csv`）。第二轮逐一核对 RAS 靶向组每个药物的作用机制：只有直接作用于 RAS 蛋白或其转录本的药物（等位基因选择性、多选择性或 pan-RAS 抑制剂与降解剂、RAS 偶联药物、RAS siRNA、针对突变 RAS 的疫苗/TCR-T/T 细胞衔接器）才计入；RAS 上游（SHP2、SOS1、法尼基转移酶）或下游（RAF、MEK、ERK）抑制剂除非联用直接 RAS 抑制剂否则不计入；RAS 仅为多抗原之一且未按 RAS 突变入组的 NANT 疫苗方案（17 项）不计入；血液肿瘤试验不计入。附图 S2 展示 353 项实体瘤直接靶向 RAS 的试验（分期、药物类别、地区）。
