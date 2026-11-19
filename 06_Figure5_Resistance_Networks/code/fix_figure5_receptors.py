import os
import shutil
import subprocess

# 1. Paths
pristine_jpg = "/Users/wangnianfei/.gemini/antigravity-cli/brain/8b3c3720-a811-42d7-95b3-6436d3b58ea8/figure5_resistance_mechanisms_combinations_final_1794906047438.jpg"

tmp_fixed_png = "/tmp/fig5_fixed_pristine.png"
tmp_500dpi_tif = "/tmp/Fig5_500dpi.tif"
tmp_500dpi_png = "/tmp/Fig5_500dpi.png"
tmp_pdf = "/tmp/Fig5.pdf"

# 2. Run R script to crop title safely and add clean padding
r_code = f"""
library(png)
library(jpeg)

orig <- readJPEG('{pristine_jpg}')
dims <- dim(orig)
# Cut title above row 70 (row 1 to 69)
# Row 70 to 768 preserves all receptors (MET, AXL, EGFR, HER2) with zero truncation!
cropped <- orig[70:dims[1], , ]

# Add 18 rows of pure white padding on top for clean breathing room
pad_top <- array(1.0, dim = c(18, dims[2], 3))
final_img <- abind::abind(pad_top, cropped, along = 1)

writePNG(final_img, '{tmp_fixed_png}')
cat('Successfully exported pristine fixed PNG: ', dim(final_img), '\\n')
"""

with open("/tmp/process_fig5.R", "w") as f:
    f.write(r_code)

subprocess.run(["Rscript", "/tmp/process_fig5.R"], check=True)

# 3. Calculate 500 DPI target dimensions for exact 180 mm width
# Width = 180 mm = 7.0866 inches -> at 500 DPI = 3543 pixels
# Aspect ratio = 717 / 1376 = 0.521075 -> Height = 3543 * 0.521075 = 1846 pixels (93.8 mm)
target_w = 3543
target_h = 1846
target_w_mm = 180.0
target_h_mm = 93.8

# Convert with ImageMagick Lanczos high-quality resampling
# 500 DPI TIFF with LZW compression
cmd_tif = f"magick {tmp_fixed_png} -filter Lanczos -resize {target_w}x{target_h} -density 500 -units PixelsPerInch -compress LZW {tmp_500dpi_tif}"
subprocess.run(cmd_tif, shell=True, check=True)

# 500 DPI PNG
cmd_png = f"magick {tmp_fixed_png} -filter Lanczos -resize {target_w}x{target_h} -density 500 -units PixelsPerInch {tmp_500dpi_png}"
subprocess.run(cmd_png, shell=True, check=True)

# Cairo PDF
r_pdf_code = f"""
library(png)
img <- readPNG('{tmp_500dpi_png}')
cairo_pdf('{tmp_pdf}', width = {target_w_mm / 25.4}, height = {target_h_mm / 25.4})
grid::grid.newpage()
grid::grid.raster(img, width = 1, height = 1)
dev.off()
cat('Successfully generated Cairo PDF\\n')
"""
with open("/tmp/make_pdf.R", "w") as f:
    f.write(r_pdf_code)
subprocess.run(["Rscript", "/tmp/make_pdf.R"], check=True)

# 4. Sync to all target directories
sync_targets = [
    ("/Users/wangnianfei/Desktop/ESMO/03_数据与图表/ESMO_Open_Submission_Figures", "Fig5"),
    ("/Users/wangnianfei/Desktop/ESMO/03_数据与图表/ESMO_Open_Submission_Figures", "Figure5_Acquired_Resistance_Networks_and_Rational_Combinations"),
    ("/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/Submission_Figures_2026", "Fig5"),
    ("/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/Submission_Figures_2026", "Figure5_Acquired_Resistance_Networks_and_Rational_Combinations"),
    ("/Users/wangnianfei/Desktop/nature_review/figures_replot/esmo_open_submission", "Fig5"),
    ("/Users/wangnianfei/Desktop/nature_review/figures_replot", "Fig5"),
    ("/Users/wangnianfei/Desktop/nature_review/figures_replot", "Figure5_Resistance_Mechanisms_Combinations"),
    ("/Users/wangnianfei/Desktop/ESMO/ESMO_Open_Submission_Package/04_Production_Figures_500DPI_TIFF", "Fig5"),
    ("/Users/wangnianfei/Desktop/ESMO/ESMO_Open_Submission_Package/05_Vector_Figures_PDF_EPS", "Fig5"),
]

for tdir, stem in sync_targets:
    os.makedirs(tdir, exist_ok=True)
    if stem == "Fig5" and "04_Production" in tdir:
        shutil.copy2(tmp_500dpi_tif, os.path.join(tdir, f"{stem}.tif"))
        print(f"Copied TIFF to {tdir}/{stem}.tif")
    elif stem == "Fig5" and "05_Vector" in tdir:
        shutil.copy2(tmp_pdf, os.path.join(tdir, f"{stem}.pdf"))
        print(f"Copied PDF to {tdir}/{stem}.pdf")
    else:
        shutil.copy2(tmp_500dpi_tif, os.path.join(tdir, f"{stem}.tif"))
        shutil.copy2(tmp_500dpi_png, os.path.join(tdir, f"{stem}.png"))
        shutil.copy2(tmp_pdf, os.path.join(tdir, f"{stem}.pdf"))
        print(f"Copied TIF/PNG/PDF to {tdir}/{stem}.*")

print("\nAll Fig 5 production files successfully regenerated and synchronized!")
