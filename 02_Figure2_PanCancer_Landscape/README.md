# Figure 2 — RAS mutation prevalence and KRAS allele spectrum in a clinical sequencing cohort

Data: MSK-IMPACT cohort (Zehir et al., *Nat Med* 2017; 10,945 samples), exported from cBioPortal. Only missense mutations are counted; the denominator is all sequenced samples of each tumour type.

**a,** Percentage of samples with a *KRAS*, *NRAS* or *HRAS* missense mutation: pancreatic (n = 502) *KRAS* 73.5%; colorectal (1,007) *KRAS* 43.1%; NSCLC (1,668) *KRAS* 26.9%; endometrial (218) *KRAS* 19.3%; melanoma (365) *NRAS* 21.4%; thyroid (231) *NRAS* 16.0%; bladder (423) *KRAS* 6.6%, *HRAS* 4.3%. Panel sequencing underestimates *KRAS* prevalence in pancreatic cancer (~90% in the literature).
**b,** KRAS missense mutations by allele: pancreatic (373 mutations) G12D 40.2%, G12V 32.7%, G12R 13.4%; colorectal (443) G12D 27.5%, G12V 19.6%, G13D 17.2%; NSCLC (456) G12C 43.0%, G12V 14.7%, G12D 13.4%.

| File | Role |
|:---|:---|
| `data/cbioportal_mutations.json`, `data/cbioportal_sample_cancertype.json` | cBioPortal export |
| `code/derive_figure2_data.py` | → `data/pancancer_isoform_frequencies.csv`, `data/kras_allele_frequencies.csv` |
| `code/run_figure2.R` | → `figures/Fig2.*` and `figures/Figure2_RAS_Prevalence_and_KRAS_Alleles.*` |

```bash
python3 02_Figure2_PanCancer_Landscape/code/derive_figure2_data.py
Rscript 02_Figure2_PanCancer_Landscape/code/run_figure2.R
```

**中文：** 数据来自 MSK-IMPACT 队列（cBioPortal 导出），仅统计错义突变，分母为该瘤种全部测序样本。a 为七个瘤种 RAS 突变率，b 为三个瘤种 KRAS 等位基因构成。
