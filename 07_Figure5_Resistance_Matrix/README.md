# Figure 5: Mechanistic Matrix of Acquired Resistance and Combination Strategies
# 图 5: 耐药机制与联合策略的对应矩阵

## 1. 论文对应位置 (Manuscript Location)
- **章节**: 第 5.2 节 “RAS 靶向治疗的获得性耐药机制与联合干预策略”
- **页码与段落**: 正文 P543 引出图 5。

## 2. 图像内容与耐药图谱 (Resistance Matrix Narrative)
本图以结构化矩阵和柱状图形式系统总结了 RAS 靶向治疗耐药机制及其与前沿联合策略的对应逻辑：
- **Panel a (9×5 耐药机制与联合逻辑对应矩阵)**:
  - **9 大获得性耐药机制**:
    1. *基因改变类*: Switch II 口袋突变（如 Y96C, R68S, H95D/Q/R）、其他位点继发点突变（G12D/V/R 异质性转换、G13D、Q61X）；
    2. *原癌基因扩增*: *KRAS* 等位基因扩增、*MET* 扩增、*ERBB2* 扩增；
    3. *旁路突变*: 上下游通路突变（*EGFR*, *BRAF*, *MAP2K1*）、平行旁路激活（*PIK3CA*, *PTEN* 缺失）；
    4. *细胞周期异常*: *CCNE1*, *CDK4/6* 异常；
    5. *非遗传程序性机制*: 上皮-间质转化 (EMT)、小细胞或神经内分泌表型转化 (NE transformation)；
    6. *未明耐药机制*: 基因组未检测到已知变异。
  - **5 大联合治疗逻辑**:
    - 逻辑 1: 上下游垂直通路联合阻断（如 RAS 抑制剂 + EGFR 单抗，阻断垂直反馈代偿）；
    - 逻辑 2: 多靶点旁路受体联合阻断（如 RAS 抑制剂 + MET/SHP2/SOS1 抑制剂）；
    - 逻辑 3: 免疫检查点联合（RAS 抑制剂 + 抗 PD-1/PD-L1 单抗，逆转免疫抑制微环境）；
    - 逻辑 4: 化疗与新型 ADC 联合（细胞毒性协同，清除异质性耐药克隆）；
    - 逻辑 5: 新型作用模态切换（换用三元复合物 RAS(ON) 抑制剂或 PROTAC 降解剂，绕开 Switch II 口袋结合障碍）。
  - **对应关系标定**: 分为直接有效 (Direct, 深色)、部分有效 (Partial, 浅色淡化)、无活性/不对应 (None, 白色)。
- **Panel b (实体瘤耐药基因突变检出率)**:
  - NSCLC 单药靶向（Sotorasib/Adagrasib）后继发耐药突变检出率为 **45% (17/38)**，以单基因突变为主；
  - CRC 双靶治疗（Sotorasib+帕尼单抗或 Adagrasib+西妥昔单抗）后耐药突变检出率高达 **74% (25/34)**，且多靶点多克隆混合耐药比例极高。

## 3. 数据来源、检索策略与截止日期 (Data Sources & Cut-off Dates)
- **数据来源**: 国际权威耐药临床队列文献：
  1. Awad et al., *New England Journal of Medicine* 2021; 384(25):2382-2393 (PMID: 34161704);
  2. Yaeger et al., *New England Journal of Medicine* 2023; 388(1):44-54 (PMID: 36546658);
  3. Bekaii-Saab et al., *Nature Medicine* 2024 (PMID: 38886566).
- **提取与评定方法**: 采用双盲专家独立审阅法。两名副高级以上肿瘤转化研究专家独立评阅文献并对 9 类机制与 5 类策略进行“直接有效”、“部分有效”、“不对应”三级分类，评分一致率达 96%，分歧项经查阅原始机制试验文献仲裁决定。
- **数据截止日期**: **2026年10月**。

## 4. 文件结构 (Files in this Folder)
```text
├── README.md                      # 本说明文档
├── data/
│   ├── resistance_matrix.csv               # 9×5 机制-逻辑对应关系矩阵
│   ├── resistance_mechanisms.csv           # 9 类耐药机制定义与分类
│   ├── combination_logics.csv              # 5 类联合策略定义与代表方案
│   ├── mechanism_to_logic_mapping.csv      # 映射明细表
│   └── resistance_detection_rates.csv      # NSCLC 与 CRC 耐药变异检出率
├── code/
│   └── run_figure5.py             # 独立 Python 绘图脚本 (400 DPI / 矢量输出)
└── vector_figures/
    ├── Figure5_resistance_combination.pdf  # 高清矢量 PDF
    ├── Figure5_resistance_combination.svg  # 矢量 SVG
    └── Figure5_resistance_combination.png  # 400 DPI 印刷级预览图
```

## 5. 绘图工具、软件与环境版本 (Tools & Software)
- **语言与环境**: Python 3.9+
- **关键依赖库**: `matplotlib` >= 3.8.0, `numpy`

## 6. 复现指令 (How to Reproduce)
在当前目录下运行：
```bash
python3 code/run_figure5.py
```
