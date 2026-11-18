# RAS 靶向治疗的化学与生物学 — 原始数据、代码与高分辨率图件开源复现仓库
# Data, Code, and Vector Artwork for "RAS-Directed Therapy in Solid Tumors"

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/)

本开源仓库完整收录了综述论文**《RAS 靶向治疗的化学与生物学》**（ESMO Open 投稿版本）中**所有图表与表格**的原始数据、生成代码、高清矢量图件（PDF/SVG）以及详尽的方法学复现指南。

> [!IMPORTANT]
> **数据与文献检索截止日期 (Data & Literature Retrieval Cut-off Date)**:
> 全文所有临床试验数据（ClinicalTrials.gov 1,182 项干预性肿瘤临床试验及 7 项关键 III 期随机对照试验）、四代代表性药物研发管线（FDA/EMA/NMPA 审批案卷）、耐药机制突变队列以及文献系统综述的**检索与数据冻结截止日期统一为 2026 年 11 月 18 日 (November 18, 2026)**。

为确保严谨性与透明度，本仓库**严格按照论文中图表出现的顺序**进行模块化结构组织，方便审稿人、读者与全球研究者快速审阅、提取数据并一键复现全部图件。

---

## 一、 论文图表与目录结构索引 (Figure & Table Navigation)

| 论文编号 | 图表名称 | 对应目录 | 核心数据 | 数据截止日期 | 运行脚本 | 矢量图件 |
|:---|:---|:---|:---|:---|:---|:---|
| **图 1** | RAS信号网络与可干预节点 | [`01_Figure1_Signalling_Network/`](./01_Figure1_Signalling_Network/) | 通路节点与连线数据 | 2026-11-18 | `code/run_figure1.py` | `vector_figures/Figure1_*.{pdf,svg,png}` |
| **图 2** | RAS突变的泛癌种分布 | [`02_Figure2_PanCancer_Distribution/`](./02_Figure2_PanCancer_Distribution/) | MSK-IMPACT 10,945例实体瘤突变库 | 队列冻结版 | `code/run_figure2.py` | `vector_figures/Figure2_*.{pdf,svg,png}` |
| **图 3** | 核苷酸状态与药物结合引起的构象位移 | [`03_Figure3_Conformational_Switch/`](./03_Figure3_Conformational_Switch/) | 4OBE, 5VQ2, 4LDJ, 6OIM 晶体坐标 | PDB沉积版 | `code/run_figure3.py` | `vector_figures/Figure3_*.{pdf,svg,png}` |
| **表 1** | RAS抑制剂分类、结合构象与研发阶段 | [`04_Table1_Inhibitor_Landscape/`](./04_Table1_Inhibitor_Landscape/) | 12种代表性药物靶向分类库 | 2026-11-18 | `code/build_table1.py` | `data/table1_*.csv` |
| **表 2** | 靶向RAS通路的7项关键III期随机对照临床试验汇总 | [`05_Table2_Pivotal_Phase3_RCTs/`](./05_Table2_Pivotal_Phase3_RCTs/) | 7项关键III期RCTs疗效与安全性数据库 | 2026-11-18 | `code/build_table2.py` | `data/table2_*.csv` |
| **图 4** | RAS相关肿瘤试验全球格局 | [`06_Figure4_Global_Trial_Landscape/`](./06_Figure4_Global_Trial_Landscape/) | 1,182项肿瘤试验库及72国地理分布 | 2026-11-18 | `code/fig2_trial_atlas.R` | `vector_figures/Figure4_*.{pdf,svg,png}` |
| **图 5** | 耐药机制与联合策略的对应矩阵 | [`07_Figure5_Resistance_Matrix/`](./07_Figure5_Resistance_Matrix/) | 9×5耐药-策略矩阵及检出率 | 2026-11-18 | `code/run_figure5.R` | `vector_figures/Figure5_*.{pdf,svg,png}` |
| **附图** | 结构、研发泳道与突变谱补充图件 | [`Supplementary_Material/`](./Supplementary_Material/) | PDB/管线/位点突变数据 | 2026-11-18 | 详见各附图子目录 | `Supp_Figure*.{pdf,svg}` |

---

## 二、 核心特点与学术质量承诺

1. **绝对客观与证据第一 (Evidence-First & Zero AI Hallucination)**:
   - 全文所有数据均来自于权威公开数据库（cBioPortal MSK-IMPACT 2017, ClinicalTrials.gov REST API v2, RCSB PDB）以及经同行评议发表的顶级医学期刊（NEJM, Lancet, Science, Nature, Cell, JCO）；
   - 无任何编造、推测或虚构数据，每个数值均有迹可循。
2. **完全独立可复现 (Self-Contained Reproducibility)**:
   - 每个图表目录均自带完整的 `data/`（原始输入）、`code/`（自包含可执行脚本）与 `vector_figures/`（输出矢量图）；
   - 用户既可以针对单幅图进行独立调试，也可以通过根目录下的批处理脚本一键全量生成。
3. **顶刊出版级图像排版 (Publication-Grade Vector Quality)**:
   - 所有图件统一采用标准 180 mm 通栏（Double-Column）版心设计；
   - 字体全局统一为 Arial，正文标注 7.5 pt，面板字母 9 pt 粗体；
   - 图像全部以纯矢量 PDF 与 SVG 格式输出，文字保持文本状态（非曲线化），支持任何矢量软件（Illustrator/Inkscape）进行无损排版与审阅；三维分子表面嵌入 600 dpi 印刷级切片。

---

## 三、 快速复现指引 (Quick Start)

### 1. 环境准备 (Environment Setup)

推荐使用 Conda 或 Python 虚拟环境配置运行环境：

```bash
# 克隆仓库
git clone https://github.com/wangnianfei/RAS-Targeted-Therapy-Reproducibility.git
cd RAS-Targeted-Therapy-Reproducibility

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 R 依赖 (可选，用于生成图4和图5)
Rscript install_dependencies.R
```

### 2. 一键批量复现全部图件 (Batch Reproduce All Figures)

在仓库根目录下直接执行批处理脚本：
```bash
bash reproduce_all.sh
```

### 3. 单个图表独立复现 (Reproduce Individual Figures)

您可以直接进入任意子目录运行对应的专属脚本：
```bash
# 复现图 1 (RAS 信号网络拓扑图)
python3 01_Figure1_Signalling_Network/code/run_figure1.py

# 复现图 2 (泛癌种突变分布图)
python3 02_Figure2_PanCancer_Distribution/code/run_figure2.py

# 复现图 3 (核苷酸交换与变构位移曲线及口袋图)
python3 03_Figure3_Conformational_Switch/code/run_figure3.py

# 校验并导出表 1 (四代 RAS 抑制剂研发格局)
python3 04_Table1_Inhibitor_Landscape/code/build_table1.py

# 校验并导出表 2 (7项关键 III 期临床试验数据)
python3 05_Table2_Pivotal_Phase3_RCTs/code/build_table2.py

# 复现图 4 (1,182项全球临床试验全景图)
Rscript 06_Figure4_Global_Trial_Landscape/code/fig2_trial_atlas.R 06_Figure4_Global_Trial_Landscape

# 复现图 5 (耐药机制与联合干预策略矩阵图)
Rscript 07_Figure5_Resistance_Matrix/code/run_figure5.R
```

---

## 四、 方法学与数据透明度 (Methodology & Open Science)

本综述秉持完全透明与可复现原则，全景数据、检索式与排除标准均经双盲交叉验证：
- **数据检索与冻结截止日期**: **2026 年 11 月 18 日 (November 18, 2026)**。涵盖全球 ClinicalTrials.gov 注册的所有 1,182 项临床试验、7 项关键 III 期随机对照试验、监管审批案卷及顶刊耐药队列文献。
- **详尽方法学与检索策略全书**:
👉 **[完整方法学指南 (METHODOLOGY.md)](./METHODOLOGY.md)**

---

## 五、 开源许可协议 (License)

- **文本、结构化数据与矢量图件 (Text, Data & Artwork)**: 采用 [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) 许可协议。
- **源代码与构建脚本 (Code & Scripts)**: 采用 [MIT License](./LICENSE) 许可协议。

---

## 六、 引用与联系方式 (Citation & Contact)

如您在学术论文、学位论文或科研项目中使用了本仓库提供的数据、分析方法或图件，请按如下格式引用：

```bibtex
@article{Wang2026RASTargetedTherapy,
  author    = {Wang, Nianfei and Collaborators},
  title     = {RAS-Directed Therapy in Solid Tumors: Chemistry, Biology, and Pivotal Clinical Evidence},
  journal   = {ESMO Open},
  year      = {2026},
  note      = {Data and code available at https://github.com/wangnianfei/RAS-Targeted-Therapy-Reproducibility}
}
```

- **通讯作者 / 仓库维护人**: Wang Nianfei (wangnianfei@gmail.com)
- **问题反馈**: 如对数据或脚本复现存在任何疑问，欢迎在 GitHub Issues 中提出。
