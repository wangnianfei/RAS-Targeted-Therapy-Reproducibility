# Figure 2: Pan-Cancer Distribution of *KRAS*, *NRAS*, and *HRAS* Mutations
# 图 2: RAS突变的泛癌种分布

## 1. 论文对应位置 (Manuscript Location)
- **章节**: 第 2.2 节 “RAS 家族基因突变的泛癌种分布与分子流行病学”
- **页码与段落**: 正文 P288 引出图 2。

## 2. 图像内容与流行病学特征 (Epidemiological Summary)
本图系统展示了三大 *RAS* 原癌基因在人类实体瘤中的突变发生率与等位基因突变图谱：
- **Panel a (*KRAS*)**: 展示 16 类主要实体瘤中 *KRAS* 突变样本百分比及等位基因细分（G12D、G12V、G12C、G12R、G13D、Q61X 及 Other）。其中胰腺导管腺癌（PDAC）突变率最高（88%），以 G12D (36%)、G12V (28%)、G12R (13%) 为主；结直肠癌（CRC）突变率为 45%，以 G12D (13%)、G12V (10%)、G13D (8%)、G12C (4%) 为主；非小细胞肺癌（NSCLC）突变率为 32%，其中 G12C 占比最高（13%）。
- **Panel b (*NRAS*)**: 展示 10 类实体瘤中 *NRAS* 突变频率，主要富集在恶性黑色素瘤（21%）与甲状腺癌（10%）。
- **Panel c (*HRAS*)**: 展示 10 类实体瘤中 *HRAS* 突变频率，主要富集于膀胱尿路上皮癌（5%）和头颈鳞癌（4%）。

## 3. 数据来源、检索策略与截止日期 (Data Sources & Cut-off Dates)
- **数据来源**: 纪念斯隆-凯特琳癌症中心（MSK）前瞻性临床测序队列 MSK-IMPACT 2017（`msk_impact_2017`，Zehir et al., *Nature Medicine* 2017; 23(6):703-713, PMID: 28481359）。
- **检索接口与检索方式**: 通过 cBioPortal REST API v2 (`/api/v2/molecular-profiles/msk_impact_2017_mutations`) 提取 10,945 例晚期实体瘤患者测序数据。
- **数据清洗与入选排除准则**:
  1. 仅纳入非同义（non-synonymous）、非沉默（non-silent）的点突变与小片段插入缺失，剔除同义突变和非翻译区（UTR）变异；
  2. 分母计算严格以各癌种实际接受靶向捕获测序的总样本数（`n_samples`）为准，而非突变事件数。单一样本若携带 2 个 KRAS 突变，仅计为 1 个突变样本；
  3. 突变等位基因分类：G12D, G12V, G12C, G12R, G13D, Q61X (包括 Q61H/K/L/R) 及 Other；
  4. 样本量限制：测序样本数少于 10 例的罕见肿瘤予以剔除。
- **数据截止日期**: **队列冻结版本 (Snapshot as distributed)**，无后续回溯污染。

## 4. 文件结构 (Files in this Folder)
```text
├── README.md                      # 本说明文档
├── data/
│   ├── cancer_type_kras_alleles.csv        # 泛癌种 KRAS 突变率与等位基因明细
│   ├── cbioportal_mutations.json           # 10,945 样本的原始突变 JSON 数据
│   ├── cbioportal_sample_cancertype.json   # 样本 ID 与癌种分类映射表
│   └── codon_share.csv                     # 密码子水平突变占比
├── code/
│   ├── fetch_cbioportal.py        # 从 cBioPortal API 检索原始突变记录
│   ├── prepare_cbioportal.py      # 数据统计与等位基因矩阵清洗
│   └── run_figure2.py             # 独立绘图脚本 (Python)
└── vector_figures/
    ├── Figure2_cancer_type_distribution.pdf  # 高清矢量 PDF
    ├── Figure2_cancer_type_distribution.svg  # 矢量 SVG
    └── Figure2_cancer_type_distribution.png  # 300 dpi 印刷级预览图
```

## 5. 绘图工具、软件与环境版本 (Tools & Software)
- **语言与环境**: Python 3.10+
- **关键依赖库**: `matplotlib` >= 3.8.0, `numpy` >= 1.26.0

## 6. 复现指令 (How to Reproduce)
在当前目录下运行独立脚本：
```bash
python3 code/run_figure2.py
```
运行后将读取 `data/` 下的清洗数据，并自动输出更新 `vector_figures/` 中的全部矢量图件。
