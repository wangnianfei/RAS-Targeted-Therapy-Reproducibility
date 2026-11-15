# Table 1: Classification, Binding Conformation, and Clinical Development Stage of RAS-Directed Inhibitors
# 表 1: RAS抑制剂分类、结合构象与研发阶段

## 1. 论文对应位置 (Manuscript Location)
- **章节**: 第 3.2 节 “不同代次 RAS 抑制剂的靶点谱与结合构象差异”
- **页码与段落**: 正文 P415 引出表 1。

## 2. 表格内容与临床研发格局 (Clinical Landscape)
本表系统梳理并归纳了全球处于不同研发阶段的四代 RAS 靶向药物共 12 种代表性分子：
1. **第 1 代: 突变特异性(OFF态)抑制剂**:
   - **Sotorasib (AMG 510)**: KRAS(G12C-OFF)，获 FDA/EMA/NMPA 加速批准用于二线 NSCLC；
   - **Adagrasib (MRTX849)**: KRAS(G12C-OFF)，获 FDA/EMA 加速批准用于 NSCLC 二线及 CRC 双靶；
   - **Divarasib (GDC-6036)**: KRAS(G12C-OFF)，III 期 Krascendo 1 获得首个 OS 与 PFS 双重统计学显著获益；
   - **格索雷塞 (Garsorasib / D-1553)**: KRAS(G12C-OFF)，获 NMPA 附条件批准上市；
2. **第 2 代: 突变特异性(OFF态)拓展抑制剂**:
   - **RMC-9805**: KRAS(G12D-OFF) 口服选择性共价抑制剂（利用天冬氨酸羟基配位），I/II 期在研；
   - **HRS-4642**: KRAS(G12D-OFF) 高选择性非共价抑制剂，国内首个进入临床的 G12D 分子；
3. **第 3 代: 广谱 pan-RAS(OFF态)抑制剂**:
   - **BI 3706674**: pan-KRAS(OFF)，高亲和力结合突变型及野生型 KRAS，阻断核苷酸交换；
4. **第 4 代: 三元复合物 RAS(ON态)分子胶抑制剂**:
   - **Daraxonrasib (RMC-6236)**: pan-RAS(ON)，III 期 RASolute 302 取得突破（OS 13.2 vs 6.7 个月，HR 0.40），已获 FDA 常规批准用于经治 PDAC；
   - **Elironrasib (RMC-6291)**: KRAS(G12C-ON) 共价三元复合物抑制剂，克服 Switch II 结合口袋耐药突变；
   - **RMC-7977**: pan-RAS(ON) 可逆型三元复合物分子，全面阻断 GTP 态 RAS 与效应蛋白结合；
5. **新型降解剂 (PROTAC / 分子胶)**:
   - **Setidegrasib (ASP3082)**: KRAS(G12D) 选择性降解剂，诱导 E3 连接酶靶向泛素化降解；
6. **通路修饰剂 (翻译后修饰抑制剂)**:
   - **Tipifarnib**: FTase 抑制剂，阻断 HRAS CAAX 基序法尼基化，用于 HRAS 过表达或突变实体瘤。

## 3. 数据来源、检索策略与截止日期 (Data Sources & Cut-off Dates)
- **数据来源**: 
  1. 美国 FDA 橙皮书与审批公布平台 (FDA Drugs@FDA);
  2. 中国国家药品监督管理局药品审评中心 (NMPA CDE);
  3. 欧洲药品管理局 (EMA);
  4. ClinicalTrials.gov 注册数据库;
  5. 国际顶级肿瘤学会议（ASCO, ESMO, AACR）官方口头报告与核心期刊论文。
- **检索式与入选准则**: 检索式为 `("RAS" OR "KRAS" OR "NRAS" OR "HRAS") AND ("inhibitor" OR "degrader" OR "tri-complex")`。严格筛选具有明确化学结构式、公布详尽 I–III 期临床药代/疗效读数且具代表性的化合物。
- **数据截止日期**: **2026年10月31日**。

## 4. 文件结构 (Files in this Folder)
```text
├── README.md                      # 本说明文档
├── data/
│   ├── table1_approved_and_pipeline_drugs.csv       # 结构化 CSV 数据表
│   ├── Table1_RAS-directed_drug_landscape.md        # 全景文献与分子机制佐证
│   └── Table2_approved_drugs_indications_regulatory_routes.md # 获批药物监管审批路径
└── code/
    └── build_table1.py            # 表格构建与校验导出脚本 (Python)
```

## 5. 复现与校验指令 (How to Reproduce)
在当前目录下运行：
```bash
python3 code/build_table1.py
```
