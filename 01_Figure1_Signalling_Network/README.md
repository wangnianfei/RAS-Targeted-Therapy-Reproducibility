# Figure 1: RAS Signalling Network and Druggable Intervention Nodes
# 图 1: RAS信号网络与可干预节点

## 1. 论文对应位置 (Manuscript Location)
- **章节**: 第 2.1 节 “RAS 蛋白的分子结构与激活-失活分子开关”
- **页码与段落**: 正文 P274 引出图 1。

## 2. 图像内容与生物学机制 (Biological Narrative)
本图以细胞生物学精细示意图的形式展示了 RAS 信号网络的全景拓扑架构与干预节点：
- **上游受体与输入**: 质膜脂质双分子层上跨膜排列的四类主要受体酪氨酸激酶（RTKs: EGFR, HER2, MET, ALK/RET）及其配体结合与胞内段酪氨酸自身磷酸化；
- **接头蛋白与调控因子**: 胞质 GRB2-SOS1 复合物招募，SHP2（PTPN11）变构磷酸酶与支架蛋白功能；KRAS 通过 C 端 CAAX 基序经历翻译后法尼基化与羧甲基化修饰，紧密锚定在细胞质膜内叶；
- **分子开关循环**: NF1/RASA1 GAP 蛋白催化 GTP 水解使 RAS 恢复为无活性的 GDP 结合态（OFF 态）；SOS1 等 GEF 催化 GDP 解离并结合胞内丰富 GTP，转换为活化的 GTP 结合态（ON 态）；
- **下游核心效应通路**: 
  1. RAF-MEK-ERK 经典有丝分裂原激活级联（胞质双激酶磷酸化后，ERK 入核磷酸化转录因子驱动增殖）；
  2. PI3K-AKT-mTOR 促存活与代谢重编程通路；
  3. RALGDS-RAL 囊泡运输与细胞运动通路；
  4. PLCε 第二信使传导通路；
  5. TIAM1-RAC 肌动蛋白细胞骨架重塑通路；
- **负反馈调控回路**: 活化的 ERK 对上游 SOS1、RAF 产生抑制性丝氨酸磷酸化，并诱导受体内吞脱敏（红色虚线负反馈箭头）；
- **药物干预节点**: 标记全球已获批（圆形）、临床在研（方形）及临床前/探索性（三角形）的干预位点（涵盖 RTK 抑制剂、SOS1 抑制剂、SHP2 变构抑制剂、第1/2/3/4代直接 RAS 抑制剂、Pan-RAF、MEK 与 ERK 抑制剂）。

## 3. 数据来源、检索策略与截止日期 (Data Sources & Cut-off Dates)
- **数据来源**: 经典文献系统审阅 (Hobbs et al., J Clin Oncol 2016; Simanshu et al., Cell 2017; Moore et al., Nat Rev Cancer 2020) 与 FDA/EMA/NMPA 靶点数据库。
- **检索与整理方法**: 由生物化学与肿瘤学专家团队交叉审阅整理，提取确切具有实验或临床证据支持的信号流向与负反馈节点。
- **数据截止日期**: **2026年10月**。

## 4. 文件结构 (Files in this Folder)
```text
├── README.md                      # 本说明文档
├── data/
│   ├── pathway_nodes.csv          # 通路主要蛋白质节点、亚细胞定位与靶向状态
│   └── pathway_edges.csv          # 信号激活、催化、磷酸化与负反馈作用连接表
├── code/
│   └── run_figure1.py             # 独立可运行的矢量图生成脚本 (Python)
└── vector_figures/
    ├── Figure1_RAS_signalling_network.pdf  # 高清矢量 PDF (出版排版级)
    ├── Figure1_RAS_signalling_network.svg  # 矢量 SVG (可编辑矢量格式)
    └── Figure1_RAS_signalling_network.png  # 300 dpi 印刷级预览图
```

## 5. 绘图工具、软件与环境版本 (Tools & Software)
- **语言与环境**: Python 3.10+
- **关键依赖库**: `Pillow` (PIL) >= 10.0.0
- **矢量转换工具**: `rsvg-convert` (librsvg 2.58+) 或 Headless Google Chrome (无头浏览器打印至矢量 PDF)。

## 6. 复现指令 (How to Reproduce)
在当前目录下运行独立脚本：
```bash
python3 code/run_figure1.py
```
运行后将自动重新生成 `vector_figures/` 下的 SVG、PDF 与 PNG 图像。
