#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure 1 - The RAS Signalling Network, drawn as a cell-biology illustration.

Plots:
  Panel a: Cell-wide molecular mechanism diagram: plasma membrane receptors (RTK, Integrin,
           GPCR, Immune), adaptors (GRB2, SOS1, SHP2), the central GDP/GTP switch (NF1/RASA1, GEFs),
           effector cascades (MAPK, PI3K-AKT-mTOR, RALGDS, PLCε, TIAM1, RASSF1A), and targeted drug classes.
  Panel b: Four phenotypic hallmarks: metabolic reprogramming, macropinocytosis/autophagy,
           immunosuppressive microenvironment, and oncogene-induced senescence.

Usage:
  python3 run_figure1.py
Output:
  ../vector_figures/Figure1_RAS_signalling_network.pdf
  ../vector_figures/Figure1_RAS_signalling_network.svg
  ../vector_figures/Figure1_RAS_signalling_network.png
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

W, H = 180.0, 0.0                        # mm; double column standard
PT = 25.4 / 72
FS = 7.5 * PT                             # 7.5 pt font size
PNs = 9.0 * PT                            # 9.0 pt bold panel letters
LH = FS * 1.28                            # line pitch

# High-contrast publication typography
INK = '#0F172A'          # Deep slate black for primary text (WCAG AAA)
INK_MUTED = '#334155'    # Slate for secondary labels
GREY = '#475569'         # Muted grey
WHITE = '#FFFFFF'

# Curated harmonious color theme with high-contrast semantics
COL = {
    'rec': '#9FBAD3',     # Receptors: Clear periwinkle blue
    'adapt': '#5878A6',   # Adaptors (GRB2, SOS1, SHP2): Steel blue (Deep)
    'gef': '#7EB2A8',     # Tissue GEFs: Deepened sage mint
    'off': '#C5E2F0',     # RAS-GDP: Soft ice blue
    'on': '#E88B94',      # RAS-GTP: Vibrant coral pink
    'gap': '#CBD5E1',     # GAPs: Crisp slate silver
    'mapk': '#5878A6',    # MAPK trunk: Steel blue
    'pi3k': '#6FAFA0',    # PI3K trunk: Deepened jade mint
    'ral': '#7BA6D4',     # RAL trunk: Clear azure blue
    'other': '#E6B8A2',   # PLCε & TIAM1: Warm terracotta apricot
    'lig': '#E29578',     # Ligands: Warm coral amber
    'red': '#BE123C',     # Warnings/Feedback: Vivid ruby crimson (High contrast)
    'rassf': '#94A3B8',   # RASSF1A: Neutral slate
}

# Protein node text color mapping:
# Deep nodes get crisp bold WHITE; light/medium nodes get deep INK (#0F172A)
TC_MAP = {
    'adapt': WHITE,
    'mapk': WHITE,
    'rec': INK,
    'gef': INK,
    'off': INK,
    'on': INK,
    'gap': INK,
    'pi3k': INK,
    'ral': INK,
    'other': INK,
    'rassf': INK,
}

SANS = "PingFang SC, Arial Unicode MS, Arial, Helvetica, sans-serif"

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
            for tag, f in (('<i>', 'it1'), ('</i>', 'it0'), ('<b>', 'bd1'), ('</b>', 'bd0')):
                if s.startswith(tag):
                    if f == 'it1': it = True
                    elif f == 'it0': it = False
                    elif f == 'bd1': bd = True
                    else: bd = bold
                    s = s[len(tag):]
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
        self.boxes = []

    def add(self, layer, s):
        self.L[layer].append(s)

    def gradient(self, col):
        gid = 'g' + col[1:]
        if gid not in self.grad:
            self.grad[gid] = (
                '<radialGradient id="%s" cx="0.36" cy="0.30" r="0.80" fx="0.32" '
                'fy="0.24"><stop offset="0" stop-color="%s"/><stop offset="0.60" '
                'stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                % (gid, mix(col, WHITE, 0.40), col, mix(col, '#000000', 0.22)))
        return 'url(#%s)' % gid

    def text(self, x, y, s, anchor='start', color=INK, bold=False, size=FS,
             layer='text', rot=None, audit=True, opacity=None, halo=False):
        w = tw(s, bold, size)
        yb = y + size * 0.355
        tf = ' transform="rotate(%.1f %.2f %.2f)"' % (rot, x, y) if rot else ''
        op = ' fill-opacity="%.2f"' % opacity if opacity else ''
        spans = ''.join(
            '<tspan%s%s>%s</tspan>' % (' font-style="italic"' if it else '',
                                        ' font-weight="bold"' if bd else '', esc(t))
            for t, it, bd in segs(s, bold))
        
        if halo:
            self.add(layer, '<text x="%.2f" y="%.2f" font-size="%.3f" fill="#FFFFFF" '
                     'stroke="#FFFFFF" stroke-width="1.8" stroke-linejoin="round" '
                     'text-anchor="%s"%s xml:space="preserve">%s</text>'
                     % (x, yb, size, anchor, tf, spans))
            
        self.add(layer, '<text x="%.2f" y="%.2f" font-size="%.3f" fill="%s" '
                 'text-anchor="%s"%s%s xml:space="preserve">%s</text>'
                 % (x, yb, size, color, anchor, tf, op, spans))
        if audit and not rot:
            x0 = x - (w if anchor == 'end' else w / 2 if anchor == 'middle' else 0)
            self.boxes.append((x0, y - size * 0.40, x0 + w, y + size * 0.40, s))
        return w

    def lines(self, x, y, rows, **kw):
        for k, r in enumerate(rows):
            self.text(x, y + k * LH, r, **kw)

    def svg(self):
        body = ''.join(''.join(self.L[k]) for k in self.L)
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%gmm" height="%gmm" '
                'viewBox="0 0 %g %g" font-family="%s">'
                '<defs>%s%s</defs>%s</svg>' % (W, H, W, H, SANS,
                                               ''.join(self.grad.values()), DEFS, body))

DEFS = (
    '<linearGradient id="exo" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#F1F5F9"/><stop offset="1" stop-color="#F8FAFC"/>'
    '</linearGradient>'
    '<linearGradient id="cyto" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F8FAFC"/>'
    '</linearGradient>'
    '<radialGradient id="head" cx="0.38" cy="0.32" r="0.75">'
    '<stop offset="0" stop-color="#E2E8F0"/><stop offset="1" stop-color="#94A3B8"/>'
    '</radialGradient>'
    '<radialGradient id="nuc" cx="0.45" cy="0.25" r="0.8">'
    '<stop offset="0" stop-color="#F1EEF5"/><stop offset="1" stop-color="#E5DEEB"/>'
    '</radialGradient>'
    '<linearGradient id="card" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFFFFF"/>'
    '</linearGradient>'
    '<clipPath id="clipA"><rect x="0" y="0" width="180" height="123" rx="2.2"/></clipPath>'
    '<filter id="subtle-shadow" x="-5%" y="-5%" width="110%" height="115%">'
    '<feDropShadow dx="0" dy="0.6" stdDeviation="0.8" flood-color="#0F172A" flood-opacity="0.06"/>'
    '</filter>'
)

D = Doc()

def pts_path(pts, close=True):
    return 'M' + ' L'.join('%.2f %.2f' % p for p in pts) + (' Z' if close else '')

def ell_pts(cx, cy, rx, ry, rot=0.0, n=56):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for k in range(n):
        t = 2 * math.pi * k / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out

def body(lobes, col, layer='body', lw=0.36, shadow=True, hl=None):
    d = ' '.join(pts_path(ell_pts(*lo)) for lo in lobes)
    if shadow:
        D.add(layer, '<path d="%s" fill="#0F172A" fill-opacity="0.08" '
                     'transform="translate(0.35 0.5)"/>' % d)
    D.add(layer, '<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" '
                 'stroke-linejoin="round"/>' % (d, mix(col, '#000000', 0.40), 2 * lw))
    D.add(layer, '<path d="%s" fill="%s"/>' % (d, D.gradient(col)))
    if hl:
        hx, hy, hrx, hry = hl
        D.add(layer, '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="#FFFFFF" '
                     'fill-opacity="0.32"/>' % (hx, hy, hrx, hry))

SHAPES = {
    'bi': lambda w, h: [(-0.19 * w, 0.02 * h, 0.33 * w, 0.48 * h, -8),
                        (0.20 * w, -0.03 * h, 0.31 * w, 0.45 * h, 10)],
    'tri': lambda w, h: [(-0.31 * w, 0.03 * h, 0.22 * w, 0.43 * h, 0),
                         (0.00 * w, -0.03 * h, 0.25 * w, 0.50 * h, 0),
                         (0.31 * w, 0.04 * h, 0.21 * w, 0.42 * h, 0)],
    'round': lambda w, h: [(0, 0, 0.5 * w, 0.5 * h, 0)],
    'kidney': lambda w, h: [(-0.22 * w, 0.06 * h, 0.30 * w, 0.44 * h, 20),
                            (0.18 * w, -0.05 * h, 0.34 * w, 0.48 * h, -12),
                            (0.05 * w, 0.22 * h, 0.22 * w, 0.26 * h, 0)],
}

def protein(cx, cy, w, h, label, col_key, shape='bi', rows=None, layer='body'):
    col = COL[col_key]
    tc = TC_MAP.get(col_key, INK)
    lobes = [(cx + a, cy + b, rx, ry, r) for a, b, rx, ry, r in SHAPES[shape](w, h)]
    body(lobes, col, layer=layer,
         hl=(cx - 0.20 * w, cy - 0.24 * h, 0.16 * w, 0.10 * h))
    rows = rows or [label]
    y0 = cy - (len(rows) - 1) * LH / 2
    for k, r in enumerate(rows):
        D.text(cx, y0 + k * LH, r, anchor='middle', color=tc, bold=True, audit=False)

def head(p, q, col, size=1.35, layer='link'):
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    a, b = size, size * 0.42
    pts = [q, (q[0] - a * math.cos(ang) + b * math.sin(ang),
               q[1] - a * math.sin(ang) - b * math.cos(ang)),
           (q[0] - a * math.cos(ang) - b * math.sin(ang),
            q[1] - a * math.sin(ang) + b * math.cos(ang))]
    D.add(layer, '<path d="%s" fill="%s"/>' % (pts_path(pts), col))

def arrow(p0, p1, c1=None, c2=None, col=INK, lw=0.48, end='head', dash=None,
          layer='link', hs=1.35):
    c1 = c1 or p0
    c2 = c2 or p1
    tail = c2 if c2 != p1 else c1 if c1 != p1 else p0
    ang = math.atan2(p1[1] - tail[1], p1[0] - tail[0])
    q = p1
    if end == 'head':
        q = (p1[0] - hs * 0.7 * math.cos(ang), p1[1] - hs * 0.7 * math.sin(ang))
    da = ' stroke-dasharray="%s"' % dash if dash else ''
    D.add(layer, '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f" fill="none" '
                 'stroke="%s" stroke-width="%.2f" stroke-linecap="round"%s/>'
          % (p0[0], p0[1], c1[0], c1[1], c2[0], c2[1], q[0], q[1], col, lw, da))
    if end == 'head':
        head(tail, p1, col, hs, layer)
    elif end == 'tee':
        nx, ny = -math.sin(ang), math.cos(ang)
        D.add(layer, '<path d="M%.2f %.2f L%.2f %.2f" stroke="%s" stroke-width="%.2f" '
                     'stroke-linecap="round"/>'
              % (p1[0] + nx, p1[1] + ny, p1[0] - nx, p1[1] - ny, col, lw * 1.8))

def marker(x, y, status, col=INK, s=1.05):
    if status == 'approved':
        D.add('text', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>'
              % (x, y, 0.85 * s, col))
    elif status == 'clinical':
        D.add('text', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" rx="0.2"/>'
              % (x - 0.75 * s, y - 0.75 * s, 1.50 * s, 1.50 * s, col))
    else:
        D.add('text', '<path d="%s" fill="%s"/>' % (pts_path(
            [(x, y - 1.0 * s), (x + 0.92 * s, y + 0.65 * s),
             (x - 0.92 * s, y + 0.65 * s)]), col))

def tag(x, y, rows, status, color=INK, halo=False):
    if isinstance(rows, str):
        rows = [rows]
    marker(x + 1.0, y, status, color)
    D.lines(x + 2.8, y, rows, color=color, halo=halo)
    return x + 2.8 + max(tw(r) for r in rows)

# ============================================================ PANEL A ========
M = 22.0
HR, HD = 0.60, 2.05
BOT = 123.0

D.add('bg', '<g clip-path="url(#clipA)">')
D.add('bg', '<rect x="0" y="0" width="180" height="%.2f" fill="url(#exo)"/>' % M)
D.add('bg', '<rect x="0" y="%.2f" width="180" height="%.2f" fill="url(#cyto)"/>'
      % (M, BOT - M))
D.add('bg', '</g>')

REC = '#7F9DB9'
gaps = []

def helix(x, y0, y1, w=1.35, col=REC, layer='body'):
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.28"/>'
          % (x - w / 2, y0, w, y1 - y0, w / 2, D.gradient(col),
             mix(col, '#000000', 0.40)))

def rtk(cx):
    for s in (-1, 1):
        x = cx + s * 2.25
        body([(x + s * 0.3, 9.6, 1.9, 2.5, 0), (x + s * 0.1, 14.4, 1.7, 2.3, 0)], REC, shadow=False)
        helix(x, 16.5, 27.0, w=1.2)
        body([(x + s * 0.4, 28.6, 2.3, 1.9, 0)], REC, shadow=False)
        for k, yy in enumerate((31.0,)):
            D.add('over', '<circle cx="%.2f" cy="%.2f" r="0.65" fill="#EAB308" stroke="#854D0E" '
                          'stroke-width="0.22"/>' % (x + s * 1.3, yy))
    body([(cx, 6.3, 1.9, 1.3, 0)], COL['lig'], shadow=False)
    gaps.append((cx - 3.6, cx + 3.6))

def integrin(cx):
    for s, top in ((-1, 9.0), (1, 10.4)):
        x = cx + s * 1.6
        D.add('body', '<path d="M%.2f %.2f L%.2f %.2f L%.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="1.2" stroke-linecap="round" '
                      'stroke-linejoin="round"/>'
              % (x, top + 1.5, x, M + HD + 1.0, x + s * 0.9, 27.6,
                 mix(REC, '#000000', 0.20)))
        body([(x + s * 0.5, top, 2.0, 1.6, s * 20)], REC, shadow=False)
    pts = [(cx - 8 + k * 0.4, 5.6 + 0.55 * math.sin(k * 0.55)) for k in range(41)]
    D.add('body', '<path d="%s" fill="none" stroke="#A8A29E" stroke-width="0.9" '
                  'stroke-linecap="round"/>' % pts_path(pts, False))
    gaps.append((cx - 2.6, cx + 2.6))

def gpcr(cx):
    xs = [cx - 4.2 + k * 1.4 for k in range(7)]
    for k in range(6):
        y = 16.9 if k % 2 else 27.1
        D.add('body', '<path d="M%.2f %.2f Q%.2f %.2f %.2f %.2f" fill="none" '
                      'stroke="%s" stroke-width="0.5"/>'
              % (xs[k], y, (xs[k] + xs[k + 1]) / 2, y + (-1.2 if k % 2 else 1.2),
                 xs[k + 1], y, mix(REC, '#000000', 0.35)))
    for k, x in enumerate(xs):
        helix(x, 17.0 - (k % 2) * 0.5, 27.0 + (k % 2) * 0.5, w=1.15)
    body([(cx + 0.3, 13.6, 1.3, 1.0, 0)], COL['lig'], shadow=False)
    gaps.append((cx - 5.0, cx + 5.0))

def immune(cx):
    for s in (-1, 1):
        x = cx + s * 1.25
        body([(x, 10.2, 1.4, 1.9, 0), (x, 14.6, 1.4, 1.9, 0)], REC, shadow=False)
        helix(x, 16.6, 27.0, w=1.1)
    for s in (-1, 1):
        x = cx + s * 4.0
        helix(x, 18.0, 27.0, w=1.0, col='#5B82A6')
        D.add('body', '<path d="M%.2f 27 L%.2f 30.2" stroke="#5B82A6" '
                      'stroke-width="0.85" stroke-linecap="round"/>' % (x, x + s * 0.4))
    body([(cx, 6.6, 2.6, 1.5, 0)], '#BE123C', shadow=False)
    gaps.append((cx - 4.8, cx + 4.8))

RX = {'rtk': 11.0, 'int': 31.0, 'gpcr': 48.0, 'imm': 66.0}
rtk(RX['rtk']); integrin(RX['int']); gpcr(RX['gpcr']); immune(RX['imm'])
for k, lb in (('rtk', 'RTK'), ('int', 'Integrin'), ('gpcr', 'GPCR'),
              ('imm', 'Immune receptor')):
    D.text(RX[k], 2.6, lb, anchor='middle', bold=True, color=INK)

STEP = 1.36
x = 0.7
while x < 180:
    if not any(a - HR <= x <= b + HR for a, b in gaps):
        for side in (-1, 1):
            y = M + side * HD
            for dx in (-0.25, 0.25):
                D.add('mem', '<path d="M%.2f %.2f Q%.2f %.2f %.2f %.2f" fill="none" '
                             'stroke="#CBD5E1" stroke-width="0.28"/>'
                      % (x + dx, y - side * 0.4, x + dx * 2.2, y - side * 1.1,
                         x + dx, M - side * 0.12))
            D.add('mem', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="url(#head)"/>'
                  % (x, y, HR))
    x += STEP
D.text(178.5, 17.6, 'Plasma membrane', anchor='end', color=GREY, bold=True)

KX = 127.0
for k, (st, lb) in enumerate((('approved', 'Approved drug class'),
                              ('clinical', 'In clinical trials (phase I–III)'),
                              ('preclinical', 'Preclinical only, or abandoned'))):
    tag(KX, 3.6 + k * LH, lb, st, color=INK)

protein(10.6, 35.4, 10.0, 6.4, 'GRB2', 'adapt', 'tri')
protein(23.6, 36.6, 13.0, 8.0, 'SOS1', 'adapt', 'bi')
protein(36.6, 38.4, 10.0, 6.4, 'SHP2', 'adapt', 'tri')
protein(59.0, 36.8, 15.0, 7.2, 'GEFs', 'gef', 'kidney')
D.text(47.0, 43.4, 'tissue-restricted', color=GREY, bold=True)

arrow((32.0, 28.6), (35.4, 34.8), (33.2, 30.6), (34.8, 32.6), col=INK_MUTED)
arrow((14.2, 30.6), (33.2, 35.4), (22.0, 28.0), (29.0, 29.6), col=INK_MUTED)
arrow((47.0, 30.4), (55.0, 33.6), (48.6, 32.4), (52.0, 33.2), col=INK_MUTED)
arrow((65.0, 30.6), (62.0, 33.6), (64.6, 31.8), (63.2, 32.8), col=INK_MUTED)

DSHP = '1.1 0.7'
arrow((36.6, 34.9), (36.6, 28.2), end='none', col='#2563EB', dash=DSHP, lw=0.55)
arrow((36.6, 28.2), (83.5, 28.2), end='none', col='#2563EB', dash=DSHP, lw=0.55)
arrow((83.5, 28.2), (83.5, 34.8), col='#2563EB', dash=DSHP, lw=0.55)
D.text(82.5, 29.8, 'pY32/pY64', anchor='end', color='#1D4ED8', bold=True)

GDP, GTP, SY = 89.0, 125.0, 39.6

def ras(cx, cy, col_key, nuc, tside):
    col = COL[col_key]
    tc = TC_MAP.get(col_key, INK)
    tx = cx + tside * 4.2
    D.add('under', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f" fill="none" '
                   'stroke="%s" stroke-width="0.6" stroke-linecap="round"/>'
          % (cx + tside * 2.5, cy - 5.0, cx + tside * 3.5, cy - 8.0, tx, cy - 10.0,
             tx, M + HD + 0.6, mix(col, '#000000', 0.35)))
    zz = [(tx + (0.45 if k % 2 else -0.45), M + HD + 0.6 - k * 0.75) for k in range(5)]
    D.add('over', '<path d="%s" fill="none" stroke="#D97706" stroke-width="0.55" '
                  'stroke-linejoin="round"/>' % pts_path(zz, False))
    body([(cx, cy, 7.8, 6.2, 0), (cx + 2.6, cy - 3.0, 3.2, 2.4, 0)], col,
         hl=(cx - 2.4, cy - 2.8, 2.6, 1.3))
    D.text(cx, cy - 1.8, 'RAS', anchor='middle', color=tc, bold=True, audit=False)
    nw = 9.2
    D.add('body', '<rect x="%.2f" y="%.2f" width="%.2f" height="3.4" rx="1.7" '
                  'fill="#FFFFFF" stroke="%s" stroke-width="0.38"/>'
          % (cx - nw / 2, cy + 0.5, nw, mix(col, '#000000', 0.45)))
    nuc_color = '#1E3A8A' if nuc == 'GDP' else '#991B1B'
    D.text(cx, cy + 2.3, nuc, anchor='middle', color=nuc_color, bold=True, audit=False)

ras(GDP, SY, 'off', 'GDP', -1)
ras(GTP, SY, 'on', 'GTP', 1)

protein(107.0, 29.2, 19.0, 6.2, 'NF1, RASA1', 'gap', 'bi')
D.text(107.0, 34.0, 'GAPs', anchor='middle', color=GREY, bold=True)

arrow((117.4, 37.0), (96.8, 37.0), (113.0, 35.0), (101.2, 35.0), col=INK, lw=0.65)
D.text(107.0, 40.5, 'hydrolysis', anchor='middle', color=GREY, bold=True, halo=True)

arrow((96.8, 44.4), (117.4, 44.4), (101.2, 47.0), (113.0, 47.0), col=INK, lw=0.65)
D.text(107.0, 50.4, 'exchange', anchor='middle', color=GREY, bold=True, halo=True)

arrow((27.4, 40.6), (97.0, 46.4), (32.0, 50.5), (78.0, 52.0), col=COL['adapt'], lw=0.55)
arrow((67.0, 40.0), (98.5, 46.2), (72.0, 47.0), (84.0, 49.5), col='#0D9488', lw=0.55)

NX = 135.5
D.lines(NX, 27.6, [
    'G12, G13 and Q61 substitutions',
    'blunt GAP-stimulated hydrolysis:',
    'mutant RAS accumulates GTP-bound'
], color='#991B1B', bold=True)

D.lines(NX, 27.6 + 3 * LH + 1.2, [
    'NF1 is lost in <i>NF1</i>-mutant tumours;',
    'germline loss causes RASopathies'
], color=GREY)

TY = 54.4
tag(6.0, TY, 'SHP2 and SOS1 inhibitors', 'clinical', color=INK)
tag(61.0, TY, 'OFF-state covalent (<i>KRAS</i> G12C)', 'approved', color=INK)
tag(61.0, TY + LH, 'OFF-state, non-cysteine alleles', 'clinical', color=INK)

tag(131.0, TY - 2 * LH + 0.4, [
    'RAS(ON) tri-complex inhibitors,',
    'allele- and multi-selective'
], 'approved', color=INK)
tag(131.0, TY + LH, 'Degraders; effector-interface binders', 'clinical', color=INK)

T1, T2, T3 = 73.4, 86.0, 98.4
BR = {'mapk': 20.0, 'rassf': 50.0, 'pi3k': 78.0, 'ral': 120.0, 'plc': 147.0, 'tiam': 168.0}
FY = 62.6

arrow((GTP, SY + 6.1), (GTP, FY), end='none', col=INK, lw=0.65)
D.text(GTP - 1.6, FY - 1.4, 'effector binding', anchor='end', color=GREY, bold=True)

for k, x in BR.items():
    arrow((GTP, FY), (x, T1 - 5.4), (GTP, FY + 3.0), (x, FY + 1.2), col=INK, lw=0.50)

M2X = 99.0
arrow((GTP, FY), (M2X, T1 - 4.4), (GTP, FY + 2.6), (M2X, FY + 1.2), col=INK, lw=0.50)

protein(BR['mapk'], T1, 22.0, 9.4, None, 'mapk', 'bi', rows=['RAF', '(BRAF, CRAF)'])
protein(BR['mapk'], T2, 20.0, 7.4, 'MEK1/2', 'mapk', 'bi')
protein(BR['mapk'], T3, 20.0, 7.4, 'ERK1/2', 'mapk', 'bi')

protein(BR['pi3k'], T1, 20.0, 9.4, None, 'pi3k', 'bi', rows=['PI3K', '(p110)'])
protein(BR['pi3k'], T2, 16.0, 7.4, 'AKT', 'pi3k', 'bi')
protein(BR['pi3k'], T3, 20.0, 7.4, 'mTORC1', 'pi3k', 'tri')

protein(BR['ral'], T1, 20.0, 8.2, 'RALGDS', 'ral', 'bi')
protein(BR['ral'], T2, 11.0, 7.0, 'RAL', 'ral', 'round')
protein(BR['ral'], T3, 13.0, 7.0, 'TBK1', 'ral', 'bi')

protein(BR['plc'], T1, 16.0, 8.2, 'PLCε', 'other', 'bi')
protein(BR['plc'], T2, 19.0, 7.4, 'DAG, PKC', 'other', 'tri')

protein(BR['tiam'], T1, 17.0, 8.2, 'TIAM1', 'other', 'bi')
protein(BR['tiam'], T2, 11.0, 7.0, 'RAC', 'other', 'round')

protein(BR['rassf'], T1, 17.0, 8.2, 'RASSF1A', 'rassf', 'bi')
protein(BR['rassf'], T2, 14.0, 7.4, 'MST2', 'rassf', 'bi')

protein(M2X, T1, 13.0, 7.6, 'mTORC2', 'pi3k', 'tri')

for x, a, b, ha, hb in ((BR['mapk'], T1, T2, 4.7, 3.7), (BR['mapk'], T2, T3, 3.7, 3.7),
                        (BR['pi3k'], T1, T2, 4.7, 3.7), (BR['pi3k'], T2, T3, 3.7, 3.7),
                        (BR['ral'], T1, T2, 4.1, 3.5), (BR['plc'], T1, T2, 4.1, 3.7),
                        (BR['tiam'], T1, T2, 4.1, 3.5)):
    arrow((x, a + ha + 0.5), (x, b - hb - 0.4), col=INK)

arrow((M2X - 6.4, T1 + 3.0), (BR['pi3k'] + 8.3, T2 - 3.7),
      (M2X - 8.6, T1 + 5.8), (BR['pi3k'] + 9.2, T2 - 1.2), col=INK)
arrow((BR['ral'], T2 + 3.9), (BR['ral'], T3 - 3.9), col=INK)

D.text(BR['ral'], 105.0, 'survival', anchor='middle', color='#1E3A8A', bold=True)

arrow((BR['rassf'], T1 + 4.4), (BR['rassf'], T2 - 3.9), col=INK)
arrow((BR['rassf'], T2 + 4.0), (BR['rassf'], 96.6), col=INK)
D.text(BR['rassf'], 99.0, 'YAP1/p73 → apoptosis', anchor='middle', color='#475569', bold=True)
arrow((31.0, 77.9), (44.4, 82.6), (34.5, 79.4), (40.5, 81.9), end='tee', col=INK, lw=0.45)

for k, (vx, vy, r) in enumerate(((101.5, 96.2, 2.0), (107.0, 94.8, 1.7), (111.6, 96.4, 1.45))):
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="#EEF2F6" stroke="%s" '
                  'stroke-width="0.5"/>' % (vx, vy, r, COL['ral']))
    for j in range(4):
        a = j * 1.6 + k
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.34" fill="%s"/>'
              % (vx + 0.5 * r * math.cos(a), vy + 0.5 * r * math.sin(a), '#2563EB'))

arrow((BR['ral'] - 5.6, T2 + 1.8), (BR['ral'] - 8.4, 94.4),
      (BR['ral'] - 7.0, 90.2), (BR['ral'] - 8.6, 92.4), col=INK)
D.lines(100.5, 100.0, ['vesicle traffic,', 'secretion'], anchor='middle', color='#1E40AF', bold=True)

AX0, AX1, AY = 138.0, 177.0, 98.6
for k in range(3):
    y = AY - 1.4 + k * 1.4
    pts = [(AX0 + j * 0.55, y + 0.28 * math.sin(j * 1.1 + k)) for j in range(72)]
    D.add('body', '<path d="%s" fill="none" stroke="%s" stroke-width="0.6" '
                  'stroke-dasharray="0.45 0.15" stroke-linecap="round"/>'
          % (pts_path(pts, False), '#9A3412'))
for bx in (143.0, 151.0, 160.0, 169.0):
    D.add('body', '<path d="M%.2f %.2f l2.2 -2.1" stroke="%s" stroke-width="0.55" '
                  'stroke-dasharray="0.45 0.15"/>' % (bx, AY - 1.4, '#9A3412'))
for x in (BR['plc'], BR['tiam']):
    arrow((x, T2 + 4.2), (x, AY - 3.6), col=INK)
D.lines((AX0 + AX1) / 2, 105.0, ['actin remodelling,', 'migration and invasion'],
        anchor='middle', color='#9A3412', bold=True)

NCX, NCY, NRX, NRY = 30.0, 134.0, 36.0, 25.0
D.add('bg', '<g clip-path="url(#clipA)">')
D.add('bg', '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="url(#nuc)" '
            'stroke="#8B5CF6" stroke-width="0.55"/>' % (NCX, NCY, NRX, NRY))
D.add('bg', '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="none" '
            'stroke="#8B5CF6" stroke-width="0.3"/>' % (NCX, NCY, NRX - 1.0, NRY - 1.0))
for ang in (-132, -104, -78, -40):
    t = math.radians(ang)
    px, py = NCX + (NRX - 0.5) * math.cos(t), NCY + (NRY - 0.5) * math.sin(t)
    D.add('bg', '<circle cx="%.2f" cy="%.2f" r="0.75" fill="#FFFFFF" stroke="#8B5CF6" '
                'stroke-width="0.35"/>' % (px, py))
for ph, colr in ((0.0, '#4C1D95'), (math.pi, '#6D28D9')):
    pts = [(4.0 + j * 0.5, 120.3 + 1.3 * math.sin(j * 0.32 + ph)) for j in range(66)]
    D.add('bg', '<path d="%s" fill="none" stroke="%s" stroke-width="0.65"/>'
          % (pts_path(pts, False), colr))
for j in range(2, 66, 4):
    xx = 4.0 + j * 0.5
    D.add('bg', '<path d="M%.2f %.2f L%.2f %.2f" stroke="#A78BFA" stroke-width="0.38"/>'
          % (xx, 120.3 + 1.3 * math.sin(j * 0.32), xx, 120.3 + 1.3 * math.sin(j * 0.32 + math.pi)))
D.add('bg', '</g>')

protein(22.0, 114.4, 8.4, 4.6, 'ERK', 'mapk', 'round', layer='over')
arrow((BR['mapk'], T3 + 3.9), (21.4, 111.8), (BR['mapk'], 106.0), (21.0, 108.4), col=INK)
D.lines(28.5, 114.3, ['ERK-dependent', 'transcription'], color='#4C1D95', bold=True)
D.text(39.0, 120.8, 'Nucleus', color='#4C1D95', bold=True, audit=False)

tag(32.0, 63.6, ['RAF and MEK', 'inhibitors'], 'approved', color=INK, halo=True)
tag(24.0, 104.6, 'ERK inhibitors', 'clinical', color=INK, halo=True)
tag(56.0, 106.4, "PI3K, AKT and mTOR inhibitors", "approved", color=INK, halo=True)

tag(68.0, 110.8, 'RAL, PLCε, TIAM1: no selective agent in clinic', 'preclinical', color=INK)
D.text(70.8, 110.8 + LH, 'Effector use differs by allele and by tissue', color=GREY, bold=True)

RD, DSH = '#BE123C', '1.2 0.8'
FX = 3.2
arrow((BR['mapk'] - 9.2, T3), (FX, T3), end='none', col=RD, dash=DSH, lw=0.6)
arrow((FX, T3), (FX, 30.0), end='none', col=RD, dash=DSH, lw=0.6)
arrow((FX, 30.0), (6.4, 30.0), end='tee', col=RD, dash=DSH, lw=0.6)
arrow((FX, T1), (BR['mapk'] - 10.6, T1), end='tee', col=RD, dash=DSH, lw=0.6)
arrow((FX, 45.2), (20.4, 45.2), end='none', col=RD, dash=DSH, lw=0.6)
arrow((20.4, 45.2), (20.4, 41.4), end='tee', col=RD, dash=DSH, lw=0.6)
D.text(2.0, (T1 + T3) / 2 + 3.0, 'ERK negative feedback', anchor='middle', color=RD,
       bold=True, rot=-90)

D.text(0.6, 2.0, 'a', bold=True, size=PNs, color=INK, audit=False)

# ============================================================ PANEL B ========
BY = 126.0
CW, CG = 43.5, 2.0
CARDS = [
    ('Metabolic reprogramming',
     'More glucose uptake, rewired glutamine use, scavenging of extracellular nutrients',
     'Metabolic co-targeting', 'preclinical'),
    ('Macropinocytosis and autophagy',
     'Protein and amino-acid recycling sustains growth and is a survival route under drug pressure',
     'Autophagy inhibition', 'clinical'),
    ('Immunosuppressive microenvironment',
     'Higher PD-L1, recruitment of myeloid suppressor cells, reduced antigen presentation',
     'Checkpoint blockade; mutant-RAS vaccines and TCR-T cells', 'clinical'),
    ('Senescence and oncogenic stress',
     'A barrier that must be bypassed: carrying a mutation is not the same as depending on it',
     'No therapeutic use; constrains how mutation data are read', 'preclinical'),
]

def wrap(s, width, bold=False):
    out, cur = [], ''
    for wd in s.split(' '):
        t = (cur + ' ' + wd).strip()
        if tw(t, bold) <= width or not cur:
            cur = t
        else:
            out.append(cur)
            cur = wd
    return out + [cur]

def cell(x, y, w, h, col_key, nuc=True, layer='body'):
    col = COL[col_key]
    D.add(layer, '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" '
                 'fill="%s" stroke="%s" stroke-width="0.95"/>'
          % (x, y, w, h, min(w, h) / 2, mix(col, WHITE, 0.85), mix(col, WHITE, 0.20)))
    if nuc:
        D.add(layer, '<ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" fill="url(#nuc)" '
                     'stroke="#8B5CF6" stroke-width="0.38"/>'
              % (x + w * 0.62, y + h * 0.52, min(w, h) * 0.24, min(w, h) * 0.20))

def hexa(x, y, r, col):
    D.add('body', '<path d="%s" fill="#FFFFFF" stroke="%s" stroke-width="0.45"/>'
          % (pts_path([(x + r * math.cos(math.pi / 3 * k + math.pi / 6),
                         y + r * math.sin(math.pi / 3 * k + math.pi / 6))
                        for k in range(6)]), col))

def icon_metabolic(x, y):
    cell(x + 10.0, y + 0.4, 30.0, 14.6, 'on', nuc=False)
    D.add('body', '<rect x="%.2f" y="%.2f" width="9.6" height="4.6" rx="2.3" '
                  'fill="#FED7AA" stroke="#C2410C" stroke-width="0.45"/>'
          % (x + 27.0, y + 6.4))
    D.add('body', '<path d="M%.2f %.2f q0.8 1.6 1.6 0 q0.8 -1.6 1.6 0 q0.8 1.6 1.6 0 '
                  'q0.8 -1.6 1.6 0" fill="none" stroke="#C2410C" stroke-width="0.38"/>'
          % (x + 28.4, y + 8.7))
    for s in (-0.9, 0.9):
        D.add('body', '<rect x="%.2f" y="%.2f" width="1.4" height="3.6" rx="0.7" '
                      'fill="%s" stroke="%s" stroke-width="0.28"/>'
              % (x + 10.2 + s - 0.7, y + 5.6, D.gradient(REC), mix(REC, '#000000', 0.4)))
    for hx, hy in ((3.0, 4.2), (5.4, 9.6), (2.4, 12.0), (15.2, 7.4)):
        hexa(x + hx, y + hy, 1.15, '#C2410C')
    for gx, gy in ((19.0, 11.4), (21.6, 4.4), (23.6, 11.0)):
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.75" fill="#15803D"/>'
              % (x + gx, y + gy))
    arrow((x + 6.8, y + 7.4), (x + 12.8, y + 7.4), hs=1.1, col=INK)

def icon_macro(x, y):
    cell(x + 2.0, y + 2.6, 38.0, 12.4, 'on', nuc=False)
    D.add('body', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f" fill="none" '
                  'stroke="%s" stroke-width="0.95" stroke-linecap="round"/>'
          % (x + 6.0, y + 3.0, x + 4.0, y - 1.6, x + 12.0, y - 1.4, x + 12.6, y + 2.0,
             mix(COL['on'], '#000000', 0.25)))
    for dx, dy in ((8.0, 0.4), (9.6, 1.4), (7.2, 1.8), (10.4, -0.2)):
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.5" fill="#C2410C"/>'
              % (x + dx, y + dy))
    D.add('body', '<circle cx="%.2f" cy="%.2f" r="2.6" fill="#FFF7ED" stroke="%s" '
                  'stroke-width="0.55"/>' % (x + 17.0, y + 8.6, mix(COL['on'], '#000000', 0.35)))
    for dx, dy in ((-0.9, -0.6), (0.8, -0.2), (0.0, 1.0)):
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="0.5" fill="#C2410C"/>'
              % (x + 17.0 + dx, y + 8.6 + dy))
    for r, sw in ((3.2, 0.48), (2.5, 0.38)):
        D.add('body', '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="#64748B" '
                      'stroke-width="%.2f"/>' % (x + 30.0, y + 8.6, r, sw))
    D.add('body', '<rect x="%.2f" y="%.2f" width="2.6" height="1.5" rx="0.6" '
                  'fill="#FED7AA" stroke="#C2410C" stroke-width="0.35"/>'
          % (x + 28.7, y + 7.85))
    arrow((x + 20.4, y + 8.6), (x + 25.8, y + 8.6), hs=1.1, col=INK)

def icon_immune(x, y):
    cell(x + 1.0, y + 1.0, 17.0, 14.0, 'on')
    cell(x + 25.0, y + 2.6, 14.0, 11.0, 'adapt')
    for yy in (5.2, 8.0, 10.8):
        D.add('body', '<path d="M%.2f %.2f h2.1" stroke="#E11D48" stroke-width="0.5"/>'
                      '<circle cx="%.2f" cy="%.2f" r="0.65" fill="#E11D48"/>'
              % (x + 18.0, y + yy, x + 20.5, y + yy))
    arrow((x + 24.8, y + 8.0), (x + 21.8, y + 8.0), end='tee', col=INK, lw=0.50)
    body([(x + 21.6, y + 14.2, 2.4, 1.6, 0), (x + 23.2, y + 13.2, 1.4, 1.2, 0)], '#7C3AED',
         shadow=False)

def icon_senescence(x, y):
    D.add('body', '<path d="M%.2f %.2f C%.2f %.2f %.2f %.2f %.2f %.2f C%.2f %.2f %.2f %.2f '
                  '%.2f %.2f Z" fill="%s" stroke="%s" stroke-width="0.95"/>'
          % (x + 2.0, y + 9.6, x + 4.0, y + 1.6, x + 26.0, y + 0.8, x + 30.0, y + 6.6,
             x + 33.0, y + 13.0, x + 6.0, y + 15.6, x + 2.0, y + 9.6,
             mix(COL['on'], WHITE, 0.85), mix(COL['on'], WHITE, 0.20)))
    D.add('body', '<ellipse cx="%.2f" cy="%.2f" rx="5.2" ry="3.6" fill="url(#nuc)" '
                  'stroke="#8B5CF6" stroke-width="0.38"/>' % (x + 15.0, y + 8.4))
    cx, cy, r = x + 36.6, y + 7.8, 2.6
    D.add('body', '<path d="M%.2f %.2f A%.2f %.2f 0 1 1 %.2f %.2f" fill="none" '
                  'stroke="%s" stroke-width="0.55"/>'
          % (cx + r, cy, r, r, cx + r * math.cos(-1.1), cy + r * math.sin(-1.1), GREY))
    head((cx + r * math.cos(-1.5), cy + r * math.sin(-1.5)),
         (cx + r * math.cos(-1.1), cy + r * math.sin(-1.1)), GREY, 1.1, 'body')
    D.add('body', '<path d="M%.2f %.2f L%.2f %.2f" stroke="%s" stroke-width="0.95" '
                  'stroke-linecap="round"/>' % (cx + 1.4, cy - 3.6, cx + 3.8, cy - 1.0,
                                                '#BE123C'))

ICONS = [icon_metabolic, icon_macro, icon_immune, icon_senescence]
TW = CW - 4.2
WR = [(wrap(t, TW, True), wrap(b, TW), wrap(g, TW - 2.8), st) for t, b, g, st in CARDS]
Y_T = BY + 20.6
Y_B = Y_T + max(len(w[0]) for w in WR) * LH + 0.6
Y_G = Y_B + max(len(w[1]) for w in WR) * LH + 1.2
BH = Y_G + (max(len(w[2]) for w in WR) - 1) * LH + 3.2 - BY
H = BY + BH + 0.4

for k, (tt, bb, gg, st) in enumerate(WR):
    x = k * (CW + CG)
    D.add('bg', '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="2.5" '
                'fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.45" filter="url(#subtle-shadow)"/>'
          % (x, BY, CW, BH))
    ICONS[k](x + 1.6, BY + 2.4)
    D.lines(x + 2.1, Y_T, tt, bold=True, color=INK)
    D.lines(x + 2.1, Y_B, bb, color=INK_MUTED)
    tag(x + 2.1, Y_G, gg, st, color=INK)

D.text(0.6, BY + 2.6, 'b', bold=True, size=PNs, color=INK, audit=False)

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
        
    print("Figure 1 generated successfully in repository:")
    print("  ->", png_file)
    print("  ->", pdf_file)
    print("  ->", svg_file)

if __name__ == '__main__':
    main()
