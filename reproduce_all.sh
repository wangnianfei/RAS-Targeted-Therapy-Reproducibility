#!/usr/bin/env bash
# ==============================================================================
# Reproduce all figures and tables of
# "Targeting RAS in solid tumours: from molecular switch dynamics and resistance
#  networks to randomised clinical trial landscapes" (submitted to ESMO Open)
#
# Requirements: Python >= 3.10 with matplotlib; R >= 4.3 with ggplot2, patchwork,
# dplyr, tidyr, scales, ggtext, ragg, maps; PyMOL (open-source, `pymol` on PATH);
# ImageMagick 7 (`magick` on PATH). Data cut-off: 18 November 2026.
# ==============================================================================
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"
cd "$REPO_DIR"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required tool: $1" >&2; exit 1; }; }
need "$PY"; need Rscript; need pymol; need magick

# R figures: copy the long-named outputs to the short submission names (FigN.*) and
# write 500-dpi LZW TIFFs from the 500-dpi PNG (the Python figures do this themselves).
r_exports() {  # folder, long base name, short base name
  local f="$1/figures"
  for e in pdf eps png; do cp "$f/$2.$e" "$f/$3.$e"; done
  magick "$f/$3.png" -background white -alpha remove -alpha off -units PixelsPerInch -density 500 -compress LZW "$f/$3.tif"
  cp "$f/$3.tif" "$f/$2.tif"
}

echo "[1/7] Figure 1: PyMOL renders of PDB 6OIM and 9BG6, then panel composition"
(cd 01_Figure1_Structural_Mechanisms && pymol -cq code/render_figure1_pymol.py)
"$PY" 01_Figure1_Structural_Mechanisms/code/run_figure1.py

echo "[2/7] Figure 2: derive prevalence and allele tables from the MSK-IMPACT cBioPortal export"
"$PY" 02_Figure2_PanCancer_Landscape/code/derive_figure2_data.py
Rscript 02_Figure2_PanCancer_Landscape/code/run_figure2.R
r_exports 02_Figure2_PanCancer_Landscape Figure2_RAS_Prevalence_and_KRAS_Alleles Fig2

echo "[3/7] Table 1: export the seven phase III trials to Markdown"
"$PY" 03_Table1_Pivotal_Phase3_RCTs/code/build_table1.py >/dev/null

echo "[4/7] Figure 3: PFS and OS forest plots"
Rscript 04_Figure3_Phase3_Efficacy_Discordance/code/run_figure3_forest.R
r_exports 04_Figure3_Phase3_Efficacy_Discordance Figure3_Phase3_RCT_PFS_OS_Forest Fig3

echo "[5/7] Supplementary Figure S2: registered trials of directly RAS-targeted agents"
"$PY" 05_FigureS2_Global_Trial_Landscape/code/apply_classification_corrections.py
"$PY" 05_FigureS2_Global_Trial_Landscape/code/summarise_trials.py >/dev/null
Rscript 05_FigureS2_Global_Trial_Landscape/code/run_figureS2_trial_landscape.R
r_exports 05_FigureS2_Global_Trial_Landscape FigureS2_Global_Clinical_Trial_Atlas_and_Geography FigS2

echo "[6/7] Supplementary Figure S1"
"$PY" 07_Supplementary_Material/code/run_figureS1_resistance_matrix.py

echo "[7/7] Supplementary Tables S1 and S3 (print from data files)"
"$PY" 07_Supplementary_Material/code/build_supplementary_tables.py >/dev/null

echo "Done. Outputs are in each folder's figures/ (and 03_Table1_Pivotal_Phase3_RCTs/data/)."
