# Supplementary Material — Figure S1 and Tables S1–S3

| Item | Content | Source file |
|:---|:---|:---|
| Figure S1 | **a,** seven resistance classes of Table S3 × six strategies (qualitative summary); **b,** 17/38 patients with ≥1 putative mechanism, 7/38 with multiple, 2/9 lung adenocarcinomas with squamous transformation after adagrasib (Awad et al. 2021) | `code/run_figureS1_resistance_matrix.py` → `figures/FigS1.*` |
| Table S1 | Direct RAS inhibitors by mechanistic class (Section 3.2) and targeted degraders: target, developer, status on 18 November 2026 | `data/tableS1_direct_ras_inhibitors.csv` |
| Table S2 | Regulatory approvals and confirmatory-trial outcomes | `data/tableS2_global_regulatory_approvals.md` |
| Table S3 | Resistance mechanisms with frequencies from Awad 2021 and Zhao 2021, and registered combination regimens (NCT numbers) | `data/tableS3_resistance_mechanisms.csv` |

`code/build_supplementary_tables.py` prints Tables S1 and S3 from the CSV files. The appendix itself is `RAS_Targeted_Therapy_Review_Supplementary_Appendix.{docx,pdf,md}`. Bracketed numbers refer to the main-text reference list.

**中文：** 附图 S1 与附表 S1–S3。附表 S1、S3 以 CSV 为数据源，耐药频率仅取自 Awad 2021 与 Zhao 2021，在研方案均给出 NCT 编号。
