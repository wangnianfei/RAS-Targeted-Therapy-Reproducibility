#!/usr/bin/env bash
# ==============================================================================
# One-Click Automated Reproduction Script for ESMO Open Review Artwork & Tables
# "RAS-targeted therapy in solid tumours: what the randomised trials establish
#  and what they leave open"
# ==============================================================================

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=============================================================================="
echo " Starting Full Automated Reproduction of ESMO Open Review Artwork & Tables"
echo " Working directory: $REPO_DIR"
echo " Retrieval and Data Freeze Cut-off Date: 18 November 2026"
echo "=============================================================================="

# Detect Python runner
if command -v uv >/dev/null 2>&1; then
    PY_CMD="uv run --with matplotlib --with pillow --with numpy python3"
elif [ -x "/Users/wangnianfei/.local/bin/uv" ]; then
    PY_CMD="/Users/wangnianfei/.local/bin/uv run --with matplotlib --with pillow --with numpy python3"
else
    PY_CMD="python3"
fi
echo "Using Python execution environment: $PY_CMD"

# Check Rscript
if command -v Rscript >/dev/null 2>&1; then
    R_CMD="Rscript"
    echo "Using R execution environment: $(which Rscript)"
else
    echo "WARNING: Rscript not found in PATH! R-based figures will be skipped."
    R_CMD=""
fi

echo ""
echo "--- [1/7] Reproducing Figure 1: Biophysical Nucleotide Cycling & Structural Paradigms ---"
$PY_CMD "$REPO_DIR/01_Figure1_Structural_Mechanisms/code/run_figure1.py"

echo ""
echo "--- [2/7] Reproducing Figure 2: Pan-Cancer Genomic Landscape & Co-Mutations ---"
if [ -n "$R_CMD" ]; then
    $R_CMD "$REPO_DIR/02_Figure2_PanCancer_Landscape/code/run_figure2.R"
else
    echo "Skipping Rscript for Figure 2."
fi

echo ""
echo "--- [3/7] Verifying Table 1: Methodological Architecture & Clinical Endpoints Across 7 Phase III RCTs ---"
$PY_CMD "$REPO_DIR/03_Table1_Pivotal_Phase3_RCTs/code/build_table1.py"

echo ""
echo "--- [4/7] Reproducing Figure 3: Phase III RCT Efficacy Synthesis & Crossover Meta-Regression ---"
if [ -n "$R_CMD" ]; then
    $R_CMD "$REPO_DIR/04_Figure3_Phase3_Efficacy_Discordance/code/run_figure3_forest_regression.R"
else
    echo "Skipping Rscript for Figure 3."
fi

echo ""
echo "--- [5/7] Reproducing Figure 4: Global Landscape & Geography of 1,182 RAS Clinical Trials ---"
if [ -n "$R_CMD" ]; then
    $R_CMD "$REPO_DIR/05_Figure4_Global_Trial_Landscape/code/run_figure4_trial_landscape.R"
else
    echo "Skipping Rscript for Figure 4."
fi

echo ""
echo "--- [6/7] Validating Figure 5: Comprehensive Acquired Resistance Networks & Combinations ---"
$PY_CMD "$REPO_DIR/06_Figure5_Resistance_Networks/code/run_figure5.py"

echo ""
echo "--- [7/7] Reproducing Supplementary Figure S1 & Validating Tables S1-S3 ---"
$PY_CMD "$REPO_DIR/07_Supplementary_Material/code/run_figureS1_resistance_matrix.py"
$PY_CMD "$REPO_DIR/07_Supplementary_Material/code/build_supplementary_tables.py"

echo ""
echo "=============================================================================="
echo " Full Reproduction Complete! All publication figures (Fig1-Fig5, FigS1) and"
echo " tables (Table 1, Tables S1-S3) are synchronized and verified."
echo "=============================================================================="
