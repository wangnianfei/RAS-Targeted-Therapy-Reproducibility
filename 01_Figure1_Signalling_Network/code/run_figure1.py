# -*- coding: utf-8 -*-
"""
Figure 1: RAS Signalling Network, Therapeutic Vulnerabilities, and Downstream Biological Hallmarks
ESMO Open Review Standard (180mm x 172mm, Nature Reviews Cancer / Science Jewel-Tone Palette)
- Panel a: Python-generated vector signaling network, polished with Science/Nature aesthetics,
  zero line collisions, dedicated 'heads' layer for visible razor-sharp arrowheads and T-bars,
  horizontal and parallel inhibitor bars, zero border clipping, centered mutation badge,
  GAP (NF1) strictly localized to the cytosol (胞浆 / 细胞膜内侧) below the unbroken lipid bilayer,
  aligned outcome baselines.
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
FS_XS = 4.8 * PT                          # Refined extra small badge font size ~4.8 pt
FS_SUB = 4.5 * PT                         # Subtitle font size ~4.5 pt for drug cards
PNs = 9.5 * PT                            # Panel bold letter size
LH = FS * 1.25                            # Line height

# Strict typography & color scheme
INK = '#0F172A'          # Deep slate black for primary text
INK_MUTED = '#475569'    # Slate for secondary labels
GREY = '#64748B'         # Muted slate grey
WHITE = '#FFFFFF'
BORDER = '#CBD5E1'       # Card & border stroke

# Primary signalling line colors (Nature Standard: Blue = Activation, Grey = Inhibition)
ACT_COL = '#1F3A5F'      # Deep Prussian Navy for activation cascades and forward arrows (Fig 4 Primary Anchor)
INH_COL = '#64748B'      # Neutral Slate Grey for inhibitory T-bars and negative feedback
MUT_COL = '#A63A2E'      # Brick Ruby / Coral accent for oncogenic mutation blockade (Fig 3 Switch-I & Fig 4 Anchor)

# Functional semantic color palette (Harmonized Jewel-Tone Palette)
COL = {
    'rec_rtk': '#EBF1F6',    # EGFR / RTK: Soft Prussian ice
    'rec_int': '#FAF4E8',    # Integrin: Soft warm champagne
    'rec_gpcr': '#F4F0F7',   # GPCR: Soft heather amethyst
    'rec_imm': '#FDF0EE',    # Cytokine / Immune R: Soft brick rose
    'rec': '#EBF1F6',
    
    'adapt': '#F8FAFC',      # GRB2, SHP2, SOS1: Luminous slate
    'gef': '#2A6F6F',        # Tissue GEFs: Deep oceanic teal (Fig 3 & Fig 4)
    
    'off': '#F1F5F9',        # KRAS-GDP (inactive): Cool light grey-slate
    'on': '#FDF0EE',         # KRAS-GTP (active): Soft coral rose
    'gap': '#F8FAFC',        # GAPs (NF1, RASA1): Crisp light neutral
    
    'mapk': '#1F3A5F',       # Column 1 MAPK (RAF, MEK, ERK): Deep Prussian Navy
    'rassf': '#5E4B8B',      # Column 2 RASSF1A & MST1/2: Muted academic amethyst
    'pi3k': '#2A6F6F',       # Column 3 PI3K-AKT-mTOR: Oceanic Deep Teal
    'ral': '#3E6B89',        # Column 4 RAL cascade: Cadet/Steel Navy
    'other': '#B47226',      # Column 5 Cytoskeleton (RAC1, F-actin): Warm golden amber
    'lig': '#C97A24',        # Ligands: Warm amber-terracotta
    'red': '#A63A2E',        # Oncogenic accents: Brick Ruby
}

TC_MAP = {
    'adapt': '#0F172A',
    'mapk': WHITE,
    'pi3k': WHITE,
    'rassf': WHITE,
    'ral': WHITE,
    'other': WHITE,
    'on': '#8B251B',
    'off': '#334155',
    'gap': '#0F172A',
    'rec': '#1F3A5F',
    'rec_rtk': '#1F3A5F',
    'rec_int': '#8A5800',
    'rec_gpcr': '#5E4B8B',
    'rec_imm': '#A63A2E',
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
        # Dedicated 'heads' layer rendered AFTER 'body' so arrowheads and tee-bars are never obscured!
        self.layers = {'bg': [], 'render': [], 'mem': [], 'link': [], 'body': [], 'heads': [], 'text': [], 'over': []}
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
                'font-family="PingFang SC, Hiragino Sans GB, Helvetica Neue, Arial, sans-serif" font-weight="%s" font-size="%.2f">%s</text>'
                % (x, y, anchor, weight, size, val))
        self.layers[layer].append(
            '<text x="%.2f" y="%.2f" text-anchor="%s" fill="%s" '
            'font-family="PingFang SC, Hiragino Sans GB, Helvetica Neue, Arial, sans-serif" font-weight="%s" font-size="%.2f">%s</text>'
            % (x, y, anchor, color, weight, size, val))

    def svg(self):
        s = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             'viewBox="0 0 %.2f %.2f" width="%.2fmm" height="%.2fmm">' % (W, H, W, H),
             '<defs>']
        s.extend(self.defs)
        s.append('</defs>')
        for l in ('bg', 'render', 'mem', 'link', 'body', 'heads', 'text', 'over'):
            s.extend(self.layers[l])
        s.append('</svg>')
        return '\n'.join(s)

D = SVGDoc()

# Filters & Gradients
D.defs.append('''
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

# Receptor positions along x-axis
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

def body(lobes, col, layer='body', lw=0.32, shadow=False, border_col=None):
    pts = []
    for l in lobes:
        pts.extend(ell_pts(l[0], l[1], l[2], l[3], l[4]))
    bc = border_col or mix(col, '#000000', 0.40)
    fill_col = D.gradient(col)
    D.add(layer, '<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f"/>'
          % (pts_path(pts, True), fill_col, bc, lw))

def pill(cx, cy, w, h, label, col_key, layer='body', rx=None, border_col=None, text_col=None):
    col = COL[col_key]
    tc = text_col or TC_MAP.get(col_key, INK)
    bc = border_col or mix(col, '#000000', 0.35)
    r = rx if rx is not None else h / 2.0
    fill_col = D.gradient(col)
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.48"/>'
          % (cx - w / 2, cy - h / 2, w, h, r, fill_col, bc))
    D.text(cx, cy + FS * 0.32, label, anchor='middle', color=tc, bold=True, size=FS)
    return {
        'top': (cx, cy - h / 2),
        'bottom': (cx, cy + h / 2),
        'left': (cx - w / 2, cy),
        'right': (cx + w / 2, cy),
        'cx': cx, 'cy': cy, 'w': w, 'h': h
    }

def head(p, q, col, size=1.1, layer='heads'):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    L = math.hypot(dx, dy)
    if L < 1e-4: return
    ux, uy = dx / L, dy / L
    vx, vy = -uy, ux
    p1 = (q[0] - ux * size * 1.5 + vx * size * 0.72,
          q[1] - uy * size * 1.5 + vy * size * 0.72)
    p2 = (q[0] - ux * size * 1.5 - vx * size * 0.72,
          q[1] - uy * size * 1.5 - vy * size * 0.72)
    D.add(layer, '<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="%s"/>'
          % (q[0], q[1], p1[0], p1[1], p2[0], p2[1], col))

def tee_bar(p, q, col, size=1.1, lw=0.48, layer='heads', tee_angle=None):
    if tee_angle is not None:
        rad = math.radians(tee_angle)
        vx, vy = math.cos(rad), math.sin(rad)
    else:
        dx = q[0] - p[0]
        dy = q[1] - p[1]
        L = math.hypot(dx, dy)
        if L < 1e-4: return
        ux, uy = dx / L, dy / L
        vx, vy = -uy, ux
    tw_bar = size * 1.2
    # Clean, refined publication standard tee-bar stroke: 0.75mm with round caps
    D.add(layer, '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="0.75" stroke-linecap="round"/>'
          % (q[0] - vx * tw_bar, q[1] - vy * tw_bar,
             q[0] + vx * tw_bar, q[1] + vy * tw_bar, col))

def arrow(p0, p1, c1=None, c2=None, col=None, lw=0.48, end='head', dash=None,
          size=1.1, layer='link', tee_angle=None):
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
        head(last_seg[0], last_seg[1], col, size=size, layer='heads')
    elif end == 'tee':
        tee_bar(last_seg[0], last_seg[1], col, size=size, lw=lw, layer='heads', tee_angle=tee_angle)

def marker(x, y, status, s=1.0):
    cfg = {
        'approved': ('#1B6A45', '#14532D', 'circle'),      # Forest Green
        'clinical': ('#1F3A5F', '#142944', 'rect'),        # Deep Prussian Navy (Fig 4 & Fig 3 Anchor)
        'preclinical': ('#64748B', '#475569', 'diamond'),  # Slate Grey
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
                  'fill="#FFFFFF" fill-opacity="0.96" stroke="%s" stroke-width="0.45"/>'
                  % (x, y, w, h, border_col))
    mx = x + 2.5
    my = y + (h / 2.0 if subtitle is None else 2.6)
    marker(mx, my, status, s=0.8)
    tx = x + 4.8
    if subtitle:
        D.text(tx, y + 3.2, title, bold=True, size=FS_SM, color=INK)
        D.text(tx, y + 6.8, subtitle, size=FS_SUB, color=INK_MUTED)
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
                  'fill="%s" stroke="%s" stroke-width="0.55"/>'
                  % (x, y, w, h, bg_col, border_col))
    D.text(x + w / 2.0, y + 3.2, title, anchor='middle', bold=True, size=FS_SM, color=title_col)
    D.text(x + w / 2.0, y + 6.8, subtitle, anchor='middle', size=FS_SUB, color=INK_MUTED)
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
    bc = '#1F3A5F'
    for s in (-1, 1):
        x = cx + s * 2.2
        body([(x + s * 0.3, 8.5, 1.8, 2.4, 0), (x + s * 0.1, 13.5, 1.6, 2.2, 0)], col, border_col=bc, shadow=False)
        helix(x, 15.5, 26.5, w=1.2, col=col, border_col=bc)
        body([(x + s * 0.4, 28.2, 2.2, 1.8, 0)], col, border_col=bc, shadow=False)
        D.add('over', '<circle cx="%.2f" cy="%.2f" r="0.75" fill="#EAB308" stroke="#854D0E" stroke-width="0.25"/>'
              % (x + s * 1.3, 30.5))
        D.text(x + s * 1.3, 30.8, 'P', anchor='middle', color='#713F12', bold=True, size=4.5*PT)
    gaps.append((cx - 4.5, cx + 4.5))

def integrin(cx):
    col = COL['rec_int']
    bc = '#B47226'
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
    bc = '#5E4B8B'
    xs = [cx - 3.8 + k * 1.25 for k in range(7)]
    for k in range(6):
        y = 16.0 if k % 2 else 26.5
        D.add('body', '<path d="M%.2f %.2f Q%.2f %.2f %.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="0.45"/>'
              % (xs[k], y, (xs[k] + xs[k + 1]) / 2, y + (-1.0 if k % 2 else 1.0),
                 xs[k + 1], y, bc))
    for k, x in enumerate(xs):
        helix(x, 16.2 - (k % 2) * 0.4, 26.5 + (k % 2) * 0.4, w=1.1, col=col, border_col=bc)
    body([(cx + 0.2, 12.8, 1.2, 0.9, 0)], '#D8CBE8', border_col='#5E4B8B', shadow=False)
    gaps.append((cx - 5.0, cx + 5.0))

def immune(cx):
    col = COL['rec_imm']
    bc = '#A63A2E'
    for s in (-1, 1):
        x = cx + s * 1.3
        body([(x, 9.2, 1.3, 1.8, 0), (x, 13.6, 1.3, 1.8, 0)], col, border_col=bc, shadow=False)
        helix(x, 15.6, 26.5, w=1.1, col=col, border_col=bc)
    body([(cx, 5.8, 2.2, 1.4, 0)], '#A63A2E', border_col='#8B251B', shadow=False)
    gaps.append((cx - 4.5, cx + 4.5))


def ras_node(cx, cy, col_key, nuc_txt):
    col = COL.get(col_key, '#F1F5F9')
    tc = TC_MAP.get(col_key, INK)
    w, h = 17.0, 9.2
    bc = '#64748B' if col_key in ('off', 'ras_gdp') else '#A63A2E'
    fill_col = D.gradient(col)
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="3.5" '
                 'fill="%s" stroke="%s" stroke-width="0.6"/>'
          % (cx - w / 2, cy - h / 2, w, h, fill_col, bc))
    D.text(cx, cy - 1.4, 'KRAS', anchor='middle', color=tc, bold=True, size=6.8*PT)
    nw, nh = 9.2, 3.2
    nuc_bg = '#8B251B' if col_key in ('on', 'ras_gtp') else '#475569'
    nuc_fill = '#FDF0EE' if col_key in ('on', 'ras_gtp') else '#F1F5F9'
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="1.6" '
                 'fill="%s" stroke="%s" stroke-width="0.35"/>'
          % (cx - nw / 2, cy + 0.8, nw, nh, nuc_fill, nuc_bg))
    D.text(cx, cy + 2.5, nuc_txt, anchor='middle', color=nuc_bg, bold=True, size=5.5*PT)
    return {
        'top': (cx, cy - h / 2),
        'bottom': (cx, cy + h / 2),
        'left': (cx - w / 2, cy),
        'right': (cx + w / 2, cy),
        'cx': cx, 'cy': cy, 'w': w, 'h': h
    }

def build_figure1_svg(lang='en'):
    global D
    D = SVGDoc()
    
    rtk(RX['rtk'])
    integrin(RX['int'])
    gpcr(RX['gpcr'])
    immune(RX['imm'])

    # Distinct matching receptor labels
    if lang == 'cn':
        D.text(RX['rtk'], 2.0, 'RTK受体 (EGFR)', anchor='middle', bold=True, color='#1F3A5F', size=FS)
        D.text(RX['int'], 2.0, '整合素受体', anchor='middle', bold=True, color='#8A5800', size=FS)
        D.text(RX['gpcr'], 2.0, 'GPCR受体', anchor='middle', bold=True, color='#5E4B8B', size=FS)
        D.text(RX['imm'], 2.0, '细胞因子受体', anchor='middle', bold=True, color='#A63A2E', size=FS)
    else:
        D.text(RX['rtk'], 2.0, 'EGFR / RTK', anchor='middle', bold=True, color='#1F3A5F', size=FS)
        D.text(RX['int'], 2.0, 'Integrin', anchor='middle', bold=True, color='#8A5800', size=FS)
        D.text(RX['gpcr'], 2.0, 'GPCR', anchor='middle', bold=True, color='#5E4B8B', size=FS)
        D.text(RX['imm'], 2.0, 'Immune R', anchor='middle', bold=True, color='#A63A2E', size=FS)

    # EGF Ligand Node
    egf_node = pill(RX['rtk'], 5.2, 8.5, 3.6, 'EGF', 'lig')
    arrow(egf_node['bottom'], (RX['rtk'], 7.6), col=ACT_COL, lw=0.50, size=0.85)

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
                          % (x + dx, y, x + dx, y - side * 0.7, x + dx * 0.4, y - side * 1.5))
                D.add('mem', '<circle cx="%.2f" cy="%.2f" r="0.68" fill="#F1F5F9" '
                             'stroke="#94A3B8" stroke-width="0.30"/>' % (x, y))
        x += STEP

    # Phosphorylation sites on RTK intracellular tail
    for s in (-1, 1):
        x = RX['rtk'] + s * 1.4
        D.add('body', '<circle cx="%.2f" cy="30.8" r="1.3" fill="#FEF08A" stroke="#CA8A04" stroke-width="0.35"/>'
              % (x + s * 1.3))
        D.text(x + s * 1.3, 30.8, 'P', anchor='middle', color='#713F12', bold=True, size=4.5*PT)

    # Plasma membrane label: floating cleanly above the bilayer in extracellular space
    D.add('body', '<rect x="70.0" y="14.2" width="18.0" height="3.6" rx="1.4" '
                 'fill="#FFFFFF" stroke="#64748B" stroke-width="0.45"/>')
    if lang == 'cn':
        D.text(79.0, 16.0, '细胞膜', anchor='middle', color='#0F172A', bold=True, size=4.5*PT)
    else:
        D.text(79.0, 16.0, 'Plasma membrane', anchor='middle', color='#0F172A', bold=True, size=4.5*PT)
    D.add('link', '<line x1="79.0" y1="17.8" x2="79.0" y2="19.3" stroke="#64748B" stroke-width="0.45"/>')
    D.add('body', '<circle cx="79.0" cy="19.3" r="0.35" fill="#64748B"/>')

    # Extracellular anti-EGFR antibody callout (placed between EGFR x=20 and Integrin x=58, width 26.5mm: x 27.2 - 53.7)
    if lang == 'cn':
        card_egfr = drug_box(27.2, 4.2, 26.5, 8.5, '抗EGFR单抗', '西妥昔单抗, 帕尼单抗', 'approved', '#1F3A5F')
    else:
        card_egfr = drug_box(27.2, 4.2, 26.5, 8.5, 'Anti-EGFR mAbs', 'cetuximab, panitumumab', 'approved', '#1F3A5F')
    # Inhibitor tee bar sits cleanly at x=25.0 outside EGFR lobe with zero overlap!
    arrow(card_egfr['left'], (25.0, card_egfr['left'][1]), end='tee', col=INH_COL, lw=0.55, size=1.1)

    # Legend annotations in top right
    D.add('bg', '<rect x="147.0" y="1.8" width="32.0" height="16.0" rx="2.0" fill="#FFFFFF" '
                'fill-opacity="0.96" stroke="#CBD5E1" stroke-width="0.45"/>')
    marker(149.5, 3.6, 'approved')
    marker(149.5, 6.6, 'clinical')
    marker(149.5, 9.6, 'preclinical')
    arrow((148.0, 12.5), (151.5, 12.5), col=ACT_COL, lw=0.55, layer='heads')
    arrow((148.0, 15.2), (151.5, 15.2), end='tee', col=INH_COL, lw=0.55, layer='heads')
    if lang == 'cn':
        D.text(153.5, 3.8, '已批准上市靶向药', size=FS_XS, color=INK_MUTED)
        D.text(153.5, 6.8, '临床试验阶段药物', size=FS_XS, color=INK_MUTED)
        D.text(153.5, 9.8, '临床前在研分子', size=FS_XS, color=INK_MUTED)
        D.text(153.5, 12.8, '正向激活级联 (→)', size=FS_XS, color=ACT_COL)
        D.text(153.5, 15.5, '抑制/负反馈 (--|)', size=FS_XS, color=INH_COL)
    else:
        D.text(153.5, 3.8, 'Approved drug class', size=FS_XS, color=INK_MUTED)
        D.text(153.5, 6.8, 'Clinical trials (Ph I–III)', size=FS_XS, color=INK_MUTED)
        D.text(153.5, 9.8, 'Preclinical candidate', size=FS_XS, color=INK_MUTED)
        D.text(153.5, 12.8, 'Activation cascade (→)', size=FS_XS, color=ACT_COL)
        D.text(153.5, 15.5, 'Inhibition / feedback (--|)', size=FS_XS, color=INH_COL)

    # Adaptor nodes: GRB2 -> SHP2 -> SOS1 (cy = 35.5)
    node_grb2 = pill(38.0, 35.5, 12.0, 5.8, 'GRB2', 'adapt')
    node_shp2 = pill(58.0, 35.5, 12.0, 5.8, 'SHP2', 'adapt')
    node_sos1 = pill(78.0, 35.5, 13.5, 5.8, 'SOS1', 'adapt')

    # Phosphorylation sites connection to GRB2
    arrow((24.5, 30.5), (node_grb2['left'][0] - 0.2, node_grb2['cy']),
          c1=(27.5, 30.5), c2=(28.5, 35.5), col=ACT_COL, lw=0.52)
    arrow(node_grb2['right'], (node_shp2['left'][0] - 0.2, node_shp2['cy']), col=ACT_COL, lw=0.50)
    arrow((RX['int'], 27.2), (node_shp2['cx'], node_shp2['top'][1] - 0.2), col=ACT_COL, lw=0.48)
    arrow(node_shp2['right'], (node_sos1['left'][0] - 0.2, node_sos1['cy']), col=ACT_COL, lw=0.50)

    # Upstream Inhibitors Card (SHP2 & SOS1) - Width 24.5mm: x 53.0 - 77.5
    if lang == 'cn':
        card_shp2 = drug_box(53.0, 45.0, 24.5, 8.5, 'SHP2 / SOS1抑制剂', 'TNO155, BI-3406', 'clinical')
    else:
        card_shp2 = drug_box(53.0, 45.0, 24.5, 8.5, 'SHP2 / SOS1 inh.', 'TNO155, BI-3406', 'clinical')

    # SHP2 vertical inhibitor tee-bar: straight up at x=58.0
    arrow((node_shp2['cx'], card_shp2['top'][1]), (node_shp2['cx'], node_shp2['bottom'][1] + 0.5),
          end='tee', col=INH_COL, lw=0.50, size=1.0, tee_angle=0.0)
    # SOS1 vertical inhibitor tee-bar: straight up at x=75.0 (plenty of clearance from title text)
    arrow((75.0, card_shp2['top'][1]), (75.0, node_sos1['bottom'][1] + 0.5),
          end='tee', col=INH_COL, lw=0.50, size=1.0, tee_angle=0.0)

    # Central Switch Nodes
    SW_Y = 36.8
    node_gdp = ras_node(102.0, SW_Y, 'ras_gdp', 'GDP')
    node_gtp = ras_node(138.0, SW_Y, 'ras_gtp', 'GTP')

    # GPCR activation down into KRAS-GDP
    arrow((RX['gpcr'], 26.5), (node_gdp['cx'] - 1.0, node_gdp['top'][1] - 0.2), col=ACT_COL, lw=0.48)
    # Immune R activation down into active KRAS-GTP
    arrow((RX['imm'], 26.5), (node_gtp['cx'], node_gtp['top'][1] - 0.2), col=ACT_COL, lw=0.48)

    # SOS1 DIRECT ACTIVATION OF KRAS-GDP (GEF Exchange)
    arrow(node_sos1['right'], (node_gdp['left'][0] - 0.2, 35.5), col=ACT_COL, lw=0.58)
    if lang == 'cn':
        D.text((node_sos1['right'][0] + node_gdp['left'][0]) / 2, 31.5, 'GEF核苷酸交换',
               anchor='middle', color='#1F3A5F', bold=True, size=4.5*PT, halo=True)
    else:
        D.text((node_sos1['right'][0] + node_gdp['left'][0]) / 2, 31.5, 'GEF exchange',
               anchor='middle', color='#1F3A5F', bold=True, size=4.5*PT, halo=True)

    # GAP (NF1) Cytosolic localization - shifted to cx=117.0 for perfect clearance from GPCR loops
    node_gap = pill(117.0, 26.2, 12.5, 3.8, 'GAP (NF1)', 'gap', border_col='#64748B')
    arrow((node_gap['cx'], node_gap['bottom'][1]), (node_gap['cx'], 30.1), col=ACT_COL, lw=0.50, size=0.85)

    # Upper Arc: GTP -> GDP (Hydrolysis, Grey pathway)
    arrow((129.5, 33.5), (110.5, 33.5), c1=(124.0, 29.8), c2=(116.0, 29.8),
          col=INH_COL, lw=0.60, end='head', size=0.9, layer='heads')

    # Oncogenic Mutation Blockade Badge Element: Centered at cx=120.0, cy=35.0, width 14.5mm (x: 112.75 - 127.25)
    # Generous 2.25mm clearance to KRAS-GDP (110.5) and 2.25mm to KRAS-GTP (129.5)! ZERO OVERLAP!
    D.add('body', '<rect x="112.75" y="33.2" width="14.5" height="3.6" rx="1.4" '
                  'fill="#FDF0EE" stroke="#A63A2E" stroke-width="0.45"/>')
    if lang == 'cn':
        D.text(120.0, 35.0, 'G12/G13/Q61 突变锁死', anchor='middle', color='#8B251B', bold=True, size=4.0*PT)
    else:
        D.text(120.0, 35.0, 'G12/G13/Q61 lock', anchor='middle', color='#8B251B', bold=True, size=4.1*PT)
    # Vertical inhibitor line UP from badge top to upper arc: does NOT cross text!
    arrow((120.0, 33.2), (120.0, 29.8), end='tee', col='#8B251B', lw=0.60, size=1.1, tee_angle=0.0)

    # Lower Arc: GDP -> GTP (GEF Exchange cycle)
    arrow((110.5, 39.8), (129.5, 39.8), c1=(116.0, 45.2), c2=(124.0, 45.2),
          col=ACT_COL, lw=0.60, end='head', size=0.9, layer='heads')
    if lang == 'cn':
        D.text(120.0, 47.2, 'GDP ⇌ GTP 循环', anchor='middle', color='#1F3A5F', bold=True, size=4.6*PT, halo=True)
    else:
        D.text(120.0, 47.2, 'GDP → GTP cycle', anchor='middle', color='#1F3A5F', bold=True, size=4.6*PT, halo=True)

    # Direct Inhibitors
    D.add('body', '<rect x="87.0" y="47.5" width="31.0" height="11.5" rx="1.8" '
                  'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45"/>')
    marker(88.8, 51.5, 'approved')
    marker(88.8, 56.1, 'clinical')
    if lang == 'cn':
        D.text(91.2, 52.1 - FS_SM * 0.35, 'Class I: 索托拉西布, 阿达格拉西布', color=INK, bold=True, size=4.5*PT)
        D.text(91.2, 56.7 - FS_SM * 0.35, 'Class II: MRTX1133 (G12D)', color=INK, bold=True, size=4.5*PT)
    else:
        D.text(91.5, 52.1 - FS_SM * 0.35, 'Class I: sotorasib, adagrasib', color=INK, bold=True, size=5.2*PT)
        D.text(91.5, 56.7 - FS_SM * 0.35, 'Class II: MRTX1133 (G12D)', color=INK, bold=True, size=5.2*PT)
    arrow((102.0, 47.5), (node_gdp['cx'], node_gdp['bottom'][1] + 0.3), end='tee', col=INH_COL, lw=0.55, size=1.1, tee_angle=0.0)

    D.add('body', '<rect x="150.0" y="30.0" width="28.5" height="11.5" rx="1.8" '
                  'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45"/>')
    marker(151.5, 34.0, 'approved')
    marker(151.5, 38.6, 'preclinical')
    if lang == 'cn':
        D.text(153.5, 34.5 - FS_SM * 0.35, 'Class III: 达拉索拉西布 (ON态)', color=INK, bold=True, size=4.8*PT)
        D.text(153.5, 39.1 - FS_SM * 0.35, 'Class IV: ASP3082 (靶向降解)', color=INK, bold=True, size=4.8*PT)
    else:
        D.text(153.5, 34.5 - FS_SM * 0.35, 'Class III: daraxonrasib', color=INK, bold=True, size=5.0*PT)
        D.text(153.5, 39.1 - FS_SM * 0.35, 'Class IV: ASP3082 (PROTAC)', color=INK, bold=True, size=5.0*PT)
    arrow((150.0, 36.8), (node_gtp['right'][0] + 0.3, node_gtp['cy']), end='tee', col=INH_COL, lw=0.55, size=1.1)

    # Downstream Effector Cascades
    BUS_Y = 57.5
    arrow((node_gtp['cx'], node_gtp['bottom'][1]), (node_gtp['cx'], BUS_Y), col=ACT_COL, lw=0.85, size=0.9)
    if lang == 'cn':
        D.text(node_gtp['cx'] + 1.8, 52.5, '招募效应蛋白', anchor='start', color='#1F3A5F', bold=True, size=4.8*PT, halo=True)
    else:
        D.text(node_gtp['cx'] + 1.8, 52.5, 'Effector recruitment', anchor='start', color='#1F3A5F', bold=True, size=4.8*PT, halo=True)

    BUS_X = {'mapk': 18.0, 'rassf': 60.0, 'pi3k': 88.0, 'ral': 132.0, 'cyto': 164.0}
    arrow((node_gtp['cx'], BUS_Y), (BUS_X['mapk'], BUS_Y), col=ACT_COL, lw=0.70)
    arrow((node_gtp['cx'], BUS_Y), (BUS_X['cyto'], BUS_Y), col=ACT_COL, lw=0.70)

    T1, T2, T3 = 69.5, 82.0, 94.5
    OUT_Y, OUT_H = 107.0, 9.5

    # 1. MAPK
    arrow((BUS_X['mapk'], BUS_Y), (BUS_X['mapk'], T1 - 3.2), col=ACT_COL, lw=0.65)
    node_raf = pill(BUS_X['mapk'], T1, 16.0, 6.2, 'RAF', 'mapk')
    node_mek = pill(BUS_X['mapk'], T2, 14.0, 5.8, 'MEK1/2', 'mapk')
    node_erk = pill(BUS_X['mapk'], T3, 14.0, 5.8, 'ERK1/2', 'mapk')

    arrow(node_raf['bottom'], node_mek['top'], col=ACT_COL, lw=0.60)
    arrow(node_mek['bottom'], node_erk['top'], col=ACT_COL, lw=0.60)

    if lang == 'cn':
        card_raf_mek = drug_box(28.5, 78.0, 22.0, 8.0, 'RAF / MEK抑制剂', '曲美替尼, 康奈非尼', 'approved')
        card_erk = drug_box(28.5, 90.7, 22.0, 7.6, 'ERK抑制剂', 'ulixertinib (Ⅰ/Ⅱ期)', 'clinical')
    else:
        card_raf_mek = drug_box(28.5, 78.0, 22.0, 8.0, 'RAF / MEK inh.', 'trametinib, encorafenib', 'approved')
        card_erk = drug_box(28.5, 90.7, 22.0, 7.6, 'ERK inh.', 'ulixertinib (Ph I/II)', 'clinical')

    arrow(card_raf_mek['left'], (node_mek['right'][0] + 0.4, node_mek['cy']), end='tee', col=INH_COL, lw=0.55, size=1.1)
    arrow(card_erk['left'], (node_erk['right'][0] + 0.4, node_erk['cy']), end='tee', col=INH_COL, lw=0.55, size=1.1)

    # Nucleus boundary
    D.add('body', '<path d="M 2.0 99.0 C 15.0 97.0, 35.0 98.0, 48.0 102.0 '
                  'C 47.0 114.0, 44.0 117.0, 42.0 118.0 L 2.0 118.0 Z" '
                  'fill="#F6F3FA" fill-opacity="0.65" stroke="#7D68A8" stroke-width="0.75" stroke-dasharray="2.5,1.5"/>')
    for y_npc in (100.5, 102.5, 104.5):
        D.add('body', '<rect x="42.5" y="%.2f" width="2.2" height="1.0" rx="0.5" fill="#5E4B8B" stroke="#453569" stroke-width="0.25"/>' % y_npc)
    if lang == 'cn':
        D.text(25.5, 100.5, '核孔复合体 (NPC)', color='#5E4B8B', bold=True, size=4.5*PT, halo=True)
        D.text(34.0, 116.0, '细胞核', color='#5E4B8B', bold=True, size=FS_SM, halo=True)
    else:
        D.text(25.5, 100.5, 'Nuclear pore (NPC)', color='#5E4B8B', bold=True, size=4.5*PT, halo=True)
        D.text(34.0, 116.0, 'Nucleus', color='#5E4B8B', bold=True, size=FS_SM, halo=True)

    node_erk_nuc = pill(BUS_X['mapk'], 105.0, 11.0, 4.8, 'ERK (p)', 'mapk')
    arrow(node_erk['bottom'], node_erk_nuc['top'], col=ACT_COL, lw=0.60)
    arrow((node_erk_nuc['left'][0], node_erk_nuc['cy']), (31.5, node_erk_nuc['cy']), col=ACT_COL, lw=0.55)

    if lang == 'cn':
        out_mapk = outcome_box(4.5, 109.5, 27.0, 7.5, '细胞增殖与周期进程', 'CCND1, MYC, FOS, ELK1',
                               '#EEF3F8', '#B0C4DE', '#1F3A5F')
    else:
        out_mapk = outcome_box(4.5, 109.5, 27.0, 7.5, 'Proliferation & Growth', 'CCND1, MYC, FOS, ELK1',
                               '#EEF3F8', '#B0C4DE', '#1F3A5F')
    arrow((BUS_X['mapk'], node_erk_nuc['bottom'][1]), (BUS_X['mapk'], out_mapk['top'][1] - 0.2), col=ACT_COL, lw=0.55)

    # 2. RASSF1A
    arrow((BUS_X['rassf'], BUS_Y), (BUS_X['rassf'], T1 - 3.2), col=ACT_COL, lw=0.60)
    node_rassf = pill(BUS_X['rassf'], T1, 15.0, 6.0, 'RASSF1A', 'rassf')
    node_mst = pill(BUS_X['rassf'], 86.0, 13.0, 5.8, 'MST1/2', 'rassf')
    arrow(node_rassf['bottom'], node_mst['top'], col=ACT_COL, lw=0.55)
    if lang == 'cn':
        out_rassf = outcome_box(50.5, OUT_Y, 19.0, OUT_H, '促凋亡与抑癌', 'MST / YAP1 / p73',
                                '#F7F4FA', '#D8CFE5', '#5E4B8B')
    else:
        out_rassf = outcome_box(50.5, OUT_Y, 19.0, OUT_H, 'Apoptosis', 'MST / YAP1 / p73',
                                '#F7F4FA', '#D8CFE5', '#5E4B8B')
    arrow(node_mst['bottom'], out_rassf['top'], col=ACT_COL, lw=0.55)

    # 3. PI3K
    arrow((BUS_X['pi3k'], BUS_Y), (BUS_X['pi3k'], T1 - 3.2), col=ACT_COL, lw=0.65)
    node_pi3k = pill(BUS_X['pi3k'], T1, 16.0, 6.2, 'PI3K (p110)', 'pi3k')
    node_akt = pill(BUS_X['pi3k'], T2, 13.0, 5.8, 'AKT', 'pi3k')
    node_mtor = pill(BUS_X['pi3k'], T3, 15.0, 5.8, 'mTORC1', 'pi3k')

    arrow(node_pi3k['bottom'], node_akt['top'], col=ACT_COL, lw=0.60)
    arrow(node_akt['bottom'], node_mtor['top'], col=ACT_COL, lw=0.60)

    if lang == 'cn':
        card_pi3k_inh = drug_box(100.0, 65.5, 22.5, 8.0, 'PI3K抑制剂', '阿培利司, 伊那利司', 'approved')
        card_mtor_inh = drug_box(100.0, 90.5, 22.5, 8.0, 'mTOR抑制剂', '依维莫司, 西罗莫司', 'approved')
    else:
        card_pi3k_inh = drug_box(100.0, 65.5, 22.5, 8.0, 'PI3K inh.', 'alpelisib, inavolisib', 'approved')
        card_mtor_inh = drug_box(100.0, 90.5, 22.5, 8.0, 'mTOR inh.', 'everolimus, sirolimus', 'approved')

    arrow(card_pi3k_inh['left'], (node_pi3k['right'][0] + 0.4, node_pi3k['cy']), end='tee', col=INH_COL, lw=0.55, size=1.1)
    arrow(card_mtor_inh['left'], (node_mtor['right'][0] + 0.4, node_mtor['cy']), end='tee', col=INH_COL, lw=0.55, size=1.1)

    if lang == 'cn':
        out_pi3k = outcome_box(76.0, OUT_Y, 24.0, OUT_H, '存活促进与代谢合成', 'S6K1, 4E-BP1, 糖酵解',
                               '#EDF5F5', '#A3CECE', '#2A6F6F')
    else:
        out_pi3k = outcome_box(76.0, OUT_Y, 24.0, OUT_H, 'Survival & Growth', 'S6K1, 4E-BP1, glycolysis',
                               '#EDF5F5', '#A3CECE', '#2A6F6F')
    arrow(node_mtor['bottom'], out_pi3k['top'], col=ACT_COL, lw=0.60)

    # 4. RAL
    arrow((BUS_X['ral'], BUS_Y), (BUS_X['ral'], T1 - 3.2), col=ACT_COL, lw=0.60)
    node_ralgds = pill(BUS_X['ral'], T1, 15.0, 6.0, 'RALGDS', 'ral')
    node_ral = pill(BUS_X['ral'], T2, 13.0, 5.8, 'RAL-A/B', 'ral')
    node_tbk1 = pill(BUS_X['ral'], T3, 15.0, 5.8, 'TBK1 / Sec5', 'ral')
    arrow(node_ralgds['bottom'], node_ral['top'], col=ACT_COL, lw=0.55)
    arrow(node_ral['bottom'], node_tbk1['top'], col=ACT_COL, lw=0.55)
    if lang == 'cn':
        out_ral = outcome_box(120.0, OUT_Y, 24.0, OUT_H, '囊泡运输与极性', '外泌小体与自噬调控',
                              '#F0F4F8', '#AFC1D0', '#3E6B89')
    else:
        out_ral = outcome_box(120.0, OUT_Y, 24.0, OUT_H, 'Vesicle Trafficking', 'Exocyst & autophagy',
                              '#F0F4F8', '#AFC1D0', '#3E6B89')
    arrow(node_tbk1['bottom'], out_ral['top'], col=ACT_COL, lw=0.55)

    # 5. Cytoskeletal / PLC
    arrow((BUS_X['cyto'], BUS_Y), (157.0, T1 - 3.2), col=ACT_COL, lw=0.55)
    arrow((BUS_X['cyto'], BUS_Y), (171.0, T1 - 3.2), col=ACT_COL, lw=0.55)
    node_plce = pill(157.0, T1, 12.0, 5.8, 'PLCε', 'other')
    node_tiam1 = pill(171.0, T1, 12.0, 5.8, 'TIAM1', 'other')
    node_rac1 = pill(BUS_X['cyto'], T2, 16.0, 6.0, 'PKC / RAC1', 'other')
    arrow(node_plce['bottom'], (161.0, node_rac1['top'][1]), col=ACT_COL, lw=0.50)
    arrow(node_tiam1['bottom'], (167.0, node_rac1['top'][1]), col=ACT_COL, lw=0.50)
    node_actin = pill(BUS_X['cyto'], T3, 21.0, 5.8, 'F-actin assembly', 'other')
    arrow(node_rac1['bottom'], node_actin['top'], col=ACT_COL, lw=0.55)
    if lang == 'cn':
        out_cyto = outcome_box(152.0, OUT_Y, 24.0, OUT_H, '骨架动力学与侵袭', '肌动蛋白动力学与迁移',
                               '#FAF4E8', '#E2D3B8', '#8A5800')
    else:
        out_cyto = outcome_box(152.0, OUT_Y, 24.0, OUT_H, 'Motility & Invasion', 'Actin dynamics & migration',
                               '#FAF4E8', '#E2D3B8', '#8A5800')
    arrow(node_actin['bottom'], out_cyto['top'], col=ACT_COL, lw=0.55)

    # ERK Negative Feedback Loop (clean left-hand orthogonal routing)
    FX_L = 4.5
    # Connect from ERK left border to FX_L and run vertically up to EGFR level (y=19.5)
    arrow(node_erk['left'], (FX_L, node_erk['cy']), end='none', col=INH_COL, dash='2.5,1.5', lw=0.60)
    arrow((FX_L, node_erk['cy']), (FX_L, 19.5), end='none', col=INH_COL, dash='2.5,1.5', lw=0.60)

    # Branch 1 to RAF
    arrow((FX_L, node_raf['cy']), (node_raf['left'][0] - 0.5, node_raf['cy']),
          end='tee', col=INH_COL, dash='2.5,1.5', lw=0.60, size=1.1, tee_angle=-math.pi/2)

    # Branch 2 to SOS1 (crosses horizontally at y=55.0 to x=82.0, then straight UP to SOS1 bottom)
    arrow((FX_L, 55.0), (82.0, 55.0), end='none', col=INH_COL, dash='2.5,1.5', lw=0.60)
    arrow((82.0, 55.0), (82.0, node_sos1['bottom'][1] + 0.5),
          end='tee', col=INH_COL, dash='2.5,1.5', lw=0.60, size=1.1, tee_angle=0.0)

    # Branch 3 to EGFR intracellular tail
    arrow((FX_L, 19.5), (15.0, 19.5), end='tee', col=INH_COL, dash='2.5,1.5', lw=0.60, size=1.1, tee_angle=math.pi/2)

    if lang == 'cn':
        D.text(38.0, 53.6, 'ERK 负反馈磷酸化抑制', anchor='middle', color=INH_COL, bold=True, size=5.0*PT, halo=True)
    else:
        D.text(38.0, 53.6, 'ERK negative feedback', anchor='middle', color=INH_COL, bold=True, size=5.2*PT, halo=True)

    # Panel a Letter
    D.text(1.0, 2.5, 'a', bold=True, size=PNs, color=INK)

    # ============================================================ PANEL B =========
    D.add('bg', '<line x1="0" y1="%.2f" x2="180" y2="%.2f" stroke="#CBD5E1" stroke-width="0.6"/>'
          % (BOT_A, BOT_A))

    BY = 120.5
    CW, CG = 43.0, 2.0
    BH = 49.5

    if lang == 'cn':
        CARDS = [
            ('代谢重编程',
             '瓦氏效应与谷氨酰胺分解',
             'GOT1与GLS1代谢流维持NADPH抗氧化稳态',
             'GOT1, GLS1, MCT4抑制剂', 'preclinical'),
            ('巨胞饮与自噬',
             '胞外营养捕获与溶酶体回收',
             '大泡内吞摄取细胞外液以维持氨基酸库',
             '羟氯喹 (HCQ) 联合方案', 'clinical'),
            ('免疫抑制微环境',
             '免疫排斥与骨髓抑制细胞浸润',
             'MDSC募集浸润并诱导CD8+ T细胞耗竭',
             'PD-(L)1抗体; RAS肿瘤疫苗', 'clinical'),
            ('逃逸细胞衰老',
             '突破癌基因诱导的细胞衰老屏障',
             'CDK4/6过度活化驱动Rb蛋白过度磷酸化',
             '衰老清除剂; CDK4/6抑制剂', 'clinical'),
        ]
        drug_subtitle = '靶向干预联合策略'
    else:
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
        drug_subtitle = 'Targeted therapeutic strategy'

    IMG_B64 = {}
    for k, fname in enumerate(['metabolism.jpg', 'macropinocytosis.jpg', 'immune.jpg', 'senescence.jpg']):
        fpath = os.path.join(ASSET_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, 'rb') as fh:
                IMG_B64[k] = base64.b64encode(fh.read()).decode('utf-8')

    for k, (title, sub, mech, drug, status) in enumerate(CARDS):
        x = k * (CW + CG) + 1.0
        D.add('bg', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2.2" '
                    'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45"/>'
              % (x, BY, CW, BH))
        
        if k in IMG_B64:
            D.add('body', '<image xlink:href="data:image/jpeg;base64,%s" href="data:image/jpeg;base64,%s" x="%.2f" y="%.2f" width="%.2f" height="19.50" '
                         'preserveAspectRatio="xMidYMid meet"/>'
                  % (IMG_B64[k], IMG_B64[k], x + 1.2, BY + 1.5, CW - 2.4))
            
        ty = BY + 22.8
        D.text(x + 2.5, ty, title, bold=True, color=INK, size=FS)
        D.text(x + 2.5, ty + 4.0, sub, color=ACT_COL, bold=True, size=FS_XS)
        D.text(x + 2.5, ty + 7.8, mech, color=INK_MUTED, size=4.2*PT)
        drug_box(x + 1.8, BY + 37.5, CW - 3.6, 9.8, drug, subtitle=drug_subtitle, status=status)

    D.text(1.0, BY + 2.5, 'b', bold=True, size=PNs, color=INK)

    return D.svg()

def main():
    CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    
    for lang in ('en', 'cn'):
        svg_str = build_figure1_svg(lang=lang)
        
        suffixes = ['_EN'] if lang == 'en' else ['_CN', '_中文版']
        if lang == 'en':
            suffixes.append('')
            
        for suf in suffixes:
            if suf == '_中文版':
                out_name = 'Figure1_RAS信号通路与干预靶点_中文版'
            else:
                out_name = NAME + suf
                
            svg_file = os.path.join(FIG, out_name + '.svg')
            png_file = os.path.join(FIG, out_name + '.png')
            pdf_file = os.path.join(FIG, out_name + '.pdf')
            
            with open(svg_file, 'w', encoding='utf-8') as fh:
                fh.write(svg_str)
                
            subprocess.run(['/opt/homebrew/bin/rsvg-convert', '--dpi-x', '400', '--dpi-y', '400', '-b', 'white',
                            '-o', png_file, svg_file], check=True)
            try:
                from PIL import Image
                _im = Image.open(png_file)
                _im.save(png_file, dpi=(400, 400))
            except Exception as _e:
                pass
                            
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
                
            print(f"Rendered Figure 1 [{lang} - {suf}]:")
            print("  ->", png_file)
            print("  ->", pdf_file)
            print("  ->", svg_file)

            # Sync to all relevant project directories
            for sdir in SYNC_DIRS:
                if os.path.exists(sdir):
                    for ext in ('.png', '.pdf', '.svg'):
                        src = os.path.join(FIG, out_name + ext)
                        dst = os.path.join(sdir, out_name + ext)
                        shutil.copy2(src, dst)
                    print(f"Synchronized Figure 1 [{out_name}] to:", sdir)

    # Legacy file name sync
    legacy_dst = "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件/图1_RAS信号网络与可干预节点-1.png"
    if os.path.exists(os.path.dirname(legacy_dst)):
        shutil.copy2(os.path.join(FIG, NAME + '_CN.png'), legacy_dst)
        print("Synchronized to legacy name with Chinese edition:", legacy_dst)

if __name__ == '__main__':
    main()
