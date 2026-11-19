# Table 1: Methodological Architecture & Clinical Endpoints Across 7 Pivotal Phase III RCTs

[English](./README.md) | [中文说明](#中文说明)

---

## English Summary

**Manuscript Reference:** Table 1 (Main Text, Section 4, Landscape Single-Page Table)  
**Table Title:** *Methodological architecture and clinical efficacy endpoints across seven pivotal phase III randomised controlled trials of direct RAS and downstream pathway inhibitors in solid tumours.*  
**Data Freeze Date:** 18 November 2026.

### Summary of Pivotal Trials:
1. **CodeBreaK 200 (Lancet 2023):** Sotorasib vs docetaxel in 2L+ *KRAS* G12C NSCLC (N=345). PFS HR 0.66 (p=0.0017); OS HR 1.01 (confounded by 34% crossover). Prompted FDA ODAC 10:2 rejection of regular approval.
2. **KRYSTAL-12 (Lancet 2025):** Adagrasib vs docetaxel in 2L+ *KRAS* G12C NSCLC (N=453). PFS HR 0.58 (p<0.0001); OS HR 0.98 (confounded by 29% salvage); established superior CNS efficacy (intracranial ORR 24% vs 11%, HR 0.55).
3. **Krascendo 1 (ESMO 2026):** Divarasib vs sotorasib active comparator in 2L+ *KRAS* G12C NSCLC (N=338). PFS HR 0.64 (p=0.001); OS HR 0.73 (p=0.038). First trial showing statistically significant OS superiority over targeted comparator with strict crossover prohibition.
4. **CodeBreaK 300 (NEJM 2023 / JCO 2025):** Sotorasib + panitumumab vs investigator's choice chemotherapy in 3L mCRC (N=160). PFS HR 0.49 (p=0.006); OS HR 0.70 (p=0.20). Proved clinical rationale of vertical EGFR+KRAS co-blockade in colorectal cancer.
5. **KRYSTAL-10 (Ann Oncol 2026):** Adagrasib + cetuximab vs standard doublet chemotherapy + bevacizumab in 2L mCRC (N=430). PFS HR 0.89 (BICR); OS HR 0.94 (p=0.62). Confirmatory study failed; FDA accelerated approval formally withdrawn on September 1, 2026.
6. **RASolute 302 (NEJM 2026):** Daraxonrasib (RMC-6236, multi-RAS tri-complex inhibitor) vs chemotherapy in 2L+ metastatic PDAC (N=500). PFS HR 0.42 (p<0.0001); OS HR 0.40 (13.2 vs 6.7 mo, p<0.0001). Granted regular approval by FDA and positive CHMP opinion by EMA.
7. **NEMO (Lancet Oncol 2017):** Binimetinib (MEKi) vs dacarbazine in *NRAS*-mutant melanoma (N=402). PFS HR 0.62 (p<0.001); OS HR 1.00 (p=0.999). Historical pathway benchmark demonstrating limitations of single-agent MEK inhibition.

### Data Files (`data/`):
- `table1_pivotal_phase3_trials.csv` (Full dataset)
- `table1_pivotal_phase3_trials_en.csv` (English formatted)
- `table1_pivotal_phase3_trials.md` (Markdown format)

### How to Verify:
```bash
python3 code/build_table1.py
```

---

## 中文说明

**论文对应编号：** 表 1（正文第四节，整版横向展示）  
**表格标题：** 靶向RAS通路及下游分子的7项关键III期随机对照试验方法学与临床终点汇总  
**数据检索截止日期：** 2026 年 11 月 18 日。

### 核心临床启示：
- **肺癌二线单药终点分离：** CodeBreaK 200 与 KRYSTAL-12 均获得显著 PFS 获益，但总生存（OS）均无统计学差异（HR 0.98–1.01），这主要受到对照组 30%–35% 后续交叉使用靶向药的混杂稀释。
- **结直肠癌二线加速批准撤销：** KRYSTAL-10 试验中阿达格拉西布联合西妥昔单抗未能在 OS 上战胜含贝伐珠单抗的标准二线双药化疗，导致美国 FDA 于 2026 年 9 月 1 日正式撤销其加速批准，表明单纯双靶难以撼动二线强化化疗基石。
- **胰腺癌多RAS三元复合物重大突破：** RASolute 302 首次证实达拉索拉西布（RMC-6236）在经治晚期胰腺癌中使 OS 实现翻倍（13.2 对 6.7 个月，HR 0.40，P<0.0001），于 2026 年 8 月获 FDA 常规批准。
