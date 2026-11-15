# Figure 3: Conformational Displacement upon Nucleotide Exchange and Drug Binding
# 图 3: 核苷酸状态与药物结合引起的构象位移

## 1. 论文对应位置 (Manuscript Location)
- **章节**: 第 3.1 节 “RAS 抑制剂的化学型演进与成药机理”
- **页码与段落**: 正文 P318 引出图 3。

## 2. 图像内容与生物物理机制 (Biophysical Narrative)
本图从三维结构与定量位移角度揭示了 RAS 从“不可成药”到成功变构干预的构象物理基础：
- **Panel a (核苷酸交换位移曲线)**: 比较处于非活性 GDP 结合态（PDB: 4OBE，1.24 Å 高分辨率单晶）与模拟活性 GTP 结合态（PDB: 5VQ2）的 KRAS 构象。Cα 空间位移表明，构象重排高度富集于 Switch I（残基 30–38）与 Switch II（残基 60–76），核心 G 结构域 RMSD 仅为 0.71 Å；
- **Panel b (共价药物诱导变构位移曲线)**: 比较无药结合的 KRAS(G12C)-GDP（PDB: 4LDJ）与共价小分子抑制剂 Sotorasib (AMG 510) 结合态（PDB: 6OIM，2.20 Å）。结合诱导 Switch II 发生剧烈空间位移（位移峰值达 4.2 Å，核心 RMSD 0.88 Å），强行撑开隐蔽的变构 Switch II 口袋；
- **Panel c (变构口袋三维结合模式)**: 6OIM 晶体复合物的 600 dpi 光线追踪表面模型，展示 Sotorasib 嵌合在 Switch II 口袋中，其丙烯酰胺弹头与 Cys12 硫原子形成不可逆共价加成键，同时邻近 Switch I、Switch II、P-loop 与结合态 GDP 及 Mg2+ 离子。

## 3. 数据来源、检索策略与截止日期 (Data Sources & Cut-off Dates)
- **数据来源**: RCSB Protein Data Bank (RCSB PDB, https://www.rcsb.org/):
  - **PDB 4OBE**: KRAS-GDP 野生型晶体，分辨率 1.24 Å（Chain B）；
  - **PDB 5VQ2**: KRAS-GTP (GppNHp) 类似物复合物（Chain A）；
  - **PDB 4LDJ**: KRAS(G12C)-GDP 载脂对照态（Chain A）；
  - **PDB 6OIM**: KRAS(G12C)-Sotorasib (AMG 510) 共价复合物晶体，分辨率 2.20 Å（Chain A）。
- **结构叠合算法与位移计算**:
  1. 提取单体 Chain A (4OBE 采用 Chain B) 中 1–169 位氨基酸的骨架 Cα 空间三维直角坐标；
  2. 采用最小二乘法（Kabsch 旋转平移算法）对高度刚性的核心 G-domain（残基 1–166，严格排除高变构区 Switch I 25–45 与 Switch II 55–76）进行空间对齐；
  3. 计算对齐后对应残基 Cα 原子的欧氏距离位移：$d_i = \| R(A_i - c_A) + c_B - B_i \|$。
- **数据截止日期**: **PDB 库沉积版本**。

## 4. 文件结构 (Files in this Folder)
```text
├── README.md                      # 本说明文档
├── data/
│   ├── 4OBE.pdb                   # KRAS-GDP (1.24 Å) 晶体结构
│   ├── 5VQ2.pdb                   # KRAS-GTP 结构
│   ├── 4LDJ.pdb                   # KRAS(G12C)-GDP 对照结构
│   ├── 6OIM.pdb                   # KRAS(G12C)-Sotorasib 共价复合物结构
│   ├── _panelC_6OIM.png           # 600 dpi PyMOL 光线追踪分子表面切片
│   ├── ca_distance_shifts.csv     # 导出的各氨基酸位点 Cα 空间位移距离矩阵
│   └── pdb_entries.json           # 晶体元数据与实验参数记录
├── code/
│   ├── render_panelC_pymol.pml    # PyMOL 三维分子表面批处理渲染脚本
│   └── run_figure3.py             # 独立位移计算与矢量拼接绘图脚本 (Python)
└── vector_figures/
    ├── Figure3_conformational_switch.pdf  # 高清矢量 PDF
    ├── Figure3_conformational_switch.svg  # 矢量 SVG
    └── Figure3_conformational_switch.png  # 300 dpi 印刷级预览图
```

## 5. 绘图工具、软件与环境版本 (Tools & Software)
- **语言与环境**: Python 3.10+, PyMOL 2.5+
- **关键依赖库**: `matplotlib` >= 3.8.0, `numpy` >= 1.26.0

## 6. 复现指令 (How to Reproduce)
在当前目录下运行独立脚本：
```bash
python3 code/run_figure3.py
```
运行后将计算三维结构位移，更新 `data/ca_distance_shifts.csv` 数据表，并重新生成 `vector_figures/` 中的全部图件。
