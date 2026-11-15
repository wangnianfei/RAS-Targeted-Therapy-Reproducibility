# Figure 4: Global Landscape of 1,182 RAS-Related Oncology Trials
# 图 4: RAS相关肿瘤试验全球格局

## 1. 论文对应位置 (Manuscript Location)
- **章节**: 第 5.1 节 “全球 RAS 靶向治疗临床试验的研发布局与发展趋势”
- **页码与段落**: 正文 P519 引出图 4。

## 2. 图像内容与图谱架构 (Landscape Narrative)
本图全面绘制了 2000–2026 年间全球在 ClinicalTrials.gov 上注册的 1,182 项 RAS 相关肿瘤临床试验的多维格局：
- **Panel a (全球地理分布热力地图)**: 呈现具有至少一个试验中心注册记录的全球 72 个国家/地区热力分布图。美国（622 项）和中国（305 项）位列前两位，欧洲以法国、西班牙、意大利、德国、英国为主力；
- **Panel b (环形分层全景图)**: 一扇区代表一项试验（1,182 项试验对应 1,182 个扇区），按 7 大瘤种板块分组（外周圆弧宽度反映试验量占比：泛瘤种 339 项、肺癌 282 项、结直肠癌 196 项、胰腺癌 148 项、血液肿瘤 85 项、黑色素瘤 71 项、妇科/泌尿生殖系统 61 项）。自外向内四个同心圆圈层分别编码：
  1. **圈层 1**: 与 RAS 的靶向关联层级（直接结合 RAS 靶向、调控因子、生物标志物入组分层、一般提及）；
  2. **圈层 2**: 最高临床分期（Early Phase 1, Phase 1, Phase 2, Phase 3）；
  3. **圈层 3**: 牵头申办方类别（制药企业 Industry, 欧美学术合作组 Other, 美国国立癌症研究所 NIH, 中国与国际合作网络 Network, 政府/非营利机构 Gov）；
  4. **圈层 4**: 招募状态（已完成 Completed, 招募中 Ongoing, 尚未招募 Not yet recruiting, 提前终止 Stopped early, 其他/未知 Other/unknown）。
- **Panel c (年度注册趋势堆叠图)**: 展示 2000 年至 2026 年历年注册试验量的演变。2013 年 Shokat 团队发现 G12C 变构口袋后，直接结合 RAS 的靶向试验（深蓝色）呈现爆发式增长。

## 3. 数据来源、检索策略与截止日期 (Data Sources & Cut-off Dates)
- **数据来源**: 美国国立卫生研究院 ClinicalTrials.gov REST API v2 (`/api/v2/studies`)。
- **检索构建与筛选漏斗**:
  1. 检索式覆盖 RAS, KRAS, NRAS, HRAS 及其代表性突变亚型词表与肿瘤学限制词，限定干预性研究（`study_type = INTERVENTIONAL`）及 I–III 期；
  2. 检索获得 3,210 条原始 NCT 编号记录；
  3. 经过两轮人工独立双盲筛查，排除 2,028 条不符合项：
     - 1,907 项：未将 RAS 作为基因或分子靶点（主要是肾素-血管紧张素-醛固酮系统 RAS/RAAS 相关的心血管、肾病研究）；
     - 54 项：临床分期不在 I–III 期范围内（非分期介入研究）；
     - 38 项：非恶性肿瘤疾病；
     - 19 项：非恶性 RASopathy（如 Noonan 综合征、Costello 综合征等）；
     - 10 项：IV 期上市后监测研究；
  4. 最终严格锁定并纳入 **1,182 项** 肿瘤临床试验。
- **数据快照截止日期**: **2026年10月20日** (API 执行抓取：2026-11-05)。

## 4. 文件结构 (Files in this Folder)
```text
├── README.md                      # 本说明文档
├── data/
│   ├── trials_1182.csv            # 1,182 项入组试验完整字段记录 (一试验一行)
│   ├── search_terms.csv           # ClinicalTrials.gov 完整检索词清单
│   ├── summary.json               # 统计漏斗与分类汇总 JSON
│   ├── table2_excluded_records_and_reasons.csv # 排除的 2,028 项记录及原因
│   ├── table3_country_distribution.csv         # 72 个国家中心数统计
│   ├── table5_phase_distribution.csv           # 分期分布
│   ├── table6_status_distribution.csv          # 招募状态分布
│   ├── table7_sponsor_class.csv                # 申办方类型分布
│   ├── table8_target_class.csv                 # 靶点类别分布
│   ├── table9_tumour_distribution.csv          # 瘤种分布
│   └── table10_ras_relevance_tier.csv          # RAS 关联层级分布
├── code/
│   ├── fig2_fetch_ctgov.py        # ClinicalTrials.gov REST API v2 数据抓取脚本
│   ├── fig2_curate.py             # 试验筛选、排除与多维分类标注脚本
│   ├── fig2_world_map.R           # Panel a 全球地理热力图 R 绘图脚本
│   └── fig2_trial_atlas.R         # Panel b & c 环形分层全景图与趋势图脚本
└── vector_figures/
    ├── Figure4_trial_atlas.pdf    # 高清矢量 PDF
    ├── Figure4_trial_atlas.svg    # 矢量 SVG
    └── Figure4_trial_atlas.png    # 300 dpi 印刷级预览图
```

## 5. 绘图工具、软件与环境版本 (Tools & Software)
- **语言与环境**: R 4.3+, Python 3.10+
- **关键 R 包**: `ggplot2` >= 3.5.0, `sf` >= 1.0-16, `rnaturalearth` >= 1.0.1, `circlize` >= 0.4.16, `cowplot`, `grid`, `dplyr`, `scales`

## 6. 复现指令 (How to Reproduce)
在当前目录下运行：
```bash
Rscript code/fig2_trial_atlas.R .
```
