#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 1 - The RAS Signalling Network, Feedback Circuits, and Therapeutic Intervention Classes.

Publication-grade medical illustration adhering to ESMO Open / Science / Nature Reviews guidelines.
Key architectural principles:
  1. Ultra-minimalist text: Only essential protein symbols, concise drug badges, and biological outcomes.
     All extended mechanistic narratives and trial details are relocated to the figure legend.
  2. Planar layout with ZERO line crossings: Dedicated vertical columns, isolated feedback corridor, and open distribution buses.
  3. Crisp unambiguous pointers: Every activation arrow and inhibitory T-bar connects cleanly to node boundaries.
     All line endpoints connect strictly to graphical elements (never floating text).
  4. Global T-bar boundary clearance: Inhibitory crossbars stop with a crisp 0.75 mm offset before target element boundaries.
  5. Distinct, verified pharmacological mappings:
     - PI3K inhibitor (alpelisib, inavolisib) specifically targets PI3K (p110)
     - mTOR inhibitor (everolimus, sirolimus) specifically targets mTORC1
     - SOS1 directly catalyzes GDP/GTP nucleotide exchange on KRAS•GDP
  6. Density-driven layout (先下后上): Downstream effectors given expansive breathing room first,
     and plasma membrane receptors dispersed across canvas according to downstream pathway density.
  7. Science / Nature flagship palette: Refined mineral and jewel tones with crisp contrast.
  8. Authentic cellular and biological morphology in Panel B (tumor cell, T cell, mitochondrion, macropinocytosis).
"""

import math
import os
import shutil
import subprocess
import sys
import tempfile
from PIL import ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'vector_figures'))
os.makedirs(FIG, exist_ok=True)
NAME = 'Figure1_RAS_signalling_network'

# Destination directories to synchronize
SYNC_DIRS = [
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件_新配色预览",
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件",
    "/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/New_Color_Theme_Preview",
]
W, H = 180.0, 172.0
PT = 25.4 / 72
FS = 7.0 * PT                             # Standard font size ~7 pt
FS_SM = 6.0 * PT                          # Small font size ~6 pt
FS_XS = 5.0 * PT                          # Extra small badge font size ~5 pt
PNs = 9.5 * PT                            # Panel bold letter size
LH = FS * 1.25                            # Line height

# Strict typography & color scheme
INK = '#0F172A'          # Deep slate black for primary text
INK_MUTED = '#475569'    # Slate for secondary labels
GREY = '#64748B'         # Muted slate grey
WHITE = '#FFFFFF'
BORDER = '#CBD5E1'       # Card & border stroke

# Primary signalling line colors (Nature Standard: Blue = Activation, Grey = Inhibition)
ACT_COL = '#2563EB'      # Royal Blue for activation cascades and forward arrows
INH_COL = '#64748B'      # Neutral Slate Grey for inhibitory T-bars and negative feedback
MUT_COL = '#E11D48'      # Crimson accent for oncogenic mutation blockade

# Functional semantic color palette (Science / Nature Upgraded Palette)
COL = {
    # Receptors (Distinct pastel identities with crisp darker borders)
    'rec_rtk': '#E0F2FE',    # EGFR / RTK: Soft sky cyan
    'rec_int': '#FEF3C7',    # Integrin: Soft warm champagne sand
    'rec_gpcr': '#EDE9FE',   # GPCR: Soft heather amethyst
    'rec_imm': '#FFE4E6',    # Cytokine / Immune R: Soft antique rose coral
    'rec': '#E0F2FE',
    
    # Upstream Adaptors (Light, luminous, readable)
    'adapt': '#F8FAFC',      # GRB2, SHP2, SOS1: Luminous slate
    'gef': '#0D9488',        # Tissue GEFs: Deep teal
    
    # Central Switch
    'off': '#F1F5F9',        # KRAS-GDP (inactive): Cool light grey-slate
    'on': '#FFF1F2',         # KRAS-GTP (active): Soft coral rose
    'gap': '#F8FAFC',        # GAPs (NF1, RASA1): Crisp light neutral
    
    # Effector Cascades (Rich Jewel Spectrum with Crisp White Bold Text)
    'mapk': '#2563EB',       # Column 1 MAPK (RAF, MEK, ERK): Kinase royal cobalt blue
    'rassf': '#4F46E5',      # Column 2 RASSF1A & MST1/2: Apoptotic royal indigo
    'pi3k': '#0D9488',       # Column 3 PI3K-AKT-mTOR: Deep oceanic emerald teal
    'ral': '#0284C7',        # Column 4 RAL cascade: Sky azure blue
    'other': '#D97706',      # Column 5 Cytoskeleton (RAC1, F-actin): Warm golden amber
    'lig': '#EA580C',        # Ligands: Warm burnt terracotta
    'red': '#E11D48',        # Oncogenic accents
}

TC_MAP = {
    'adapt': '#0F172A',      # Deep navy text on luminous slate
    'mapk': WHITE,           # White text on kinase blue
    'pi3k': WHITE,           # White text on emerald teal
    'rassf': WHITE,          # White text on royal indigo
    'ral': WHITE,            # White text on sky azure
    'other': WHITE,          # White text on amber ochre
    'on': '#991B1B',         # Deep crimson on soft coral
    'off': '#334155',        # Slate text on cool grey
    'gap': '#0F172A',        # Deep navy on light neutral
    'rec_rtk': '#0369A1',
    'rec_int': '#92400E',
    'rec_gpcr': '#5B21B6',
    'rec_imm': '#9F1239',
    'rec': '#0F172A',
    'lig': WHITE,
    'gef': WHITE,
}

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

def mix(c, t, f):
    a = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(t[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * f) for x, y in zip(a, b))

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class Doc:
    def __init__(self):
        self.L = {k: [] for k in ('bg', 'mem', 'under', 'link', 'body', 'over', 'text')}
        self.grad = {}

    def add(self, layer, s):
        self.L[layer].append(s)

    def gradient(self, col):
        gid = 'g' + col[1:]
        if gid not in self.grad:
            self.grad[gid] = (
                '<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">'
                '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
                '</linearGradient>'
                % (gid, mix(col, WHITE, 0.12), mix(col, '#000000', 0.18)))
        return 'url(#%s)' % gid

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
                '<defs>%s%s</defs>%s</svg>' % (W, H, W, H, SANS,
                                               ''.join(self.grad.values()), DEFS, body_content))

DEFS = (
    '<linearGradient id="exo" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#F8FAFC"/><stop offset="1" stop-color="#F1F5F9"/>'
    '</linearGradient>'
    '<linearGradient id="cyto" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F8FAFC"/>'
    '</linearGradient>'
    '<radialGradient id="head" cx="0.38" cy="0.32" r="0.75">'
    '<stop offset="0" stop-color="#E2E8F0"/><stop offset="1" stop-color="#94A3B8"/>'
    '</radialGradient>'
    '<radialGradient id="nuc" cx="0.45" cy="0.25" r="0.8">'
    '<stop offset="0" stop-color="#F5F3FF"/><stop offset="1" stop-color="#EDE9FE"/>'
    '</radialGradient>'
    '<clipPath id="clipA"><rect x="0" y="0" width="180" height="124" rx="2.0"/></clipPath>'
    '<filter id="subtle-shadow" x="-3%" y="-3%" width="106%" height="110%">'
    '<feDropShadow dx="0" dy="0.5" stdDeviation="0.6" flood-color="#0F172A" flood-opacity="0.06"/>'
    '</filter>'
)

D = Doc()

def pts_path(pts, close=True):
    return 'M' + ' L'.join('%.2f %.2f' % p for p in pts) + (' Z' if close else '')

def ell_pts(cx, cy, rx, ry, rot=0.0, n=48):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for k in range(n):
        t = 2 * math.pi * k / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out

def body(lobes, col, layer='body', lw=0.32, shadow=True, border_col=None):
    d = ' '.join(pts_path(ell_pts(*lo)) for lo in lobes)
    if shadow:
        D.add(layer, '<path d="%s" fill="#0F172A" fill-opacity="0.05" '
                     'transform="translate(0.20 0.30)"/>' % d)
    bc = border_col or mix(col, '#000000', 0.28)
    fill_col = D.gradient(col) if not col.startswith('#F') else col
    D.add(layer, '<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f" '
                 'stroke-linejoin="round"/>' % (d, fill_col, bc, 2 * lw))

def pill(cx, cy, w, h, label, col_key, rows=None, layer='body', rx=None, border_col=None, text_col=None):
    col = COL[col_key]
    tc = text_col or TC_MAP.get(col_key, INK)
    r = rx if rx is not None else h / 2.0
    bc = border_col or mix(col, '#000000', 0.30)
    # Subtle drop shadow
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="#0F172A" fill-opacity="0.05" transform="translate(0.20 0.30)"/>'
          % (cx - w / 2, cy - h / 2, w, h, r))
    # Pill body
    fill_col = D.gradient(col) if not col.startswith('#F') else col
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.55"/>'
          % (cx - w / 2, cy - h / 2, w, h, r, fill_col, bc))
    rows = rows or [label]
    y0 = cy - (len(rows) - 1) * (LH * 0.95) / 2
    for k, row in enumerate(rows):
        D.text(cx, y0 + k * (LH * 0.95), row, anchor='middle', color=tc, bold=True, size=FS)
    # Return bounding anchors: top, bottom, left, right
    return {
        'top': (cx, cy - h / 2),
        'bottom': (cx, cy + h / 2),
        'left': (cx - w / 2, cy),
        'right': (cx + w / 2, cy),
        'cx': cx, 'cy': cy, 'w': w, 'h': h
    }

def head(p, q, col, size=1.25, layer='link'):
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    a, b = size, size * 0.42
    pts = [q, (q[0] - a * math.cos(ang) + b * math.sin(ang),
               q[1] - a * math.sin(ang) - b * math.cos(ang)),
           (q[0] - a * math.cos(ang) - b * math.sin(ang),
            q[1] - a * math.sin(ang) + b * math.cos(ang))]
    D.add(layer, '<path d="%s" fill="%s"/>' % (pts_path(pts), col))

def arrow(p0, p1, c1=None, c2=None, col=None, lw=0.48, end='head', dash=None,
          layer='link', hs=1.25):
    """Draw connecting lines between elements."""
    if col is None:
        col = INH_COL if end == 'tee' else ACT_COL
    c1 = c1 or p0
    c2 = c2 or p1
    tail = c2 if c2 != p1 else c1 if c1 != p1 else p0
    ang = math.atan2(p1[1] - tail[1], p1[0] - tail[0])
    q = p1
    if end == 'head':
        q = (p1[0] - hs * 0.7 * math.cos(ang), p1[1] - hs * 0.7 * math.sin(ang))
    elif end == 'tee':
        gap = 0.75
        q = (p1[0] - gap * math.cos(ang), p1[1] - gap * math.sin(ang))
    da = ' stroke-dasharray="%s"' % dash if dash else ''
    D.add(layer, '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f" fill="none" '
                 'stroke="%s" stroke-width="%.2f" stroke-linecap="round"%s/>'
          % (p0[0], p0[1], c1[0], c1[1], c2[0], c2[1], q[0], q[1], col, lw, da))
    if end == 'head':
        head(tail, p1, col, hs, layer)
    elif end == 'tee':
        nx, ny = -math.sin(ang), math.cos(ang)
        tw_len = 1.25
        D.add(layer, '<path d="M%.2f %.2f L%.2f %.2f" stroke="%s" stroke-width="%.2f" '
                     'stroke-linecap="round"/>'
              % (q[0] + nx * tw_len, q[1] + ny * tw_len,
                 q[0] - nx * tw_len, q[1] - ny * tw_len, col, lw * 2.0))

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
        D.text(x + 4.8, y + 6.0, subtitle, color=INK_MUTED, size=4.0*PT)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

def outcome_box(x, y, w, h, title, subtitle, bg_col, border_col, title_col):
    """Draw a dedicated container card for cellular hallmarks/endpoints."""
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.8" '
                 'fill="%s" stroke="%s" stroke-width="0.60" filter="url(#subtle-shadow)"/>'
          % (x, y, w, h, bg_col, border_col))
    D.text(x + w / 2.0, y + 2.4, title, anchor='middle', bold=True, size=FS_SM, color=title_col)
    D.text(x + w / 2.0, y + 5.8, subtitle, anchor='middle', size=FS_XS, color=INK_MUTED)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

# ============================================================ PANEL A ========
M = 21.0       # Membrane baseline y
HD = 1.9       # Membrane thickness half-height
BOT_A = 124.0

D.add('bg', '<g clip-path="url(#clipA)">')
D.add('bg', '<rect x="0" y="0" width="180" height="%.2f" fill="url(#exo)"/>' % M)
D.add('bg', '<rect x="0" y="%.2f" width="180" height="%.2f" fill="url(#cyto)"/>'
      % (M, BOT_A - M))
D.add('bg', '</g>')

# Receptor positions along x-axis (Dispersed and spaced according to downstream density)
# EGFR at 20.0, Integrin at 58.0, GPCR at 100.0, Immune R at 136.0
RX = {'rtk': 20.0, 'int': 58.0, 'gpcr': 100.0, 'imm': 136.0}
gaps = []

def helix(x, y0, y1, w=1.2, col=None, border_col=None, layer='body'):
    c = col or COL['rec']
    bc = border_col or mix(c, '#000000', 0.40)
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.30"/>'
           % (x - w / 2, y0, w, y1 - y0, w / 2, D.gradient(c), bc))

# 1. EGFR / RTK Dimer (Nature style: Soft Sky Cyan)
def rtk(cx):
    col = COL['rec_rtk']
    bc = '#0284C7'
    for s in (-1, 1):
        x = cx + s * 2.2
        body([(x + s * 0.3, 8.5, 1.8, 2.4, 0), (x + s * 0.1, 13.5, 1.6, 2.2, 0)], col, border_col=bc, shadow=False)
        helix(x, 15.5, 26.5, w=1.2, col=col, border_col=bc)
        body([(x + s * 0.4, 28.2, 2.2, 1.8, 0)], col, border_col=bc, shadow=False)
        # Phosphotyrosine sites
        D.add('over', '<circle cx="%.2f" cy="%.2f" r="0.75" fill="#EAB308" stroke="#854D0E" stroke-width="0.25"/>'
              % (x + s * 1.3, 30.5))
        D.text(x + s * 1.3, 30.8, 'P', anchor='middle', color='#713F12', bold=True, size=4.5*PT)
    gaps.append((cx - 4.5, cx + 4.5))

# 2. Integrin Heterodimer (Nature style: Soft Warm Champagne Sand)
def integrin(cx):
    col = COL['rec_int']
    bc = '#D97706'
    for s, top in ((-1, 8.2), (1, 9.6)):
        x = cx + s * 1.6
        D.add('body', '<path d="M%.2f %.2f L%.2f %.2f L%.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="1.1" stroke-linecap="round"/>'
              % (x, top + 1.4, x, M + HD + 0.8, x + s * 0.8, 27.2, bc))
        body([(x + s * 0.4, top, 1.9, 1.5, s * 18)], col, border_col=bc, shadow=False)
    # ECM ligand strand (x: cx - 4.5 to cx + 5.5)
    pts = [(cx - 4.5 + k * 0.30, 5.0 + 0.5 * math.sin(k * 0.6)) for k in range(34)]
    D.add('body', '<path d="%s" fill="none" stroke="#94A3B8" stroke-width="0.8" stroke-linecap="round"/>'
          % pts_path(pts, False))
    gaps.append((cx - 3.5, cx + 3.5))

# 3. GPCR 7-TM (Nature style: Soft Heather Amethyst)
def gpcr(cx):
    col = COL['rec_gpcr']
    bc = '#7C3AED'
    xs = [cx - 3.8 + k * 1.25 for k in range(7)]
    for k in range(6):
        y = 16.0 if k % 2 else 26.5
        D.add('body', '<path d="M%.2f %.2f Q%.2f %.2f %.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="0.45"/>'
              % (xs[k], y, (xs[k] + xs[k + 1]) / 2, y + (-1.0 if k % 2 else 1.0),
                 xs[k + 1], y, bc))
    for k, x in enumerate(xs):
        helix(x, 16.2 - (k % 2) * 0.4, 26.5 + (k % 2) * 0.4, w=1.1, col=col, border_col=bc)
    body([(cx + 0.2, 12.8, 1.2, 0.9, 0)], '#FB7185', border_col='#E11D48', shadow=False)
    gaps.append((cx - 5.0, cx + 5.0))

# 4. Cytokine / Immune Receptor (Nature style: Soft Antique Rose Coral)
def immune(cx):
    col = COL['rec_imm']
    bc = '#E11D48'
    for s in (-1, 1):
        x = cx + s * 1.3
        body([(x, 9.2, 1.3, 1.8, 0), (x, 13.6, 1.3, 1.8, 0)], col, border_col=bc, shadow=False)
        helix(x, 15.6, 26.5, w=1.1, col=col, border_col=bc)
    body([(cx, 5.8, 2.2, 1.4, 0)], '#E11D48', border_col='#9F1239', shadow=False)
    gaps.append((cx - 4.5, cx + 4.5))

rtk(RX['rtk'])
integrin(RX['int'])
gpcr(RX['gpcr'])
immune(RX['imm'])

# Distinct matching receptor labels
D.text(RX['rtk'], 2.0, 'EGFR / RTK', anchor='middle', bold=True, color='#0369A1', size=FS)
D.text(RX['int'], 2.0, 'Integrin', anchor='middle', bold=True, color='#92400E', size=FS)
D.text(RX['gpcr'], 2.0, 'GPCR', anchor='middle', bold=True, color='#6D28D9', size=FS)
D.text(RX['imm'], 2.0, 'Immune R', anchor='middle', bold=True, color='#9F1239', size=FS)

# EGF Ligand Node
egf_node = pill(RX['rtk'], 5.2, 8.5, 3.6, 'EGF', 'lig')
arrow(egf_node['bottom'], (RX['rtk'], 7.8), col=ACT_COL, lw=0.50)

# Add gap in lipid bilayer for high-contrast Plasma membrane badge
gaps.append((69.0, 87.0))
# GAP (NF1) is a cytosolic protein recruited to juxtamembrane region, so lipid bilayer is continuous here!

# Lipid bilayer rendering
STEP = 1.36
x = 0.7
while x < 180:
    if not any(a - 0.6 <= x <= b + 0.6 for a, b in gaps):
        for side in (-1, 1):
            y = M + side * HD
            for dx in (-0.25, 0.25):
                D.add('mem', '<path d="M%.2f %.2f Q%.2f %.2f %.2f %.2f" fill="none" '
                             'stroke="#CBD5E1" stroke-width="0.25"/>'
                      % (x + dx, y - side * 0.35, x + dx * 2.0, y - side * 1.0,
                         x + dx, M - side * 0.10))
            D.add('mem', '<circle cx="%.2f" cy="%.2f" r="0.60" fill="url(#head)"/>' % (x, y))
    x += STEP

# Plasma membrane badge (High-contrast label embedded in lipid bilayer)
D.add('body', '<rect x="69.0" y="19.1" width="18.0" height="3.8" rx="1.4" '
             'fill="#FFFFFF" stroke="#64748B" stroke-width="0.45" filter="url(#subtle-shadow)"/>')
D.text(78.0, 21.0, 'Plasma membrane', anchor='middle', color='#0F172A', bold=True, size=4.5*PT)

# Extracellular anti-EGFR antibody callout (ON THE RIGHT OF EGFR per user instruction 3)
card_egfr = drug_box(26.5, 4.2, 22.5, 8.5, 'Anti-EGFR mAbs', 'cetuximab, panitumumab', 'approved', '#0284C7')
arrow(card_egfr['left'], (23.8, card_egfr['left'][1]), end='tee', col=INH_COL, lw=0.55)

# Top Right: Standardization Legend Box (Strictly above membrane)
D.add('bg', '<rect x="147.0" y="1.8" width="32.0" height="16.0" rx="2.0" fill="#FFFFFF" '
            'fill-opacity="0.96" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>')
marker(149.5, 3.6, 'approved')
D.text(152.5, 3.6, 'Approved drug class', color=INK, size=4.2*PT, bold=True)
marker(149.5, 6.6, 'clinical')
D.text(152.5, 6.6, 'Clinical trials (Ph I–III)', color=INK, size=4.2*PT, bold=True)
marker(149.5, 9.6, 'preclinical')
D.text(152.5, 9.6, 'Preclinical / investigational', color=INK, size=4.2*PT, bold=True)
# Activation cascade (Solid Blue Arrow)
arrow((148.0, 12.5), (151.5, 12.5), col=ACT_COL, lw=0.60, layer='over')
D.text(152.5, 12.5, 'Activation cascade (→)', color=ACT_COL, size=4.2*PT, bold=True)
# Inhibition / feedback (Dashed Grey T-bar)
arrow((148.0, 15.2), (151.5, 15.2), end='tee', col=INH_COL, lw=0.60, layer='over')
D.text(152.5, 15.2, 'Inhibition / feedback (--|)', color=INH_COL, size=4.2*PT, bold=True)

# Adaptors & Upstream Modulation: GRB2 -> SHP2 -> SOS1 (Shifted right and spaced out per user instruction 1)
node_grb2 = pill(38.0, 35.0, 11.5, 5.6, 'GRB2', 'adapt')
node_shp2 = pill(58.0, 35.0, 11.5, 5.6, 'SHP2', 'adapt')
node_sos1 = pill(80.0, 35.0, 13.0, 6.0, 'SOS1', 'adapt')

# Blue activation arrows connecting upstream cascade
arrow((RX['rtk'] + 1.3, 30.5), node_grb2['left'],
      c1=(RX['rtk'] + 5.5, 31.0), c2=(node_grb2['left'][0] - 4.5, 35.0),
      col=ACT_COL, lw=0.52)
arrow(node_grb2['right'], node_shp2['left'], col=ACT_COL, lw=0.50)
arrow((RX['int'], 27.2), (node_shp2['cx'], node_shp2['top'][1]), col=ACT_COL, lw=0.50)
arrow(node_shp2['right'], node_sos1['left'], col=ACT_COL, lw=0.50)

# Upstream Inhibitors Card (SHP2 & SOS1) - Narrower width to avoid blocking the feedback dashed line
card_upstream = drug_box(49.0, 44.5, 26.0, 8.8, 'SHP2 / SOS1 inh.', 'TNO155, BI 1701963', 'clinical')
arrow((node_shp2['cx'], card_upstream['top'][1]), node_shp2['bottom'], end='tee', col=INH_COL, lw=0.50)
arrow((card_upstream['right'][0] - 2.5, card_upstream['top'][1]), (76.5, node_sos1['bottom'][1]), end='tee', col=INH_COL, lw=0.50)

# ============================================================ CENTRAL SWITCH ==
# Central switch shifted right: GDP at 104.0, GTP at 136.0 (perfect alignment under GPCR and Immune R)
GDP_X, GTP_X, SW_Y = 104.0, 136.0, 35.5

def ras_node(cx, cy, col_key, nuc_txt):
    col = COL[col_key]
    tc = TC_MAP.get(col_key, INK)
    w, h = 17.0, 9.2
    bc = '#64748B' if col_key == 'off' else '#E11D48'
    fill_col = D.gradient(col)
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="3.5" '
                 'fill="%s" stroke="%s" stroke-width="0.6"/>'
          % (cx - w / 2, cy - h / 2, w, h, fill_col, bc))
    D.text(cx, cy - 1.4, 'KRAS', anchor='middle', color=tc, bold=True, size=6.8*PT)
    nw, nh = 9.2, 3.2
    nuc_bg = '#1E3A8A' if nuc_txt == 'GDP' else '#991B1B'
    nuc_fill = '#EFF6FF' if nuc_txt == 'GDP' else '#FEF2F2'
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.6" '
                 'fill="%s" stroke="%s" stroke-width="0.40"/>'
          % (cx - nw / 2, cy + 0.8, nw, nh, nuc_fill, nuc_bg))
    D.text(cx, cy + 2.5, nuc_txt, anchor='middle', color=nuc_bg, bold=True, size=5.5*PT)
    return {
        'top': (cx, cy - h / 2),
        'bottom': (cx, cy + h / 2),
        'left': (cx - w / 2, cy),
        'right': (cx + w / 2, cy),
        'cx': cx, 'cy': cy, 'w': w, 'h': h
    }

node_gdp = ras_node(GDP_X, SW_Y, 'off', 'GDP')
node_gtp = ras_node(GTP_X, SW_Y, 'on', 'GTP')

# GPCR activation down into KRAS-GDP
arrow((RX['gpcr'], 26.5), (node_gdp['cx'] - 2.0, node_gdp['top'][1]), col=ACT_COL, lw=0.48)

# Blue activation arrow from Immune R to active KRAS-GTP (Straight vertical alignment)
arrow((RX['imm'], 26.5), (node_gtp['cx'], node_gtp['top'][1]), col=ACT_COL, lw=0.48)

# SOS1 DIRECT ACTIVATION OF KRAS-GDP (Spacious blue forward activation arrow)
arrow(node_sos1['right'], node_gdp['left'], col=ACT_COL, lw=0.58)
D.text((node_sos1['right'][0] + node_gdp['left'][0]) / 2, 32.5, 'GEF exchange',
       anchor='middle', color='#1D4ED8', bold=True, size=4.8*PT, halo=True)

# GAP (NF1, RASA1) - Dedicated Cytoplasmic Pill Element (Below plasma membrane in cytosol)
node_gap = pill(120.0, 25.6, 14.5, 4.6, 'GAP (NF1)', 'gap', border_col='#64748B')

# Upper Arc: GTP -> GDP (Hydrolysis, Grey pathway, no redundant 10^5 text per user request)
arrow((GTP_X - 6.0, SW_Y - 4.5), (GDP_X + 6.0, SW_Y - 4.5),
      (GTP_X - 10.0, 29.2), (GDP_X + 10.0, 29.2), col=INH_COL, lw=0.60)
arrow(node_gap['bottom'], (120.0, 29.2), col=ACT_COL, lw=0.50)

# Oncogenic Mutation Blockade Badge Element
D.add('body', '<rect x="111.0" y="31.2" width="18.0" height="3.8" rx="1.4" '
             'fill="#FFF1F2" stroke="#E11D48" stroke-width="0.45"/>')
D.text(120.0, 33.0, 'G12/G13/Q61 lock', anchor='middle', color='#991B1B', bold=True, size=4.8*PT)
arrow((120.0, 31.2), (120.0, 29.6), end='tee', col=INH_COL, lw=0.55)

# Lower Arc: GDP -> GTP (GEF Exchange, Blue activation cycle)
arrow((GDP_X + 6.0, SW_Y + 4.5), (GTP_X - 6.0, SW_Y + 4.5),
      (GDP_X + 10.0, 44.5), (GTP_X - 10.0, 44.5), col=ACT_COL, lw=0.60)
D.text(120.0, 46.8, 'GDP → GTP cycle', anchor='middle', color='#2563EB', bold=True, size=4.8*PT, halo=True)

# ============================================================ DIRECT DRUGS ====
# Class I & II docked to RAS-GDP (Bottom of RAS-GDP, centered at 104.0)
D.add('body', '<rect x="86.0" y="49.0" width="36.0" height="10.5" rx="1.8" fill="#FFFFFF" '
             'fill-opacity="0.96" stroke="#94A3B8" stroke-width="0.50" filter="url(#subtle-shadow)"/>')
marker(88.5, 51.6, 'approved', s=0.85)
D.text(91.0, 51.6 - FS_SM * 0.35, 'Class I: sotorasib, adagrasib', color=INK, bold=True, size=FS_SM)
marker(88.5, 56.2, 'clinical', s=0.85)
D.text(91.0, 56.2 - FS_SM * 0.35, 'Class II: MRTX1133 (G12D)', color=INK, bold=True, size=FS_SM)
arrow((node_gdp['cx'], 49.0), node_gdp['bottom'], end='tee', col=INH_COL, lw=0.55)

# Class III & IV docked to RAS-GTP (Right side of RAS-GTP, clean 2-line layout without CYPA note per user request)
D.add('body', '<rect x="146.5" y="30.5" width="32.5" height="10.0" rx="1.8" fill="#FFFFFF" '
             'fill-opacity="0.96" stroke="#E11D48" stroke-width="0.50" filter="url(#subtle-shadow)"/>')
marker(149.0, 33.2, 'clinical', s=0.85)
D.text(151.5, 33.2 - FS_SM * 0.35, 'Class III: daraxonrasib', color=INK, bold=True, size=5.5*PT)

marker(149.0, 37.8, 'clinical', s=0.85)
D.text(151.5, 37.8 - FS_SM * 0.35, 'Class IV: ASP3082 (PROTAC)', color=INK, bold=True, size=5.5*PT)
arrow((146.5, node_gtp['cy']), node_gtp['right'], end='tee', col=INH_COL, lw=0.55)

# ============================================================ EFFECTOR BUS ====
BUS_Y = 62.0
# Spaced out columns ensuring completely relaxed downstream breathing room
BUS_X = {'mapk': 18.0, 'rassf': 60.0, 'pi3k': 88.0, 'ral': 132.0, 'cyto': 164.0}

# Drop from active KRAS-GTP to horizontal bus
arrow(node_gtp['bottom'], (node_gtp['cx'], BUS_Y), end='none', col=ACT_COL, lw=0.65)
D.text(node_gtp['cx'] - 1.5, BUS_Y - 1.2, 'effector recruitment', anchor='end', color='#1D4ED8', bold=True, size=5.5*PT)

# Horizontal distribution bus spanning across the 5 functional lanes
D.add('link', '<path d="M%.2f %.2f L%.2f %.2f" stroke="%s" stroke-width="0.55"/>'
      % (BUS_X['mapk'], BUS_Y, BUS_X['cyto'], BUS_Y, ACT_COL))

# Perpendicular downward branches into each effector column
for k, x in BUS_X.items():
    arrow((x, BUS_Y), (x, 67.4), col=ACT_COL, lw=0.55)

# ============================================================ EFFECTOR COLUMNS =
T1, T2, T3 = 70.5, 83.5, 96.5

# Column 1: MAPK Pathway (x = 18.0)
node_raf = pill(BUS_X['mapk'], T1, 16.0, 6.2, 'RAF', 'mapk')
node_mek = pill(BUS_X['mapk'], T2, 14.0, 5.8, 'MEK1/2', 'mapk')
node_erk = pill(BUS_X['mapk'], T3, 14.0, 5.8, 'ERK1/2', 'mapk')

arrow(node_raf['bottom'], node_mek['top'], col=ACT_COL)
arrow(node_mek['bottom'], node_erk['top'], col=ACT_COL)

# MAPK drug callout cards (x: 26.0 - 45.5, ample clearance to Column 2)
card_raf_mek = drug_box(26.0, 79.5, 19.5, 8.0, 'RAF / MEK inh.', 'trametinib, encorafenib', 'approved')
arrow(card_raf_mek['left'], node_mek['right'], end='tee', col=INH_COL, lw=0.50)

card_erk = drug_box(26.0, 92.5, 19.5, 8.0, 'ERK inh.', 'ulixertinib (Ph I/II)', 'clinical')
arrow(card_erk['left'], node_erk['right'], end='tee', col=INH_COL, lw=0.50)

# ============================================================ NUCLEAR ENVELOPE & NUCLEAR PORE ====
NCX, NCY = 18.0, 126.0
NRX, NRY = 28.0, 21.5
PORE_X1, PORE_X2 = 14.5, 21.5
PORE_Y = 104.5

# Nucleoplasm base fill
D.add('bg', '<g clip-path="url(#clipA)">')
D.add('bg', '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="url(#nuc)"/>'
      % (NCX, NCY, NRX, NRY))

# Double membrane nuclear envelope with open pore channel at x in [PORE_X1, PORE_X2]
D.add('bg', '<path d="M %.2f %.2f A %.2f %.2f 0 0 0 0.0 %.2f '
             'M %.2f %.2f A %.2f %.2f 0 0 1 46.0 %.2f" '
             'fill="none" stroke="#7C3AED" stroke-width="0.55"/>'
      % (PORE_X1, PORE_Y, NRX, NRY, NCY + 5.0, PORE_X2, PORE_Y, NRX, NRY, NCY + 5.0))
D.add('bg', '<path d="M %.2f %.2f A %.2f %.2f 0 0 0 0.0 %.2f '
             'M %.2f %.2f A %.2f %.2f 0 0 1 44.5 %.2f" '
             'fill="none" stroke="#9333EA" stroke-width="0.45" stroke-dasharray="2.5 1.0"/>'
      % (PORE_X1, PORE_Y + 1.2, NRX - 1.2, NRY - 1.2, NCY + 5.0, PORE_X2, PORE_Y + 1.2, NRX - 1.2, NRY - 1.2, NCY + 5.0))
D.add('bg', '<path d="M %.2f %.2f C %.2f %.2f %.2f %.2f %.2f %.2f" fill="none" stroke="#7C3AED" stroke-width="0.55"/>'
      % (PORE_X1, PORE_Y, PORE_X1 - 0.8, PORE_Y + 0.3, PORE_X1 - 0.8, PORE_Y + 0.9, PORE_X1, PORE_Y + 1.2))
D.add('bg', '<path d="M %.2f %.2f C %.2f %.2f %.2f %.2f %.2f %.2f" fill="none" stroke="#7C3AED" stroke-width="0.55"/>'
      % (PORE_X2, PORE_Y, PORE_X2 + 0.8, PORE_Y + 0.3, PORE_X2 + 0.8, PORE_Y + 0.9, PORE_X2, PORE_Y + 1.2))

# Nuclear Pore Complex (NPC) nucleoporin ring scaffold subunits
D.add('body', '<rect x="12.6" y="103.2" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<rect x="12.6" y="105.6" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<circle cx="14.3" cy="105.5" r="0.65" fill="#8B5CF6"/>')
D.add('body', '<rect x="20.0" y="103.2" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<rect x="20.0" y="105.6" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<circle cx="21.7" cy="105.5" r="0.65" fill="#8B5CF6"/>')
D.add('bg', '</g>')

D.text(25.5, 104.5, 'Nuclear pore (NPC)', color='#6D28D9', bold=True, size=4.8*PT, halo=True)
D.text(34.0, 122.0, 'Nucleus', color='#6D28D9', bold=True, size=FS_SM, halo=True)

# Translocated ERK inside Nucleus
node_erk_nuc = pill(BUS_X['mapk'], 110.5, 11.0, 4.8, 'ERK (p)', 'mapk')
arrow(node_erk['bottom'], node_erk_nuc['top'], col=ACT_COL, lw=0.55)

# Outcome Box 1: Proliferation & Cell Cycle (Inside Nucleus)
out_mapk = outcome_box(4.5, 115.5, 27.0, 8.0, 'Proliferation & Growth', 'CCND1, MYC, FOS, ELK1',
                       '#FAF5FF', '#C084FC', '#581C87')
arrow(node_erk_nuc['bottom'], out_mapk['top'], col=ACT_COL, lw=0.55)

# Column 2: Pro-Apoptotic Branch (RASSF1A) (x = 60.0, Nature style Royal Indigo)
node_rassf = pill(BUS_X['rassf'], T1, 15.0, 6.0, 'RASSF1A', 'rassf')
node_mst = pill(BUS_X['rassf'], 87.0, 13.0, 5.8, 'MST1/2', 'rassf')
arrow(node_rassf['bottom'], node_mst['top'], col=ACT_COL)

# Cross-talk: RAF inhibits RASSF1A (Grey inhibitory T-bar)
arrow(node_raf['right'], node_rassf['left'], end='tee', col=INH_COL, lw=0.50)

# Outcome Box 2: Apoptosis (Shifted down, 8.0 mm clearance from MAPK drugs)
out_rassf = outcome_box(51.0, 106.5, 18.0, 8.5, 'Apoptosis', 'MST / YAP1 / p73',
                        '#EEF2FF', '#818CF8', '#312E81')
arrow(node_mst['bottom'], out_rassf['top'], col=ACT_COL, lw=0.55)

# Column 3: PI3K-AKT-mTOR Pathway (x = 88.0, Nature style Deep Emerald Teal)
node_pi3k = pill(BUS_X['pi3k'], T1, 16.0, 6.2, 'PI3K (p110)', 'pi3k')
node_akt = pill(BUS_X['pi3k'], T2, 13.0, 5.8, 'AKT', 'pi3k')
node_mtor = pill(BUS_X['pi3k'], T3, 15.0, 5.8, 'mTORC1', 'pi3k')

arrow(node_pi3k['bottom'], node_akt['top'], col=ACT_COL)
arrow(node_akt['bottom'], node_mtor['top'], col=ACT_COL)

# Separate PI3K & mTOR Inhibitor Cards (x: 98.0 - 119.0)
card_pi3k_inh = drug_box(98.0, 66.5, 21.0, 8.0, 'PI3K inh.', 'alpelisib, inavolisib', 'approved')
arrow(card_pi3k_inh['left'], node_pi3k['right'], end='tee', col=INH_COL, lw=0.50)

card_mtor_inh = drug_box(98.0, 92.5, 21.0, 8.0, 'mTOR inh.', 'everolimus, sirolimus', 'approved')
arrow(card_mtor_inh['left'], node_mtor['right'], end='tee', col=INH_COL, lw=0.50)

# Outcome Box 3: Survival & Growth
out_pi3k = outcome_box(76.0, 108.5, 24.0, 8.5, 'Survival & Growth', 'S6K1, 4E-BP1, glycolysis',
                       '#F0FDFA', '#5EEAD4', '#0F766E')
arrow(node_mtor['bottom'], out_pi3k['top'], col=ACT_COL, lw=0.55)

# Column 4: RAL GTPases (x = 132.0, Nature style Sky Azure)
node_ralgds = pill(BUS_X['ral'], T1, 15.0, 6.0, 'RALGDS', 'ral')
node_ral = pill(BUS_X['ral'], T2, 13.0, 5.8, 'RAL-A/B', 'ral')
node_tbk1 = pill(BUS_X['ral'], T3, 15.0, 5.8, 'TBK1 / Sec5', 'ral')

arrow(node_ralgds['bottom'], node_ral['top'], col=ACT_COL)
arrow(node_ral['bottom'], node_tbk1['top'], col=ACT_COL)

# (Small circles previously on RAL-AB deleted per user instruction 5)

# Outcome Box 4: Vesicle Trafficking
out_ral = outcome_box(120.0, 108.5, 24.0, 8.5, 'Vesicle Trafficking', 'Exocyst & autophagy',
                      '#F0F9FF', '#7DD3FC', '#0284C7')
arrow(node_tbk1['bottom'], out_ral['top'], col=ACT_COL, lw=0.55)

# Column 5: Cytoskeletal Remodelling (PLCε & TIAM1, Nature style Warm Golden Amber)
node_plce = pill(157.0, T1, 12.0, 5.8, 'PLCε', 'other')
node_tiam1 = pill(171.0, T1, 12.0, 5.8, 'TIAM1', 'other')
node_rac1 = pill(BUS_X['cyto'], T2, 16.0, 6.0, 'PKC / RAC1', 'other')

arrow(node_plce['bottom'], (BUS_X['cyto'] - 3.0, node_rac1['top'][1]), col=ACT_COL)
arrow(node_tiam1['bottom'], (BUS_X['cyto'] + 3.0, node_rac1['top'][1]), col=ACT_COL)

# F-actin Assembly Node
node_actin = pill(BUS_X['cyto'], T3, 21.0, 5.8, 'F-actin assembly', 'other')
arrow(node_rac1['bottom'], node_actin['top'], col=ACT_COL)

# Outcome Box 5: Motility & Invasion
out_cyto = outcome_box(152.0, 108.5, 24.0, 8.5, 'Motility & Invasion', 'Actin dynamics & migration',
                       '#FFFBEB', '#FCD34D', '#B45309')
arrow(node_actin['bottom'], out_cyto['top'], col=ACT_COL, lw=0.55)

# ============================================================ FEEDBACK LOOP ===
# Dedicated planar feedback corridor with ZERO crossings
FX = 4.5
arrow(node_erk['left'], (FX, node_erk['cy']), end='none', col=INH_COL, dash='1.2 0.8', lw=0.6)
arrow((FX, node_erk['cy']), (FX, 19.5), end='none', col=INH_COL, dash='1.2 0.8', lw=0.6)

# Branch 1 to RAF: From corridor straight into RAF left border
arrow((FX, node_raf['cy']), node_raf['left'], end='tee', col=INH_COL, dash='1.2 0.8', lw=0.6)

# Branch 2 to SOS1: Passing cleanly beneath card_upstream at y=56.5 to avoid crossing SHP2 drug line
arrow((FX, 56.5), (82.5, 56.5), end='none', col=INH_COL, dash='1.2 0.8', lw=0.6)
arrow((82.5, 56.5), (82.5, node_sos1['bottom'][1]), end='tee', col=INH_COL, dash='1.2 0.8', lw=0.6)

# Branch 3 to EGFR: Straight into intracellular tail of EGFR at x=16.0
arrow((FX, 19.5), (RX['rtk'] - 4.0, 19.5), end='tee', col=INH_COL, dash='1.2 0.8', lw=0.6)

# Minimalist label along the feedback corridor
D.text(FX + 1.6, 54.0, 'ERK negative feedback', color=INH_COL, bold=True, size=5.5*PT)

# Panel a Letter
D.text(1.0, 2.5, 'a', bold=True, size=PNs, color=INK)

# ============================================================ PANEL B =========
D.add('bg', '<line x1="0" y1="%.2f" x2="180" y2="%.2f" stroke="#E2E8F0" stroke-width="0.6"/>'
      % (BOT_A, BOT_A))

BY = 126.0
CW, CG = 43.0, 2.0
BH = 44.0

CARDS = [
    ('Metabolic Rewiring',
     'Glycolysis & glutaminolysis',
     'Macromolecule scavenging & nutrient flux',
     'GOT1, GLS1, MCT4 inh.', 'preclinical'),
    ('Macropinocytosis & Autophagy',
     'Nutrient scavenging & recycling',
     'Lysosomal degradation sustains viability',
     'Hydroxychloroquine (HCQ)', 'clinical'),
    ('Immunosuppressive Microenv.',
     'Immune exclusion & myeloid influx',
     'MDSC influx & PD-L1 upregulation',
     'Anti-PD-(L)1; RAS vaccines', 'clinical'),
    ('Senescence Bypass',
     'Escape from oncogenic stress',
     'Bypasses OIS barrier via TP53/CDKN2A loss',
     'Senolytics; CDK4/6 inh.', 'preclinical'),
]

# ============================================================ HIGH-END BIOLOGICAL ILLUSTRATIONS (PANEL B) ====
# Fully redesigned per user instruction 4: authentic cellular morphology, tumor cell, T cell, mitochondrion, macropinosome
# All icons strictly contained within y in [BY + 1.0, BY + 16.0] to maintain zero collision with card text (y >= BY + 19.5).

def icon_metabolic(x, y):
    """Authentic mitochondrion with double membrane & cristae, alongside glycolysis & glutamine flux."""
    # Outer mitochondrial membrane (bean shape)
    mx, my, mrx, mry = x + 27.0, y + 8.0, 10.5, 5.6
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="#FFFBEB" stroke="#D97706" stroke-width="0.65"/>'
          % (mx, my, mrx, mry))
    # Inner mitochondrial matrix
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="#FEF3C7" stroke="#B45309" stroke-width="0.40"/>'
          % (mx, my, mrx - 1.1, mry - 0.9))
    # Cristae folds (invaginations alternating from top and bottom)
    for cx_off in (-6.0, -2.0, 2.0, 6.0):
        # Top fold
        D.add('body', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#92400E" stroke-width="0.55" stroke-linecap="round"/>'
              % (mx + cx_off - 0.8, my - 3.2, mx + cx_off, my - 0.4))
        # Bottom fold
        D.add('body', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#92400E" stroke-width="0.55" stroke-linecap="round"/>'
              % (mx + cx_off + 1.0, my + 3.2, mx + cx_off + 0.2, my + 0.4))
    
    # Glucose transporter & glycolysis flux
    D.add('body', '<rect x="%.2f" y="%.2f" width="4.0" height="2.0" rx="0.6" fill="#EFF6FF" stroke="#2563EB" stroke-width="0.35"/>'
          % (x + 2.0, y + 2.2))
    D.text(x + 4.0, y + 3.2, 'GLUT', anchor='middle', color='#1D4ED8', bold=True, size=3.5*PT)
    D.text(x + 1.5, y + 1.2, 'Glucose', color='#1D4ED8', bold=True, size=3.8*PT)
    
    # Glycolytic flux arrow curving to lactate & pyruvate
    D.add('link', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f" fill="none" stroke="#2563EB" stroke-width="0.50"/>'
          % (x + 4.0, y + 4.5, x + 4.0, y + 8.5, x + 6.5, y + 9.5, x + 9.5, y + 9.5))
    head((x + 7.5, y + 9.5), (x + 9.5, y + 9.5), '#2563EB', 0.9, 'body')
    D.text(x + 4.2, y + 7.5, 'Glycolysis', color='#2563EB', bold=True, size=3.4*PT)
    
    # Lactate efflux (Warburg effect)
    D.add('link', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#DC2626" stroke-width="0.45"/>'
          % (x + 9.5, y + 11.2, x + 2.0, y + 13.0))
    head((x + 4.0, y + 12.6), (x + 2.0, y + 13.0), '#DC2626', 0.8, 'body')
    D.text(x + 1.8, y + 14.8, 'Lactate', color='#DC2626', bold=True, size=3.6*PT)
    
    # Glutamine flux entering mitochondrion
    arrow((x + 7.5, y + 3.0), (mx - 5.5, my - 2.0), col='#D97706', lw=0.45)
    D.text(x + 8.8, y + 2.0, 'Gln', color='#B45309', bold=True, size=3.8*PT)
    
    # ATP energy burst star badge inside mitochondrion
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="1.8" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.30"/>'
          % (mx + 2.5, my + 0.2))
    D.text(mx + 2.5, my + 0.5, 'ATP', anchor='middle', color='#854D0E', bold=True, size=3.2*PT)


def icon_macro(x, y):
    """Macropinocytic cup & autophagosome fusing with lysosome."""
    # 1. Macropinocytic cup (Plasma membrane ruffle engulfing fluid/protein cargo)
    D.add('body', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f '
                 'C%.2f %.2f %.2f %.2f %.2f %.2f '
                 'C%.2f %.2f %.2f %.2f %.2f %.2f" '
                 'fill="none" stroke="#0284C7" stroke-width="0.75" stroke-linecap="round"/>'
          % (x + 1.5, y + 12.5, x + 2.8, y + 3.0, x + 5.5, y + 1.5, x + 8.5, y + 3.8,
             x + 10.2, y + 6.0, x + 10.8, y + 8.0, x + 13.0, y + 8.0,
             x + 15.2, y + 8.0, x + 16.2, y + 3.0, x + 18.5, y + 2.0))
    D.text(x + 2.0, y + 1.2, 'Macropinocytosis', color='#0284C7', bold=True, size=3.8*PT)
    
    # Extracellular protein / albumin droplets being engulfed
    for px, py, pr in ((x + 7.0, y + 4.8, 0.8), (x + 8.8, y + 3.8, 0.7), (x + 7.8, y + 6.6, 0.6)):
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#BAE6FD" stroke="#0284C7" stroke-width="0.25"/>'
              % (px, py, pr))
        
    # Internalized macropinosome vesicle
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="2.0" fill="#F0F9FF" stroke="#0284C7" stroke-width="0.50"/>'
          % (x + 10.8, y + 11.2))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.7" fill="#38BDF8"/>' % (x + 10.8, y + 11.2))
    
    # 2. Autophagosome (double-membrane vesicle enclosing damaged organelle)
    ax, ay = x + 26.0, y + 5.0
    # Outer autophagosome membrane
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="3.6" fill="#F8FAFC" stroke="#64748B" stroke-width="0.45"/>' % (ax, ay))
    # Inner autophagosome membrane
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="2.7" fill="#F1F5F9" stroke="#64748B" stroke-width="0.35" stroke-dasharray="1.2 0.7"/>' % (ax, ay))
    # Cargo inside (damaged organelle fragment)
    D.add('body', '<rect x="%.2f" y="%.2f" width="2.0" height="1.4" rx="0.3" fill="#FCA5A5" stroke="#DC2626" stroke-width="0.25"/>'
          % (ax - 1.0, ay - 0.7))
    D.text(ax, y + 0.8, 'Autophagosome', anchor='middle', color='#475569', bold=True, size=3.5*PT)
    
    # 3. Lysosome fusing with autophagosome -> Autolysosome (Height strictly <= y + 15.5)
    lx, ly = x + 35.5, y + 10.5
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="2.8" fill="#FEF2F2" stroke="#EF4444" stroke-width="0.50"/>' % (lx, ly))
    # Acid hydrolase enzyme granules inside lysosome
    for ex_off, ey_off in ((-0.8, -0.6), (0.7, -0.5), (-0.3, 0.7), (0.8, 0.6)):
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.30" fill="#DC2626"/>' % (lx + ex_off, ly + ey_off))
    D.text(lx, ly + 4.2, 'Lysosome', anchor='middle', color='#DC2626', bold=True, size=3.5*PT)
    
    # Fusion arrow between autophagosome and lysosome
    arrow((ax + 2.2, ay + 2.5), (lx - 1.8, ly - 1.8), col='#EA580C', lw=0.45)


def icon_immune(x, y):
    """Authentic Tumor Cell & Cytotoxic T Cell immune synapse (PD-L1 / PD-1 blockade)."""
    # 1. Tumor Cell (Realistic irregular/pleomorphic cancer cell with membrane ruffles)
    cx_t, cy_t = x + 9.0, y + 7.5
    # Tumor cell pleomorphic membrane path (organic ruffles)
    pts_tumor = [
        (cx_t - 6.2, cy_t - 1.8), (cx_t - 4.8, cy_t - 4.8), (cx_t - 1.8, cy_t - 5.6),
        (cx_t + 2.2, cy_t - 5.2), (cx_t + 4.8, cy_t - 3.8), (cx_t + 6.0, cy_t - 0.8),
        (cx_t + 5.6, cy_t + 2.2), (cx_t + 3.8, cy_t + 4.8), (cx_t + 0.8, cy_t + 5.8),
        (cx_t - 3.0, cy_t + 5.2), (cx_t - 5.6, cy_t + 2.6), (cx_t - 6.4, cy_t + 0.4)
    ]
    D.add('body', '<path d="%s" fill="#FFF1F2" stroke="#E11D48" stroke-width="0.70" filter="url(#subtle-shadow)"/>'
          % pts_path(pts_tumor, True))
    
    # Large, irregular hyperchromatic cancer nucleus with textured chromatin
    pts_nuc = [
        (cx_t - 3.5, cy_t - 0.8), (cx_t - 2.2, cy_t - 3.2), (cx_t + 1.2, cy_t - 3.0),
        (cx_t + 3.2, cy_t - 0.8), (cx_t + 2.4, cy_t + 2.8), (cx_t - 0.8, cy_t + 3.5),
        (cx_t - 3.2, cy_t + 2.2)
    ]
    D.add('body', '<path d="%s" fill="#FEE2E2" stroke="#BE123C" stroke-width="0.40"/>'
          % pts_path(pts_nuc, True))
    # Nucleolus inside cancer cell
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.85" fill="#9F1239"/>' % (cx_t - 0.4, cy_t - 0.2))
    D.text(cx_t, y + 14.8, 'Tumor cell', anchor='middle', color='#9F1239', bold=True, size=4.0*PT)
    
    # PD-L1 surface ligands protruding from tumor cell membrane toward T cell
    D.add('body', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#E11D48" stroke-width="0.60" stroke-linecap="round"/>'
          % (cx_t + 5.6, cy_t - 1.2, cx_t + 8.4, cy_t - 1.2))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.65" fill="#E11D48"/>' % (cx_t + 8.8, cy_t - 1.2))
    
    # 2. Cytotoxic T Cell (CD8+ lymphocyte: spherical, high nuclear:cytoplasm ratio)
    cx_cd8, cy_cd8 = x + 29.5, y + 7.5
    r_cd8 = 5.4
    # Lymphocyte outer plasma membrane
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#EFF6FF" stroke="#2563EB" stroke-width="0.70" filter="url(#subtle-shadow)"/>'
          % (cx_cd8, cy_cd8, r_cd8))
    # Characteristic high nuclear:cytoplasm ratio (large round nucleus filling almost entire cell)
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="0.45"/>'
          % (cx_cd8, cy_cd8, r_cd8 - 1.2))
    # Chromatin shading inside T cell nucleus
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="2.2" ry="1.8" fill="#BFDBFE" stroke="#1E40AF" stroke-width="0.30"/>'
          % (cx_cd8 - 0.4, cy_cd8 - 0.4))
    D.text(cx_cd8, y + 14.8, 'T cell (CD8+)', anchor='middle', color='#1D4ED8', bold=True, size=4.0*PT)
    
    # PD-1 receptor and TCR on T cell surface membrane facing tumor cell
    D.add('body', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#2563EB" stroke-width="0.60" stroke-linecap="round"/>'
          % (cx_cd8 - r_cd8, cy_cd8 - 1.2, cx_cd8 - r_cd8 - 2.6, cy_cd8 - 1.2))
    # Y-shaped receptor head (PD-1)
    D.add('body', '<path d="M%.2f %.2f L%.2f %.2f M%.2f %.2f L%.2f %.2f" stroke="#2563EB" stroke-width="0.50"/>'
          % (cx_cd8 - r_cd8 - 2.6, cy_cd8 - 1.2, cx_cd8 - r_cd8 - 3.7, cy_cd8 - 2.1,
             cx_cd8 - r_cd8 - 2.6, cy_cd8 - 1.2, cx_cd8 - r_cd8 - 3.7, cy_cd8 - 0.3))
    
    # 3. Immunological Synapse Inhibitory T-bar (PD-L1 -| PD-1 Immune Exhaustion)
    syn_x = (cx_t + 8.8 + cx_cd8 - r_cd8 - 3.7) / 2.0
    arrow((cx_t + 8.8, cy_cd8 - 1.2), (cx_cd8 - r_cd8 - 2.0, cy_cd8 - 1.2), end='tee', col=INH_COL, lw=0.55)
    D.text(syn_x, cy_cd8 - 3.5, 'PD-L1 / PD-1', anchor='middle', color='#64748B', bold=True, size=3.6*PT)
    D.text(syn_x, cy_cd8 + 2.8, 'exhaustion', anchor='middle', color='#DC2626', bold=True, size=3.4*PT)


def icon_senescence(x, y):
    """Senescence bypass: OIS growth arrest broken by TP53/CDKN2A loss leading to proliferative mitotic escape."""
    # 1. Enlarged, flattened senescent cell (Oncogene-Induced Senescence / OIS)
    sx, sy = x + 10.5, y + 7.5
    # Flattened "fried-egg" senescent cell contour
    pts_sen = [
        (sx - 7.8, sy - 1.8), (sx - 5.6, sy - 4.8), (sx, sy - 5.6), (sx + 6.0, sy - 4.2),
        (sx + 8.2, sy - 0.8), (sx + 7.0, sy + 4.2), (sx + 0.8, sy + 5.8), (sx - 5.6, sy + 4.8)
    ]
    D.add('body', '<path d="%s" fill="#FAF5FF" stroke="#9333EA" stroke-width="0.60"/>' % pts_path(pts_sen, True))
    # Enlarged senescence nucleus with SAHF (heterochromatin foci dots)
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="3.5" ry="2.4" fill="#F3E8FF" stroke="#7C3AED" stroke-width="0.40"/>'
          % (sx, sy))
    for fx, fy in ((sx - 1.5, sy - 0.6), (sx + 1.2, sy - 0.4), (sx - 0.4, sy + 0.8)):
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.40" fill="#6B21A8"/>' % (fx, fy))
    D.text(sx, y + 14.8, 'Senescent (OIS)', anchor='middle', color='#6B21A8', bold=True, size=3.6*PT)
    
    # 2. Senescence Barrier (p16 / p53 Lock)
    bx = x + 22.5
    D.add('body', '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#E11D48" stroke-width="1.0" stroke-linecap="round"/>'
          % (bx, y + 2.5, bx, y + 12.0))
    D.text(bx - 1.0, y + 7.2, 'p53/p16', anchor='end', color='#E11D48', bold=True, size=3.5*PT)
    
    # Breakthrough / Bypass lightning arrow
    arrow((bx - 2.2, y + 4.2), (bx + 2.6, y + 4.2), col='#DC2626', lw=0.70)
    D.text(bx + 1.0, y + 2.2, 'Loss', color='#DC2626', bold=True, size=3.4*PT)
    
    # 3. Active Proliferating / Dividing Tumor Cells (Mitotic Escape)
    mx1, my1 = x + 29.5, y + 5.0
    mx2, my2 = x + 35.0, y + 9.5
    # Daughter cell 1
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="2.7" ry="2.0" fill="#FFF1F2" stroke="#E11D48" stroke-width="0.50"/>' % (mx1, my1))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.95" fill="#FDA4AF"/>' % (mx1, my1))
    # Daughter cell 2
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="2.7" ry="2.0" fill="#FFF1F2" stroke="#E11D48" stroke-width="0.50"/>' % (mx2, my2))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.95" fill="#FDA4AF"/>' % (mx2, my2))
    # Division spindle / cytokinesis connection
    D.add('body', '<path d="M%.2f %.2f Q%.2f %.2f %.2f %.2f" fill="none" stroke="#E11D48" stroke-width="0.45" stroke-dasharray="1.0 0.7"/>'
          % (mx1 + 1.3, my1 + 0.8, (mx1 + mx2) / 2, (my1 + my2) / 2, mx2 - 1.3, my2 - 0.8))
    D.text(x + 32.5, y + 14.8, 'Mitotic escape', anchor='middle', color='#991B1B', bold=True, size=3.6*PT)

ICONS = [icon_metabolic, icon_macro, icon_immune, icon_senescence]

for k, (title, sub, mech, drug, status) in enumerate(CARDS):
    x = k * (CW + CG) + 1.0
    D.add('bg', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2.2" '
                'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>'
          % (x, BY, CW, BH))
    ICONS[k](x + 1.5, BY + 1.5)
    D.text(x + 2.5, BY + 19.5, title, bold=True, color=INK, size=FS)
    D.text(x + 2.5, BY + 24.0, sub, color=INK_MUTED, bold=True, size=FS_XS)
    D.text(x + 2.5, BY + 28.5, mech, color=GREY, size=FS_XS)
    drug_box(x + 2.0, BY + 34.0, CW - 4.0, 7.5, drug, status=status)

D.text(1.0, BY + 2.5, 'b', bold=True, size=PNs, color=INK)

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
        
    print("Figure 1 rendered successfully:")
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
                dst_newtheme = os.path.join(sdir, NAME + '_newtheme' + ext)
                shutil.copy2(src, dst_newtheme)
            print(f"Synchronized Figure 1 to: {sdir}")
            
    # Also synchronize to legacy Chinese name
    cn_dst = "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件/图1_RAS信号网络与可干预节点-1.png"
    if os.path.exists(os.path.dirname(cn_dst)):
        shutil.copy2(png_file, cn_dst)
        print(f"Synchronized to legacy name: {cn_dst}")

if __name__ == '__main__':
    main()
