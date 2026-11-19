#!/usr/bin/env Rscript
# ==============================================================================
# Figure 3: Phase III RCT Efficacy Discordance and Crossover Confounding
# Production Script for ESMO Open
# Strictly 180.0 mm double-column width, 145.0 mm height, TrueType Arial font
# Panel tags (A, B, C) matching manuscript citations
# ==============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(scales)
  library(ggrepel)
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

trials_df <- read.csv(file.path(data_dir, "phase3_rct_outcomes_crossover.csv"), stringsAsFactors = FALSE)
trials_df$row_id <- rev(seq_len(nrow(trials_df)))
trials_df$os_status <- ifelse(trials_df$os_high < 1.0, "Significant OS Benefit", "No Significant OS Benefit")

make_info_panel <- function(tag_label = "A") {
  ggplot(trials_df, aes(y = row_id)) +
    geom_text(aes(x = 0, label = trial_id), hjust = 0, size = 2.2, fontface = "bold", family = "Arial", color = "#111111") +
    geom_text(aes(x = 3.2, label = disease), hjust = 0, size = 2.05, family = "Arial", color = "#333333") +
    geom_text(aes(x = 5.8, label = paste0("n=", n_pts)), hjust = 0, size = 1.95, family = "Arial", color = "#555555") +
    annotate("text", x = 0, y = 8.1, label = "Trial", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
    annotate("text", x = 3.2, y = 8.1, label = "Setting", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
    annotate("text", x = 5.8, y = 8.1, label = "Pts", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
    geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
    scale_x_continuous(limits = c(0, 7.2), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
    labs(tag = tag_label) +
    theme_void(base_family = "Arial") +
    theme(
      plot.tag = element_text(face = "bold", size = 8.5, family = "Arial", color = "#111111"),
      plot.tag.position = c(0.01, 0.98),
      plot.margin = margin(t = 2, r = 2, b = 2, l = 4)
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
    plot.margin = margin(t = 2, r = 2, b = 2, l = 2)
  ) +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  annotate("text", x = 0.45, y = 0.5, label = "◄ Favours Targeted", size = 1.85, color = "#2980B9", fontface = "bold", family = "Arial") +
  annotate("text", x = 1.15, y = 0.5, label = "Favours Control ►", size = 1.85, color = "#777777", family = "Arial")

pfs_stat_labels <- sprintf("%.2f (%.2f-%.2f)", trials_df$pfs_hr, trials_df$pfs_low, trials_df$pfs_high)
p_pfs_stats <- ggplot(trials_df, aes(y = row_id)) +
  geom_text(aes(x = 0, label = pfs_stat_labels), hjust = 0, size = 2.1, color = "#111111", family = "Arial") +
  geom_text(aes(x = 3.6, label = pfs_pval), hjust = 0, size = 2.0, color = "#0E6251", fontface = "italic", family = "Arial") +
  annotate("text", x = 0, y = 8.1, label = "HR (95% CI)", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
  annotate("text", x = 3.6, y = 8.1, label = "P-value", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  scale_x_continuous(limits = c(0, 5.8), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(t = 2, r = 4, b = 2, l = 2))

panel_a <- (make_info_panel("A") | p_pfs_forest | p_pfs_stats) + plot_layout(widths = c(1.3, 1.4, 1.1))

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
    plot.margin = margin(t = 2, r = 2, b = 2, l = 2)
  ) +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  annotate("text", x = 0.45, y = 0.5, label = "◄ Favours Targeted", size = 1.85, color = "#C0392B", fontface = "bold", family = "Arial") +
  annotate("text", x = 1.15, y = 0.5, label = "Favours Control ►", size = 1.85, color = "#777777", family = "Arial")

os_stat_labels <- sprintf("%.2f (%.2f-%.2f)", trials_df$os_hr, trials_df$os_low, trials_df$os_high)
p_os_stats <- ggplot(trials_df, aes(y = row_id)) +
  geom_text(aes(x = 0, label = os_stat_labels), hjust = 0, size = 2.1, color = "#111111", family = "Arial") +
  geom_text(aes(x = 3.6, label = os_pval, color = os_status), hjust = 0, size = 2.0, fontface = "italic", family = "Arial") +
  scale_color_manual(values = os_colors, guide = "none") +
  annotate("text", x = 0, y = 8.1, label = "HR (95% CI)", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
  annotate("text", x = 3.6, y = 8.1, label = "P-value", hjust = 0, size = 2.3, fontface = "bold", family = "Arial", color = "#111111") +
  geom_hline(yintercept = 7.45, linewidth = 0.35, color = "#333333") +
  scale_x_continuous(limits = c(0, 5.8), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0.2, 8.6), expand = c(0, 0)) +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(t = 2, r = 4, b = 2, l = 2))

panel_b <- (make_info_panel("B") | p_os_forest | p_os_stats) + plot_layout(widths = c(1.3, 1.4, 1.1))

# Panel C: Crossover vs OS Correlation
ras_direct <- filter(trials_df, trial_id != "NEMO (MEKi)")

p_corr <- ggplot(ras_direct, aes(x = crossover_pct, y = os_hr)) +
  geom_hline(yintercept = 1.0, linetype = "dashed", color = "#95A5A6", linewidth = 0.35) +
  geom_smooth(method = "lm", formula = y ~ x, se = TRUE, color = "#2C3E50", fill = "#BDC3C7", linewidth = 0.55, alpha = 0.25) +
  geom_point(aes(fill = cancer_type), size = 3.4, shape = 21, color = "#111111", stroke = 0.4) +
  geom_text_repel(
    aes(label = paste0(trial_id, " (HR ", sprintf("%.2f", os_hr), ")")),
    size = 2.0,
    family = "Arial",
    color = "#111111",
    box.padding = 0.50,
    point.padding = 0.35,
    max.overlaps = 50,
    force = 5,
    seed = 42
  ) +
  scale_fill_manual(name = "Tumour Type", values = c("NSCLC" = "#2980B9", "CRC" = "#E67E22", "PDAC" = "#C0392B")) +
  scale_x_continuous(limits = c(-3, 44), breaks = seq(0, 40, by = 10), labels = paste0(seq(0, 40, by = 10), "%")) +
  scale_y_continuous(limits = c(0.30, 1.25), breaks = seq(0.4, 1.2, by = 0.2), labels = c("0.40", "0.60", "0.80", "1.00", "1.20")) +
  labs(
    tag = "C",
    x = "Effective Crossover Rate to Targeted Therapy in Control Arm (%)",
    y = "Observed OS Hazard Ratio"
  ) +
  theme_classic(base_size = 7.0, base_family = "Arial") %+replace%
  theme(
    axis.line = element_line(colour = "#333333", linewidth = 0.35),
    axis.ticks = element_line(colour = "#333333", linewidth = 0.35),
    axis.text = element_text(colour = "#222222", size = 6.5),
    axis.title = element_text(colour = "#111111", face = "bold", size = 7.0),
    plot.tag = element_text(colour = "#111111", face = "bold", size = 8.5, family = "Arial"),
    plot.tag.position = c(0.01, 0.98),
    legend.text = element_text(size = 6.2, colour = "#222222"),
    legend.title = element_text(size = 6.8, face = "bold", colour = "#111111"),
    legend.position = "top",
    legend.justification = "center",
    legend.margin = margin(b = -6, t = 0),
    plot.margin = margin(t = 2, r = 6, b = 2, l = 4)
  ) +
  annotate("label", x = 22, y = 0.36, label = "Restricted Crossover (<5%):\nUnconfounded OS benefit\n(HR 0.40–0.56, p < 0.001)", size = 1.85, fill = alpha("#FADBD8", 0.8), color = "#922B21", fontface = "bold", hjust = 0.5, family = "Arial") +
  annotate("label", x = 18, y = 1.16, label = "High Crossover (30–35%):\nControl survival prolonged;\nOS HR diluted toward 1.0", size = 1.85, fill = alpha("#E8F8F5", 0.8), color = "#117864", fontface = "bold", hjust = 0.5, family = "Arial")

fig3_combined <- (panel_a / panel_b / p_corr) + plot_layout(heights = c(1, 1, 1.15))

out_pdf <- file.path(fig_dir, "Figure3_Phase3_RCT_Efficacy_and_Crossover_Regression.pdf")
out_png <- file.path(fig_dir, "Figure3_Phase3_RCT_Efficacy_and_Crossover_Regression.png")
out_eps <- file.path(fig_dir, "Figure3_Phase3_RCT_Efficacy_and_Crossover_Regression.eps")

cairo_pdf(out_pdf, width = 180 / 25.4, height = 145 / 25.4, family = "Arial")
print(fig3_combined)
dev.off()

cairo_ps(out_eps, width = 180 / 25.4, height = 145 / 25.4, family = "Arial")
print(fig3_combined)
dev.off()

ragg::agg_png(out_png, width = 180, height = 145, units = "mm", res = 500)
print(fig3_combined)
dev.off()

cat("Successfully generated Figure 3 in:", fig_dir, "\n")
