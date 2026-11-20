#!/usr/bin/env Rscript
# Install the R packages used by the figure scripts (Figures 2-4).
packages <- c("ggplot2", "patchwork", "dplyr", "tidyr", "scales", "ggtext", "ragg", "maps")
missing <- packages[!(packages %in% installed.packages()[, "Package"])]
if (length(missing)) {
  message("Installing: ", paste(missing, collapse = ", "))
  install.packages(missing, repos = "https://cloud.r-project.org")
} else {
  message("All required R packages are installed.")
}
