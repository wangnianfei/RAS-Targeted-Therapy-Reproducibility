# Methodology, Data Sources, and Software Specifications
# 《RAS靶向治疗综述》方法学、数据来源、检索策略与软件环境全景指南

本综述旨在为全球肿瘤学同道提供一份客观、详实、可精确复现的 RAS 靶向治疗临床与转化研究全景指引。为践行国际最高学术透明度准则（Nature Portfolio, Cell Press, ESMO Open），本研究将所有图表的原始数据、分析流程、绘图脚本与高分辨率矢量图件全部开源公开。

本文档系统汇总全篇综述中**所有图表按论文出现顺序**的数据来源、检索策略、排除规则、数据截止日期及所使用的软件与计算环境。

---

## 一、 图表全景方法学汇总表 (Methodology Matrix)

| 序号 / 编号 | 图表名称 | 对应正文章节 | 原始数据来源 (Data Source) | 数据检索策略与入选标准 | 数据截止日期 | 核心工具与软件版本 |
|:---|:---|:---|:---|:---|:---|:---|
| **图 1 (Figure 1)** | RAS信号网络与可干预节点 | Section 2.1 (P274) | 权威文献系统综述与 FDA/NMPA 靶点库 | 提取受体输入、GEF/GAP调控、5大效应通路及负反馈环路；标注获批与在研靶点 | 2026年10月 | Python 3.10+, Matplotlib 3.8.0, PIL 10.0+, rsvg-convert 2.58+ |
| **图 2 (Figure 2)** | RAS突变的泛癌种分布 | Section 2.2 (P288) | MSK-IMPACT 泛癌种临床测序队列 (PMID: 28481359) | cBioPortal REST API v2 提取 10,945 例晚期实体瘤数据；严格限定非同义/非沉默点突变；分母为该癌种测序总样本数；单样本多突变计1次；排除样本数 <10 的肿瘤 | 队列冻结版本 (无后续更新) | Python 3.10+, Matplotlib 3.8.0, NumPy 1.26.0 |
| **图 3 (Figure 3)** | 核苷酸状态与药物结合引起的构象位移 | Section 3.1 (P318) | RCSB Protein Data Bank (PDB): 4OBE, 5VQ2, 4LDJ, 6OIM | 提取高分辨率（≤2.2 Å）单体 Cα 坐标；基于核心 G-domain（残基 1–166，剔除 Switch I/II）进行最小二乘法三维刚体叠合；计算各残基 Cα 欧氏距离位移 | PDB 库沉积版本 | Python 3.10+, NumPy, Matplotlib, PyMOL 2.5.0 (600 dpi 光线追踪渲染) |
| **表 1 (Table 1)** | RAS抑制剂分类、结合构象与研发阶段 | Section 3.2 (P415) | FDA Orange Book, NMPA CDE, EMA 公示, ClinicalTrials.gov, 药企年报 | 系统梳理四代代表性药物（第1代至第4代RAS抑制剂、降解剂及FTase抑制剂共12种）；提取靶点、构象、分期与监管状态 | 2026年10月31日 | Python 3.10+, Markdown, CSV, python-docx 1.1.2 |
| **表 2 (Table 2)** | 靶向RAS通路的7项关键III期随机对照临床试验汇总 | Section 4.0 (P460) | PubMed, ClinicalTrials.gov, ASCO, ESMO, AACR, NEJM, Lancet, JCO | 检索式: `("RAS" OR "KRAS" OR "NRAS") AND ("Phase 3" OR "randomized") AND ("solid tumors" OR "NSCLC" OR "colorectal" OR "pancreatic" OR "melanoma")`；严格提取7项关键III期RCTs（CodeBreaK 200, KRYSTAL-12, Krascendo 1, CodeBreaK 300, KRYSTAL-10, RASolute 302, NEMO）的人群、样本量、对照组、交叉方案、随访、PFS、OS、ORR及≥3级AEs | 2026年10月31日 | Python 3.10+, Markdown, CSV, python-docx 1.1.2 |
| **图 4 (Figure 4)** | RAS相关肿瘤试验全球格局 | Section 5.1 (P519) | ClinicalTrials.gov REST API v2 (`/api/v2/studies`) | 检索获得 3,210 条记录，经两轮人工独立双盲筛查：排除非肿瘤学适应证（如心血管RAAS系统 1,907 项、RASopathy 19 项、非肿瘤疾病 38 项）、非I–III期（54 项）、IV期（10 项），最终纳入 1,182 项临床试验；按靶向层级、分期、申办方及 72 国地理分布结构化归类 | 2026年10月20日快照 (API 执行: 2026-11-05) | R 4.3.0+, ggplot2 3.5.0, sf 1.0-16, rnaturalearth 1.0.1, circlize 0.4.16, grid, dplyr |
| **图 5 (Figure 5)** | 耐药机制与联合策略的对应矩阵 | Section 5.2 (P543) | 顶刊耐药临床队列文献 (Awad 2021, Yaeger 2023, Bekaii-Saab 2024) | 双盲专家评阅提取法：提取 9 类耐药机制与 5 类干预逻辑的对应关系（直接有效、部分有效、无明显活性）；提取 NSCLC 单药与 CRC 双靶治疗后耐药基因变异检出率（45% vs 74%） | 2026年10月 | R 4.3.0+, ggplot2 3.5.0, grid, dplyr |
| **附图 1 (Supp Fig 1)** | KRAS结构特征与同工型差异 | Supplementary | RCSB PDB (4OBE) 与 UniProt (P01116, P01111, P01112) | 全局两两比对算法（Match +1, Mismatch 0, Gap -1）；比对 G-domain (1–166) 与高变区 (HVR, 167–189) 残基差异；高亮碱性残基簇与脂质修饰位点 | 2026年10月 | Python 3.10+, PyMOL 2.5.0 |
| **附图 2 (Supp Fig 2)** | RAS靶向药物研发阶段泳道图 | Supplementary | 60 种临床化合物库与 1,182 项试验关联库 | 归纳 6 大化学型在各临床阶段的分布泳道及突变等位基因覆盖度 | 2026年10月 | R 4.3.0+, ggplot2 3.5.0 |
| **附图 3 (Supp Fig 3)** | 三种RAS基因的氨基酸位点突变图谱 | Supplementary | MSK-IMPACT 2017 队列 (10,945 例) | 统计 KRAS (1,670 突变)、NRAS (252 突变)、HRAS (101 突变) 密码子非同义突变频数与百分比 | 队列冻结版本 | Python 3.10+, Matplotlib 3.8.0 |

---

## 二、 详细数据检索策略与方法学规范

### 1. MSK-IMPACT 临床测序队列提取方法 (Figure 2 & Supp Fig 3)
- **数据来源**: 纪念斯隆-凯特琳癌症中心（MSK）前瞻性临床测序队列 `msk_impact_2017`（PMID: 28481359）。
- **检索接口**: cBioPortal REST API v2。
- **提取字段**: 样本编号 (`sample_id`)、癌种主类别 (`cancer_type`)、基因符号 (`Hugo_Symbol`)、氨基酸改变 (`HGVSp_Short`)、突变类型 (`Variant_Classification`) 及等位基因突变深度。
- **过滤准则**:
  1. 仅保留非同义、非沉默点突变及编码区移码/同工框缺失变异；
  2. 样本分母：严格按该肿瘤实际完成靶向捕获深度测序的患者样本数计算（`n_samples`），杜绝因单一样本多重突变引起百分比畸高；
  3. 过滤样本量：总测序样本数小于 10 例的罕见肿瘤在绘图中不予显示，防止小样本偏倚。

### 2. ClinicalTrials.gov 全球临床试验数据库检索策略 (Figure 4)
- **数据接口**: ClinicalTrials.gov REST API v2 (`/api/v2/studies`)。
- **快照时间**: **2026年10月20日** (检索执行日期: 2026-11-05)。
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

### 3. PDB 结构坐标提取与最小二乘拟合算法 (Figure 3 & Supp Fig 1)
- **晶体学数据来源**: RCSB Protein Data Bank。
- **纳入结构号**:
  - PDB 4OBE: 野生型 KRAS-GDP 复合物晶体，高分辨率 1.24 Å；
  - PDB 5VQ2: KRAS-GTP (GppNHp 类似物) 活性态晶体；
  - PDB 4LDJ: KRAS(G12C)-GDP 载脂对照晶体；
  - PDB 6OIM: KRAS(G12C)-Sotorasib (AMG 510) 共价复合物晶体（2.20 Å）。
- **刚体三维空间叠合算法 (Kabsch 算法)**:
  为精确衡量变构位移，避免高柔性环区的构象形变干扰全局对齐，对齐基准严格限定为**核心 G 结构域刚体骨架**：
  $$\min_{R, \mathbf{t}} \sum_{i \in 	ext{Core}} \| R \mathbf{x}_{1,i} + \mathbf{t} - \mathbf{x}_{2,i} \|^2$$
  其中 $	ext{Core} = \{ r \in [1, 166] \mid r 
otin [25, 45] \cup [55, 76] \}$（剔除 Switch I 与 Switch II 区域）。
  对齐后，计算全长各残基 Cα 欧氏距离位移：$d_i = \| R(\mathbf{x}_{1,i} - \mathbf{c}_1) + \mathbf{c}_2 - \mathbf{x}_{2,i} \|$。

### 4. 关键 III 期 RCT 数据提取与交叉治疗稀释分析 (Table 2)
- **文献与数据来源**: PubMed 数据库检索、ClinicalTrials.gov 官方终点更新、各大国际肿瘤学大会口头报告（ASCO, ESMO, AACR）及正式发表全文。
- **检索式**: `("RAS" OR "KRAS" OR "NRAS") AND ("Phase 3" OR "randomized controlled trial") AND ("solid tumors" OR "NSCLC" OR "colorectal" OR "pancreatic" OR "melanoma")`。
- **重点统计指标**: 意向治疗人群（ITT）样本量、对照组方案、方案允许交叉治疗比例、盲态独立中心评估（BICR）的中位 PFS 及风险比（HR, 95% CI, P值）、中位 OS 及风险比（HR, 95% CI, P值）、客观缓解率（ORR）及 $\ge$3 级不良事件（AEs）发生率。
- **关于 OS 终点去偶联的方法学解读**:
  在二线 NSCLC 试验中（CodeBreaK 200 与 KRYSTAL-12），PFS 与 ORR 均表现出统计学显著优效（HR 分别为 0.66 与 0.58），但 OS 曲线出现重合（HR 分别为 1.01 与 0.99）。方法学分析确认：对照组患者在疾病进展后接受交叉方案使用 G12C 抑制剂的比例分别达到 34% 与 39%，后续有效靶向治疗对对照组的生存期产生了显著延展效应，从而稀释了初始随机化分组的 OS 差异。相比之下，Krascendo 1 采用阳性对照（头对头比较 Divarasib 与 Sotorasib/Adagrasib）以及 RASolute 302（PDAC 严格禁止交叉治疗），均顺利实现了 PFS 与 OS 的双重显著获益（HR 分别为 0.56 与 0.40）。

### 5. 耐药机制矩阵文献提取与双盲评定准则 (Figure 5)
- **文献队列**: 国际公认的晚期 NSCLC 与 CRC 靶向后继发耐药大样本转化研究（Awad et al., NEJM 2021; Yaeger et al., NEJM 2023; Bekaii-Saab et al., Nat Med 2024）。
- **双盲评定方法**:
  由两名具有十年以上肿瘤分子生物学经验的副高级专家对 9 类耐药机制与 5 类前沿联合治疗策略进行交叉打分：
  - **直接有效 (Direct)**: 具有明确的体内外前临床数据或早期临床试验读数，能特异性克服该耐药变异；
  - **部分有效 (Partial)**: 仅在特定突变亚型或特定组织微环境中显示出抗肿瘤活性；
  - **无明显活性/不对应 (None)**: 机制上无法阻断该变异或已有临床数据证明耐药。
  初始评定一致率达到 96%，分歧项经复核原始论文中的体外激酶活化实验及细胞活力曲线后仲裁解决。

---

## 三、 计算环境与开源依赖包版本规范

### 1. Python 运行环境
- **Python**: 3.10.x / 3.11.x / 3.12.x / 3.14.x
- **核心依赖包**:
  - `matplotlib` >= 3.8.0（高分辨率矢量排版与图形渲染）
  - `numpy` >= 1.26.0（矩阵计算与刚体空间拟合）
  - `pillow` (PIL) >= 10.0.0（图像高保真处理）
  - `requests` >= 2.31.0（API 检索与下载）
  - `python-docx` >= 1.1.2（稿件自动化排版与样式渲染）

### 2. R 运行环境
- **R**: >= 4.3.0
- **核心 CRAN / Bioconductor 依赖包**:
  - `ggplot2` >= 3.5.0
  - `sf` >= 1.0-16
  - `rnaturalearth` >= 1.0.1
  - `circlize` >= 0.4.16
  - `dplyr` >= 1.1.4
  - `tidyr` >= 1.3.1
  - `cowplot` >= 1.1.3
  - `scales` >= 1.3.0

### 3. 结构生物学与矢量渲染辅助工具
- **PyMOL**: 2.5.0+（用于高分辨率光线追踪分子表面渲染，脚本在 `code/render_panelC_pymol.pml`）
- **rsvg-convert**: 2.58+（用于 SVG 矢量图像与 PDF 印刷版格式转换）
- **Headless Google Chrome**: 用于将高精度 SVG 矢量以 A4 物理毫米尺寸无损打印为嵌入字体矢量的 PDF。

---

## 四、 数据可用性与代码共享声明 (Data & Code Availability)

本研究所有数据与代码均完全开源，无任何专有私有算法封装：
- **代码仓库**: [GitHub 托管公开仓库]
- **数据许可协议**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **代码许可协议**: MIT License
- **学术引用规范**: 如在后续研究中复用本仓库的数据、脚本或矢量图件，请按 `CITATION.cff` 规范标明引用来源。
