#!/usr/bin/env Rscript
# ==============================================================================
# Figure 2: RAS mutation prevalence and KRAS allele spectrum (MSK-IMPACT 2017, derived by derive_figure2_data.py)
# Production Script for ESMO Open
# 180.0 mm width, 80.0 mm height, Arial. Panels A, B. Former panel C (co-mutation subgroups,
# unsourced values and treatment advice) removed in revision.
# ==============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(tidyr)
  library(scales)
  library(ggtext)
})

initial_options <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("--file=", initial_options, value = TRUE)
if (length(file_arg) > 0) {
  script_dir <- dirname(normalizePath(sub("--file=", "", file_arg)))
} else {
  script_dir <- getwd()
}
data_dir <- file.path(dirname(script_dir), "data")
fig_dir <- file.path(dirname(script_dir), "figures")
dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)

theme_esmo_tight <- function(base_size = 7.0) {
  theme_classic(base_size = base_size, base_family = "Arial") %+replace%
    theme(
      axis.line = element_line(colour = "#333333", linewidth = 0.35),
      axis.ticks = element_line(colour = "#333333", linewidth = 0.35),
      axis.text = element_text(colour = "#222222", size = 6.4),
      axis.title = element_text(colour = "#111111", face = "bold", size = 6.8),
      plot.tag = element_text(colour = "#111111", face = "bold", size = 8.5, family = "Arial"),
      plot.tag.position = c(0.01, 0.98),
      plot.title = element_blank(),
      plot.subtitle = element_blank(),
      legend.text = element_text(size = 6.2, colour = "#222222"),
      legend.title = element_blank(),
      plot.margin = margin(t = 2, r = 4, b = 2, l = 4)
    )
}

isoform_df <- read.csv(file.path(data_dir, "pancancer_isoform_frequencies.csv"), stringsAsFactors = FALSE)
isoform_long <- tidyr::pivot_longer(isoform_df, cols = c("KRAS", "NRAS", "HRAS"), names_to = "Gene", values_to = "Freq")
isoform_long$cancer_type <- factor(isoform_long$cancer_type, levels = rev(isoform_df$cancer_type))
isoform_long$Gene <- factor(isoform_long$Gene, levels = c("HRAS", "NRAS", "KRAS"))

allele_df <- read.csv(file.path(data_dir, "kras_allele_frequencies.csv"), stringsAsFactors = FALSE)
allele_df$cancer_type <- factor(allele_df$cancer_type, levels = rev(c("PDAC", "CRC", "NSCLC")))
allele_df$allele <- factor(allele_df$allele, levels = rev(c("G12C", "G12D", "G12V", "G12R", "G13D", "Q61X", "Other")))

p_isoform <- ggplot(isoform_long, aes(y = cancer_type, x = Freq, fill = Gene)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.78), width = 0.75, color = "#FFFFFF", linewidth = 0.2) +
  geom_text(aes(label = ifelse(Freq >= 1, sprintf("%.1f", Freq), "")), position = position_dodge(width = 0.78), hjust = -0.15, size = 1.7, family = "Arial", color = "#222222") +
  scale_fill_manual(values = c("KRAS" = "#2C3E50", "NRAS" = "#16A085", "HRAS" = "#E67E22"), breaks = c("KRAS", "NRAS", "HRAS")) +
  guides(fill = guide_legend(keywidth = unit(3, "mm"), keyheight = unit(2.5, "mm"))) +
  scale_x_continuous(limits = c(0, 100), breaks = seq(0, 100, by = 25), labels = paste0(seq(0, 100, by = 25), "%")) +
  labs(tag = "a", x = "Samples with missense mutation (%)", y = "") +
  theme_esmo_tight() +
  theme(legend.position = "bottom", legend.justification = "center", legend.margin = margin(t = -4, b = 0))

p_allele <- ggplot(allele_df, aes(y = cancer_type, x = pct, fill = allele)) +
  geom_bar(stat = "identity", position = "fill", width = 0.60, color = "#FFFFFF", linewidth = 0.25) +
  scale_fill_manual(values = c("G12C" = "#C0392B", "G12D" = "#2980B9", "G12V" = "#27AE60", "G12R" = "#8E44AD", "G13D" = "#E84393", "Q61X" = "#F1C40F", "Other" = "#BDC3C7"), breaks = c("G12C", "G12D", "G12V", "G12R", "G13D", "Q61X", "Other")) +
  guides(fill = guide_legend(nrow = 1, keywidth = unit(3, "mm"), keyheight = unit(2.5, "mm"))) +
  scale_x_continuous(labels = scales::percent_format(), breaks = seq(0, 1, by = 0.25)) +
  labs(tag = "b", x = "Share of <i>KRAS</i> missense mutations", y = "") +
  theme_esmo_tight() +
  theme(
    axis.title.x = element_markdown(colour = "#111111", face = "bold", size = 6.8),
    legend.position = "bottom",
    legend.justification = "center",
    legend.margin = margin(t = -4, b = 0)
  )

fig2_combined <- (p_isoform | p_allele) + plot_layout(widths = c(1, 1.15))

out_pdf <- file.path(fig_dir, "Figure2_RAS_Prevalence_and_KRAS_Alleles.pdf")
out_png <- file.path(fig_dir, "Figure2_RAS_Prevalence_and_KRAS_Alleles.png")
out_eps <- file.path(fig_dir, "Figure2_RAS_Prevalence_and_KRAS_Alleles.eps")

cairo_pdf(out_pdf, width = 180 / 25.4, height = 88 / 25.4, family = "Arial")
print(fig2_combined)
dev.off()

cairo_ps(out_eps, width = 180 / 25.4, height = 88 / 25.4, family = "Arial")
print(fig2_combined)
dev.off()

ragg::agg_png(out_png, width = 180, height = 88, units = "mm", res = 500)
print(fig2_combined)
dev.off()

cat("Successfully generated Figure 2 in:", fig_dir, "\n")
