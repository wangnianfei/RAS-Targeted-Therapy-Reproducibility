# Figure 2 — RAS mutation prevalence and KRAS allele spectrum in a clinical sequencing cohort

Data: MSK-IMPACT cohort (Zehir et al., *Nat Med* 2017; 10,945 samples), exported from cBioPortal. Only missense mutations are counted; the denominator is all sequenced samples of each tumour type. Pancreatic cancer is restricted to pancreatic adenocarcinoma (cBioPortal detailed cancer type; 384 of 502 pancreatic samples), because the broader pancreatic group also contains neuroendocrine, acinar-cell and other tumours, which lowered the apparent *KRAS* rate to 73.5% in earlier versions.

**a,** Percentage of samples with a *KRAS*, *NRAS* or *HRAS* missense mutation: pancreatic adenocarcinoma (n = 384) *KRAS* 90.4%; colorectal (1,007) *KRAS* 43.1%; NSCLC (1,668) *KRAS* 26.9%; endometrial (218) *KRAS* 19.3%; melanoma (365) *NRAS* 21.4%; thyroid (231) *NRAS* 16.0%; bladder (423) *KRAS* 6.6%, *HRAS* 4.3%.
**b,** KRAS missense mutations by allele: pancreatic adenocarcinoma (351 mutations) G12D 41.3%, G12V 32.8%, G12R 13.4%, G12C 2.0%; colorectal (443) G12D 27.5%, G12V 19.6%, G13D 17.2%; NSCLC (456) G12C 43.0%, G12V 14.7%, G12D 13.4%.

Layout: **a** is a bubble matrix (circle area proportional to the percentage, value printed in every cell, n = samples); **b** uses 100% bars with the share printed in each segment of 6% or more (n = mutations).

| File | Role |
|:---|:---|
| `data/cbioportal_mutations.json`, `data/cbioportal_sample_cancertype.json`, `data/cbioportal_sample_cancertype_detailed.json` | cBioPortal export |
| `code/derive_figure2_data.py` | → `data/pancancer_isoform_frequencies.csv`, `data/kras_allele_frequencies.csv`, `data/cohort_ras_rates.csv` (whole cohort: 17.8% of samples carry a RAS missense mutation) |
| `code/tcga_ras_rate.py` | → `data/tcga_pancan_ras_rate.csv` (TCGA PanCancer Atlas, 10.7%; queries the cBioPortal API, needs internet) |
| `code/run_figure2.R` | → `figures/Fig2.*` and `figures/Figure2_RAS_Prevalence_and_KRAS_Alleles.*` |

```bash
python3 02_Figure2_PanCancer_Landscape/code/derive_figure2_data.py
Rscript 02_Figure2_PanCancer_Landscape/code/run_figure2.R
```

**中文：** 数据来自 MSK-IMPACT 队列（cBioPortal 导出），仅统计错义突变，分母为该瘤种全部测序样本。胰腺癌仅取胰腺导管腺癌（详细癌种分类，502 例中的 384 例）；此前把神经内分泌瘤等非导管肿瘤一并计入，使 KRAS 突变率显示为 73.5%。a 为七个瘤种 RAS 突变率，b 为三个瘤种 KRAS 等位基因构成。
