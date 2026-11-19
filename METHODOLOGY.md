# Methodology, Data Sources, and Software Specifications
# 《RAS靶向治疗综述》方法学、数据来源、检索策略与软件环境全景指南

本综述旨在为全球肿瘤学同道提供一份客观、详实、可精确复现的 RAS 靶向治疗临床与转化研究全景指引。为践行国际最高学术透明度准则（Nature Portfolio, Cell Press, ESMO Open），本研究将论文中涉及的所有图表的原始数据、分析流程、绘图脚本与出版级高分辨率图件全部开源公开。

本文档系统汇总全篇投稿论文（ESMO Open Submission）中**所有 5 幅主图、1 张主表及补充附图附表**的数据来源、检索策略、排除规则、数据冻结截止日期及所使用的软件与计算环境。

---

## 一、 论文图表与方法学全景对照表 (Methodology Matrix)

| 论文编号 | 图表名称 | 对应正文章节 | 原始数据来源 (Data Source) | 数据检索策略与入选标准 | 数据截止日期 | 核心工具与软件环境 | 对应目录 |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **图 1 (Figure 1)** | **RAS核苷酸循环与直接靶向抑制模式** | Section 2 | RCSB PDB: 4OBE, 5VQ2, 4LDJ, 6OIM | 提取高分辨率（≤2.2 Å）单体 Cα 坐标；基于核心 G-domain（残基 1–166）进行三维刚体叠合；计算各残基 Cα 欧氏距离位移；提取 4 大代际抑制剂构象特征 | PDB 沉积版 | Python 3.10+, NumPy, Matplotlib, PyMOL 2.5 (600 dpi 光线追踪表面) | `01_Figure1_Structural_Mechanisms/` |
| **图 2 (Figure 2)** | **RAS突变的泛癌种图谱与共突变分层** | Section 3 | MSK-IMPACT 泛癌种临床测序队列 (10,945 例, PMID: 28481359) | cBioPortal REST API v2 提取晚期实体瘤数据；严格限定非同义/非沉默点突变；分母为该肿瘤测序总样本数；提炼 7 大肿瘤 prevalence、G>T 吸烟颠换指纹及 KP/KL/KEAP1/KC 亚型微环境与治疗 | 队列冻结版 | R 4.3+, ggplot2 3.5, patchwork, scales, ggtext | `02_Figure2_PanCancer_Landscape/` |
| **表 1 (Table 1)** | **7项关键III期RCT方法学与临床终点汇总** | Section 4 | PubMed, ClinicalTrials.gov, ASCO, ESMO, AACR, NEJM, Lancet, JCO | 严格系统性提取 7 项关键 III 期 RCTs（CodeBreaK 200, KRYSTAL-12, Krascendo 1, CodeBreaK 300, KRYSTAL-10, RASolute 302, NEMO）的试验人群、样本量、对照组、交叉方案、随访时间、PFS、OS、ORR、≥3级AEs 及停药率 | 2026年11月18日 | Python 3.10+, Markdown, CSV, python-docx 1.1 | `03_Table1_Pivotal_Phase3_RCTs/` |
| **图 3 (Figure 3)** | **III期RCT疗效综合与交叉用药元回归** | Section 4 | 7项关键III期RCT临床终点数据库 | 提取 PFS 与 OS 风险比（HR）及 95% 置信区间；构建以对照组后线交叉靶向用药比例为自变量、观察到的 OS HR 为因变量的定量线性元回归模型 ($R^2=0.88, p=0.005$) | 2026年11月18日 | R 4.3+, ggplot2, patchwork, ggrepel, scales | `04_Figure3_Phase3_Efficacy_Discordance/` |
| **图 4 (Figure 4)** | **1,182项全球RAS临床试验全景图谱** | Section 5 | ClinicalTrials.gov REST API v2 (`/api/v2/studies`) | 检索获得 3,210 条原始记录，经两轮人工独立双盲筛查：排除心血管 RAAS（1,907 项）、RASopathy（19 项）、非恶性肿瘤（38 项）、非I–III期（54 项）、IV期（10 项），严格纳入 1,182 项试验；按分期漏斗、分子类型、单药 vs 联合及全球 72 国地理分布结构化归类 | 2026年11月18日快照 (检索执行: 2026-11-18) | R 4.3+, ggplot2, patchwork, dplyr, scales | `05_Figure4_Global_Trial_Landscape/` |
| **图 5 (Figure 5)** | **获得性耐药分子网络与多维度联合策略** | Section 6 | 顶刊耐药临床队列文献 (Awad 2021, Yaeger 2023, Bekaii-Saab 2024, JCO 2025) | 梳理靶内 Switch-II 继发突变（Y96, H95, R68, A59）、上游 RTK 反馈扩增（MET/HER2/AXL/EGFR）、下游 MAPK 旁路（BRAF/CRAF/MEK1）、表型可塑性及液体活检 ctDNA 早期清除与提前预警窗口；保留完整胞外受体结构域 | 2026年11月18日 | Python 3.10+, ImageMagick 7.1, Lanczos 重采样, R Cairo PDF | `06_Figure5_Resistance_Networks/` |
| **附图 S1 (Fig S1)** | **9种耐药机制与5大联合逻辑决策矩阵** | Supplementary Appendix | 配对组织与液体活检耐药队列 | 建立 9 类耐药变异与 5 大联合治疗逻辑（垂直通路、水平旁路、免疫调节、状态应激与动态 ctDNA 监测）的功能对应矩阵；对比 NSCLC 与 CRC 配对血浆与组织检出率 | 2026年11月18日 | Python 3.10+, Matplotlib, Cairo PDF, ImageMagick (500 DPI) | `07_Supplementary_Material/` |
| **附表 S1–S3** | **四代抑制剂、全球批准案卷与耐药干预** | Supplementary Appendix | FDA Orange Book, EMA CHMP, NMPA CDE, PMDA 公示 | 梳理四代代表性药物结合构象与分期（表S1）；四大监管机构批准案卷与上市后确证性试验轨迹（表S2，含 KRYSTAL-10 撤销全记录）；耐药机制受累生化通路与前瞻性补救方案（表S3） | 2026年11月18日 | Python 3.10+, Markdown, CSV, python-docx | `07_Supplementary_Material/` |

---

## 二、 详细数据检索策略与方法学规范

### 1. MSK-IMPACT 泛癌种临床测序队列提取方法 (Figure 2)
- **数据来源**: 纪念斯隆-凯特琳癌症中心（MSK）前瞻性临床测序队列 `msk_impact_2017`（PMID: 28481359）。
- **检索接口**: cBioPortal REST API v2。
- **提取字段**: 样本编号 (`sample_id`)、癌种主类别 (`cancer_type`)、基因符号 (`Hugo_Symbol`)、氨基酸改变 (`HGVSp_Short`)、突变类型 (`Variant_Classification`) 及等位基因突变深度。
- **过滤准则**:
  1. 仅保留非同义、非沉默点突变及编码区移码/同工框缺失变异；
  2. 样本分母：严格按该肿瘤实际完成靶向捕获深度测序的患者样本数计算（`n_samples`），杜绝因单一样本多重突变引起百分比畸高；
  3. 过滤样本量：总测序样本数小于 10 例的罕见肿瘤在绘图中不予显示，防止小样本偏倚。

### 2. ClinicalTrials.gov 全球临床试验数据库检索策略 (Figure 4)
- **数据接口**: ClinicalTrials.gov REST API v2 (`/api/v2/studies`)。
- **快照与检索截止时间**: **2026年11月18日** (检索与数据冻结执行日期: 2026-11-18)。
- **初始检索式**:
  ```text
  ("RAS" OR "KRAS" OR "NRAS" OR "HRAS" OR "G12C" OR "G12D" OR "G12V" OR "G12R" OR "G13D" OR "Q61H" OR "Q61L" OR "Q61R" OR "Q61K")
  AND (cancer OR tumor OR neoplasm OR carcinoma OR adenocarcinoma OR oncology OR lymphoma OR leukemia OR melanoma)
  ```
  限定条件: `study_type = INTERVENTIONAL`, `phase IN (EARLY_PHASE1, PHASE1, PHASE2, PHASE3)`。
- **两轮人工独立筛查与排除漏斗**:
  - 检索命中原始记录: **3,210 项**。
  - 排除记录: **2,028 项**，具体构成如下:
    - 排除心血管/肾素-血管紧张素系统（RAAS: Renin-Angiotensin System）相关研究: 1,907 项；
    - 排除非恶性肿瘤适应证: 38 项；
    - 排除非恶性发育遗传综合征（RASopathies, 如 Noonan 综合征）: 19 项；
    - 排除临床分期不符合项（如无分期介入研究）: 54 项；
    - 排除 IV 期上市后监测研究: 10 项。
  - 最终严格纳入: **1,182 项** RAS 相关干预性肿瘤临床试验。
- **RAS 关联层级四分法标定规则**:
  - `RAS-targeted` (358 项): 药物直接结合 RAS 蛋白本身（包括 G12C/G12D/G12V 抑制剂、三元复合物 RAS(ON) 抑制剂、PROTAC 降解剂）；
  - `RAS-regulator` (134 项): 药物作用于 RAS 关键上游调节因子（SOS1 抑制剂、SHP2 变构抑制剂、法尼基转移酶 FTase 抑制剂）；
  - `Biomarker-selected` (639 项): RAS 突变或野生型状态作为入组筛选、分层或排除标准，但干预药物非直接针对 RAS 通路（如抗 EGFR 单抗限野生型入组、化疗/免疫分层研究）；
  - `RAS-mentioned` (51 项): 试验方案提及 RAS 但不属于上述三类。

### 3. III 期 RCT 元回归模型构建规范 (Figure 3)
- **纳入研究**: 7 项完成并在经同行评议期刊发表或国际顶级肿瘤学术会议（ASCO/ESMO/AACR）正式报告的 III 期随机对照试验。
- **终点参数**: 盲态独立中心阅片委员会（BICR）评估的无进展生存期（PFS）风险比（HR）、总生存期（OS）风险比及 95% 置信区间。
- **交叉率定义**: 对照组患者疾病进展后实际交叉接受靶向药物治疗的比例（Effective Crossover Rate, %）。
- **回归模型**: 采用加权普通最小二乘法（WLS），样本量平方根作为权重，检验交叉率与 OS HR 的线性相关性（$y = eta_0 + eta_1 x + \epsilon$）。结果证实二者具有高度显著正相关性（$R^2 = 0.88, p = 0.005$），解释了肺癌二线单药试验中 PFS 获益无法转化为 OS 获益的方法学根源。

---

## 三、 出版级图像排版规范 (Artwork Production Standards)

1. **版心尺寸标准**: 全文所有主图（Fig 1–5）与附图（Fig S1）统一采用国际顶级期刊（ESMO Open / Elsevier）标准的 **180.0 mm 双栏通栏宽（Double-Column Width）** 设计。
2. **字体与排版统一**: 全局统一为 TrueType Arial 字体；面板标签统一采用大写粗体（**A**, **B**, **C**），字号 8.5–9.5 pt；正文标注统一为 6.2–7.2 pt；保证全图 **零文字重叠碰撞（Zero Text Collision）**。
3. **输出格式与分辨率**:
   - **500 DPI TIFF**: 采用 LZW 无损压缩算法，严格保证印刷级出版精度（像素宽 3,543 px）；
   - **纯矢量 Cairo PDF / EPS**: 保持所有文本为纯字符状态（非轮廓化），方便编辑排版与检索；
   - **高清晰 PNG**: 方便网页端快速审阅与学术交流。
