# 实体瘤 RAS 靶向治疗综述：数据与复现代码

本仓库收录投稿至 *ESMO Open* 的综述 *Targeting RAS in solid tumours: from molecular switch dynamics and resistance networks to randomised clinical trial landscapes* 全部图表的数据与代码。[English](./README.md)

**作者：** Nianfei Wang¹、Chiyu Sheng¹、Jian Qi²˒³、Shumin Shen⁴、Shanghu Wang⁵*（单位见英文说明）
**通讯作者：** wangshanghu@mail.ustc.edu.cn
**基金：** 安徽省卫生健康科研项目（项目编号：AHWJ:2025BAd20016）
**数据截止：** 2026 年 11 月 18 日

## 综述主要结论

- 七项 III 期试验中，RAS 通路抑制剂全部提高了客观缓解率，六项延长了无进展生存期（PFS）。
- 总生存期（OS）获益见于两项试验：Krascendo 1 中 divarasib 优于 sotorasib 或 adagrasib（经治 *KRAS* G12C 非小细胞肺癌，HR 0.56，期中分析）；RASolute 302 中 daraxonrasib 优于化疗（经治胰腺癌，中位 13.2 vs 6.7 个月，HR 0.40，期中分析）。
- CodeBreaK 200 中 sotorasib 未改善 OS（HR 1.01），交叉用药使比较复杂化；KRYSTAL-12 的 OS 在首次报告时尚不成熟。
- 结直肠癌中，sotorasib 联合帕尼单抗在难治性疾病中延长 PFS（CodeBreaK 300）；adagrasib 联合西妥昔单抗在二线未优于化疗（KRYSTAL-10），该加速批准适应证于 2026 年 9 月 1 日应申办方请求撤回。
- ClinicalTrials.gov 中经逐条复核保留 1,151 项 RAS 相关干预性肿瘤试验，其中 353 项在实体瘤中检验直接靶向 RAS 的药物（RAS 上下游通路抑制剂、仅按 RAS 状态入组的试验及血液肿瘤试验均不计入）。

## 图表与目录对应

| 图表 | 内容 | 目录 |
|:---|:---|:---|
| 图 1 | sotorasib–KRAS(G12C)（PDB 6OIM）与 daraxonrasib–亲环素 A–KRAS(G12V) 三元复合物（PDB 9BG6）晶体结构 | `01_Figure1_Structural_Mechanisms` |
| 图 2 | 七个瘤种 RAS 突变率与胰腺癌、结直肠癌、非小细胞肺癌 KRAS 等位基因构成（MSK-IMPACT） | `02_Figure2_PanCancer_Landscape` |
| 表 1 | 七项 III 期试验设计与结局 | `03_Table1_Pivotal_Phase3_RCTs` |
| 图 3 | 七项试验 PFS 与 OS 风险比森林图 | `04_Figure3_Phase3_Efficacy_Discordance` |
| 图 4 | KRAS G12C 抑制剂获得性耐药与对应策略示意图 | `06_Figure4_Resistance_Networks` |
| 附图 S1 | 353 项实体瘤直接靶向 RAS 试验的分期、药物类别与地区分布（首投稿中的图 4） | `05_FigureS1_Global_Trial_Landscape` |
| 附图 S2、附表 S1–S3 | 耐药类别×策略矩阵；抑制剂一览；监管审批；耐药机制 | `07_Supplementary_Material` |

图 1–3 与附图 S1、S2 由脚本根据数据或结构坐标绘制；图 4 为作者用绘图软件绘制、借助 AI 工具修改的示意图，不由代码生成。各目录 README 写明数据来源与细节，方法见 [`METHODOLOGY.md`](./METHODOLOGY.md)。

## 复现

依赖：Python ≥ 3.10（matplotlib）；R ≥ 4.3（ggplot2、patchwork、dplyr、tidyr、scales、ggtext、ragg、maps）；PyMOL 开源版；ImageMagick 7。

```bash
pip install -r requirements.txt
Rscript install_dependencies.R
bash reproduce_all.sh      # 可用 PYTHON=/path/to/python 指定解释器
```

## 许可

代码采用 MIT 许可；图件与数据采用 CC BY 4.0。引用信息见 [`CITATION.cff`](./CITATION.cff)。
