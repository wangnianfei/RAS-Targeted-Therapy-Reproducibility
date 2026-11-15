# Table 2: Key Phase III Randomized Controlled Trials of RAS Pathway-Directed Therapies
# 表 2: 靶向RAS通路的7项关键III期随机对照临床试验汇总

## 1. 论文对应位置 (Manuscript Location)
- **章节**: 第 4.0 节 “RAS 靶向治疗的临床研究证据与关键随机对照试验解读”
- **页码与段落**: 正文 P460 引出表 2。

## 2. 表格内容与关键随机对照试验汇总 (Pivotal RCT Evidence)
本表系统汇总了全球已报告或完成的 7 项关键 III 期随机对照临床试验（RCTs）：
1. **CodeBreaK 200 (NCT04303780)**: 
   - 经治 *KRAS* G12C NSCLC (N=345)
   - Sotorasib 960 mg qd vs 多西他赛
   - PFS 显著改善：5.6 vs 4.5 个月（HR 0.66, 95% CI 0.51–0.86, P=0.0017）
   - OS 无显著差异：10.6 vs 11.3 个月（HR 1.01, 95% CI 0.77–1.33），主因 34% 方案内交叉治疗及对照组高比例后续靶向治疗稀释。
2. **KRYSTAL-12 (NCT04685135)**:
   - 经治 *KRAS* G12C NSCLC (N=453)
   - Adagrasib 600 mg bid vs 多西他赛
   - PFS 显著获益：5.5 vs 3.8 个月（HR 0.58, 95% CI 0.45–0.76, P<0.0001），颅内 ORR 达 24%，中位颅内 PFS 6.0 个月
   - OS 同样去偶联：10.4 vs 10.8 个月（HR 0.99），对照组后续商业化使用 G12C 抑制剂比例达 39%。
3. **Krascendo 1 (NCT05737719)**:
   - 经治 *KRAS* G12C NSCLC (N=580)
   - Divarasib 400 mg qd vs Sotorasib/Adagrasib（首个阳性对照 III 期头对头）
   - 取得双重统计学突破：PFS 9.8 vs 5.7 个月（HR 0.58, P<0.0001）；OS 17.7 vs 12.0 个月（HR 0.56, P=0.0005）；ORR 58.4% vs 32.3%。
4. **CodeBreaK 300 (NCT05198934)**:
   - 化疗难治性 *KRAS* G12C 结直肠癌 (N=160)
   - Sotorasib 960 mg + 帕尼单抗 vs Sotorasib 240 mg + 帕尼单抗 vs 瑞戈非尼/TAS-102
   - PFS: 5.6 vs 3.9 vs 2.2 个月（960mg组 HR 0.49, P=0.006）；OS 虽未达显著但呈积极获益趋势（11.9 vs 10.3 个月，HR 0.70）；试验禁止交叉治疗，支持 FDA 常规批准。
5. **KRYSTAL-10 (NCT04793425)**:
   - 二线 *KRAS* G12C 结直肠癌 (N=482)
   - Adagrasib + 西妥昔单抗 vs FOLFIRI/mFOLFOX6 + 贝伐珠单抗
   - 未达到双重主要终点：PFS 7.5 vs 8.1 个月（HR 0.89, P=0.32）；OS 21.6 vs 21.7 个月（HR 0.83, P=0.09），加速批准于 2026-09 撤回。
6. **RASolute 302 (NCT06389773)**:
   - 经治 *RAS* 突变胰腺导管腺癌 (N=468)
   - Daraxonrasib (RMC-6236) vs 医师选择化疗 (吉西他滨/白蛋白紫杉醇或5-FU方案)
   - 压倒性生存优势：PFS 7.2 vs 3.6 个月（HR 0.49, P<0.001）；OS 13.2 vs 6.7 个月（HR 0.40, 95% CI 0.30–0.53, P=4.6×10^-11），死亡风险降低 60%，获 FDA 常规批准。
7. **NEMO (NCT01763164)**:
   - 初治或免疫经治 *NRAS* 突变黑色素瘤 (N=402)
   - 比美替尼 (Binimetinib, MEK 抑制剂) 45 mg bid vs 达卡巴嗪
   - PFS: 2.8 vs 1.5 个月（HR 0.62, P<0.001）；OS 无显著差异（11.0 vs 10.1 个月，HR 1.00），主因进展后广泛接受免疫治疗。

## 3. 数据来源、检索策略与截止日期 (Data Sources & Cut-off Dates)
- **数据来源**: ClinicalTrials.gov, PubMed, ASCO/ESMO/AACR 官网口头报告，《新英格兰医学杂志》(NEJM)、《柳叶刀》(Lancet)、《临床肿瘤学杂志》(JCO) 正文发表论文。
- **检索策略**: `("RAS" OR "KRAS" OR "NRAS") AND ("Phase 3" OR "randomized controlled trial") AND ("solid tumors" OR "NSCLC" OR "colorectal" OR "pancreatic" OR "melanoma")`。
- **数据截止日期**: **2026年10月31日**。

## 4. 文件结构 (Files in this Folder)
```text
├── README.md                      # 本说明文档
├── data/
│   ├── table2_pivotal_phase3_trials.csv       # 7 项 III 期试验核心数据表
│   ├── Table3_key_clinical_studies.md         # 试验设计、入排与终点元数据
│   └── toxicity_summary_20261114.md           # 毒性与不良反应汇总表
└── code/
    └── build_table2.py            # 表格构建与终点分析校验脚本 (Python)
```

## 5. 复现与校验指令 (How to Reproduce)
在当前目录下运行：
```bash
python3 code/build_table2.py
```
