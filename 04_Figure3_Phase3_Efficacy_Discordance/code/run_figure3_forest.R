#!/usr/bin/env Rscript
# ==============================================================================
# Figure 3: PFS and OS hazard ratios across seven phase III RCTs (descriptive forest plots)
# Production Script for ESMO Open
# 180.0 mm double-column width, 100.0 mm height, Arial
# Panel tags (A, B). The former crossover-vs-OS regression panel (C) was removed in revision:
# n = 6 heterogeneous trials, an active-comparator trial, and unsourced crossover values.
# ==============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(scales)
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

trials_df <- read.csv(file.path(data_dir, "phase3_rct_outcomes.csv"), stringsAsFactors = FALSE)
trials_df$row_id <- rev(seq_len(nrow(trials_df)))
trials_df$os_status <- ifelse(!is.na(trials_df$os_high) & trials_df$os_high < 1.0, "Significant OS Benefit", "No Significant OS Benefit")
trials_df$os_note[is.na(trials_df$os_note)] <- ""

make_info_panel <- function(tag_label = "A") {
  ggplot(trials_df, aes(y = row_id)) +
    geom_text(aes(x = 0, label = trial_id), hjust = 0, size = 2.2, fontface = "bold", family = "Arial", color = "#111111") +
    geom_text(aes(x = 2.9, label = setting), hjust = 0, size = 1.95, family = "Arial", color = "#333333") +
    geom_text(aes(x = 8.6, label = paste0("n=", n_pts)), hjust = 0, size = 1.95, family = "Arial", color = "#555555") +
    annotate("text", x = 0, y = 8.1, label = "Trial", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
    annotate("text", x = 2.9, y = 8.1, label = "Setting (comparator)", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
    annotate("text", x = 8.6, y = 8.1, label = "n", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
    geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
    scale_x_continuous(limits = c(0, 9.6), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
    labs(tag = tag_label) +
    theme_void(base_family = "Arial") +
    theme(
      plot.tag = element_text(face = "bold", size = 8.5, family = "Arial", color = "#111111"),
      plot.tag.position = c(0.0, 1.0),
      plot.margin = margin(t = 9, r = 2, b = 2, l = 8)
    )
}

p_pfs_forest <- ggplot(trials_df, aes(y = row_id, x = pfs_hr)) +
  geom_vline(xintercept = 1.0, linetype = "dashed", color = "#888888", linewidth = 0.35) +
  geom_errorbar(aes(xmin = pfs_low, xmax = pfs_high), orientation = "y", width = 0.25, color = "#1B4F72", linewidth = 0.5) +
  geom_point(aes(size = sqrt(n_pts)), shape = 22, fill = "#2980B9", color = "#1B4F72", stroke = 0.4) +
  scale_size_continuous(range = c(2.0, 4.0), guide = "none") +
  scale_x_continuous(
    trans = "log10",
    breaks = c(0.3, 0.5, 0.7, 1.0, 1.5),
    limits = c(0.25, 1.6),
    labels = c("0.3", "0.5", "0.7", "1.0", "1.5")
  ) +
  scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
  labs(x = "PFS Hazard Ratio (95% CI)", y = "") +
  theme_classic(base_size = 7.0, base_family = "Arial") %+replace%
  theme(
    axis.line.x = element_line(colour = "#333333", linewidth = 0.35),
    axis.ticks.x = element_line(colour = "#333333", linewidth = 0.35),
    axis.line.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.text.y = element_blank(),
    axis.text.x = element_text(colour = "#222222", size = 6.2),
    axis.title.x = element_text(colour = "#111111", face = "bold", size = 6.8, margin = margin(t = 2, b = 1)),
    plot.margin = margin(t = 9, r = 2, b = 2, l = 2)
  ) +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  annotate("text", x = 0.62, y = 0.5, label = "◄ Favours Targeted", size = 1.85, color = "#2980B9", fontface = "bold", family = "Arial") +
  annotate("text", x = 1.33, y = 0.5, label = "Favours Control ►", size = 1.85, color = "#777777", family = "Arial")

pfs_stat_labels <- sprintf("%.2f (%.2f-%.2f)", trials_df$pfs_hr, trials_df$pfs_low, trials_df$pfs_high)
p_pfs_stats <- ggplot(trials_df, aes(y = row_id)) +
  geom_text(aes(x = 0, label = pfs_stat_labels), hjust = 0, size = 2.1, color = "#111111", family = "Arial") +
  annotate("text", x = 0, y = 8.1, label = "HR (95% CI)", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  scale_x_continuous(limits = c(0, 5.8), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(t = 9, r = 4, b = 2, l = 2))

panel_a <- (make_info_panel("A") | p_pfs_forest | p_pfs_stats) + plot_layout(widths = c(1.9, 1.4, 0.9))

os_colors <- c("Significant OS Benefit" = "#C0392B", "No Significant OS Benefit" = "#7F8C8D")
p_os_forest <- ggplot(trials_df, aes(y = row_id, x = os_hr)) +
  geom_vline(xintercept = 1.0, linetype = "dashed", color = "#888888", linewidth = 0.35) +
  geom_errorbar(aes(xmin = os_low, xmax = os_high, color = os_status), orientation = "y", width = 0.25, linewidth = 0.5) +
  geom_point(aes(size = sqrt(n_pts), fill = os_status, color = os_status), shape = 22, stroke = 0.4) +
  scale_color_manual(values = os_colors, guide = "none") +
  scale_fill_manual(values = os_colors, guide = "none") +
  scale_size_continuous(range = c(2.0, 4.0), guide = "none") +
  scale_x_continuous(
    trans = "log10",
    breaks = c(0.3, 0.5, 0.7, 1.0, 1.5),
    limits = c(0.25, 1.6),
    labels = c("0.3", "0.5", "0.7", "1.0", "1.5")
  ) +
  scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
  labs(x = "OS Hazard Ratio (95% CI)", y = "") +
  theme_classic(base_size = 7.0, base_family = "Arial") %+replace%
  theme(
    axis.line.x = element_line(colour = "#333333", linewidth = 0.35),
    axis.ticks.x = element_line(colour = "#333333", linewidth = 0.35),
    axis.line.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.text.y = element_blank(),
    axis.text.x = element_text(colour = "#222222", size = 6.2),
    axis.title.x = element_text(colour = "#111111", face = "bold", size = 6.8, margin = margin(t = 2, b = 1)),
    plot.margin = margin(t = 9, r = 2, b = 2, l = 2)
  ) +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  annotate("text", x = 0.62, y = 0.5, label = "◄ Favours Targeted", size = 1.85, color = "#C0392B", fontface = "bold", family = "Arial") +
  annotate("text", x = 1.33, y = 0.5, label = "Favours Control ►", size = 1.85, color = "#777777", family = "Arial")

os_stat_labels <- ifelse(is.na(trials_df$os_hr), trials_df$os_note, sprintf("%.2f (%.2f-%.2f)", trials_df$os_hr, trials_df$os_low, trials_df$os_high))
p_os_stats <- ggplot(trials_df, aes(y = row_id)) +
  geom_text(aes(x = 0, label = os_stat_labels), hjust = 0, size = 2.1, color = "#111111", family = "Arial") +
  scale_color_manual(values = os_colors, guide = "none") +
  annotate("text", x = 0, y = 8.1, label = "HR (95% CI)", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  scale_x_continuous(limits = c(0, 5.8), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(t = 9, r = 4, b = 2, l = 2))

panel_b <- (make_info_panel("B") | p_os_forest | p_os_stats) + plot_layout(widths = c(1.9, 1.4, 0.9))

fig3_combined <- (panel_a / panel_b) + plot_layout(heights = c(1, 1))

out_pdf <- file.path(fig_dir, "Figure3_Phase3_RCT_PFS_OS_Forest.pdf")
out_png <- file.path(fig_dir, "Figure3_Phase3_RCT_PFS_OS_Forest.png")
out_eps <- file.path(fig_dir, "Figure3_Phase3_RCT_PFS_OS_Forest.eps")

cairo_pdf(out_pdf, width = 180 / 25.4, height = 100 / 25.4, family = "Arial")
print(fig3_combined)
dev.off()

cairo_ps(out_eps, width = 180 / 25.4, height = 100 / 25.4, family = "Arial")
print(fig3_combined)
dev.off()

ragg::agg_png(out_png, width = 180, height = 100, units = "mm", res = 500)
print(fig3_combined)
dev.off()

cat("Successfully generated Figure 3 in:", fig_dir, "\n")
