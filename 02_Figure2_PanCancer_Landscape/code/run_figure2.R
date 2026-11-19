#!/usr/bin/env Rscript
# ==============================================================================
# Figure 2: Pan-Cancer RAS Alteration Landscape and Co-Mutation Phenotypes
# Production Script for ESMO Open
# Strictly 180.0 mm double-column width, 125.0 mm height, TrueType Arial font
# Panel tags (A, B, C) matching manuscript citations
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
allele_df$cancer_type <- factor(allele_df$cancer_type, levels = rev(c("PDAC", "CRC", "LUAD")))
allele_df$allele <- factor(allele_df$allele, levels = rev(c("G12C", "G12D", "G12V", "G12R / G13D", "Other")))

comut_df <- read.csv(file.path(data_dir, "comutation_subgroups_nsclc.csv"), stringsAsFactors = FALSE)
comut_df$subgroup_label <- factor(comut_df$subgroup, levels = rev(comut_df$subgroup))
comut_df$y_pos <- 4:1

p_isoform <- ggplot(isoform_long, aes(y = cancer_type, x = Freq, fill = Gene)) +
  geom_bar(stat = "identity", width = 0.65, color = "#FFFFFF", linewidth = 0.25) +
  scale_fill_manual(values = c("KRAS" = "#2C3E50", "NRAS" = "#16A085", "HRAS" = "#E67E22")) +
  scale_x_continuous(limits = c(0, 100), breaks = seq(0, 100, by = 25), labels = paste0(seq(0, 100, by = 25), "%")) +
  labs(tag = "A", x = "Mutation Prevalence (%)", y = "") +
  theme_esmo_tight() +
  theme(legend.position = "top", legend.justification = "right", legend.margin = margin(b = -6, t = 0))

p_allele <- ggplot(allele_df, aes(y = cancer_type, x = pct, fill = allele)) +
  geom_bar(stat = "identity", position = "fill", width = 0.60, color = "#FFFFFF", linewidth = 0.25) +
  scale_fill_manual(values = c("G12C" = "#C0392B", "G12D" = "#2980B9", "G12V" = "#27AE60", "G12R / G13D" = "#8E44AD", "Other" = "#BDC3C7")) +
  scale_x_continuous(labels = scales::percent_format(), breaks = seq(0, 1, by = 0.25)) +
  labs(tag = "B", x = "Proportion of <i>KRAS</i> Mutations", y = "") +
  theme_esmo_tight() +
  theme(
    axis.title.x = element_markdown(colour = "#111111", face = "bold", size = 6.8),
    legend.position = "top",
    legend.justification = "right",
    legend.margin = margin(b = -6, t = 0)
  )

p_comut_bar <- ggplot(comut_df, aes(y = subgroup_label, x = freq_pct)) +
  geom_segment(aes(y = subgroup_label, yend = subgroup_label, x = 0, xend = freq_pct), color = "#BDC3C7", linewidth = 0.8) +
  geom_point(aes(color = subgroup_label), size = 6.2) +
  geom_text(aes(label = paste0(freq_pct, "%")), color = "#FFFFFF", size = 2.3, fontface = "bold", family = "Arial", vjust = 0.5) +
  scale_color_manual(values = c("KP" = "#2980B9", "KL" = "#E67E22", "KEAP1" = "#C0392B", "KC" = "#8E44AD"), guide = "none") +
  scale_y_discrete(labels = c(
    "KP" = "KP (<i>TP53</i>)",
    "KL" = "KL (<i>STK11</i>)",
    "KEAP1" = "<i>KEAP1</i>",
    "KC" = "KC (<i>CDKN2A</i>)"
  )) +
  scale_x_continuous(limits = c(0, 52), breaks = seq(0, 40, by = 10), labels = paste0(seq(0, 40, by = 10), "%")) +
  labs(tag = "C", x = "Prevalence in <i>KRAS</i>-Mutant NSCLC (%)", y = "") +
  theme_esmo_tight() +
  theme(
    axis.text.y = element_markdown(colour = "#222222", size = 6.4, face = "bold"),
    axis.title.x = element_markdown(colour = "#111111", face = "bold", size = 6.8)
  )

p_comut_cards <- ggplot(comut_df, aes(y = y_pos)) +
  geom_rect(aes(ymin = y_pos - 0.42, ymax = y_pos + 0.42, xmin = 0, xmax = 10),
            fill = c("#EBF5FB", "#FEF9E7", "#FDEDEC", "#F4ECF7"),
            color = "#D5D8DC", linewidth = 0.3) +
  geom_text(aes(x = 0.15, y = y_pos + 0.16, label = paste0(subgroup, " (", gene, ")")), hjust = 0, size = 2.2, fontface = "bold", color = "#111111", family = "Arial") +
  geom_text(aes(x = 0.15, y = y_pos + 0.01, label = paste0("• Biology: ", tme_biology)), hjust = 0, size = 1.9, color = "#2C3E50", family = "Arial") +
  geom_text(aes(x = 0.15, y = y_pos - 0.22, label = paste0("• Therapy: ", clinical_implications)), hjust = 0, size = 1.9, color = "#78281F", family = "Arial") +
  scale_y_continuous(limits = c(0.4, 4.6)) +
  scale_x_continuous(limits = c(0, 10)) +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(t = 2, r = 4, b = 2, l = 0))

p_bottom <- (p_comut_bar | p_comut_cards) + plot_layout(widths = c(1, 1.45))
p_top <- (p_isoform | p_allele) + plot_layout(widths = c(1, 1.05))
fig2_combined <- (p_top / p_bottom) + plot_layout(heights = c(1, 1.15))

out_pdf <- file.path(fig_dir, "Figure2_PanCancer_RAS_Landscape_and_CoMutations.pdf")
out_png <- file.path(fig_dir, "Figure2_PanCancer_RAS_Landscape_and_CoMutations.png")
out_eps <- file.path(fig_dir, "Figure2_PanCancer_RAS_Landscape_and_CoMutations.eps")

cairo_pdf(out_pdf, width = 180 / 25.4, height = 125 / 25.4, family = "Arial")
print(fig2_combined)
dev.off()

cairo_ps(out_eps, width = 180 / 25.4, height = 125 / 25.4, family = "Arial")
print(fig2_combined)
dev.off()

ragg::agg_png(out_png, width = 180, height = 125, units = "mm", res = 500)
print(fig2_combined)
dev.off()

cat("Successfully generated Figure 2 in:", fig_dir, "\n")
