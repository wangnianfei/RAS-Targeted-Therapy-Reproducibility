# Methods, data sources and software

This file describes how each figure and table of the review was produced. Every number below can be recomputed from the files in this repository unless stated otherwise. Data cut-off: **18 November 2026**.

## Figure 1 — crystal structures

- **Data:** RCSB Protein Data Bank entries 6OIM (KRAS G12C covalently bound to sotorasib, GDP) and 9BG6 (daraxonrasib–cyclophilin A–KRAS G12V tri-complex with GMPPNP; Cregg et al., *J Med Chem* 2025). Coordinates are in `01_Figure1_Structural_Mechanisms/data/`.
- **Method:** PyMOL (`code/render_figure1_pymol.py`) renders both structures. In 9BG6, chains B and D (the second copy of the complex) are removed and KRAS chain A is superposed onto KRAS in 6OIM so that both panels share one orientation. `code/run_figure1.py` trims the renders with ImageMagick and composes the figure with matplotlib.

## Figure 2 — RAS mutation prevalence and KRAS alleles

- **Data:** MSK-IMPACT clinical sequencing cohort (Zehir et al., *Nat Med* 2017; 10,945 tumour samples), exported from cBioPortal (`data/cbioportal_mutations.json`, `data/cbioportal_sample_cancertype.json`, `data/cbioportal_sample_cancertype_detailed.json`).
- **Method:** `code/derive_figure2_data.py` counts samples with at least one *KRAS*, *NRAS* or *HRAS* **missense** mutation in seven tumour types (denominator: all sequenced samples of that type) and the distribution of KRAS missense mutations by allele (G12C, G12D, G12V, G12R, G13D, any Q61, other) in pancreatic cancer, colorectal cancer and NSCLC. Output: `pancancer_isoform_frequencies.csv`, `kras_allele_frequencies.csv`. `code/run_figure2.R` draws the two panels.
- **Note:** pancreatic cancer is restricted to pancreatic adenocarcinoma (384 samples; *KRAS* 90.4%, matching the 90% reported by Zehir et al.). Earlier versions used the whole pancreatic group (502 samples, including neuroendocrine and acinar-cell tumours) and showed 73.5%, which the text wrongly attributed to low tumour cellularity. The cohort-wide RAS missense rate (17.8%) is written to `cohort_ras_rates.csv`; the TCGA PanCancer Atlas rate quoted in Section 2.2 (10.7% of 10,967 samples) comes from `code/tcga_ras_rate.py`.

## Table 1 — seven phase III trials

- **Data:** CodeBreaK 200 (de Langen, *Lancet* 2023), KRYSTAL-12 (Barlesi, *Lancet* 2025), Krascendo 1 (Skoulidis, *N Engl J Med* 2026), CodeBreaK 300 (Fakih, *N Engl J Med* 2023), KRYSTAL-10 (Tabernero, *Ann Oncol* 2026, LBA1), RASolute 302 (O'Reilly, *N Engl J Med* 2026) and NEMO (Dummer, *Lancet Oncol* 2017). Values were extracted from the primary publications.
- **Files:** `data/table1_pivotal_phase3_trials.csv` is extracted from the submitted manuscript; `code/build_table1.py` writes the Markdown version. Discontinuation values for Krascendo 1 and KRYSTAL-10 (treatment-related) come from conference coverage of the primary presentations.

## Figure 3 — forest plots

- **Data:** `data/phase3_rct_outcomes.csv` lists the PFS and OS hazard ratios with 95% CIs and the source of each row. KRYSTAL-12 OS is shown as immature.
- **Method:** `code/run_figure3_forest.R` draws descriptive forest plots (log scale). No pooling or meta-regression is performed; an earlier crossover-versus-OS regression panel was removed because it rested on six heterogeneous trials, one with an active comparator, and on crossover values that could not be sourced.

## Supplementary Figure S2 — registered trials (Figure 4 in the first submission)

- **Harvest** (`code/fetch_ctgov.py`): ClinicalTrials.gov API v2, two sweeps combined and de-duplicated by NCT number — (A) gene and biomarker terms (*KRAS*, *NRAS*, *HRAS*, specific alleles, "RAS mutation", "RAS wild-type" and related phrases) and (B) names and codes of RAS-directed and RAS-regulator agents. The query text, eligibility criteria, keywords and outcome fields are searched.
- **Curation** (`code/curate_trials.py`): explicit rules keep interventional oncology trials of phase 1–3 that mention a RAS gene or a RAS-directed agent, and assign each trial one relation to RAS: **RAS-targeted**, **RAS-regulator-targeted** (SHP2, SOS1 or farnesyltransferase strategies), **RAS-biomarker-selected** (RAS status used for eligibility or stratification) or **RAS-mentioned**; the output is `data/trials_1182.csv` (1,182 records). Excluded records are written out with the reason. Both scripts were written for the original project layout; the raw API payloads and the exclusion log are not included in this repository.
- **Record-level review** (`code/apply_classification_corrections.py`): the rules match agent names anywhere in a record (including eligibility text) and know RAS-directed agents only from a name list, so every RAS-targeted trial whose interventions did not name a listed agent, and every other trial whose title or interventions suggested a RAS-directed agent, was checked against the registry intervention description. A second round (20 November 2026) re-checked the mechanism of every agent in the RAS-targeted tier against the registry, sponsor or NCI Drug Dictionary descriptions and swept all other tiers for unlisted RAS inhibitors. A trial counts as RAS-targeted only if a registered intervention acts on the RAS protein or transcript (allele-selective, multi-selective or pan-RAS inhibitors and degraders, RAS-directed conjugates, RAS siRNA, vaccines, TCR-T cells or T-cell engagers against mutant RAS); upstream (SHP2, SOS1, farnesyltransferase) and downstream (RAF, MEK, ERK) inhibitors count only when combined with a direct RAS inhibitor, and multi-antigen vaccine regimens in which RAS is one of several antigens and patients are not RAS-selected do not count. `data/classification_corrections.csv` lists each change with its reason: 31 records removed as not oncology trials in patients with cancer (23 healthy-volunteer or organ-impairment pharmacology studies, 8 non-oncology studies) and 80 reclassified (45 into and 26 out of the RAS-targeted tier, 8 drug-class labels, and one SHP2 inhibitor moved to the regulator tier). Output: `data/trials_curated.csv` (1,151 trials: RAS-targeted 355, RAS-regulator-targeted 129, RAS-biomarker-selected 605, RAS-mentioned 62) and `data/trials_excluded_on_review.csv`. `code/summarise_trials.py` prints every number in Section 5.1 and the Supplementary Methods.
- **Figure** (`code/run_figureS2_trial_landscape.R`, input `data/trials_curated.csv`): the 353 RAS-targeted trials in solid tumours (the two trials in haematological malignancies excluded; no RAS-targeted trial enrolled both solid and haematological malignancies) by phase (phase 2/3 grouped with phase 3), principal drug class (trials covering several classes assigned in the order KRAS G12C > KRAS G12D > multi-RAS(ON)/pan-RAS > vaccine/TCR-T) split by whether more than one intervention is registered, and by region (a trial counts once in every region in which it has a site).

## Figure 4 and Supplementary Figure S1 — resistance

- **Figure 4** (Figure 5 in the first submission) is a schematic drawn by the authors in graphics software and edited with AI assistance; it is not regenerated by code. The resistance alterations shown are those reported in 38 patients with acquired resistance to adagrasib (Awad et al., *N Engl J Med* 2021); adaptive EGFR feedback in colorectal cancer is from Amodio et al. (*Cancer Discov* 2020). Strategies follow Section 5.3 of the manuscript. The histological-transformation label reads 2/10 repeat tissue biopsies (corrected from 2/9).
- **Figure S1** (`code/run_figureS1_resistance_matrix.py`): panel a maps the seven resistance classes of Table S3 to six strategies (a qualitative summary of the review, not new data); panel b shows 17/38 patients with at least one putative mechanism, 7/38 with multiple mechanisms and squamous transformation in 2 of the 10 patients with a repeat tissue biopsy (Awad et al. 2021).
- **Tables S1 and S3** are stored as `data/tableS1_direct_ras_inhibitors.csv` and `data/tableS3_resistance_mechanisms.csv`; bracketed numbers refer to the main-text reference list. Clinical status is from ClinicalTrials.gov and regulatory records at the cut-off date.

## Software

| Tool | Used for |
|:---|:---|
| Python ≥ 3.10, matplotlib ≥ 3.8 | Figures 1 (composition), 5 and S1; data derivation for Figure 2; Table 1 export |
| R ≥ 4.3: ggplot2, patchwork, dplyr, tidyr, scales, ggtext, ragg, maps | Figures 2, 3 and 4 |
| PyMOL (open-source) ≥ 2.5 | Figure 1 structure renders |
| ImageMagick ≥ 7.1 | Trimming renders; 500-dpi LZW TIFF export |

Figures are 180 mm wide (double column), set in Arial, and exported as 500-dpi LZW TIFF, vector PDF (and EPS for the R figures) and PNG.
