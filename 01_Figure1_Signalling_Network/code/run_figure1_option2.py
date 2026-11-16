#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 1 (Option 2) - The 3D Cellular Landscape of the RAS Signalling Network and Hallmarks.

Publication-grade composite medical illustration combining:
  - Panel a: 3D Cellular Landscape of RAS signalling, receptors, and targeted drugs with precision vector annotations.
  - Panel b: Four 3D AI-rendered hallmarks of RAS-driven cancer (Metabolism, Macropinocytosis, Immune Synapse, Senescence Bypass).
Adheres strictly to Nature Reviews Cancer / ESMO Open visual guidelines.
"""

import base64
import math
import os
import shutil
import subprocess
import sys
import tempfile
from PIL import ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'vector_figures'))
ASSET_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'assets'))
os.makedirs(FIG, exist_ok=True)
NAME = 'Figure1_Option2_3D_Landscape'

# Destination directories to synchronize
SYNC_DIRS = [
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件_新配色预览",
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件",
    "/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/New_Color_Theme_Preview",
]
W, H = 180.0, 172.0
PT = 25.4 / 72
FS = 6.8 * PT                             # Standard font size ~7 pt
FS_SM = 5.8 * PT                          # Small font size ~6 pt
FS_XS = 4.8 * PT                          # Extra small badge font size ~5 pt
PNs = 9.5 * PT                            # Panel bold letter size
LH = FS * 1.25                            # Line height

# Typography & color scheme
INK = '#0F172A'          # Deep slate black
INK_MUTED = '#475569'    # Slate
GREY = '#64748B'         # Muted slate grey
WHITE = '#FFFFFF'
BORDER = '#CBD5E1'

ACT_COL = '#2563EB'      # Royal Blue
INH_COL = '#64748B'      # Slate Grey

SANS = "Arial, Helvetica, 'Liberation Sans', sans-serif"

# Exact font metric measurement via PIL
_F = None
for font_dir in ['/System/Library/Fonts/Supplemental', '/System/Library/Fonts', '/Library/Fonts']:
    if os.path.exists(os.path.join(font_dir, 'Arial.ttf')):
        _F = {k: ImageFont.truetype(os.path.join(font_dir, '%s.ttf' % f), 1000)
              for k, f in (('r', 'Arial'), ('b', 'Arial Bold'), ('i', 'Arial Italic'),
                           ('bi', 'Arial Bold Italic'))}
        break

if _F is None:
    def tw(s, bold=False, size=FS):
        return len(s) * size * 0.52
else:
    def segs(s, bold=False):
        out, it, bd = [], False, bold
        while s:
            k = min([p for p in (s.find('<i>'), s.find('</i>'), s.find('<b>'),
                                 s.find('</b>')) if p >= 0] or [len(s)])
            if k:
                out.append((s[:k], it, bd))
                s = s[k:]
                continue
            for tag_name, f in (('<i>', 'it1'), ('</i>', 'it0'), ('<b>', 'bd1'), ('</b>', 'bd0')):
                if s.startswith(tag_name):
                    if f == 'it1': it = True
                    elif f == 'it0': it = False
                    elif f == 'bd1': bd = True
                    else: bd = bold
                    s = s[len(tag_name):]
                    break
        return out

    def tw(s, bold=False, size=FS):
        w = 0.0
        for t, it, bd in segs(s, bold):
            w += _F[('b' if bd else 'r') if not it else ('bi' if bd else 'i')].getlength(t)
        return w / 1000.0 * size

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class Doc:
    def __init__(self):
        self.L = {k: [] for k in ('bg', 'render', 'mem', 'under', 'link', 'body', 'over', 'text')}

    def add(self, layer, s):
        self.L[layer].append(s)

    def text(self, x, y, s, anchor='start', color=INK, bold=False, size=FS,
             layer='text', rot=None, opacity=None, halo=False):
        yb = y + size * 0.355
        tf = ' transform="rotate(%.1f %.2f %.2f)"' % (rot, x, y) if rot else ''
        op = ' fill-opacity="%.2f"' % opacity if opacity else ''
        spans = ''.join(
            '<tspan%s%s>%s</tspan>' % (' font-style="italic"' if it else '',
                                        ' font-weight="bold"' if bd else '', esc(t))
            for t, it, bd in segs(s, bold))
        
        if halo:
            self.add(layer, '<text x="%.2f" y="%.2f" font-size="%.3f" fill="#FFFFFF" '
                     'stroke="#FFFFFF" stroke-width="2.2" stroke-linejoin="round" '
                     'text-anchor="%s"%s xml:space="preserve">%s</text>'
                     % (x, yb, size, anchor, tf, spans))
            
        self.add(layer, '<text x="%.2f" y="%.2f" font-size="%.3f" fill="%s" '
                 'text-anchor="%s"%s%s xml:space="preserve">%s</text>'
                 % (x, yb, size, color, anchor, tf, op, spans))
        return tw(s, bold, size)

    def svg(self):
        body_content = ''.join(''.join(self.L[k]) for k in self.L)
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%gmm" height="%gmm" '
                'viewBox="0 0 %g %g" font-family="%s">'
                '<defs>%s</defs>%s</svg>' % (W, H, W, H, SANS, DEFS, body_content))

DEFS = (
    '<filter id="subtle-shadow" x="-3%" y="-3%" width="106%" height="110%">'
    '<feDropShadow dx="0" dy="0.5" stdDeviation="0.6" flood-color="#0F172A" flood-opacity="0.08"/>'
    '</filter>'
    '<filter id="glow-badge" x="-10%" y="-10%" width="120%" height="120%">'
    '<feDropShadow dx="0" dy="0.5" stdDeviation="0.8" flood-color="#E11D48" flood-opacity="0.15"/>'
    '</filter>'
)

D = Doc()

def marker(x, y, status, s=1.0):
    if status == 'approved':
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#16A34A" stroke="#15803D" stroke-width="0.30"/>'
              % (x, y, 1.10 * s))
    elif status == 'clinical':
        D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="0.30" fill="#2563EB" stroke="#1D4ED8" stroke-width="0.30"/>'
              % (x - 1.0 * s, y - 1.0 * s, 2.0 * s, 2.0 * s))
    else:
        D.add('body', '<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="#64748B" stroke="#475569" stroke-width="0.30"/>'
              % (x, y - 1.20 * s, x + 1.20 * s, y, x, y + 1.20 * s, x - 1.20 * s, y))

def drug_box(x, y, w, h, title, subtitle=None, status='approved', border_col=BORDER):
    """Draw a dedicated container card for therapeutic interventions."""
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.6" '
                 'fill="#FFFFFF" fill-opacity="0.96" stroke="%s" stroke-width="0.50" filter="url(#subtle-shadow)"/>'
          % (x, y, w, h, border_col))
    my = y + 3.8 if subtitle else y + h / 2.0
    marker(x + 2.5, my, status, s=0.85)
    D.text(x + 4.8, y + 2.4 if subtitle else y + h / 2.0 - FS * 0.35, title,
           bold=True, size=FS_SM, color=INK)
    if subtitle:
        D.text(x + 4.8, y + 5.8, subtitle, color=INK_MUTED, size=4.0*PT)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

def label_badge(cx, cy, text, bg_col='#FFFFFF', border_col='#64748B', text_col='#0F172A', size=FS_SM, bold=True):
    tw_val = tw(text, bold, size)
    w = tw_val + 4.0
    h = 4.2
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.4" '
                 'fill="%s" fill-opacity="0.95" stroke="%s" stroke-width="0.45" filter="url(#subtle-shadow)"/>'
          % (cx - w / 2, cy - h / 2, w, h, bg_col, border_col))
    D.text(cx, cy - size * 0.35, text, anchor='middle', color=text_col, bold=bold, size=size)
    return {'cx': cx, 'cy': cy, 'w': w, 'h': h, 'left': (cx - w/2, cy), 'right': (cx + w/2, cy), 'top': (cx, cy - h/2), 'bottom': (cx, cy + h/2)}

def outcome_box(x, y, w, h, title, subtitle, bg_col, border_col, title_col):
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.8" '
                 'fill="%s" stroke="%s" stroke-width="0.60" filter="url(#subtle-shadow)"/>'
          % (x, y, w, h, bg_col, border_col))
    D.text(x + w / 2.0, y + 2.5, title, anchor='middle', bold=True, size=FS_SM, color=title_col)
    D.text(x + w / 2.0, y + 6.2, subtitle, anchor='middle', size=FS_XS, color=INK_MUTED)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

# ============================================================ LOAD ASSETS ====
f1a_img_path = os.path.join(ASSET_DIR, 'figure1a_3d_ai_render.jpg')
with open(f1a_img_path, 'rb') as fh:
    F1A_B64 = base64.b64encode(fh.read()).decode('utf-8')

HALLMARK_B64 = {}
for k, fname in enumerate(['metabolism.jpg', 'macropinocytosis.jpg', 'immune.jpg', 'senescence.jpg']):
    fpath = os.path.join(ASSET_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, 'rb') as fh:
            HALLMARK_B64[k] = base64.b64encode(fh.read()).decode('utf-8')

# ============================================================ PANEL A ========
# Canvas Background
D.add('bg', '<rect width="180" height="172" fill="#FFFFFF"/>')

# Embed 3D AI Rendered Landscape across Panel a
# Render size: 180mm x 100.5mm (exact 16:9 ratio)
RENDER_H = 100.5
D.add('render', '<image href="data:image/jpeg;base64,%s" x="0.0" y="0.0" width="180.0" height="%.2f" '
                'preserveAspectRatio="xMidYMid meet"/>' % (F1A_B64, RENDER_H))

# Panel a Label
D.text(1.0, 3.2, 'a', bold=True, size=PNs, color=INK)

# 1. Standardization Legend Box (Top Left: x=6.5, y=1.8 - completely clear of receptors)
D.add('body', '<rect x="6.5" y="1.8" width="31.5" height="15.8" rx="1.8" fill="#FFFFFF" '
              'fill-opacity="0.96" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>')
marker(8.8, 3.6, 'approved', s=0.75)
D.text(11.0, 3.6, 'Approved drug class', color=INK, size=3.8*PT, bold=True)
marker(8.8, 6.4, 'clinical', s=0.75)
D.text(11.0, 6.4, 'Clinical trials (Ph I–III)', color=INK, size=3.8*PT, bold=True)
marker(8.8, 9.2, 'preclinical', s=0.75)
D.text(11.0, 9.2, 'Preclinical / investigational', color=INK, size=3.8*PT, bold=True)
D.add('link', '<line x1="7.5" y1="12.0" x2="10.2" y2="12.0" stroke="#2563EB" stroke-width="0.55"/>')
D.add('body', '<polygon points="10.2,11.3 11.5,12.0 10.2,12.7" fill="#2563EB"/>')
D.text(12.6, 12.0, 'Activation cascade (→)', color=ACT_COL, size=3.6*PT, bold=True)
D.add('link', '<line x1="7.5" y1="14.5" x2="10.5" y2="14.5" stroke="#64748B" stroke-width="0.55" stroke-dasharray="1.0 0.6"/>')
D.add('body', '<line x1="10.8" y1="13.7" x2="10.8" y2="15.3" stroke="#64748B" stroke-width="0.9"/>')
D.text(12.6, 14.5, 'Inhibition / target (--|)', color=INH_COL, size=3.6*PT, bold=True)

# 2. Plasma Membrane Badge
label_badge(18.0, 23.5, 'Plasma membrane', bg_col='#FFFFFF', border_col='#64748B', text_col='#0F172A')

# 3. Membrane Receptors (Balanced across top)
label_badge(44.0, 3.5, 'EGFR / RTK', bg_col='#F0F9FF', border_col='#0284C7', text_col='#0369A1')
label_badge(118.0, 4.0, 'GPCR (7-TM)', bg_col='#FAF5FF', border_col='#7C3AED', text_col='#6D28D9')
label_badge(156.0, 4.0, 'Integrin (α/β)', bg_col='#FFFBEB', border_col='#D97706', text_col='#92400E')

# Anti-EGFR mAb drug callout card (Placed to right of EGFR)
card_egfr = drug_box(53.5, 3.0, 25.5, 8.5, 'Anti-EGFR mAbs', 'cetuximab, panitumumab', 'approved', '#0284C7')
D.add('link', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#64748B" stroke-width="0.55" stroke-dasharray="1.2 0.8"/>'
      % (card_egfr['left'][0], card_egfr['left'][1], 48.0, 8.5))
D.add('body', '<line x1="47.5" y1="7.5" x2="48.5" y2="9.5" stroke="#64748B" stroke-width="1.1"/>')

# 4. Cytosolic Adaptor Complex (GRB2 • SHP2 • SOS1)
label_badge(58.0, 37.5, 'GRB2', bg_col='#F8FAFC', border_col='#94A3B8', text_col='#0F172A', size=5.2*PT)
label_badge(68.0, 37.5, 'SHP2', bg_col='#F8FAFC', border_col='#94A3B8', text_col='#0F172A', size=5.2*PT)
label_badge(78.0, 37.5, 'SOS1', bg_col='#F8FAFC', border_col='#94A3B8', text_col='#0F172A', size=5.2*PT)

# SHP2 / SOS1 inhibitor drug card
card_shp2 = drug_box(52.5, 46.5, 26.5, 8.5, 'SHP2 / SOS1 inh.', 'TNO155, BI 1701963', 'clinical')
D.add('link', '<line x1="68.0" y1="46.5" x2="68.0" y2="40.0" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="66.5" y1="40.0" x2="69.5" y2="40.0" stroke="#64748B" stroke-width="1.0"/>')

# 5. Central KRAS Molecular Switch
label_badge(104.0, 36.5, 'KRAS•GTP (Active)', bg_col='#FFF1F2', border_col='#E11D48', text_col='#991B1B', size=6.0*PT, bold=True)

# Direct KRAS Inhibitors Card (Class I & II) - Positioned gracefully to the left of RAF
card_kras = drug_box(68.0, 57.5, 33.5, 10.5, 'Class I: sotorasib, adagrasib', 'Class II: MRTX1133 (G12D)', 'approved')
D.add('link', '<path d="M101.5 59.0 L97.0 48.0" stroke="#64748B" stroke-width="0.55"/>')
D.add('body', '<line x1="95.5" y1="47.5" x2="98.5" y2="48.5" stroke="#64748B" stroke-width="1.1"/>')

# 6. Downstream Kinase Cascades
# Column 1: MAPK (Blue globes)
label_badge(114.0, 60.5, 'RAF', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8')
label_badge(114.0, 73.5, 'MEK1/2', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8')
label_badge(114.0, 86.5, 'ERK1/2', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8')

card_mek = drug_box(81.5, 70.0, 23.5, 8.0, 'RAF/MEK inh.', 'trametinib, avutometinib', 'approved')
D.add('link', '<line x1="105.0" y1="73.5" x2="108.5" y2="73.5" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="108.5" y1="72.0" x2="108.5" y2="75.0" stroke="#64748B" stroke-width="1.0"/>')

card_erk = drug_box(81.5, 83.0, 23.5, 8.0, 'ERK inh.', 'ulixertinib', 'clinical')
D.add('link', '<line x1="105.0" y1="86.5" x2="108.5" y2="86.5" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="108.5" y1="85.0" x2="108.5" y2="88.0" stroke="#64748B" stroke-width="1.0"/>')

# Column 2: PI3K-AKT-mTOR (Teal globes)
label_badge(141.5, 61.5, 'PI3K (p110)', bg_col='#F0FDFA', border_col='#0D9488', text_col='#0F766E')
label_badge(141.5, 73.5, 'AKT', bg_col='#F0FDFA', border_col='#0D9488', text_col='#0F766E')
label_badge(141.5, 86.5, 'mTORC1', bg_col='#F0FDFA', border_col='#0D9488', text_col='#0F766E')

card_pi3k = drug_box(153.0, 57.5, 24.0, 8.0, 'PI3K inh.', 'alpelisib, inavolisib', 'approved')
D.add('link', '<line x1="153.0" y1="61.5" x2="148.5" y2="61.5" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="148.5" y1="60.0" x2="148.5" y2="63.0" stroke="#64748B" stroke-width="1.0"/>')

card_mtor = drug_box(153.0, 82.5, 24.0, 8.0, 'mTOR inh.', 'everolimus', 'approved')
D.add('link', '<line x1="153.0" y1="86.5" x2="148.5" y2="86.5" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="148.5" y1="85.0" x2="148.5" y2="88.0" stroke="#64748B" stroke-width="1.0"/>')

# 7. Nuclear Envelope & Nuclear Pore Complex (Bottom Left)
label_badge(14.0, 61.5, 'Nuclear envelope', bg_col='#FAF5FF', border_col='#7C3AED', text_col='#6D28D9', size=4.8*PT)
label_badge(40.0, 66.0, 'Nuclear pore (NPC)', bg_col='#FAF5FF', border_col='#7C3AED', text_col='#6D28D9', size=4.8*PT)
label_badge(36.0, 85.0, 'Translocated ERK (p)', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8', size=4.8*PT)

out_mapk = outcome_box(4.0, 89.5, 29.0, 9.0, 'Proliferation & Survival', 'CCND1, MYC, FOS, ELK1',
                       '#FAF5FF', '#C084FC', '#581C87')

# ============================================================ PANEL B =========
BOT_A = 101.5
D.add('bg', '<line x1="0" y1="%.2f" x2="180" y2="%.2f" stroke="#CBD5E1" stroke-width="0.6"/>'
      % (BOT_A, BOT_A))

BY = 103.5
CW, CG = 43.0, 2.0
BH = 66.0  # Expansive height for full hallmark cards with rich text

CARDS = [
    ('Metabolic Rewiring',
     'Warburg effect & glutaminolysis',
     [
         'Upregulates GLUT1, LDHA & MCT4 lactate efflux',
         'GOT1 & GLS1 flux fuels NADPH redox defense',
         'Drives nucleotide biosynthesis for rapid division',
         'Trial: Phase I/II CB-839 combos in solid tumours',
     ],
     'GOT1, GLS1, MCT4 inh.', 'CB-839, syrosingopine', 'preclinical'),

    ('Macropinocytosis & Autophagy',
     'Nutrient scavenging & lysosomal recycling',
     [
         'RAC1/CDC42 membrane ruffling & bulk fluid uptake',
         'Scavenges extracellular albumin & degraded proteins',
         'Autophagic flux sustains amino acid & lipid pools',
         'Trial: HCQ + trametinib in KRAS-mutant PDAC',
     ],
     'Autophagy / Pinocytosis inh.', 'hydroxychloroquine (HCQ)', 'clinical'),

    ('Immunosuppressive Microenv.',
     'Immune exclusion & myeloid recruitment',
     [
         'Secretes GM-CSF, IL-6 & CXCL1/2 to recruit MDSCs',
         'Upregulates PD-L1; induces CD8+ T-cell exhaustion',
         'Excludes effector lymphocytes from tumour core',
         'Trial: sotorasib/adagrasib + anti-PD-(L)1 regimens',
     ],
     'Anti-PD-(L)1 + RAS vaccines', 'pembrolizumab; mRNA-5671', 'clinical'),

    ('Senescence Bypass',
     'Overcoming oncogenic stress (OIS)',
     [
         'Bypasses OIS barrier via TP53 mutation / CDKN2A loss',
         'CDK4/6 hyperactivation drives RB phosphorylation',
         'Permits uncontrolled mitotic entry & genomic flux',
         'Trial: CDK4/6 inh. + SHP2/KRAS targeted combos',
     ],
     'CDK4/6 inh. & Senolytics', 'palbociclib; navitoclax', 'clinical'),
]

# Panel b Label
D.text(1.0, BY + 3.2, 'b', bold=True, size=PNs, color=INK)

for k, (title, sub, bullets, drug_title, drug_sub, status) in enumerate(CARDS):
    x = k * (CW + CG) + 1.0
    # Card Background with subtle shadow
    D.add('bg', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2.2" '
                'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>'
          % (x, BY, CW, BH))
    
    # Embed 3D AI Artwork (aspect ratio 16:9, height 23.5mm)
    if k in HALLMARK_B64:
        D.add('body', '<image href="data:image/jpeg;base64,%s" x="%.2f" y="%.2f" width="%.2f" height="23.50" '
                     'preserveAspectRatio="xMidYMid meet"/>'
              % (HALLMARK_B64[k], x + 1.2, BY + 1.8, CW - 2.4))
        
    # Card Text below image
    ty = BY + 27.5
    D.text(x + 2.2, ty, title, bold=True, color=INK, size=FS)
    D.text(x + 2.2, ty + 3.8, sub, color=ACT_COL, bold=True, size=FS_XS)
    
    # Divider line
    D.add('link', '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#E2E8F0" stroke-width="0.4"/>'
          % (x + 2.0, ty + 5.5, x + CW - 2.0, ty + 5.5))
    
    # Bullet points
    b_y = ty + 7.5
    for b_idx, bullet in enumerate(bullets):
        # Bullet dot
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.6" fill="%s"/>'
              % (x + 3.2, b_y + b_idx * 3.6 - 0.2, GREY))
        D.text(x + 4.8, b_y + b_idx * 3.6, bullet, color=INK_MUTED, size=4.0*PT)
        
    # Drug container box anchored at bottom
    drug_box(x + 1.8, BY + 54.0, CW - 3.6, 9.5, drug_title, drug_sub, status=status)

def main():
    svg_str = D.svg()
    svg_file = os.path.join(FIG, NAME + '.svg')
    png_file = os.path.join(FIG, NAME + '.png')
    pdf_file = os.path.join(FIG, NAME + '.pdf')
    
    with open(svg_file, 'w', encoding='utf-8') as fh:
        fh.write(svg_str)
        
    subprocess.run(['rsvg-convert', '--dpi-x', '400', '--dpi-y', '400', '-b', 'white',
                    '-o', png_file, svg_file], check=True)
                    
    CHROME = os.environ.get('CHROME',
                            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    if os.path.exists(CHROME):
        tmp = tempfile.mkdtemp()
        try:
            html = os.path.join(tmp, 'f.html')
            with open(html, 'w', encoding='utf-8') as fh:
                fh.write('<html><head><style>@page{size:%gmm %gmm;margin:0}html,body{margin:0}'
                         'svg{display:block}</style></head><body>%s</body></html>'
                         % (W, H, svg_str))
            subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                            '--user-data-dir=' + os.path.join(tmp, 'u'),
                            '--print-to-pdf=' + pdf_file,
                            'file://' + html], check=True, capture_output=True)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', pdf_file, svg_file], check=True)
        
    print("Figure 1 (Option 2) rendered successfully:")
    print("  ->", png_file)
    print("  ->", pdf_file)
    print("  ->", svg_file)

    # Sync to all relevant project directories
    for sdir in SYNC_DIRS:
        if os.path.exists(sdir):
            for ext in ('.png', '.pdf', '.svg'):
                src = os.path.join(FIG, NAME + ext)
                dst = os.path.join(sdir, NAME + ext)
                shutil.copy2(src, dst)
            print(f"Synchronized Figure 1 (Option 2) to: {sdir}")

if __name__ == '__main__':
    main()
