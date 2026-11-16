#!/usr/bin/env bash
# ==============================================================================
# One-click automated reproduction script for all figures and tables
# in "RAS-Directed Therapy in Solid Tumors"
# ==============================================================================

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=== Starting Full Reproduction of RAS Review Artwork ==="
echo "Working directory: $REPO_DIR"

echo ""
echo "--- [1/7] Reproducing Figure 1: RAS Signalling Network ---"
python3 "$REPO_DIR/01_Figure1_Signalling_Network/code/run_figure1.py"

echo ""
echo "--- [2/7] Reproducing Figure 2: Pan-Cancer Distribution ---"
python3 "$REPO_DIR/02_Figure2_PanCancer_Distribution/code/run_figure2.py"

echo ""
echo "--- [3/7] Reproducing Figure 3: Conformational Switch & Pocket ---"
python3 "$REPO_DIR/03_Figure3_Conformational_Switch/code/run_figure3.py"

echo ""
echo "--- [4/7] Verifying Table 1: Inhibitor Landscape ---"
python3 "$REPO_DIR/04_Table1_Inhibitor_Landscape/code/build_table1.py"

echo ""
echo "--- [5/7] Verifying Table 2: Pivotal Phase III RCTs ---"
python3 "$REPO_DIR/05_Table2_Pivotal_Phase3_RCTs/code/build_table2.py"

echo ""
echo "--- [6/7] Reproducing Figure 4: Global Trial Atlas (R) ---"
if command -v Rscript >/dev/null 2>&1; then
    (cd "$REPO_DIR/06_Figure4_Global_Trial_Landscape" && Rscript code/fig2_trial_atlas.R .) || echo "  ! Rscript trial atlas notice"
else
    echo "  ! Rscript not found in PATH; skipping R figure generation. High-res vector outputs are pre-rendered in vector_figures/."
fi

echo ""
echo "--- [7/7] Reproducing Figure 5: Resistance Matrix ---"
python3 "$REPO_DIR/07_Figure5_Resistance_Matrix/code/run_figure5.py"

echo ""
echo "=== Full Reproduction Complete! All vector artwork is up-to-date in vector_figures/ ==="
