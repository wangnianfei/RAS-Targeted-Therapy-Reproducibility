#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 1 - The RAS Signalling Network, Feedback Circuits, and Therapeutic Intervention Classes.

Publication-grade medical illustration adhering to ESMO Open / Nature Reviews guidelines.
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
  6. Harmonious spatial balance: Even column distribution across 180 mm canvas without blank voids or congestion.
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

# Physical dimensions (ESMO Open double-column width = 180 mm)
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

# Functional semantic color palette
COL = {
    'rec': '#475569',     # Receptors: Slate steel
    'adapt': '#1E293B',   # Upstream Adaptors (GRB2, SOS1, SHP2): Deep slate navy
    'gef': '#0D9488',     # Tissue GEFs: Deep teal
    'off': '#64748B',     # RAS-GDP (inactive): Slate steel blue
    'on': '#E11D48',      # RAS-GTP (active): Vibrant ruby crimson
    'gap': '#F1F5F9',     # GAPs (NF1, RASA1): Crisp light slate
    'mapk': '#1D4ED8',    # MAPK cascade (RAF, MEK, ERK): Vibrant kinase blue
    'pi3k': '#0F766E',    # PI3K-AKT-mTOR cascade: Deep emerald teal
    'ral': '#0284C7',     # RAL cascade: Sky azure blue
    'other': '#D97706',   # PLCε & TIAM1: Warm amber terracotta
    'lig': '#EA580C',     # Ligands: Warm burnt orange
    'red': '#BE123C',     # Feedback inhibition: Ruby crimson
    'rassf': '#475569',   # RASSF1A (pro-apoptotic): Slate
}

TC_MAP = {
    'adapt': WHITE,
    'mapk': WHITE,
    'pi3k': WHITE,
    'on': WHITE,
    'rec': WHITE,
    'gef': WHITE,
    'ral': WHITE,
    'other': WHITE,
    'rassf': WHITE,
    'off': WHITE,
    'gap': INK,
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

def body(lobes, col, layer='body', lw=0.32, shadow=True):
    d = ' '.join(pts_path(ell_pts(*lo)) for lo in lobes)
    if shadow:
        D.add(layer, '<path d="%s" fill="#0F172A" fill-opacity="0.05" '
                     'transform="translate(0.20 0.30)"/>' % d)
    D.add(layer, '<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f" '
                 'stroke-linejoin="round"/>' % (d, D.gradient(col), mix(col, '#000000', 0.28), 2 * lw))

def pill(cx, cy, w, h, label, col_key, rows=None, layer='body', rx=None, border_col=None):
    col = COL[col_key]
    tc = TC_MAP.get(col_key, INK)
    r = rx if rx is not None else h / 2.0
    bc = border_col or mix(col, '#000000', 0.30)
    # Subtle drop shadow
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="#0F172A" fill-opacity="0.05" transform="translate(0.20 0.30)"/>'
          % (cx - w / 2, cy - h / 2, w, h, r))
    # Pill body
    fill_col = D.gradient(col) if col != '#F1F5F9' else '#F1F5F9'
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

def arrow(p0, p1, c1=None, c2=None, col=INK, lw=0.48, end='head', dash=None,
          layer='link', hs=1.25):
    """Draw connecting lines between elements.
    When end=='tee', crossbar is offset by 0.75 mm before the destination boundary
    so it cleanly avoids overlapping with the destination element's border stroke.
    """
    c1 = c1 or p0
    c2 = c2 or p1
    tail = c2 if c2 != p1 else c1 if c1 != p1 else p0
    ang = math.atan2(p1[1] - tail[1], p1[0] - tail[0])
    q = p1
    if end == 'head':
        q = (p1[0] - hs * 0.7 * math.cos(ang), p1[1] - hs * 0.7 * math.sin(ang))
    elif end == 'tee':
        # 0.75 mm crisp buffer outside the element boundary
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
        tw_len = 1.6
        D.add(layer, '<path d="M%.2f %.2f L%.2f %.2f" stroke="%s" stroke-width="%.2f" '
                     'stroke-linecap="round"/>'
              % (q[0] + nx * tw_len, q[1] + ny * tw_len,
                 q[0] - nx * tw_len, q[1] - ny * tw_len, col, lw * 2.2))

def marker(x, y, status, s=1.0):
    if status == 'approved':
        # Green solid circle
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#16A34A" stroke="#15803D" stroke-width="0.30"/>'
              % (x, y, 1.10 * s))
    elif status == 'clinical':
        # Blue solid square
        D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="0.30" fill="#2563EB" stroke="#1D4ED8" stroke-width="0.30"/>'
              % (x - 1.0 * s, y - 1.0 * s, 2.0 * s, 2.0 * s))
    else:
        # Slate solid diamond
        D.add('body', '<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="#64748B" stroke="#475569" stroke-width="0.30"/>'
              % (x, y - 1.20 * s, x + 1.20 * s, y, x, y + 1.20 * s, x - 1.20 * s, y))

def drug_box(x, y, w, h, title, subtitle=None, status='approved', border_col=BORDER):
    """Draw a dedicated, self-contained container card for therapeutic interventions."""
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.6" '
                 'fill="#FFFFFF" fill-opacity="0.96" stroke="%s" stroke-width="0.50" filter="url(#subtle-shadow)"/>'
          % (x, y, w, h, border_col))
    # Marker dot
    my = y + 3.8 if subtitle else y + h / 2.0
    marker(x + 3.2, my, status, s=0.9)
    # Title
    D.text(x + 5.6, y + 2.5 if subtitle else y + h / 2.0 - FS * 0.35, title,
           bold=True, size=FS_SM, color=INK)
    # Subtitle
    if subtitle:
        D.text(x + 5.6, y + 6.0, subtitle, color=INK_MUTED, size=FS_XS)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

def outcome_box(x, y, w, h, title, subtitle, bg_col, border_col, title_col):
    """Draw a dedicated, distinct container card for cellular hallmarks/endpoints."""
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

# Receptor positions along x-axis
RX = {'rtk': 28.0, 'int': 56.0, 'gpcr': 84.0, 'imm': 112.0}
gaps = []

def helix(x, y0, y1, w=1.2, col=COL['rec'], layer='body'):
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.25"/>'
           % (x - w / 2, y0, w, y1 - y0, w / 2, D.gradient(col), mix(col, '#000000', 0.40)))

# 1. EGFR / RTK Dimer
def rtk(cx):
    for s in (-1, 1):
        x = cx + s * 2.2
        body([(x + s * 0.3, 8.5, 1.8, 2.4, 0), (x + s * 0.1, 13.5, 1.6, 2.2, 0)], COL['rec'], shadow=False)
        helix(x, 15.5, 26.5, w=1.2)
        body([(x + s * 0.4, 28.2, 2.2, 1.8, 0)], COL['rec'], shadow=False)
        # Phosphotyrosine sites
        D.add('over', '<circle cx="%.2f" cy="%.2f" r="0.75" fill="#EAB308" stroke="#854D0E" stroke-width="0.25"/>'
              % (x + s * 1.3, 30.5))
        D.text(x + s * 1.3, 30.8, 'P', anchor='middle', color='#713F12', bold=True, size=4.5*PT)
    gaps.append((cx - 3.5, cx + 3.5))

# 2. Integrin Heterodimer
def integrin(cx):
    for s, top in ((-1, 8.2), (1, 9.6)):
        x = cx + s * 1.6
        D.add('body', '<path d="M%.2f %.2f L%.2f %.2f L%.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="1.1" stroke-linecap="round"/>'
              % (x, top + 1.4, x, M + HD + 0.8, x + s * 0.8, 27.2, mix(COL['rec'], '#000000', 0.20)))
        body([(x + s * 0.4, top, 1.9, 1.5, s * 18)], COL['rec'], shadow=False)
    # ECM ligand strand
    pts = [(cx - 6 + k * 0.35, 5.0 + 0.5 * math.sin(k * 0.6)) for k in range(35)]
    D.add('body', '<path d="%s" fill="none" stroke="#94A3B8" stroke-width="0.8" stroke-linecap="round"/>'
          % pts_path(pts, False))
    gaps.append((cx - 2.5, cx + 2.5))

# 3. GPCR 7-TM
def gpcr(cx):
    xs = [cx - 3.8 + k * 1.25 for k in range(7)]
    for k in range(6):
        y = 16.0 if k % 2 else 26.5
        D.add('body', '<path d="M%.2f %.2f Q%.2f %.2f %.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="0.45"/>'
              % (xs[k], y, (xs[k] + xs[k + 1]) / 2, y + (-1.0 if k % 2 else 1.0),
                 xs[k + 1], y, mix(COL['rec'], '#000000', 0.35)))
    for k, x in enumerate(xs):
        helix(x, 16.2 - (k % 2) * 0.4, 26.5 + (k % 2) * 0.4, w=1.1)
    body([(cx + 0.2, 12.8, 1.2, 0.9, 0)], COL['lig'], shadow=False)
    gaps.append((cx - 4.5, cx + 4.5))

# 4. Cytokine / Immune Receptor
def immune(cx):
    for s in (-1, 1):
        x = cx + s * 1.3
        body([(x, 9.2, 1.3, 1.8, 0), (x, 13.6, 1.3, 1.8, 0)], COL['rec'], shadow=False)
        helix(x, 15.6, 26.5, w=1.1)
    body([(cx, 5.8, 2.2, 1.4, 0)], '#BE123C', shadow=False)
    gaps.append((cx - 4.0, cx + 4.0))

rtk(RX['rtk'])
integrin(RX['int'])
gpcr(RX['gpcr'])
immune(RX['imm'])

# Receptor labels
D.text(RX['rtk'], 2.0, 'EGFR / RTK', anchor='middle', bold=True, color=INK, size=FS)
D.text(RX['int'], 2.0, 'Integrin', anchor='middle', bold=True, color=INK, size=FS)
D.text(RX['gpcr'], 2.0, 'GPCR', anchor='middle', bold=True, color=INK, size=FS)
D.text(RX['imm'], 2.0, 'Immune R', anchor='middle', bold=True, color=INK, size=FS)

# EGF Ligand Node (explicit pill element)
egf_node = pill(RX['rtk'], 5.2, 9.0, 3.8, 'EGF', 'lig')
# Arrow from EGF ligand to EGFR extracellular domain
arrow(egf_node['bottom'], (RX['rtk'], 7.8), col='#EA580C', lw=0.50)

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

D.text(178.5, 17.0, 'Plasma membrane', anchor='end', color=GREY, bold=True, size=FS_SM)

# Extracellular anti-EGFR antibody callout (Distinct Drug Card Element)
card_egfr = drug_box(1.5, 4.5, 21.0, 8.5, 'Anti-EGFR mAbs', 'cetuximab, panitumumab', 'approved', '#BE123C')
# Inhibitory T-bar from right edge of drug card straight to EGFR extracellular domain (offset by 0.75mm)
arrow(card_egfr['right'], (RX['rtk'] - 2.8, card_egfr['right'][1]), end='tee', col='#BE123C', lw=0.55)

# Top Right: Standardization Legend Box
D.add('bg', '<rect x="135.0" y="1.5" width="43.5" height="18.5" rx="2.0" fill="#FFFFFF" '
            'fill-opacity="0.95" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>')
marker(138.0, 4.5, 'approved')
D.text(141.0, 4.5, 'Approved drug class', color=INK, size=FS_XS, bold=True)
marker(138.0, 8.5, 'clinical')
D.text(141.0, 8.5, 'Clinical trials (Ph I–III)', color=INK, size=FS_XS, bold=True)
marker(138.0, 12.5, 'preclinical')
D.text(141.0, 12.5, 'Preclinical / investigational', color=INK, size=FS_XS, bold=True)
D.add('link', '<path d="M136.5 16.5 L140.0 16.5" stroke="#BE123C" stroke-width="0.65" stroke-dasharray="1.2 0.8"/>')
D.text(141.0, 16.5, 'Negative feedback / inh.', color='#BE123C', size=FS_XS, bold=True)

# Adaptors & Upstream Modulation: GRB2 -> SHP2 -> SOS1 (Linear forward cascade)
node_grb2 = pill(28.0, 35.0, 11.0, 5.6, 'GRB2', 'adapt')
node_shp2 = pill(42.0, 35.0, 11.5, 5.6, 'SHP2', 'adapt')
node_sos1 = pill(56.0, 35.0, 12.5, 6.2, 'SOS1', 'adapt')

# Receptor intracellular tail to adaptor activation
arrow((RX['rtk'], 30.5), (node_grb2['cx'], node_grb2['top'][1]), col=INK_MUTED, lw=0.50)
arrow(node_grb2['right'], node_shp2['left'], col=INK_MUTED, lw=0.50)
arrow((RX['int'], 27.5), (node_shp2['cx'] + 1.0, node_shp2['top'][1]), col=INK_MUTED, lw=0.50)
arrow(node_shp2['right'], node_sos1['left'], col=INK_MUTED, lw=0.50)

# Upstream Inhibitors Card (SHP2 & SOS1) - Dedicated Drug Box Element
card_upstream = drug_box(34.0, 44.5, 32.0, 8.8, 'SHP2 / SOS1 inh.', 'TNO155, BI 1701963', 'clinical', '#2563EB')
# Direct T-bars connecting from card top border to target protein pill boundaries
arrow((node_shp2['cx'], card_upstream['top'][1]), node_shp2['bottom'], end='tee', col=INK, lw=0.48)
arrow((node_sos1['cx'] + 1.5, card_upstream['top'][1]), (node_sos1['cx'] + 1.5, node_sos1['bottom'][1]), end='tee', col=INK, lw=0.48)

# ============================================================ CENTRAL SWITCH ==
GDP_X, GTP_X, SW_Y = 80.0, 112.0, 36.5

def ras_node(cx, cy, col_key, nuc_txt):
    col = COL[col_key]
    tc = TC_MAP.get(col_key, INK)
    # Farnesyl lipid anchor into inner leaflet
    D.add('under', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f" fill="none" '
                   'stroke="%s" stroke-width="0.55" stroke-linecap="round"/>'
          % (cx, cy - 4.5, cx, cy - 7.5, cx, cy - 9.5, cx, M + HD + 0.6, mix(col, '#000000', 0.35)))
    zz = [(cx + (0.4 if k % 2 else -0.4), M + HD + 0.6 - k * 0.7) for k in range(5)]
    D.add('over', '<path d="%s" fill="none" stroke="#D97706" stroke-width="0.50" stroke-linejoin="round"/>'
          % pts_path(zz, False))
    # RAS main G-domain body
    w, h = 17.0, 9.2
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="3.5" '
                 'fill="%s" stroke="%s" stroke-width="0.6"/>'
          % (cx - w / 2, cy - h / 2, w, h, D.gradient(col), mix(col, '#000000', 0.35)))
    D.text(cx, cy - 1.4, 'KRAS', anchor='middle', color=tc, bold=True, size=6.8*PT)
    # Nucleotide badge
    nw, nh = 9.2, 3.2
    nuc_bg = '#1E3A8A' if nuc_txt == 'GDP' else '#991B1B'
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.6" '
                 'fill="#FFFFFF" stroke="%s" stroke-width="0.35"/>'
          % (cx - nw / 2, cy + 0.8, nw, nh, nuc_bg))
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

# SOS1 DIRECT ACTIVATION OF KRAS-GDP (No stray lines! Perfectly connecting element to element)
arrow(node_sos1['right'], node_gdp['left'], col='#0D9488', lw=0.58)
D.text((node_sos1['right'][0] + node_gdp['left'][0]) / 2, 33.2, 'GEF exchange',
       anchor='middle', color='#0F766E', bold=True, size=4.8*PT, halo=True)

# GAP (NF1, RASA1) - Dedicated Pill Element
node_gap = pill(96.0, 20.0, 15.0, 5.0, 'GAP (NF1)', 'gap', border_col='#64748B')

# Upper Arc: GTP -> GDP (Hydrolysis)
arrow((GTP_X - 6.0, SW_Y - 4.5), (GDP_X + 6.0, SW_Y - 4.5),
      (GTP_X - 10.0, 26.5), (GDP_X + 10.0, 26.5), col=INK, lw=0.60)
# GAP stimulation arrow pointing from GAP bottom border straight down to the hydrolysis arc
arrow(node_gap['bottom'], (96.0, 26.5), col='#334155', lw=0.50)
D.text(105.0, 23.5, 'hydrolysis (10⁵×)', anchor='start', color=GREY, bold=True, size=4.8*PT)

# Oncogenic Mutation Blockade Badge Element
D.add('body', '<rect x="86.0" y="30.5" width="20.0" height="4.0" rx="1.4" '
             'fill="#FEE2E2" stroke="#EF4444" stroke-width="0.40"/>')
D.text(96.0, 32.5, 'G12/G13/Q61 lock', anchor='middle', color='#991B1B', bold=True, size=4.8*PT)
# Inhibitory T-bar from mutation lock badge up to the GAP hydrolysis arc
arrow((96.0, 30.5), (96.0, 27.2), end='tee', col='#BE123C', lw=0.55)

# Lower Arc: GDP -> GTP (GEF Exchange)
arrow((GDP_X + 6.0, SW_Y + 4.5), (GTP_X - 6.0, SW_Y + 4.5),
      (GDP_X + 10.0, 44.5), (GTP_X - 10.0, 44.5), col=INK, lw=0.60)
D.text(96.0, 46.8, 'GDP → GTP cycle', anchor='middle', color=GREY, bold=True, size=4.8*PT, halo=True)

# ============================================================ DIRECT DRUGS ====
# Class I & II docked to RAS-GDP (Bottom of RAS-GDP, x: 68-96, y: 49.0-59.5)
D.add('body', '<rect x="66.0" y="49.0" width="36.0" height="11.0" rx="1.8" fill="#FFFFFF" '
             'fill-opacity="0.96" stroke="#94A3B8" stroke-width="0.50" filter="url(#subtle-shadow)"/>')
marker(68.5, 51.8, 'approved', s=0.85)
D.text(71.0, 51.8 - FS_SM * 0.35, 'Class I: sotorasib, adagrasib', color=INK, bold=True, size=FS_SM)
marker(68.5, 56.5, 'clinical', s=0.85)
D.text(71.0, 56.5 - FS_SM * 0.35, 'Class II: MRTX1133 (G12D)', color=INK, bold=True, size=FS_SM)
# Vertical T-bar straight UP from top edge of Drug Box to bottom of KRAS-GDP (zero crossing)
arrow((node_gdp['cx'], 49.0), node_gdp['bottom'], end='tee', col=INK, lw=0.55)

# Class III & IV docked to RAS-GTP (Right side of RAS-GTP, x: 126-174, y: 30.5-42.5)
D.add('body', '<rect x="126.0" y="30.5" width="48.0" height="12.0" rx="1.8" fill="#FFFFFF" '
             'fill-opacity="0.96" stroke="#E11D48" stroke-width="0.50" filter="url(#subtle-shadow)"/>')
marker(128.5, 33.5, 'clinical', s=0.85)
D.text(131.0, 33.5 - FS_SM * 0.35, 'Class III: daraxonrasib', color=INK, bold=True, size=FS_SM)
# CYPA chaperone badge element
D.add('body', '<rect x="163.5" y="31.8" width="8.8" height="3.5" rx="1.6" fill="#EDE9FE" stroke="#8B5CF6" stroke-width="0.35"/>')
D.text(167.9, 33.5, '+ CYPA', anchor='middle', color='#6D28D9', bold=True, size=4.6*PT)

marker(128.5, 38.5, 'clinical', s=0.85)
D.text(131.0, 38.5 - FS_SM * 0.35, 'Class IV: ASP3082 (PROTAC)', color=INK, bold=True, size=FS_SM)
# Horizontal T-bar straight LEFT from left edge of Drug Box to right of KRAS-GTP (zero crossing)
arrow((126.0, node_gtp['cy']), node_gtp['right'], end='tee', col=INK, lw=0.55)

# ============================================================ EFFECTOR BUS ====
# Completely open central corridor at x = 112.0 dropping down to horizontal bus at y = 62.0!
BUS_Y = 62.0
BUS_X = {'mapk': 22.0, 'rassf': 56.0, 'pi3k': 84.0, 'ral': 128.0, 'cyto': 162.0}

# Drop from active KRAS-GTP (Passing cleanly between Class I/II at x<=102 and Class III/IV at x>=126)
arrow(node_gtp['bottom'], (node_gtp['cx'], BUS_Y), end='none', col=INK, lw=0.65)
D.text(node_gtp['cx'] - 1.5, BUS_Y - 1.2, 'effector recruitment', anchor='end', color=GREY, bold=True, size=5.5*PT)

# Horizontal distribution bus spanning across the 5 functional lanes
D.add('link', '<path d="M%.2f %.2f L%.2f %.2f" stroke="%s" stroke-width="0.55"/>'
      % (BUS_X['mapk'], BUS_Y, BUS_X['cyto'], BUS_Y, INK))

# Perpendicular downward branches into each effector column
for k, x in BUS_X.items():
    arrow((x, BUS_Y), (x, 67.4), col=INK, lw=0.55)

# ============================================================ EFFECTOR COLUMNS =
T1, T2, T3 = 70.5, 83.5, 96.5

# Column 1: MAPK Pathway (x = 22.0)
node_raf = pill(BUS_X['mapk'], T1, 16.0, 6.2, 'RAF', 'mapk')
node_mek = pill(BUS_X['mapk'], T2, 14.0, 5.8, 'MEK1/2', 'mapk')
node_erk = pill(BUS_X['mapk'], T3, 14.0, 5.8, 'ERK1/2', 'mapk')

arrow(node_raf['bottom'], node_mek['top'], col=INK)
arrow(node_mek['bottom'], node_erk['top'], col=INK)

# MAPK drug callout cards (Dedicated element containers, centered horizontally with target nodes)
card_raf_mek = drug_box(33.0, 79.5, 18.5, 8.0, 'RAF / MEK inh.', 'trametinib, encorafenib', 'approved')
arrow(card_raf_mek['left'], node_mek['right'], end='tee', col=INK, lw=0.48)

card_erk = drug_box(33.0, 92.5, 18.5, 8.0, 'ERK inh.', 'ulixertinib (Ph I/II)', 'clinical')
arrow(card_erk['left'], node_erk['right'], end='tee', col=INK, lw=0.48)

# Nucleus & Proliferation (Bottom of Column 1)
NCX, NCY, NRX, NRY = 22.0, 130.0, 28.0, 20.0
D.add('bg', '<g clip-path="url(#clipA)">')
D.add('bg', '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="url(#nuc)" stroke="#8B5CF6" stroke-width="0.55"/>'
      % (NCX, NCY, NRX, NRY))
D.add('bg', '</g>')
D.text(38.0, 120.0, 'Nucleus', color='#6D28D9', bold=True, size=FS_SM)

# Translocated ERK inside Nucleus
node_erk_nuc = pill(BUS_X['mapk'], 107.0, 10.5, 4.8, 'ERK (p)', 'mapk')
arrow(node_erk['bottom'], node_erk_nuc['top'], col=INK)

# Outcome Box 1: Proliferation & Cell Cycle (Dedicated Element Container)
out_mapk = outcome_box(8.0, 113.5, 28.0, 8.5, 'Proliferation & Growth', 'CCND1, MYC, FOS, ELK1',
                       '#FAF5FF', '#C084FC', '#581C87')
arrow(node_erk_nuc['bottom'], out_mapk['top'], col='#581C87', lw=0.55)

# Column 2: Pro-Apoptotic Branch (RASSF1A) (x = 56.0)
node_rassf = pill(BUS_X['rassf'], T1, 16.0, 6.0, 'RASSF1A', 'rassf')
node_mst = pill(BUS_X['rassf'], T2, 13.0, 5.8, 'MST1/2', 'rassf')
arrow(node_rassf['bottom'], node_mst['top'], col=INK)

# Cross-talk: RAF inhibits RASSF1A (Horizontal line with T-bar connecting protein elements)
arrow(node_raf['right'], node_rassf['left'], end='tee', col='#BE123C', lw=0.48)

# Outcome Box 2: Apoptosis (Dedicated Element Container)
out_rassf = outcome_box(46.0, 96.0, 20.0, 8.5, 'Apoptosis', 'MST / YAP1 / p73',
                        '#F8FAFC', '#94A3B8', '#334155')
arrow(node_mst['bottom'], out_rassf['top'], col=INK, lw=0.55)

# Column 3: PI3K-AKT-mTOR Pathway (x = 84.0)
node_pi3k = pill(BUS_X['pi3k'], T1, 16.0, 6.2, 'PI3K (p110)', 'pi3k')
node_akt = pill(BUS_X['pi3k'], T2, 13.0, 5.8, 'AKT', 'pi3k')
node_mtor = pill(BUS_X['pi3k'], T3, 15.0, 5.8, 'mTORC1', 'pi3k')

arrow(node_pi3k['bottom'], node_akt['top'], col=INK)
arrow(node_akt['bottom'], node_mtor['top'], col=INK)

# ============================================================ SEPARATE PI3K & mTOR INHIBITOR CARDS ====
# User requirement: PI3K inhibitor specifically inhibits PI3K (p110); mTOR inhibitor specifically inhibits mTORC1!
card_pi3k_inh = drug_box(96.0, 66.5, 21.0, 8.0, 'PI3K inh.', 'alpelisib, inavolisib', 'approved')
arrow(card_pi3k_inh['left'], node_pi3k['right'], end='tee', col=INK, lw=0.48)

card_mtor_inh = drug_box(96.0, 92.5, 21.0, 8.0, 'mTOR inh.', 'everolimus, sirolimus', 'approved')
arrow(card_mtor_inh['left'], node_mtor['right'], end='tee', col=INK, lw=0.48)

# Outcome Box 3: Survival & Growth (Dedicated Element Container)
out_pi3k = outcome_box(71.5, 108.0, 25.0, 8.5, 'Survival & Growth', 'S6K1, 4E-BP1, glycolysis',
                       '#F0FDFA', '#5EEAD4', '#0F766E')
arrow(node_mtor['bottom'], out_pi3k['top'], col='#0F766E', lw=0.55)

# Column 4: RAL GTPases (x = 128.0)
node_ralgds = pill(BUS_X['ral'], T1, 15.0, 6.0, 'RALGDS', 'ral')
node_ral = pill(BUS_X['ral'], T2, 13.0, 5.8, 'RAL-A/B', 'ral')
node_tbk1 = pill(BUS_X['ral'], T3, 15.0, 5.8, 'TBK1 / Sec5', 'ral')

arrow(node_ralgds['bottom'], node_ral['top'], col=INK)
arrow(node_ral['bottom'], node_tbk1['top'], col=INK)

# Vesicle trafficking icons
for k, (vx, vy, r) in enumerate(((138.5, 84.0, 1.8), (143.0, 82.8, 1.5), (147.0, 84.2, 1.3))):
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#EEF2F6" stroke="%s" stroke-width="0.45"/>'
          % (vx, vy, r, COL['ral']))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.30" fill="#2563EB"/>' % (vx, vy))

# Outcome Box 4: Vesicle Trafficking (Dedicated Element Container)
out_ral = outcome_box(115.5, 108.0, 25.0, 8.5, 'Vesicle Trafficking', 'Exocyst & autophagy',
                      '#F0F9FF', '#7DD3FC', '#0284C7')
arrow(node_tbk1['bottom'], out_ral['top'], col='#0284C7', lw=0.55)

# Column 5: Cytoskeletal Remodelling (PLCε & TIAM1)
node_plce = pill(155.0, T1, 12.0, 5.8, 'PLCε', 'other')
node_tiam1 = pill(169.0, T1, 12.0, 5.8, 'TIAM1', 'other')
node_rac1 = pill(BUS_X['cyto'], T2, 16.0, 6.0, 'PKC / RAC1', 'other')

arrow(node_plce['bottom'], (BUS_X['cyto'] - 3.0, node_rac1['top'][1]), col=INK)
arrow(node_tiam1['bottom'], (BUS_X['cyto'] + 3.0, node_rac1['top'][1]), col=INK)

# Actin filament waves
AY = 94.5
for k in range(2):
    y = AY + k * 1.5
    pts = [(150.0 + j * 0.5, y + 0.25 * math.sin(j * 1.1 + k)) for j in range(48)]
    D.add('body', '<path d="%s" fill="none" stroke="#D97706" stroke-width="0.55" stroke-linecap="round"/>'
          % pts_path(pts, False))

# Outcome Box 5: Motility & Invasion (Dedicated Element Container)
out_cyto = outcome_box(149.5, 108.0, 25.0, 8.5, 'Motility & Invasion', 'Actin dynamics & migration',
                       '#FFFBEB', '#FCD34D', '#B45309')
arrow(node_rac1['bottom'], out_cyto['top'], col='#D97706', lw=0.55)

# ============================================================ FEEDBACK LOOP ===
# Far-left corridor: Single clean red dashed line with ZERO line crossings!
FX = 6.0
# Leaves ERK1/2 left border
arrow(node_erk['left'], (FX, node_erk['cy']), end='none', col='#BE123C', dash='1.2 0.8', lw=0.6)
# Travels along vertical corridor
arrow((FX, node_erk['cy']), (FX, 19.5), end='none', col='#BE123C', dash='1.2 0.8', lw=0.6)

# Branch 1 to RAF: From corridor straight into RAF left border
arrow((FX, node_raf['cy']), node_raf['left'], end='tee', col='#BE123C', dash='1.2 0.8', lw=0.6)

# Branch 2 to SOS1: Under GRB2/SHP2 at y=41.5, entering left-side bottom of SOS1 at x = 52.0 (zero overlap with drug T-bar at x=57.5)
arrow((FX, 41.5), (52.0, 41.5), end='none', col='#BE123C', dash='1.2 0.8', lw=0.6)
arrow((52.0, 41.5), (52.0, node_sos1['bottom'][1]), end='tee', col='#BE123C', dash='1.2 0.8', lw=0.6)

# Branch 3 to EGFR: Straight into intracellular tail of EGFR
arrow((FX, 19.5), (RX['rtk'] - 4.5, 19.5), end='tee', col='#BE123C', dash='1.2 0.8', lw=0.6)

# Minimalist label along the feedback corridor
D.text(FX + 1.8, 54.0, 'ERK negative feedback', color='#BE123C', bold=True, size=5.8*PT)

# Panel a Letter
D.text(1.0, 2.5, 'a', bold=True, size=PNs, color=INK)

# ============================================================ PANEL B =========
# Dividing hairline
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

def icon_metabolic(x, y):
    # Mitochondrion with cristae
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="9.5" ry="5.8" fill="%s" stroke="%s" stroke-width="0.75"/>'
          % (x + 12.0, y + 8.0, mix(COL['other'], WHITE, 0.85), COL['other']))
    pts = [(x + 4.5 + k * 1.5, y + 8.0 + 3.0 * math.sin(k * 1.2)) for k in range(11)]
    D.add('body', '<path d="%s" fill="none" stroke="%s" stroke-width="0.55"/>'
          % (pts_path(pts, False), mix(COL['other'], '#000000', 0.20)))
    # Nutrient influx arrow
    arrow((x + 2.0, y + 2.0), (x + 6.0, y + 6.0), col=COL['other'], lw=0.55)
    D.text(x + 1.0, y + 1.5, 'Glc/Gln', color=COL['other'], bold=True, size=FS_XS)

def icon_macro(x, y):
    # Membrane ruffle & vesicle engulfment
    D.add('body', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f" '
                 'fill="none" stroke="%s" stroke-width="0.80"/>'
          % (x + 2.0, y + 12.0, x + 6.0, y + 2.0, x + 12.0, y + 1.5, x + 16.0, y + 6.0,
             x + 20.0, y + 10.5, x + 26.0, y + 11.5, x + 30.0, y + 3.0, COL['ral']))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="3.2" fill="%s" stroke="%s" stroke-width="0.55"/>'
          % (x + 15.0, y + 9.5, mix(COL['ral'], WHITE, 0.85), COL['ral']))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="1.0" fill="%s"/>'
          % (x + 15.0, y + 9.5, COL['ral']))

def icon_immune(x, y):
    # Cancer cell expressing PD-L1 and MDSC infiltration
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="6.0" fill="%s" stroke="%s" stroke-width="0.65"/>'
          % (x + 9.0, y + 8.0, mix(COL['on'], WHITE, 0.85), COL['on']))
    D.text(x + 9.0, y + 8.5, 'Tumor', anchor='middle', color=COL['on'], bold=True, size=FS_XS)
    # T-cell exhaustion interaction
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="4.8" fill="%s" stroke="%s" stroke-width="0.55"/>'
          % (x + 27.0, y + 8.0, '#EFF6FF', '#3B82F6'))
    D.text(x + 27.0, y + 8.5, 'T cell', anchor='middle', color='#1D4ED8', bold=True, size=FS_XS)
    # Inhibitory immune checkpoint interaction
    arrow((x + 15.5, y + 8.0), (x + 21.8, y + 8.0), end='tee', col='#BE123C', lw=0.55)
    D.text(x + 18.6, y + 6.0, 'PD-L1', anchor='middle', color='#BE123C', bold=True, size=4.5*PT)

def icon_senescence(x, y):
    # Flattened, enlarged senescent morphology bypassed
    D.add('body', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f Z" '
                 'fill="%s" stroke="%s" stroke-width="0.75"/>'
          % (x + 2.0, y + 9.0, x + 4.0, y + 1.5, x + 25.0, y + 0.8, x + 29.0, y + 6.0,
             x + 32.0, y + 12.0, x + 6.0, y + 14.5, x + 2.0, y + 9.0,
             mix(COL['on'], WHITE, 0.88), mix(COL['on'], WHITE, 0.25)))
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="4.8" ry="3.2" fill="url(#nuc)" stroke="#8B5CF6" stroke-width="0.35"/>'
          % (x + 14.0, y + 7.8))
    # Cell cycle arrest symbol bypassed
    cx, cy, r = x + 34.5, y + 7.5, 2.4
    D.add('body', '<path d="M%.2f %.2f A%.2f %.2f 0 1 1 %.2f %.2f" fill="none" stroke="%s" stroke-width="0.50"/>'
          % (cx + r, cy, r, r, cx + r * math.cos(-1.1), cy + r * math.sin(-1.1), GREY))
    head((cx + r * math.cos(-1.5), cy + r * math.sin(-1.5)),
         (cx + r * math.cos(-1.1), cy + r * math.sin(-1.1)), GREY, 1.0, 'body')
    D.add('body', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#BE123C" stroke-width="0.85" stroke-linecap="round"/>'
          % (cx + 1.2, cy - 3.2, cx + 3.5, cy - 0.8))

ICONS = [icon_metabolic, icon_macro, icon_immune, icon_senescence]

# Render Panel b Cards
for k, (title, sub, mech, drug, status) in enumerate(CARDS):
    x = k * (CW + CG) + 1.0
    # Background card
    D.add('bg', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2.2" '
                'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>'
          % (x, BY, CW, BH))
    # Icon
    ICONS[k](x + 1.5, BY + 2.0)
    # Text hierarchy (ultra-clean, no paragraph walls)
    D.text(x + 2.5, BY + 20.0, title, bold=True, color=INK, size=FS)
    D.text(x + 2.5, BY + 24.5, sub, color=INK_MUTED, bold=True, size=FS_XS)
    D.text(x + 2.5, BY + 29.0, mech, color=GREY, size=FS_XS)
    # Drug badge
    drug_box(x + 2.0, BY + 34.5, CW - 4.0, 7.5, drug, status=status)

# Panel b Letter
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
