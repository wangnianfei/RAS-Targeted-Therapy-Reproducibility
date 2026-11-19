# Methods, data sources and software

This file describes how each figure and table of the review was produced. Every number below can be recomputed from the files in this repository unless stated otherwise. Data cut-off: **18 November 2026**.

## Figure 1 — crystal structures

- **Data:** RCSB Protein Data Bank entries 6OIM (KRAS G12C covalently bound to sotorasib, GDP) and 9BG6 (daraxonrasib–cyclophilin A–KRAS G12V tri-complex with GMPPNP; Cregg et al., *J Med Chem* 2025). Coordinates are in `01_Figure1_Structural_Mechanisms/data/`.
- **Method:** PyMOL (`code/render_figure1_pymol.py`) renders both structures. In 9BG6, chains B and D (the second copy of the complex) are removed and KRAS chain A is superposed onto KRAS in 6OIM so that both panels share one orientation. `code/run_figure1.py` trims the renders with ImageMagick and composes the figure with matplotlib.

## Figure 2 — RAS mutation prevalence and KRAS alleles

- **Data:** MSK-IMPACT clinical sequencing cohort (Zehir et al., *Nat Med* 2017; 10,945 tumour samples), exported from cBioPortal (`data/cbioportal_mutations.json`, `data/cbioportal_sample_cancertype.json`).
- **Method:** `code/derive_figure2_data.py` counts samples with at least one *KRAS*, *NRAS* or *HRAS* **missense** mutation in seven tumour types (denominator: all sequenced samples of that type) and the distribution of KRAS missense mutations by allele (G12C, G12D, G12V, G12R, G13D, any Q61, other) in pancreatic cancer, colorectal cancer and NSCLC. Output: `pancancer_isoform_frequencies.csv`, `kras_allele_frequencies.csv`. `code/run_figure2.R` draws the two panels.
- **Note:** tissue-based panel sequencing gives a lower *KRAS* prevalence in pancreatic cancer (73.5%) than the ~90% usually quoted, probably because of low tumour cellularity; the manuscript states this.

## Table 1 — seven phase III trials

- **Data:** CodeBreaK 200 (de Langen, *Lancet* 2023), KRYSTAL-12 (Barlesi, *Lancet* 2025), Krascendo 1 (Skoulidis, *N Engl J Med* 2026), CodeBreaK 300 (Fakih, *N Engl J Med* 2023), KRYSTAL-10 (Tabernero, *Ann Oncol* 2026, LBA1), RASolute 302 (O'Reilly, *N Engl J Med* 2026) and NEMO (Dummer, *Lancet Oncol* 2017). Values were extracted from the primary publications.
- **Files:** `data/table1_pivotal_phase3_trials.csv` is extracted from the submitted manuscript; `code/build_table1.py` writes the Markdown version. Discontinuation values for Krascendo 1 and KRYSTAL-10 (treatment-related) come from conference coverage of the primary presentations.

## Figure 3 — forest plots

- **Data:** `data/phase3_rct_outcomes.csv` lists the PFS and OS hazard ratios with 95% CIs and the source of each row. KRYSTAL-12 OS is shown as immature.
- **Method:** `code/run_figure3_forest.R` draws descriptive forest plots (log scale). No pooling or meta-regression is performed; an earlier crossover-versus-OS regression panel was removed because it rested on six heterogeneous trials, one with an active comparator, and on crossover values that could not be sourced.

## Figure 4 — registered trials

- **Harvest** (`code/fetch_ctgov.py`): ClinicalTrials.gov API v2, two sweeps combined and de-duplicated by NCT number — (A) gene and biomarker terms (*KRAS*, *NRAS*, *HRAS*, specific alleles, "RAS mutation", "RAS wild-type" and related phrases) and (B) names and codes of RAS-directed and RAS-regulator agents. The query text, eligibility criteria, keywords and outcome fields are searched.
- **Curation** (`code/curate_trials.py`): explicit rules keep interventional oncology trials of phase 1–3 that mention a RAS gene or a RAS-directed agent, and assign each trial one relation to RAS: **RAS-targeted** (a RAS-directed agent is an intervention; n = 358), **RAS-regulator-targeted** (SHP2, SOS1 or farnesyltransferase strategies; n = 134), **RAS-biomarker-selected** (RAS status used for eligibility or stratification; n = 639) or **RAS-mentioned** (n = 51). Excluded records are written out with the reason. Both scripts were written for the original project layout; the raw API payloads and the exclusion log are not included in this repository.
- **Figure** (`code/run_figure4_trial_landscape.R`, input `data/trials_1182.csv`): the 358 RAS-targeted trials by phase (phase 2/3 grouped with phase 3), principal drug class (trials covering several classes assigned in the order KRAS G12C > KRAS G12D > multi-RAS(ON)/pan-RAS > vaccine/TCR-T) split by whether more than one intervention is registered, and by region (a trial counts once in every region in which it has a site).

## Figure 5 and Supplementary Figure S1 — resistance

- **Figure 5** (`code/run_figure5.py`) is a schematic. The resistance alterations shown are those reported in 38 patients with acquired resistance to adagrasib (Awad et al., *N Engl J Med* 2021); adaptive EGFR feedback in colorectal cancer is from Amodio et al. (*Cancer Discov* 2020). Strategies follow Section 5.3 of the manuscript.
- **Figure S1** (`code/run_figureS1_resistance_matrix.py`): panel a maps the seven resistance classes of Table S3 to six strategies (a qualitative summary of the review, not new data); panel b shows 17/38 patients with at least one putative mechanism, 7/38 with multiple mechanisms and 2/9 lung adenocarcinomas with squamous transformation (Awad et al. 2021).
- **Tables S1 and S3** are stored as `data/tableS1_direct_ras_inhibitors.csv` and `data/tableS3_resistance_mechanisms.csv`; bracketed numbers refer to the main-text reference list. Clinical status is from ClinicalTrials.gov and regulatory records at the cut-off date.

## Software

| Tool | Used for |
|:---|:---|
| Python ≥ 3.10, matplotlib ≥ 3.8 | Figures 1 (composition), 5 and S1; data derivation for Figure 2; Table 1 export |
| R ≥ 4.3: ggplot2, patchwork, dplyr, tidyr, scales, ggtext, ragg | Figures 2, 3 and 4 |
| PyMOL (open-source) ≥ 2.5 | Figure 1 structure renders |
| ImageMagick ≥ 7.1 | Trimming renders; 500-dpi LZW TIFF export |

Figures are 180 mm wide (double column), set in Arial, and exported as 500-dpi LZW TIFF, vector PDF (and EPS for the R figures) and PNG.
