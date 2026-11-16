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
FS_SM = 5.6 * PT                          # Small font size ~5.8 pt
FS_XS = 4.6 * PT                          # Extra small badge font size ~4.8 pt
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
              % (x, y, 1.05 * s))
    elif status == 'clinical':
        D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="0.30" fill="#2563EB" stroke="#1D4ED8" stroke-width="0.30"/>'
              % (x - 0.95 * s, y - 0.95 * s, 1.90 * s, 1.90 * s))
    else:
        D.add('body', '<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="#64748B" stroke="#475569" stroke-width="0.30"/>'
              % (x, y - 1.15 * s, x + 1.15 * s, y, x, y + 1.15 * s, x - 1.15 * s, y))

def drug_box(x, y, w, h, title, subtitle=None, status='approved', border_col=BORDER):
    """Draw a dedicated container card for therapeutic interventions."""
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.6" '
                 'fill="#FFFFFF" fill-opacity="0.96" stroke="%s" stroke-width="0.45" filter="url(#subtle-shadow)"/>'
          % (x, y, w, h, border_col))
    my = y + 3.6 if subtitle else y + h / 2.0
    marker(x + 2.4, my, status, s=0.80)
    D.text(x + 4.6, y + 2.3 if subtitle else y + h / 2.0 - FS_SM * 0.35, title,
           bold=True, size=FS_SM, color=INK)
    if subtitle:
        D.text(x + 4.6, y + 5.7, subtitle, color=INK_MUTED, size=3.8*PT)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

def label_badge(cx, cy, text, bg_col='#FFFFFF', border_col='#64748B', text_col='#0F172A', size=FS_SM, bold=True, pad_x=2.8, h=3.8):
    tw_val = tw(text, bold, size)
    w = tw_val + pad_x * 2
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.3" '
                 'fill="%s" fill-opacity="0.95" stroke="%s" stroke-width="0.40" filter="url(#subtle-shadow)"/>'
          % (cx - w / 2, cy - h / 2, w, h, bg_col, border_col))
    D.text(cx, cy - size * 0.35, text, anchor='middle', color=text_col, bold=bold, size=size)
    return {'cx': cx, 'cy': cy, 'w': w, 'h': h, 'left': (cx - w/2, cy), 'right': (cx + w/2, cy), 'top': (cx, cy - h/2), 'bottom': (cx, cy + h/2)}

def outcome_box(x, y, w, h, title, subtitle, bg_col, border_col, title_col):
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.8" '
                 'fill="%s" stroke="%s" stroke-width="0.55" filter="url(#subtle-shadow)"/>'
          % (x, y, w, h, bg_col, border_col))
    D.text(x + w / 2.0, y + 2.5, title, anchor='middle', bold=True, size=FS_SM, color=title_col)
    D.text(x + w / 2.0, y + 6.3, subtitle, anchor='middle', size=FS_XS, color=INK_MUTED)
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
RENDER_H = 100.5
D.add('render', '<image href="data:image/jpeg;base64,%s" x="0.0" y="0.0" width="180.0" height="%.2f" '
                'preserveAspectRatio="xMidYMid meet"/>' % (F1A_B64, RENDER_H))

# Panel a Label
D.text(1.0, 3.2, 'a', bold=True, size=PNs, color=INK)

# 1. Standardization Legend Box (Top Left: x=5.0, y=1.8, w=29.5, h=15.5)
D.add('body', '<rect x="5.0" y="1.8" width="29.5" height="15.5" rx="1.6" fill="#FFFFFF" '
              'fill-opacity="0.96" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>')
marker(7.0, 3.5, 'approved', s=0.75)
D.text(9.2, 3.5, 'Approved drug class', color=INK, size=3.7*PT, bold=True)
marker(7.0, 6.3, 'clinical', s=0.75)
D.text(9.2, 6.3, 'Clinical trials (Ph I–III)', color=INK, size=3.7*PT, bold=True)
marker(7.0, 9.1, 'preclinical', s=0.75)
D.text(9.2, 9.1, 'Preclinical / investigational', color=INK, size=3.7*PT, bold=True)
D.add('link', '<line x1="6.0" y1="11.8" x2="8.5" y2="11.8" stroke="#2563EB" stroke-width="0.55"/>')
D.add('body', '<polygon points="8.5,11.1 9.8,11.8 8.5,12.5" fill="#2563EB"/>')
D.text(10.7, 11.8, 'Activation cascade (→)', color=ACT_COL, size=3.5*PT, bold=True)
D.add('link', '<line x1="6.0" y1="14.3" x2="8.8" y2="14.3" stroke="#64748B" stroke-width="0.55" stroke-dasharray="1.0 0.6"/>')
D.add('body', '<line x1="9.1" y1="13.5" x2="9.1" y2="15.1" stroke="#64748B" stroke-width="0.9"/>')
D.text(10.7, 14.3, 'Inhibition / target (--|)', color=INH_COL, size=3.5*PT, bold=True)

# 2. Cellular Compartment Labels (Left Margin: Plasma membrane & Cytosol)
label_badge(16.5, 21.0, 'Plasma membrane', bg_col='#FFFFFF', border_col='#64748B', text_col='#0F172A', size=4.8*PT)
D.add('link', '<line x1="16.5" y1="22.9" x2="16.5" y2="28.0" stroke="#64748B" stroke-width="0.45"/>')
D.add('body', '<circle cx="16.5" cy="28.0" r="0.4" fill="#64748B"/>')

label_badge(16.5, 34.0, 'Cytosol', bg_col='#F8FAFC', border_col='#94A3B8', text_col='#475569', size=4.6*PT)

# 3. Membrane Receptors
# EGFR / RTK (Centered above EGFR dimer stalk heads at x=41.5)
label_badge(41.5, 3.2, 'EGFR / RTK', bg_col='#F0F9FF', border_col='#0284C7', text_col='#0369A1')

# Anti-EGFR mAb drug callout card (Placed in top-middle open whitespace at x=80.0, y=3.5)
card_egfr = drug_box(80.0, 3.5, 25.5, 8.5, 'Anti-EGFR mAbs', 'cetuximab, panitumumab', 'approved', '#0284C7')
D.add('link', '<path d="M%.2f %.2f L74.0 13.0" stroke="#64748B" stroke-width="0.50" stroke-dasharray="1.2 0.8"/>'
      % (card_egfr['left'][0], card_egfr['left'][1]))
D.add('body', '<line x1="72.8" y1="12.0" x2="75.2" y2="14.0" stroke="#64748B" stroke-width="1.0"/>')

# GPCR (7-TM) (Centered above 7-TM bundle at x=116.0)
label_badge(116.0, 4.5, 'GPCR (7-TM)', bg_col='#FAF5FF', border_col='#7C3AED', text_col='#6D28D9')
D.add('link', '<line x1="116.0" y1="6.4" x2="116.0" y2="12.0" stroke="#7C3AED" stroke-width="0.45"/>')
D.add('body', '<circle cx="116.0" cy="12.0" r="0.4" fill="#7C3AED"/>')

# Integrin (α/β) (Centered above heterodimer at x=148.0)
label_badge(148.0, 3.2, 'Integrin (α/β)', bg_col='#FFFBEB', border_col='#D97706', text_col='#92400E')
D.add('link', '<line x1="148.0" y1="5.1" x2="148.0" y2="8.5" stroke="#D97706" stroke-width="0.45"/>')
D.add('body', '<circle cx="148.0" cy="8.5" r="0.4" fill="#D97706"/>')

# 4. Cytosolic Adaptor Complex (GRB2 • SHP2 • SOS1)
label_badge(54.0, 30.5, 'GRB2', bg_col='#F8FAFC', border_col='#94A3B8', text_col='#0F172A', size=4.8*PT, pad_x=2.0, h=3.4)
label_badge(66.0, 30.5, 'SHP2', bg_col='#F8FAFC', border_col='#94A3B8', text_col='#0F172A', size=4.8*PT, pad_x=2.0, h=3.4)
label_badge(78.0, 30.5, 'SOS1', bg_col='#F8FAFC', border_col='#94A3B8', text_col='#0F172A', size=4.8*PT, pad_x=2.0, h=3.4)

# SHP2 / SOS1 inhibitor drug card (Placed directly below SHP2/SOS1 at x=47.0, y=46.5)
# Zero line crossing: vertical link straight up into SHP2/SOS1
card_shp2 = drug_box(47.0, 46.5, 26.0, 8.5, 'SHP2 / SOS1 inh.', 'TNO155, BI 1701963', 'clinical')
D.add('link', '<line x1="60.0" y1="46.5" x2="60.0" y2="38.5" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="57.5" y1="38.5" x2="62.5" y2="38.5" stroke="#64748B" stroke-width="1.0"/>')

# 5. Central KRAS Molecular Switch & Direct Inhibitors
label_badge(105.0, 33.5, 'KRAS•GTP (Active)', bg_col='#FFF1F2', border_col='#E11D48', text_col='#991B1B', size=5.8*PT, bold=True)

# Direct KRAS Inhibitors Card (Class I & II)
# Placed cleanly below the Switch-II chemical wireframe (y=61.5 > 59.4), leaving the chemical structure 100% visible!
card_kras = drug_box(76.0, 61.5, 27.5, 10.0, 'Class I: sotorasib, adagrasib', 'Class II: MRTX1133 (G12D)', 'approved')
D.add('link', '<line x1="88.0" y1="61.5" x2="88.0" y2="59.0" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="85.5" y1="59.0" x2="90.5" y2="59.0" stroke="#64748B" stroke-width="1.0"/>')

# 6. Downstream Kinase Cascades
# Column 1: MAPK (Blue globes centered at x=114.0)
label_badge(114.0, 64.0, 'RAF', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8', size=5.4*PT, pad_x=2.2, h=3.6)
label_badge(114.0, 76.5, 'MEK1/2', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8', size=5.4*PT, pad_x=2.2, h=3.6)
label_badge(114.0, 89.0, 'ERK1/2', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8', size=5.4*PT, pad_x=2.2, h=3.6)

# MAPK inhibitor drug boxes (smoothly stacked at x=76.0 below card_kras, horizontally aligned to targets)
card_mek = drug_box(76.0, 73.5, 25.5, 8.0, 'RAF/MEK inh.', 'trametinib, avutometinib', 'approved')
D.add('link', '<line x1="%.2f" y1="%.2f" x2="108.5" y2="76.5" stroke="#64748B" stroke-width="0.50"/>'
      % (card_mek['right'][0], card_mek['right'][1]))
D.add('body', '<line x1="108.5" y1="75.0" x2="108.5" y2="78.0" stroke="#64748B" stroke-width="1.0"/>')

card_erk = drug_box(76.0, 84.5, 25.5, 8.0, 'ERK inh.', 'ulixertinib', 'clinical')
D.add('link', '<line x1="%.2f" y1="%.2f" x2="108.5" y2="88.5" stroke="#64748B" stroke-width="0.50"/>'
      % (card_erk['right'][0], card_erk['right'][1]))
D.add('body', '<line x1="108.5" y1="87.0" x2="108.5" y2="90.0" stroke="#64748B" stroke-width="1.0"/>')

# Column 2: PI3K-AKT-mTOR (Teal globes centered at x=141.5)
label_badge(141.5, 64.0, 'PI3K (p110)', bg_col='#F0FDFA', border_col='#0D9488', text_col='#0F766E', size=5.4*PT, pad_x=2.2, h=3.6)
label_badge(141.5, 76.5, 'AKT', bg_col='#F0FDFA', border_col='#0D9488', text_col='#0F766E', size=5.4*PT, pad_x=2.2, h=3.6)
label_badge(141.5, 89.0, 'mTORC1', bg_col='#F0FDFA', border_col='#0D9488', text_col='#0F766E', size=5.4*PT, pad_x=2.2, h=3.6)

# PI3K/mTOR inhibitor drug boxes (placed at x=153.0)
card_pi3k = drug_box(153.0, 59.0, 24.5, 8.0, 'PI3K inh.', 'alpelisib, inavolisib', 'approved')
D.add('link', '<line x1="153.0" y1="63.0" x2="147.5" y2="63.0" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="147.5" y1="61.5" x2="147.5" y2="64.5" stroke="#64748B" stroke-width="1.0"/>')

card_mtor = drug_box(153.0, 84.0, 24.5, 8.0, 'mTOR inh.', 'everolimus', 'approved')
D.add('link', '<line x1="153.0" y1="88.0" x2="147.5" y2="88.0" stroke="#64748B" stroke-width="0.50"/>')
D.add('body', '<line x1="147.5" y1="86.5" x2="147.5" y2="89.5" stroke="#64748B" stroke-width="1.0"/>')

# 7. Nuclear Envelope, Nuclear Pore Complex & Nuclear Translocation (Bottom Left)
# Nuclear envelope callout badge
label_badge(22.0, 56.5, 'Nuclear envelope', bg_col='#FAF5FF', border_col='#7C3AED', text_col='#6D28D9', size=4.6*PT)
D.add('link', '<line x1="22.0" y1="58.4" x2="22.0" y2="64.0" stroke="#7C3AED" stroke-width="0.45"/>')
D.add('body', '<circle cx="22.0" cy="64.0" r="0.4" fill="#7C3AED"/>')

# Nuclear pore (NPC) callout badge (Placed at cx=38.0, cy=62.0 with pointer line down-right to the pore channel)
label_badge(38.0, 62.0, 'Nuclear pore (NPC)', bg_col='#FAF5FF', border_col='#7C3AED', text_col='#6D28D9', size=4.6*PT)
D.add('link', '<path d="M44.5 63.5 L50.0 67.5" stroke="#7C3AED" stroke-width="0.45"/>')
D.add('body', '<circle cx="50.0" cy="67.5" r="0.4" fill="#7C3AED"/>')

# Translocated Nuclear ERK badge placed cleanly to the right of the ribbon protein
label_badge(55.0, 84.0, 'Nuclear p-ERK', bg_col='#EFF6FF', border_col='#2563EB', text_col='#1D4ED8', size=4.8*PT)
D.add('link', '<line x1="48.5" y1="84.0" x2="43.0" y2="84.0" stroke="#2563EB" stroke-width="0.50"/>')
D.add('body', '<polygon points="43.0,83.2 41.5,84.0 43.0,84.8" fill="#2563EB"/>')

# Biological Outcome box placed in clean nucleoplasm (x=5.0, y=85.5)
out_mapk = outcome_box(5.0, 85.5, 27.5, 9.5, 'Proliferation & Survival', 'CCND1, MYC, FOS, ELK1',
                       '#FAF5FF', '#C084FC', '#581C87')
D.add('link', '<path d="M35.0 86.5 L32.5 86.5" stroke="#7C3AED" stroke-width="0.55"/>')
D.add('body', '<polygon points="34.0,85.7 32.5,86.5 34.0,87.3" fill="#7C3AED"/>')

# ============================================================ PANEL B =========
BOT_A = 101.5
D.add('bg', '<line x1="0" y1="%.2f" x2="180" y2="%.2f" stroke="#CBD5E1" stroke-width="0.6"/>'
      % (BOT_A, BOT_A))

BY = 103.5
CW, CG = 43.0, 2.0
BH = 66.0

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
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.6" fill="%s"/>'
              % (x + 3.2, b_y + b_idx * 3.6 - 0.2, GREY))
        D.text(x + 4.8, b_y + b_idx * 3.6, bullet, color=INK_MUTED, size=4.0*PT)
        
    # Drug container box anchored at bottom
    drug_box(x + 1.8, BY + 53.5, CW - 3.6, 10.0, drug_title, drug_sub, status=status)

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
