#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 5 - Resistance Mechanism x Combination Logic Decision Matrix.

Redesigned with ESMO Open / Nature Reviews jewel-tone aesthetics and high precision:
- Panel a: Strategy decision matrix mapping 9 acquired resistance mechanisms across 3 functional classes against 5 clinical combination logics.
- Panel b: Clinical detection rates of acquired resistance alterations in paired plasma vs. tissue cohorts.

Usage:
  python3 run_figure5.py
Outputs:
  ../vector_figures/Figure5_resistance_combination.pdf
  ../vector_figures/Figure5_resistance_combination.svg
  ../vector_figures/Figure5_resistance_combination.png
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'vector_figures'))
os.makedirs(FIG, exist_ok=True)

# Layout constants
MM = 1 / 25.4
W = 180.0  # Double column width (mm)
H = 168.0  # Height (mm)
T = 7.2    # Primary text size (pt)
T_SM = 6.2 # Secondary text size (pt)
T_XS = 5.3 # Micro text size (pt)
PN = 9.5   # Panel identifier (pt, bold)

CANVAS_BG = '#FFFFFF'
INK = '#0F172A'
INK_MUTED = '#475569'
GREY = '#64748B'

# Unified Jewel-Tone Group Palette (Harmonized with Fig 1 & Fig 4)
GRP_COLORS = {
    'genetic': {
        'main': '#1F3A5F',       # Deep Prussian Navy (Fig 4 Primary Anchor)
        'light': '#F1F5F9',
        'border': '#CBD5E1',
        'label': 'GENOMIC ALTERATIONS'
    },
    'nongenetic': {
        'main': '#A63A2E',       # Deep Brick Ruby Crimson (Fig 4 Secondary Anchor)
        'light': '#FFF1F2',
        'border': '#FECDD3',
        'label': 'PHENOTYPIC & LINEAGE PLASTICITY'
    },
    'carrier': {
        'main': '#2A6F6F',       # Oceanic Deep Teal (Fig 4 Biomarker & Fig 1 PI3K)
        'light': '#F0FDFA',
        'border': '#99F6E4',
        'label': 'ORGANELLE & METABOLIC REWIRING'
    }
}

LOGICS = [
    {
        'num': '1',
        'title': 'Vertical',
        'subtitle': 'Same pathway clamp',
        'metric': 'ORR 71% (1L)',
        'source': 'Zhong 2026',
        'color': '#2563EB',      # Cobalt Royal Blue (Fig 1 MAPK)
        'bg': '#EFF6FF'
    },
    {
        'num': '2',
        'title': 'Horizontal',
        'subtitle': 'Parallel bypass switch',
        'metric': 'PFS 5.6 vs 2.2 mo',
        'source': 'Fakih 2023',
        'color': '#0D9488',      # Teal Emerald (Fig 1 PI3K)
        'bg': '#F0FDFA'
    },
    {
        'num': '3',
        'title': 'Immunotherapy',
        'subtitle': 'Effector engagement',
        'metric': 'Durability, not ORR',
        'source': 'Chour 2023',
        'color': '#E11D48',      # Crimson Accent (Fig 1 Immune)
        'bg': '#FFF1F2'
    },
    {
        'num': '4',
        'title': 'State & Stress',
        'subtitle': 'Survival switch',
        'metric': 'ORR 82% (n=33)',
        'source': 'Song 2026',
        'color': '#7C3AED',      # Deep Violet (Fig 1 Apoptosis)
        'bg': '#F5F3FF'
    },
    {
        'num': '5',
        'title': 'Cytotoxic',
        'subtitle': 'Off-axis cell kill',
        'metric': 'ORR 88.9%',
        'source': 'Akamatsu 2025',
        'color': '#D97706',      # Warm Golden Amber (Fig 1/4)
        'bg': '#FFFBEB'
    }
]

ROWS = [
    ('genetic', 'Receptor-level bypass', 'MET ampl.; NRAS/BRAF/RET mut.; fusions',
     {1: ('direct', 'SOS1'), 2: ('direct', 'EGFR (CRC)')}),
    ('genetic', 'Downstream MAPK nodes', 'BRAF, MAP2K1, NRAS reactivate ERK',
     {1: ('direct', 'ERK')}),
    ('genetic', 'Parallel chains', 'PI3K-AKT-mTOR & YAP1/TAZ bypass',
     {2: ('partial', 'PI3K-AKT')}),
    ('nongenetic', 'Cell state plasticity', 'Epithelial state; transcriptional reprogramming',
     {4: ('direct', 'cell state → GPX4')}),
    ('nongenetic', 'Lineage exit', 'Adeno-to-squamous transition; Paneth-like state',
     {4: ('direct', 'lineage programme')}),
    ('carrier', 'Proteostasis stress', 'Heat-shock & IRE1α reactivation',
     {4: ('direct', 'IRE1α')}),
    ('carrier', 'Polarity & cytoskeleton', 'YAP-MRAS axis & actin remodeling',
     {4: ('direct', 'YAP-MRAS')}),
    ('carrier', 'Signalling condensates', 'ARAF-RAS condensates defeat NF1',
     {4: ('direct', 'ARAF condensates')}),
    ('carrier', 'Metabolic rewiring', 'Mevalonate membrane tether & OXPHOS/ZBTB11',
     {4: ('direct', 'mevalonate, ZBTB11')}),
]

plt.rcParams.update({
    'font.family': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'svg.fonttype': 'none',
})

def draw_pill(ax, x, y, w, h, bg, border, lw=0.6, r=1.4):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       facecolor=bg, edgecolor=border, linewidth=lw, zorder=3)
    ax.add_patch(p)
    return p


SYNC_DIRS = [
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件_新配色预览",
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件",
    "/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/New_Color_Theme_Preview",
]
import shutil

def run_figure5_pipeline(lang='en'):
    plt.rcParams['font.family'] = 'sans-serif'
    if lang == 'cn':
        plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'Arial Unicode MS', 'DejaVu Sans']
    else:
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(figsize=(W * MM, H * MM), facecolor=CANVAS_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis('off')

    # Top title
    y_top = H - 5.0
    ax.text(3.5, y_top, 'a', fontsize=PN, fontweight='bold', color=INK, va='top', ha='left')
    main_title = '获得性耐药机制演进与联合干预策略对应决策矩阵' if lang == 'cn' else 'Resistance Mechanism × Combination Logic Decision Matrix'
    ax.text(8.0, y_top - 0.2, main_title,
            fontsize=T + 1.2, fontweight='bold', color=INK, va='top', ha='left')

    X_ROW_LABEL = 3.5
    X_MATRIX_START = 58.5
    W_MATRIX = W - X_MATRIX_START - 3.5
    CW = W_MATRIX / 5.0
    GAP = 1.0

    # Column Headers
    y_header_top = y_top - 6.5
    h_header = 16.5
    y_header_bot = y_header_top - h_header

    if lang == 'cn':
        logics_data = [
            {'num': '1', 'title': '垂直联合', 'subtitle': '同通路双重阻断', 'metric': 'ORR 71% (一线)', 'color': '#2563EB', 'bg': '#EFF6FF'},
            {'num': '2', 'title': '水平联合', 'subtitle': '并行旁路开关切断', 'metric': 'PFS 5.6 对 2.2月', 'color': '#0D9488', 'bg': '#F0FDFA'},
            {'num': '3', 'title': '免疫联合', 'subtitle': '效应细胞募集与重塑', 'metric': '持久应答, 延缓耐药', 'color': '#E11D48', 'bg': '#FFF1F2'},
            {'num': '4', 'title': '状态与应激', 'subtitle': '细胞应激稳态瓦解', 'metric': 'ORR 82% (n=33)', 'color': '#7C3AED', 'bg': '#F5F3FF'},
            {'num': '5', 'title': '细胞毒化疗', 'subtitle': '离轴合成致死杀伤', 'metric': 'ORR 88.9%', 'color': '#D97706', 'bg': '#FFFBEB'},
        ]
    else:
        logics_data = LOGICS

    for i, log in enumerate(logics_data):
        cx = X_MATRIX_START + i * CW
        draw_pill(ax, cx + GAP/2, y_header_bot, CW - GAP, h_header,
                  bg=log['bg'], border=log['color'], lw=0.7, r=1.8)
        
        pill_txt = f"策略 {log['num']}" if lang == 'cn' else f"Logic {log['num']}"
        draw_pill(ax, cx + CW/2 - 6.5, y_header_top - 3.8, 13.0, 3.0,
                  bg=log['color'], border='none', lw=0, r=1.0)
        ax.text(cx + CW/2, y_header_top - 2.3, pill_txt,
                fontsize=T_XS, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=5)
        
        ax.text(cx + CW/2, y_header_top - 6.0, log['title'],
                fontsize=T - 0.2, fontweight='bold', color=INK, ha='center', va='center', zorder=5)
        
        ax.text(cx + CW/2, y_header_top - 8.8, log['subtitle'],
                fontsize=T_XS, color=INK_MUTED, ha='center', va='center', zorder=5)
        
        draw_pill(ax, cx + GAP/2 + 1.2, y_header_bot + 1.4, CW - GAP - 2.4, 3.8,
                  bg='#FFFFFF', border='#CBD5E1', lw=0.45, r=1.0)
        ax.text(cx + CW/2, y_header_bot + 3.3, log['metric'],
                fontsize=T_SM, fontweight='bold', color=log['color'], ha='center', va='center', zorder=5)

    # Matrix rows
    y_curr = y_header_bot - 3.2
    row_height = 7.0
    group_bar_h = 4.0
    
    current_grp = None

    if lang == 'cn':
        rows_data = [
            ('genetic', '受体层级旁路激活', 'MET扩增; NRAS/BRAF突变; 融合重排', {1: ('direct', 'SOS1'), 2: ('direct', 'EGFR (CRC)')}),
            ('genetic', '下游MAPK节点突变', 'BRAF、MAP2K1突变重新激活ERK', {1: ('direct', 'ERK')}),
            ('genetic', '并行信号链代偿', 'PI3K-AKT-mTOR及YAP1/TAZ旁路', {2: ('partial', 'PI3K-AKT')}),
            ('nongenetic', '细胞状态可塑性', 'EMT上皮间质转化; 转录重编程', {4: ('direct', '细胞状态→GPX4')}),
            ('nongenetic', '谱系分化偏离', '腺癌向鳞癌转化; 神经内分泌表型', {4: ('direct', '谱系分化调控')}),
            ('carrier', '蛋白稳态应激', '热休克蛋白与IRE1α应激反应激活', {4: ('direct', 'IRE1α')}),
            ('carrier', '极性与细胞骨架', 'YAP-MRAS轴与肌动蛋白动力学', {4: ('direct', 'YAP-MRAS')}),
            ('carrier', '信号无膜凝聚物', 'ARAF-RAS凝聚物抵抗NF1水解', {4: ('direct', 'ARAF凝聚物')}),
            ('carrier', '代谢通路重构', '甲羟戊酸膜锚定与OXPHOS依赖', {4: ('direct', '甲羟戊酸, ZBTB11')}),
        ]
        grp_labels = {
            'genetic': '基因组改变与旁路激酶活化',
            'nongenetic': '细胞表型可塑性与谱系转化',
            'carrier': '细胞器应激与代谢重编程'
        }
    else:
        rows_data = ROWS
        grp_labels = {k: v['label'] for k, v in GRP_COLORS.items()}

    for grp_key, row_title, row_sub, cells in rows_data:
        # Group header if new group
        if grp_key != current_grp:
            current_grp = grp_key
            gcfg = GRP_COLORS[grp_key]
            y_curr -= (group_bar_h + 1.2)
            draw_pill(ax, X_ROW_LABEL, y_curr, W - X_ROW_LABEL - 3.5, group_bar_h,
                      bg=gcfg['light'], border=gcfg['border'], lw=0.45, r=1.0)
            ax.text(X_ROW_LABEL + 3.0, y_curr + group_bar_h / 2.0, grp_labels[grp_key],
                    fontsize=T_XS + 0.3, fontweight='bold', color=gcfg['main'], va='center', zorder=5)
            y_curr -= 1.0

        y_curr -= row_height
        # Row label on left
        ax.text(X_ROW_LABEL + 2.0, y_curr + row_height - 1.2, row_title,
                fontsize=T_SM, fontweight='bold', color=INK, va='top', zorder=5)
        ax.text(X_ROW_LABEL + 2.0, y_curr + 1.1, row_sub,
                fontsize=T_XS, color=INK_MUTED, va='bottom', zorder=5)

        # 5 cells across
        for ci in range(1, 6):
            cx = X_MATRIX_START + (ci - 1) * CW
            if ci in cells:
                status, label = cells[ci]
                bg = '#EFF6FF' if status == 'direct' else '#FEF3C7'
                bd = '#2563EB' if status == 'direct' else '#D97706'
                tc = '#1E3A8A' if status == 'direct' else '#78350F'
                draw_pill(ax, cx + GAP/2 + 0.6, y_curr + 0.8, CW - GAP - 1.2, row_height - 1.6,
                          bg=bg, border=bd, lw=0.5, r=1.2)
                ax.text(cx + CW/2, y_curr + row_height / 2.0, label,
                        fontsize=T_XS, fontweight='bold', color=tc, ha='center', va='center', zorder=5)
            else:
                draw_pill(ax, cx + GAP/2 + 0.6, y_curr + 0.8, CW - GAP - 1.2, row_height - 1.6,
                          bg='#F8FAFC', border='#E2E8F0', lw=0.35, r=1.2)
                ax.text(cx + CW/2, y_curr + row_height / 2.0, '—',
                        fontsize=T_SM, color='#94A3B8', ha='center', va='center', zorder=5)
        y_curr -= 0.6

    # -------------------------------------------------------------
    # Panel b: Detection Rates in Paired Cohorts
    # -------------------------------------------------------------
    y_b_top = y_curr - 7.5
    ax.text(3.5, y_b_top, 'b', fontsize=PN, fontweight='bold', color=INK, va='top', ha='left')
    b_title = '获得性耐药改变临床检出率 (配对血浆 ctDNA 对 组织活检)' if lang == 'cn' else 'Clinical Detection Rates of Acquired Resistance Alterations (Paired ctDNA vs Tissue)'
    ax.text(8.0, y_b_top - 0.2, b_title,
            fontsize=T + 1.0, fontweight='bold', color=INK, va='top', ha='left')

    hb_box = 18.0
    y_b_box = y_b_top - hb_box - 4.5
    w_box = (W - 3.5 * 2 - 8.0) / 2.0

    # Box 1: NSCLC Monotherapy
    draw_pill(ax, 3.5, y_b_box, w_box, hb_box, bg='#F8FAFC', border='#CBD5E1', lw=0.55, r=2.0)
    b1_t = '非小细胞肺癌 单药治疗 (CodeBreaK / KRYSTAL)' if lang == 'cn' else 'NSCLC Monotherapy (CodeBreaK / KRYSTAL)'
    b1_s = '45% (17/38) 检出获得性耐药改变' if lang == 'cn' else '45% (17/38) acquired alterations detected'
    b1_sub = '主要包括 S-IIP 口袋突变 (Y96D, R68S, H95D) 与旁路激活' if lang == 'cn' else 'Switch-II pocket mutations (Y96D, R68S, H95D) & bypass activation'
    ax.text(6.0, y_b_box + hb_box - 3.2, b1_t, fontsize=T_SM + 0.2, fontweight='bold', color='#1E293B', va='top')
    ax.text(6.0, y_b_box + hb_box - 7.5, b1_s, fontsize=T_SM, fontweight='bold', color='#2563EB', va='top')
    ax.text(6.0, y_b_box + 2.8, b1_sub, fontsize=T_XS, color=INK_MUTED, va='bottom')

    # Box 2: CRC Vertical Doublet
    draw_pill(ax, 3.5 + w_box + 8.0, y_b_box, w_box, hb_box, bg='#F8FAFC', border='#CBD5E1', lw=0.55, r=2.0)
    b2_t = '结直肠癌 垂直双靶治疗 (CodeBreaK 300 / KRYSTAL-10)' if lang == 'cn' else 'CRC Vertical Doublet (CodeBreaK 300 / KRYSTAL-10)'
    b2_s = '74% (25/34) 检出复合多克隆耐药改变' if lang == 'cn' else '74% (25/34) polyclonal resistance alterations'
    b2_sub = '以 RTK/下游激酶突变与旁路激活为主 (多克隆复合突变)' if lang == 'cn' else 'High prevalence of RTK/MAPK reactivation & polyclonal alterations'
    ax.text(3.5 + w_box + 10.5, y_b_box + hb_box - 3.2, b2_t, fontsize=T_SM + 0.2, fontweight='bold', color='#1E293B', va='top')
    ax.text(3.5 + w_box + 10.5, y_b_box + hb_box - 7.5, b2_s, fontsize=T_SM, fontweight='bold', color='#D97706', va='top')
    ax.text(3.5 + w_box + 10.5, y_b_box + 2.8, b2_sub, fontsize=T_XS, color=INK_MUTED, va='bottom')

    suffixes = ['_EN'] if lang == 'en' else ['_CN', '_中文版']
    if lang == 'en':
        suffixes.append('')

    for suf in suffixes:
        if suf == '_中文版':
            stem = 'Figure5_耐药机制与应对策略_中文版'
        else:
            stem = 'Figure5_resistance_combination' + suf
            
        pdf_out = os.path.join(FIG, stem + '.pdf')
        svg_out = os.path.join(FIG, stem + '.svg')
        png_out = os.path.join(FIG, stem + '.png')

        fig.savefig(pdf_out, format='pdf', dpi=400)
        fig.savefig(svg_out, format='svg')
        fig.savefig(png_out, format='png', dpi=400)
        print(f"Figure 5 [{lang} - {suf}] generated:")
        print("  ->", pdf_out)
        print("  ->", svg_out)
        print("  ->", png_out)

        for sdir in SYNC_DIRS:
            if os.path.exists(sdir):
                for ext in ('.png', '.pdf', '.svg'):
                    shutil.copy2(os.path.join(FIG, stem + ext), os.path.join(sdir, stem + ext))
                print(f"Synchronized Figure 5 [{stem}] to:", sdir)

    plt.close(fig)

def main():
    for lang in ('en', 'cn'):
        run_figure5_pipeline(lang=lang)

if __name__ == '__main__':
    main()
