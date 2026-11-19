#!/usr/bin/env Rscript
# Check and install required R packages for RAS Review reproducibility
packages <- c("ggplot2", "dplyr", "tidyr", "stringr", "scales", "grid", "cowplot", "png", "readr", "maps", "ggrepel", "patchwork", "ggtext")
new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) {
  message("Installing missing R packages: ", paste(new_packages, collapse = ", "))
  install.packages(new_packages, repos = "https://cloud.r-project.org")
} else {
  message("All required core R packages are already installed!")
}
