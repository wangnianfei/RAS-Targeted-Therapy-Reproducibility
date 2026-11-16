# -*- coding: utf-8 -*-
"""
Figure 1: RAS Signalling Network, Therapeutic Vulnerabilities, and Downstream Biological Hallmarks
ESMO Open Review Standard (180mm x 172mm, Nature Reviews Cancer / Science Jewel-Tone Palette)
- Panel a: Python-generated vector signaling network, polished with Science/Nature aesthetics,
  zero line collisions, perfect spacing, cytosolic NF1, unbroken lipid bilayer, aligned outcome baselines.
- Panel b: AI-generated 4 hallmark illustrations with rich clinical annotations and drug boxes.
"""

import os, sys, math, base64, tempfile, shutil, subprocess
from PIL import ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'vector_figures'))
ASSET_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'assets'))
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
    'rec_rtk': '#E0F2FE',    # EGFR / RTK: Soft sky cyan
    'rec_int': '#FEF3C7',    # Integrin: Soft warm champagne sand
    'rec_gpcr': '#EDE9FE',   # GPCR: Soft heather amethyst
    'rec_imm': '#FFE4E6',    # Cytokine / Immune R: Soft antique rose coral
    'rec': '#E0F2FE',
    
    'adapt': '#F8FAFC',      # GRB2, SHP2, SOS1: Luminous slate
    'gef': '#0D9488',        # Tissue GEFs: Deep teal
    
    'off': '#F1F5F9',        # KRAS-GDP (inactive): Cool light grey-slate
    'on': '#FFF1F2',         # KRAS-GTP (active): Soft coral rose
    'gap': '#F8FAFC',        # GAPs (NF1, RASA1): Crisp light neutral
    
    'mapk': '#2563EB',       # Column 1 MAPK (RAF, MEK, ERK): Kinase royal cobalt blue
    'rassf': '#4F46E5',      # Column 2 RASSF1A & MST1/2: Apoptotic royal indigo
    'pi3k': '#0D9488',       # Column 3 PI3K-AKT-mTOR: Deep oceanic emerald teal
    'ral': '#0284C7',        # Column 4 RAL cascade: Sky azure blue
    'other': '#D97706',      # Column 5 Cytoskeleton (RAC1, F-actin): Warm golden amber
    'lig': '#EA580C',        # Ligands: Warm burnt terracotta
    'red': '#E11D48',        # Oncogenic accents
}

TC_MAP = {
    'adapt': '#0F172A',
    'mapk': WHITE,
    'pi3k': WHITE,
    'rassf': WHITE,
    'ral': WHITE,
    'other': WHITE,
    'on': '#991B1B',
    'off': '#334155',
    'gap': '#0F172A',
    'rec': '#0369A1',
    'rec_rtk': '#0369A1',
    'rec_int': '#92400E',
    'rec_gpcr': '#6D28D9',
    'rec_imm': '#9F1239',
    'lig': WHITE,
}

_FONT_CACHE = {}
def _get_font(bold=False, size_pt=7.0):
    k = (bold, size_pt)
    if k not in _FONT_CACHE:
        cand = [
            '/System/Library/Fonts/Helvetica.ttc',
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/Library/Fonts/Arial.ttf',
        ]
        f = None
        for c in cand:
            if os.path.exists(c):
                try:
                    f = ImageFont.truetype(c, int(size_pt * 4 / 3 * 2), index=1 if (bold and 'Helvetica' in c) else 0)
                    break
                except Exception:
                    continue
        if f is None:
            f = ImageFont.load_default()
        _FONT_CACHE[k] = f
    return _FONT_CACHE[k]

def tw(s, bold=False, size=FS):
    size_pt = size / PT
    font = _get_font(bold, size_pt)
    try:
        bbox = font.getbbox(s)
        w_px = bbox[2] - bbox[0]
        return (w_px / 2.0) * (size_pt / (font.size * 3 / 4 if hasattr(font, 'size') else 10)) * PT
    except Exception:
        return len(s) * size * 0.52

def mix(c, t, f):
    c = c.lstrip('#')
    t = t.lstrip('#')
    rgb1 = [int(c[i:i+2], 16) for i in (0, 2, 4)]
    rgb2 = [int(t[i:i+2], 16) for i in (0, 2, 4)]
    res = [int(rgb1[i] * (1 - f) + rgb2[i] * f) for i in range(3)]
    return '#%02x%02x%02x' % tuple(res)

def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class SVGDoc:
    def __init__(self):
        self.layers = {'bg': [], 'render': [], 'mem': [], 'link': [], 'body': [], 'text': [], 'over': []}
        self.defs = []
        self.grad_id = 0

    def add(self, layer, s):
        self.layers[layer].append(s)

    def gradient(self, col):
        self.grad_id += 1
        gid = 'g%d' % self.grad_id
        c1 = mix(col, '#ffffff', 0.22)
        c2 = mix(col, '#000000', 0.12)
        self.defs.append(
            '<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0%%" stop-color="%s"/>'
            '<stop offset="100%%" stop-color="%s"/>'
            '</linearGradient>' % (gid, c1, c2))
        return 'url(#%s)' % gid

    def text(self, x, y, s, anchor='start', color=INK, bold=False, size=FS,
             halo=False, layer='text'):
        weight = 'bold' if bold else 'normal'
        val = esc(s)
        if halo:
            self.layers[layer].append(
                '<text x="%.2f" y="%.2f" text-anchor="%s" fill="#ffffff" '
                'stroke="#ffffff" stroke-width="1.8" stroke-linejoin="round" '
                'font-family="Arial, Helvetica, sans-serif" font-weight="%s" font-size="%.2f">%s</text>'
                % (x, y, anchor, weight, size, val))
        self.layers[layer].append(
            '<text x="%.2f" y="%.2f" text-anchor="%s" fill="%s" '
            'font-family="Arial, Helvetica, sans-serif" font-weight="%s" font-size="%.2f">%s</text>'
            % (x, y, anchor, color, weight, size, val))

    def svg(self):
        s = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             'viewBox="0 0 %.2f %.2f" width="%.2fmm" height="%.2fmm">' % (W, H, W, H),
             '<defs>']
        s.extend(self.defs)
        s.append('</defs>')
        for l in ('bg', 'render', 'mem', 'link', 'body', 'text', 'over'):
            s.extend(self.layers[l])
        s.append('</svg>')
        return '\n'.join(s)

D = SVGDoc()

# Filters & Gradients
D.defs.append('''
<filter id="subtle-shadow" x="-5%" y="-5%" width="115%" height="120%">
  <feDropShadow dx="0" dy="0.4" stdDeviation="0.5" flood-color="#0F172A" flood-opacity="0.08"/>
</filter>
<linearGradient id="head" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#E2E8F0"/>
  <stop offset="100%" stop-color="#94A3B8"/>
</linearGradient>
<radialGradient id="nuc" cx="35%" cy="30%" r="70%">
  <stop offset="0%" stop-color="#FAF5FF"/>
  <stop offset="65%" stop-color="#F3E8FF"/>
  <stop offset="100%" stop-color="#E9D5FF"/>
</radialGradient>
<linearGradient id="cyto-grad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#FFFFFF"/>
  <stop offset="100%" stop-color="#F8FAFC"/>
</linearGradient>
<clipPath id="clipA"><rect x="0" y="0" width="180" height="118.5"/></clipPath>
''')

# Canvas base
D.add('bg', '<rect width="180" height="172" fill="#FFFFFF"/>')

# Extracellular & Cytosolic compartments
M = 21.0
HD = 1.9
BOT_A = 118.5

D.add('bg', '<g clip-path="url(#clipA)">')
D.add('bg', '<rect x="0" y="0" width="180" height="%.2f" fill="#F8FAFC"/>' % M)
D.add('bg', '<rect x="0" y="%.2f" width="180" height="%.2f" fill="url(#cyto-grad)"/>'
      % (M, BOT_A - M))
D.add('bg', '</g>')

# Receptor positions along x-axis (Dispersed and spaced according to downstream density)
# EGFR at 20.0, Integrin at 58.0, GPCR at 100.0, Immune R at 138.0
RX = {'rtk': 20.0, 'int': 58.0, 'gpcr': 100.0, 'imm': 138.0}
gaps = []

def pts_path(pts, close=True):
    d = ['M %.2f %.2f' % pts[0]]
    for p in pts[1:]:
        d.append('L %.2f %.2f' % p)
    if close:
        d.append('Z')
    return ' '.join(d)

def ell_pts(cx, cy, rx, ry, rot=0.0, n=36):
    r = math.radians(rot)
    cr, sr = math.cos(r), math.sin(r)
    pts = []
    for i in range(n):
        th = 2.0 * math.pi * i / n
        px, py = rx * math.cos(th), ry * math.sin(th)
        pts.append((cx + px * cr - py * sr, cy + px * sr + py * cr))
    return pts

def body(lobes, col, layer='body', lw=0.32, shadow=True, border_col=None):
    pts = []
    for l in lobes:
        pts.extend(ell_pts(l[0], l[1], l[2], l[3], l[4]))
    bc = border_col or mix(col, '#000000', 0.40)
    sh = ' filter="url(#subtle-shadow)"' if shadow else ''
    fill_col = D.gradient(col)
    D.add(layer, '<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f"%s/>'
          % (pts_path(pts, True), fill_col, bc, lw, sh))

def pill(cx, cy, w, h, label, col_key, layer='body', rx=None, border_col=None, text_col=None):
    col = COL[col_key]
    tc = text_col or TC_MAP.get(col_key, INK)
    bc = border_col or mix(col, '#000000', 0.35)
    r = rx if rx is not None else h / 2.0
    fill_col = D.gradient(col)
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.48" filter="url(#subtle-shadow)"/>'
          % (cx - w / 2, cy - h / 2, w, h, r, fill_col, bc))
    D.text(cx, cy + FS * 0.32, label, anchor='middle', color=tc, bold=True, size=FS)
    return {
        'top': (cx, cy - h / 2),
        'bottom': (cx, cy + h / 2),
        'left': (cx - w / 2, cy),
        'right': (cx + w / 2, cy),
        'cx': cx, 'cy': cy, 'w': w, 'h': h
    }

def head(p, q, col, size=1.2, layer='link'):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    L = math.hypot(dx, dy)
    if L < 1e-4: return
    ux, uy = dx / L, dy / L
    vx, vy = -uy, ux
    p1 = (q[0] - ux * size * 1.5 + vx * size * 0.75,
          q[1] - uy * size * 1.5 + vy * size * 0.75)
    p2 = (q[0] - ux * size * 1.5 - vx * size * 0.75,
          q[1] - uy * size * 1.5 - vy * size * 0.75)
    D.add(layer, '<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="%s"/>'
          % (q[0], q[1], p1[0], p1[1], p2[0], p2[1], col))

def arrow(p0, p1, c1=None, c2=None, col=None, lw=0.48, end='head', dash=None,
          size=1.2, layer='link'):
    col = col or ACT_COL
    d = ('stroke-dasharray="%s" ' % dash) if dash else ''
    if c1 and c2:
        pth = 'M %.2f %.2f C %.2f %.2f, %.2f %.2f, %.2f %.2f' \
              % (p0[0], p0[1], c1[0], c1[1], c2[0], c2[1], p1[0], p1[1])
        last_seg = (c2, p1)
    elif c1:
        pth = 'M %.2f %.2f Q %.2f %.2f, %.2f %.2f' \
              % (p0[0], p0[1], c1[0], c1[1], p1[0], p1[1])
        last_seg = (c1, p1)
    else:
        pth = 'M %.2f %.2f L %.2f %.2f' % (p0[0], p0[1], p1[0], p1[1])
        last_seg = (p0, p1)
    D.add(layer, '<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" %s/>'
          % (pth, col, lw, d))
    if end == 'head':
        head(last_seg[0], last_seg[1], col, size=size, layer=layer)
    elif end == 'tee':
        dx = last_seg[1][0] - last_seg[0][0]
        dy = last_seg[1][1] - last_seg[0][1]
        L = math.hypot(dx, dy)
        if L > 1e-4:
            ux, uy = dx / L, dy / L
            vx, vy = -uy, ux
            tw_bar = size * 1.4
            D.add(layer, '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"/>'
                  % (p1[0] - vx * tw_bar, p1[1] - vy * tw_bar,
                     p1[0] + vx * tw_bar, p1[1] + vy * tw_bar, col, lw * 2.2))

def marker(x, y, status, s=1.0):
    cfg = {
        'approved': ('#16A34A', '#15803D', 'circle'),
        'clinical': ('#2563EB', '#1D4ED8', 'rect'),
        'preclinical': ('#64748B', '#475569', 'diamond'),
    }
    fill, stroke, shape = cfg.get(status, ('#64748B', '#475569', 'circle'))
    if shape == 'circle':
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" stroke-width="0.30"/>'
              % (x, y, 1.1 * s, fill, stroke))
    elif shape == 'rect':
        D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s" stroke="%s" stroke-width="0.30"/>'
              % (x - 1.0 * s, y - 1.0 * s, 2.0 * s, 2.0 * s, 0.4 * s, fill, stroke))
    else:
        D.add('body', '<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="%s" stroke="%s" stroke-width="0.30"/>'
              % (x, y - 1.2 * s, x + 1.2 * s, y, x, y + 1.2 * s, x - 1.2 * s, y, fill, stroke))

def drug_box(x, y, w, h, title, subtitle=None, status='approved', border_col=BORDER):
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.8" '
                  'fill="#FFFFFF" fill-opacity="0.96" stroke="%s" stroke-width="0.45" '
                  'filter="url(#subtle-shadow)"/>' % (x, y, w, h, border_col))
    mx = x + 2.5
    my = y + (h / 2.0 if subtitle is None else 2.6)
    marker(mx, my, status, s=0.8)
    tx = x + 4.8
    if subtitle:
        D.text(tx, y + 3.2, title, bold=True, size=FS_SM, color=INK)
        D.text(tx, y + 6.8, subtitle, size=FS_XS, color=INK_MUTED)
    else:
        D.text(tx, y + h / 2.0 + FS_SM * 0.32, title, bold=True, size=FS_SM, color=INK)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

def outcome_box(x, y, w, h, title, subtitle, bg_col, border_col, title_col):
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2.0" '
                  'fill="%s" stroke="%s" stroke-width="0.55" filter="url(#subtle-shadow)"/>'
          % (x, y, w, h, bg_col, border_col))
    D.text(x + w / 2.0, y + 3.2, title, anchor='middle', bold=True, size=FS_SM, color=title_col)
    D.text(x + w / 2.0, y + 6.8, subtitle, anchor='middle', size=FS_XS, color=INK_MUTED)
    return {
        'top': (x + w / 2.0, y),
        'bottom': (x + w / 2.0, y + h),
        'left': (x, y + h / 2.0),
        'right': (x + w, y + h / 2.0),
        'x': x, 'y': y, 'w': w, 'h': h
    }

def helix(x, y0, y1, w=1.2, col=None, border_col=None, layer='body'):
    c = col or COL['rec']
    bc = border_col or mix(c, '#000000', 0.40)
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.30"/>'
           % (x - w / 2, y0, w, y1 - y0, w / 2, D.gradient(c), bc))

# Receptors
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

def integrin(cx):
    col = COL['rec_int']
    bc = '#D97706'
    for s, top in ((-1, 8.2), (1, 9.6)):
        x = cx + s * 1.6
        D.add('body', '<path d="M%.2f %.2f L%.2f %.2f L%.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="1.1" stroke-linecap="round"/>'
              % (x, top + 1.4, x, M + HD + 0.8, x + s * 0.8, 27.2, bc))
        body([(x + s * 0.4, top, 1.9, 1.5, s * 18)], col, border_col=bc, shadow=False)
    pts = [(cx - 4.5 + k * 0.30, 5.0 + 0.5 * math.sin(k * 0.6)) for k in range(34)]
    D.add('body', '<path d="%s" fill="none" stroke="#94A3B8" stroke-width="0.8" stroke-linecap="round"/>'
          % pts_path(pts, False))
    gaps.append((cx - 3.5, cx + 3.5))

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

# Unbroken lipid bilayer rendering across entire membrane
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

# Plasma membrane label: floating cleanly above the bilayer in extracellular space with callout line
D.add('body', '<rect x="70.0" y="14.2" width="18.0" height="3.6" rx="1.4" '
             'fill="#FFFFFF" stroke="#64748B" stroke-width="0.45" filter="url(#subtle-shadow)"/>')
D.text(79.0, 16.0, 'Plasma membrane', anchor='middle', color='#0F172A', bold=True, size=4.5*PT)
D.add('link', '<line x1="79.0" y1="17.8" x2="79.0" y2="19.3" stroke="#64748B" stroke-width="0.45"/>')
D.add('body', '<circle cx="79.0" cy="19.3" r="0.35" fill="#64748B"/>')

# Extracellular anti-EGFR antibody callout (ON THE RIGHT OF EGFR)
card_egfr = drug_box(26.5, 4.2, 22.5, 8.5, 'Anti-EGFR mAbs', 'cetuximab, panitumumab', 'approved', '#0284C7')
arrow(card_egfr['left'], (23.8, card_egfr['left'][1]), end='tee', col=INH_COL, lw=0.55)

# Top Right: Standardization Legend Box
D.add('bg', '<rect x="147.0" y="1.8" width="32.0" height="16.0" rx="2.0" fill="#FFFFFF" '
            'fill-opacity="0.96" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>')
marker(149.5, 3.6, 'approved')
D.text(152.5, 3.6, 'Approved drug class', color=INK, size=4.2*PT, bold=True)
marker(149.5, 6.6, 'clinical')
D.text(152.5, 6.6, 'Clinical trials (Ph I–III)', color=INK, size=4.2*PT, bold=True)
marker(149.5, 9.6, 'preclinical')
D.text(152.5, 9.6, 'Preclinical / investigational', color=INK, size=4.2*PT, bold=True)
arrow((148.0, 12.5), (151.5, 12.5), col=ACT_COL, lw=0.60, layer='over')
D.text(152.5, 12.5, 'Activation cascade (→)', color=ACT_COL, size=4.2*PT, bold=True)
arrow((148.0, 15.2), (151.5, 15.2), end='tee', col=INH_COL, lw=0.60, layer='over')
D.text(152.5, 15.2, 'Inhibition / feedback (--|)', color=INH_COL, size=4.2*PT, bold=True)

# Adaptors & Upstream Modulation: GRB2 -> SHP2 -> SOS1
node_grb2 = pill(38.0, 35.0, 11.5, 5.6, 'GRB2', 'adapt')
node_shp2 = pill(58.0, 35.0, 11.5, 5.6, 'SHP2', 'adapt')
node_sos1 = pill(80.0, 35.0, 13.0, 6.0, 'SOS1', 'adapt')

# Blue activation arrow connecting EGFR tail to LEFT of GRB2
arrow((24.5, 30.5), node_grb2['left'],
      c1=(27.5, 30.5), c2=(28.5, 35.0),
      col=ACT_COL, lw=0.52)
arrow(node_grb2['right'], node_shp2['left'], col=ACT_COL, lw=0.50)
arrow((RX['int'], 27.2), (node_shp2['cx'], node_shp2['top'][1]), col=ACT_COL, lw=0.50)
arrow(node_shp2['right'], node_sos1['left'], col=ACT_COL, lw=0.50)

# Upstream Inhibitors Card (SHP2 & SOS1) - Width 24.0mm (x: 49.0 - 73.0), generous 10mm clearance to vertical dashed line at x=83.0!
card_upstream = drug_box(49.0, 44.5, 24.0, 8.5, 'SHP2 / SOS1 inh.', 'TNO155, BI 1701963', 'clinical')
arrow((node_shp2['cx'], card_upstream['top'][1]), node_shp2['bottom'], end='tee', col=INH_COL, lw=0.50)
arrow((card_upstream['right'][0] - 1.5, card_upstream['top'][1]), (76.5, node_sos1['bottom'][1]), end='tee', col=INH_COL, lw=0.50)

# ============================================================ CENTRAL SWITCH ==
GDP_X, GTP_X, SW_Y = 102.0, 138.0, 35.5

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
arrow((RX['gpcr'], 26.5), (node_gdp['cx'] - 1.0, node_gdp['top'][1]), col=ACT_COL, lw=0.48)

# Immune R activation down into active KRAS-GTP (Straight vertical alignment at x=138.0!)
arrow((RX['imm'], 26.5), (node_gtp['cx'], node_gtp['top'][1]), col=ACT_COL, lw=0.48)

# SOS1 DIRECT ACTIVATION OF KRAS-GDP (GEF Exchange)
arrow(node_sos1['right'], node_gdp['left'], col=ACT_COL, lw=0.58)
D.text((node_sos1['right'][0] + node_gdp['left'][0]) / 2, 32.5, 'GEF exchange',
       anchor='middle', color='#1D4ED8', bold=True, size=4.8*PT, halo=True)

# GAP (NF1) - Dedicated Cytoplasmic Pill Element (Below plasma membrane in cytosol at y=24.5)
node_gap = pill(115.0, 24.5, 14.0, 4.5, 'GAP (NF1)', 'gap', border_col='#64748B')

# Upper Arc: GTP -> GDP (Hydrolysis, Grey pathway)
arrow((GTP_X - 6.0, SW_Y - 4.5), (GDP_X + 6.0, SW_Y - 4.5),
      (GTP_X - 10.0, 28.5), (GDP_X + 10.0, 28.5), col=INH_COL, lw=0.60)
# GAP promotes hydrolysis (Arrow entering the arc at x=115.0)
arrow(node_gap['bottom'], (115.0, 28.5), col=ACT_COL, lw=0.50)

# Oncogenic Mutation Blockade Badge Element (Positioned at x=125.0, width 14.5mm, fits cleanly in gap!)
D.add('body', '<rect x="117.75" y="32.5" width="14.5" height="3.6" rx="1.4" '
             'fill="#FFF1F2" stroke="#E11D48" stroke-width="0.45"/>')
D.text(125.0, 34.3, 'G12/G13/Q61 lock', anchor='middle', color='#991B1B', bold=True, size=4.4*PT)
arrow((125.0, 32.5), (125.0, 29.5), end='tee', col=INH_COL, lw=0.55)

# Lower Arc: GDP -> GTP (GEF Exchange, Blue activation cycle)
arrow((GDP_X + 6.0, SW_Y + 4.5), (GTP_X - 6.0, SW_Y + 4.5),
      (GDP_X + 10.0, 44.5), (GTP_X - 10.0, 44.5), col=ACT_COL, lw=0.60)
D.text(120.0, 46.8, 'GDP → GTP cycle', anchor='middle', color='#2563EB', bold=True, size=4.8*PT, halo=True)

# ============================================================ DIRECT DRUGS ====
# Class I & II docked to RAS-GDP (Bottom of RAS-GDP, centered at 102.0)
D.add('body', '<rect x="85.0" y="49.0" width="34.0" height="10.5" rx="1.8" fill="#FFFFFF" '
             'fill-opacity="0.96" stroke="#94A3B8" stroke-width="0.50" filter="url(#subtle-shadow)"/>')
marker(87.5, 51.6, 'approved', s=0.85)
D.text(90.0, 51.6 - FS_SM * 0.35, 'Class I: sotorasib, adagrasib', color=INK, bold=True, size=FS_SM)
marker(87.5, 56.2, 'clinical', s=0.85)
D.text(90.0, 56.2 - FS_SM * 0.35, 'Class II: MRTX1133 (G12D)', color=INK, bold=True, size=FS_SM)
arrow((node_gdp['cx'], 49.0), node_gdp['bottom'], end='tee', col=INH_COL, lw=0.55)

# Class III & IV docked to RAS-GTP (Right side of RAS-GTP, clean 2-line layout without CYPA note)
D.add('body', '<rect x="148.5" y="30.5" width="30.5" height="10.0" rx="1.8" fill="#FFFFFF" '
             'fill-opacity="0.96" stroke="#E11D48" stroke-width="0.50" filter="url(#subtle-shadow)"/>')
marker(151.0, 33.2, 'clinical', s=0.85)
D.text(153.2, 33.2 - FS_SM * 0.35, 'Class III: daraxonrasib', color=INK, bold=True, size=5.4*PT)
marker(151.0, 37.8, 'clinical', s=0.85)
D.text(153.2, 37.8 - FS_SM * 0.35, 'Class IV: ASP3082 (PROTAC)', color=INK, bold=True, size=5.4*PT)
arrow((148.5, node_gtp['cy']), node_gtp['right'], end='tee', col=INH_COL, lw=0.55)

# ============================================================ EFFECTOR BUS ====
BUS_Y = 61.0
BUS_X = {'mapk': 18.0, 'rassf': 60.0, 'pi3k': 88.0, 'ral': 132.0, 'cyto': 164.0}

# Drop from active KRAS-GTP to horizontal bus
arrow(node_gtp['bottom'], (node_gtp['cx'], BUS_Y), end='none', col=ACT_COL, lw=0.65)
D.text(node_gtp['cx'] - 1.5, BUS_Y - 1.2, 'effector recruitment', anchor='end', color='#1D4ED8', bold=True, size=5.5*PT)

# Horizontal distribution bus spanning across the 5 functional lanes
D.add('link', '<path d="M%.2f %.2f L%.2f %.2f" stroke="%s" stroke-width="0.55"/>'
      % (BUS_X['mapk'], BUS_Y, BUS_X['cyto'], BUS_Y, ACT_COL))

for k, x in BUS_X.items():
    arrow((x, BUS_Y), (x, 66.4), col=ACT_COL, lw=0.55)

# ============================================================ EFFECTOR COLUMNS =
T1, T2, T3 = 69.5, 82.0, 94.5

# Column 1: MAPK Pathway (x = 18.0)
node_raf = pill(BUS_X['mapk'], T1, 16.0, 6.2, 'RAF', 'mapk')
node_mek = pill(BUS_X['mapk'], T2, 14.0, 5.8, 'MEK1/2', 'mapk')
node_erk = pill(BUS_X['mapk'], T3, 14.0, 5.8, 'ERK1/2', 'mapk')

arrow(node_raf['bottom'], node_mek['top'], col=ACT_COL)
arrow(node_mek['bottom'], node_erk['top'], col=ACT_COL)

card_raf_mek = drug_box(26.0, 78.0, 19.5, 8.0, 'RAF / MEK inh.', 'trametinib, encorafenib', 'approved')
arrow(card_raf_mek['left'], node_mek['right'], end='tee', col=INH_COL, lw=0.50)

card_erk = drug_box(26.0, 90.5, 19.5, 8.0, 'ERK inh.', 'ulixertinib (Ph I/II)', 'clinical')
arrow(card_erk['left'], node_erk['right'], end='tee', col=INH_COL, lw=0.50)

# ============================================================ NUCLEAR ENVELOPE & NUCLEAR PORE ====
NCX, NCY = 18.0, 120.0
NRX, NRY = 28.0, 20.0
PORE_X1, PORE_X2 = 14.5, 21.5
PORE_Y = 100.0

D.add('bg', '<g clip-path="url(#clipA)">')
D.add('bg', '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="url(#nuc)"/>'
      % (NCX, NCY, NRX, NRY))

# Double membrane nuclear envelope with open pore channel
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

# NPC subunits
D.add('body', '<rect x="12.6" y="98.8" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<rect x="12.6" y="101.2" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<circle cx="14.3" cy="101.1" r="0.65" fill="#8B5CF6"/>')
D.add('body', '<rect x="20.0" y="98.8" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<rect x="20.0" y="101.2" width="3.4" height="2.2" rx="0.9" fill="#EDE9FE" stroke="#7C3AED" stroke-width="0.35"/>')
D.add('body', '<circle cx="21.7" cy="101.1" r="0.65" fill="#8B5CF6"/>')
D.add('bg', '</g>')

D.text(25.5, 100.0, 'Nuclear pore (NPC)', color='#6D28D9', bold=True, size=4.8*PT, halo=True)
D.text(34.0, 116.0, 'Nucleus', color='#6D28D9', bold=True, size=FS_SM, halo=True)

# Translocated ERK inside Nucleus
node_erk_nuc = pill(BUS_X['mapk'], 105.0, 11.0, 4.8, 'ERK (p)', 'mapk')
arrow(node_erk['bottom'], node_erk_nuc['top'], col=ACT_COL, lw=0.55)

# Outcome Box 1: Proliferation & Growth (Inside Nucleus at y=109.5, ends at 117.0 < 118.5!)
out_mapk = outcome_box(4.5, 109.5, 27.0, 7.5, 'Proliferation & Growth', 'CCND1, MYC, FOS, ELK1',
                       '#FAF5FF', '#C084FC', '#581C87')
arrow(node_erk_nuc['bottom'], out_mapk['top'], col=ACT_COL, lw=0.55)

# Column 2: Pro-Apoptotic Branch (RASSF1A) (x = 60.0)
node_rassf = pill(BUS_X['rassf'], T1, 15.0, 6.0, 'RASSF1A', 'rassf')
node_mst = pill(BUS_X['rassf'], 86.0, 13.0, 5.8, 'MST1/2', 'rassf')
arrow(node_rassf['bottom'], node_mst['top'], col=ACT_COL)
arrow(node_raf['right'], node_rassf['left'], end='tee', col=INH_COL, lw=0.50)

# Aligned Cytoplasmic Outcome Boxes: All sharing baseline y = 106.5, height = 8.5!
OUT_Y = 106.5
OUT_H = 8.5

out_rassf = outcome_box(50.5, OUT_Y, 19.0, OUT_H, 'Apoptosis', 'MST / YAP1 / p73',
                        '#EEF2FF', '#818CF8', '#312E81')
arrow(node_mst['bottom'], out_rassf['top'], col=ACT_COL, lw=0.55)

# Column 3: PI3K-AKT-mTOR Pathway (x = 88.0)
node_pi3k = pill(BUS_X['pi3k'], T1, 16.0, 6.2, 'PI3K (p110)', 'pi3k')
node_akt = pill(BUS_X['pi3k'], T2, 13.0, 5.8, 'AKT', 'pi3k')
node_mtor = pill(BUS_X['pi3k'], T3, 15.0, 5.8, 'mTORC1', 'pi3k')

arrow(node_pi3k['bottom'], node_akt['top'], col=ACT_COL)
arrow(node_akt['bottom'], node_mtor['top'], col=ACT_COL)

card_pi3k_inh = drug_box(98.0, 65.5, 21.0, 8.0, 'PI3K inh.', 'alpelisib, inavolisib', 'approved')
arrow(card_pi3k_inh['left'], node_pi3k['right'], end='tee', col=INH_COL, lw=0.50)

card_mtor_inh = drug_box(98.0, 90.5, 21.0, 8.0, 'mTOR inh.', 'everolimus, sirolimus', 'approved')
arrow(card_mtor_inh['left'], node_mtor['right'], end='tee', col=INH_COL, lw=0.50)

out_pi3k = outcome_box(76.0, OUT_Y, 24.0, OUT_H, 'Survival & Growth', 'S6K1, 4E-BP1, glycolysis',
                       '#F0FDFA', '#5EEAD4', '#0F766E')
arrow(node_mtor['bottom'], out_pi3k['top'], col=ACT_COL, lw=0.55)

# Column 4: RAL GTPases (x = 132.0)
node_ralgds = pill(BUS_X['ral'], T1, 15.0, 6.0, 'RALGDS', 'ral')
node_ral = pill(BUS_X['ral'], T2, 13.0, 5.8, 'RAL-A/B', 'ral')
node_tbk1 = pill(BUS_X['ral'], T3, 15.0, 5.8, 'TBK1 / Sec5', 'ral')

arrow(node_ralgds['bottom'], node_ral['top'], col=ACT_COL)
arrow(node_ral['bottom'], node_tbk1['top'], col=ACT_COL)

out_ral = outcome_box(120.0, OUT_Y, 24.0, OUT_H, 'Vesicle Trafficking', 'Exocyst & autophagy',
                      '#F0F9FF', '#7DD3FC', '#0284C7')
arrow(node_tbk1['bottom'], out_ral['top'], col=ACT_COL, lw=0.55)

# Column 5: Cytoskeletal Remodelling (PLCε & TIAM1)
node_plce = pill(157.0, T1, 12.0, 5.8, 'PLCε', 'other')
node_tiam1 = pill(171.0, T1, 12.0, 5.8, 'TIAM1', 'other')
node_rac1 = pill(BUS_X['cyto'], T2, 16.0, 6.0, 'PKC / RAC1', 'other')

arrow(node_plce['bottom'], (BUS_X['cyto'] - 3.0, node_rac1['top'][1]), col=ACT_COL)
arrow(node_tiam1['bottom'], (BUS_X['cyto'] + 3.0, node_rac1['top'][1]), col=ACT_COL)

node_actin = pill(BUS_X['cyto'], T3, 21.0, 5.8, 'F-actin assembly', 'other')
arrow(node_rac1['bottom'], node_actin['top'], col=ACT_COL)

out_cyto = outcome_box(152.0, OUT_Y, 24.0, OUT_H, 'Motility & Invasion', 'Actin dynamics & migration',
                       '#FFFBEB', '#FCD34D', '#B45309')
arrow(node_actin['bottom'], out_cyto['top'], col=ACT_COL, lw=0.55)

# ============================================================ FEEDBACK LOOP ===
FX = 4.5
arrow(node_erk['left'], (FX, node_erk['cy']), end='none', col=INH_COL, dash='1.2 0.8', lw=0.6)
arrow((FX, node_erk['cy']), (FX, 19.5), end='none', col=INH_COL, dash='1.2 0.8', lw=0.6)

# Branch 1 to RAF
arrow((FX, node_raf['cy']), node_raf['left'], end='tee', col=INH_COL, dash='1.2 0.8', lw=0.6)

# Branch 2 to SOS1: Passing cleanly beneath card_upstream at y=56.5 to avoid crossing SHP2 drug line
arrow((FX, 56.5), (83.0, 56.5), end='none', col=INH_COL, dash='1.2 0.8', lw=0.6)
arrow((83.0, 56.5), (83.0, node_sos1['bottom'][1]), end='tee', col=INH_COL, dash='1.2 0.8', lw=0.6)

# Branch 3 to EGFR
arrow((FX, 19.5), (RX['rtk'] - 4.0, 19.5), end='tee', col=INH_COL, dash='1.2 0.8', lw=0.6)

D.text(FX + 1.6, 54.0, 'ERK negative feedback', color=INH_COL, bold=True, size=5.5*PT)

# Panel a Letter
D.text(1.0, 2.5, 'a', bold=True, size=PNs, color=INK)

# ============================================================ PANEL B =========
D.add('bg', '<line x1="0" y1="%.2f" x2="180" y2="%.2f" stroke="#CBD5E1" stroke-width="0.6"/>'
      % (BOT_A, BOT_A))

BY = 120.5
CW, CG = 43.0, 2.0
BH = 49.5

CARDS = [
    ('Metabolic Rewiring',
     'Warburg flux & glutaminolysis',
     'GOT1, GLS1 flux fuels NADPH redox defense',
     'GOT1, GLS1, MCT4 inh.', 'preclinical'),
    ('Macropinocytosis & Autophagy',
     'Nutrient scavenging & lysosomal recycling',
     'Bulk fluid uptake sustains amino acid pools',
     'Hydroxychloroquine (HCQ)', 'clinical'),
    ('Immunosuppressive Microenv.',
     'Immune exclusion & myeloid recruitment',
     'MDSC recruitment & CD8+ T-cell exhaustion',
     'Anti-PD-(L)1; RAS vaccines', 'clinical'),
    ('Senescence Bypass',
     'Escape from oncogenic stress (OIS)',
     'CDK4/6 hyperactivation drives RB phosphorylation',
     'Senolytics; CDK4/6 inh.', 'clinical'),
]

IMG_B64 = {}
for k, fname in enumerate(['metabolism.jpg', 'macropinocytosis.jpg', 'immune.jpg', 'senescence.jpg']):
    fpath = os.path.join(ASSET_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, 'rb') as fh:
            IMG_B64[k] = base64.b64encode(fh.read()).decode('utf-8')

for k, (title, sub, mech, drug, status) in enumerate(CARDS):
    x = k * (CW + CG) + 1.0
    D.add('bg', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2.2" '
                'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>'
          % (x, BY, CW, BH))
    
    # Embed publication-grade 3D scientific illustration from AI model
    if k in IMG_B64:
        D.add('body', '<image href="data:image/jpeg;base64,%s" x="%.2f" y="%.2f" width="%.2f" height="19.50" '
                     'preserveAspectRatio="xMidYMid meet"/>'
              % (IMG_B64[k], x + 1.2, BY + 1.5, CW - 2.4))
        
    ty = BY + 22.8
    D.text(x + 2.5, ty, title, bold=True, color=INK, size=FS)
    D.text(x + 2.5, ty + 4.0, sub, color=ACT_COL, bold=True, size=FS_XS)
    D.text(x + 2.5, ty + 7.8, mech, color=INK_MUTED, size=4.2*PT)
    drug_box(x + 1.8, BY + 37.5, CW - 3.6, 9.8, drug, subtitle='Targeted therapeutic strategy', status=status)

D.text(1.0, BY + 2.5, 'b', bold=True, size=PNs, color=INK)

def main():
    svg_str = D.svg()
    svg_file = os.path.join(FIG, NAME + '.svg')
    png_file = os.path.join(FIG, NAME + '.png')
    pdf_file = os.path.join(FIG, NAME + '.pdf')
    
    with open(svg_file, 'w', encoding='utf-8') as fh:
        fh.write(svg_str)
        
    subprocess.run(['/opt/homebrew/bin/rsvg-convert', '--dpi-x', '400', '--dpi-y', '400', '-b', 'white',
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
        subprocess.run(['/opt/homebrew/bin/rsvg-convert', '-f', 'pdf', '-o', pdf_file, svg_file], check=True)
        
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
            print("Synchronized Figure 1 to:", sdir)
            
    # Legacy file name sync
    legacy_dst = "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件/图1_RAS信号网络与可干预节点-1.png"
    if os.path.exists(os.path.dirname(legacy_dst)):
        shutil.copy2(png_file, legacy_dst)
        print("Synchronized to legacy name:", legacy_dst)

if __name__ == '__main__':
    main()
