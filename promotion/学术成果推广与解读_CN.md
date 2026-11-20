# 公众号 / 知乎 / 丁香园 解读稿（模板，录用后发布）

**标题：** 实体瘤 RAS 靶向治疗：七项 III 期试验证实了什么，又留下了什么
**论文：** Targeting RAS in solid tumours: from molecular switch dynamics and resistance networks to randomised clinical trial landscapes（*ESMO Open*，已投稿）
**作者：** 王年飞，盛池雨，齐健，沈淑敏，王尚虎*
**数据与代码：** https://github.com/wangnianfei/RAS-Targeted-Therapy-Reproducibility

> 录用后将 `[DOI]` 替换为文章链接。文中数字均取自稿件，数据截止 2026 年 11 月 18 日。

---

## 导语

RAS 曾被认为"不可成药"。2013 年开关 II 口袋（switch-II pocket）被发现后，直接抑制 KRAS 成为现实。本文综述了七项 III 期随机试验，区分哪些结论已有随机证据支持，哪些仍待证实；同时整理了 1,151 项注册试验与已报道的耐药机制。全部图表可由开源代码复现。[DOI]

## 一、两类直接抑制剂（图 1）

- **OFF 态共价抑制剂**：结合失活态 KRAS G12C 的开关 II 口袋，与 Cys12 形成共价键，如 sotorasib（索托拉西布）、adagrasib（阿达格拉西布）、divarasib（PDB 6OIM）。
- **RAS(ON) 三元复合物抑制剂**：药物先结合亲环素 A，再与活性态 RAS 结合、阻断效应蛋白，如 daraxonrasib（PDB 9BG6）。

## 二、III 期试验：PFS 普遍改善，OS 获益仅见于两项（表 1、图 3）

- 七项试验客观缓解率全部提高，六项延长 PFS。
- **OS 获益**：Krascendo 1 中 divarasib 优于 sotorasib 或 adagrasib（经治 *KRAS* G12C 非小细胞肺癌，HR 0.56，期中分析）；RASolute 302 中 daraxonrasib 优于化疗（经治转移性胰腺癌，中位 13.2 vs 6.7 个月，HR 0.40，期中分析，不允许交叉）。
- **未见 OS 获益或尚不成熟**：CodeBreaK 200 中 sotorasib 对比多西他赛 OS 无差异（HR 1.01），多西他赛组 26% 交叉至 sotorasib；KRYSTAL-12 中 adagrasib 的 OS 在首次报告时尚不成熟。
- **结直肠癌**：单药疗效有限，需联合抗 EGFR。sotorasib 联合帕尼单抗在化疗难治人群中延长 PFS（CodeBreaK 300）；adagrasib 联合西妥昔单抗在二线未优于化疗（KRYSTAL-10），该加速批准适应证于 2026 年 9 月 1 日应申办方请求撤回。

## 三、1,151 项注册试验（附图 S2）

ClinicalTrials.gov 中经逐条复核保留的 1,151 项 RAS 相关干预性肿瘤试验里，353 项在实体瘤中检验直接靶向 RAS 的药物：KRAS G12C 抑制剂 201 项、G12D 抑制剂 60 项、疫苗/TCR-T 40 项、multi-RAS(ON)/pan-RAS 抑制剂 39 项。其中 198 项在美国、152 项在中国设有中心；行业资助 241 项，并主导全部 43 项 II/III 或 III 期试验。

## 四、获得性耐药（图 4、附表 S3）

adagrasib 耐药的 38 例患者中，17 例检出可能机制：开关 II 口袋二次突变（R68S、H95D/Q/R、Y96C，4 例）、其他 KRAS 改变、*MET* 扩增与致癌融合、NRAS/BRAF/MAP2K1 突变，以及进展时重复组织活检的 10 例患者（其中 9 例为 NSCLC）中 2 例出现鳞癌转化。H95 突变体外对 sotorasib 仍敏感，但临床上均伴随其他交叉耐药改变，因此不能据此直接换药。

## 五、未来方向

非 G12C 等位基因抑制剂、一线与围手术期试验、按耐药机制匹配的联合方案，以及在统计分析计划中预先规定交叉用药的处理方法。

---

**开源复现**：图 1 由 PDB 结构经 PyMOL 渲染，图 2 来自 MSK-IMPACT 数据，图 3 与附图 S1、S2 由脚本生成，`reproduce_all.sh` 一键复现；图 4 为作者绘制的示意图，借助 AI 工具修改。
