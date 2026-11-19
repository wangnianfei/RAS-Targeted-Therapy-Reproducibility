#!/usr/bin/env Rscript
# ==============================================================================
# Figure 4: Global Clinical Trial Landscape of RAS-Targeted Therapies
# Production Script for ESMO Open
# Strictly 180.0 mm double-column width, 125.0 mm height, TrueType Arial font
# Panel tags (A, B, C) matching manuscript citations
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

data_file <- file.path(data_dir, "trials_1182.csv")
trials <- read.csv(data_file, stringsAsFactors = FALSE)
targeted <- trials %>% filter(ras_tier == "RAS-targeted")
targeted <- targeted %>%
  mutate(phase_clean = case_when(
    phase %in% c("Phase 1", "Early Phase 1") ~ "Phase 1",
    phase %in% c("Phase 1/Phase 2") ~ "Phase 1/2",
    phase %in% c("Phase 2") ~ "Phase 2",
    phase %in% c("Phase 3") ~ "Phase 3",
    TRUE ~ "Phase 1/2"
  ), modality = case_when(
    grepl("KRAS G12C", target_class) ~ "KRAS(G12C) Inhibitor",
    grepl("KRAS G12D", target_class) ~ "KRAS(G12D) Inhibitor",
    grepl("pan-RAS / multi-selective RAS\\(ON\\)", target_class) ~ "Multi-RAS(ON) / Pan-RAS",
    grepl("SOS1|SHP2", target_class) ~ "Indirect (SOS1 / SHP2)",
    grepl("vaccine|immunotherapy", target_class) ~ "RAS Vaccine / TCR-T",
    grepl("farnesyl", target_class) ~ "FTase Inhibitor",
    TRUE ~ "Other Targeted"
  ), strategy = case_when(
    grepl("\\|", interventions) ~ "Combination Regimen",
    grepl("with|plus|\\+", brief_title, ignore.case = TRUE) ~ "Combination Regimen",
    TRUE ~ "Monotherapy"
  ))

phase_counts <- targeted %>% count(phase_clean) %>% mutate(pct = n / sum(n) * 100, pct_label = sprintf("%d (%.1f%%)", n, pct))
phase_counts$phase_clean <- factor(phase_counts$phase_clean, levels = rev(c("Phase 1", "Phase 1/2", "Phase 2", "Phase 3")))

p_phase <- ggplot(phase_counts, aes(y = phase_clean, x = n, fill = phase_clean)) +
  geom_bar(stat = "identity", width = 0.62, color = "#FFFFFF", linewidth = 0.25) +
  geom_text(aes(label = pct_label), hjust = -0.1, size = 2.1, color = "#222222", family = "Arial", fontface = "bold") +
  scale_fill_manual(values = c("Phase 1" = "#2C3E50", "Phase 1/2" = "#16A085", "Phase 2" = "#2980B9", "Phase 3" = "#C0392B"), guide = "none") +
  scale_x_continuous(limits = c(0, max(phase_counts$n) * 1.45), breaks = seq(0, 200, by = 50)) +
  labs(tag = "A", x = "Number of Active Trials", y = "") +
  theme_esmo_tight()

modality_counts <- targeted %>%
  filter(modality %in% c("KRAS(G12C) Inhibitor", "KRAS(G12D) Inhibitor", "Multi-RAS(ON) / Pan-RAS", "Indirect (SOS1 / SHP2)", "RAS Vaccine / TCR-T")) %>%
  count(modality, strategy) %>% group_by(modality) %>% mutate(total = sum(n)) %>% ungroup() %>% arrange(total)
modality_counts$modality <- factor(modality_counts$modality, levels = unique(modality_counts$modality))
modality_counts$strategy <- factor(modality_counts$strategy, levels = c("Combination Regimen", "Monotherapy"))

p_modality <- ggplot(modality_counts, aes(y = modality, x = n, fill = strategy)) +
  geom_bar(stat = "identity", position = "stack", width = 0.62, color = "#FFFFFF", linewidth = 0.25) +
  scale_fill_manual(values = c("Combination Regimen" = "#E67E22", "Monotherapy" = "#2980B9")) +
  scale_x_continuous(limits = c(0, 220), breaks = seq(0, 200, by = 50)) +
  labs(tag = "B", x = "Number of Registered Trials", y = "") +
  theme_esmo_tight() +
  theme(legend.position = "top", legend.justification = "right", legend.margin = margin(b = -6, t = 0))

geo_summary <- read.csv(file.path(data_dir, "trial_geographic_summary.csv"), stringsAsFactors = FALSE)
geo_summary$y_pos <- 4:1
geo_summary$region_label <- factor(geo_summary$region, levels = rev(geo_summary$region))

p_geo_bar <- ggplot(geo_summary, aes(y = region_label, x = trials)) +
  geom_bar(stat = "identity", fill = "#34495E", width = 0.62) +
  geom_text(aes(label = paste0(trials, " trials")), hjust = -0.1, size = 2.1, color = "#222222", fontface = "bold", family = "Arial") +
  scale_x_continuous(limits = c(0, 280), breaks = seq(0, 200, by = 50)) +
  labs(tag = "C", x = "Registered Trial Programs", y = "") +
  theme_esmo_tight()

p_geo_cards <- ggplot(geo_summary, aes(y = y_pos)) +
  geom_rect(aes(ymin = y_pos - 0.42, ymax = y_pos + 0.42, xmin = 0, xmax = 10),
            fill = c("#EAECEE", "#E8F8F5", "#FEF9E7", "#EBF5FB"), color = "#D5D8DC", linewidth = 0.3) +
  geom_text(aes(x = 0.15, y = y_pos + 0.16, label = paste0(region, ":")), hjust = 0, size = 2.2, fontface = "bold", color = "#111111", family = "Arial") +
  geom_text(aes(x = 0.15, y = y_pos - 0.16, label = paste0("• Strategic Focus: ", focus)), hjust = 0, size = 1.95, color = "#2C3E50", family = "Arial") +
  scale_y_continuous(limits = c(0.4, 4.6)) +
  scale_x_continuous(limits = c(0, 10)) +
  theme_void(base_family = "Arial") +
  theme(plot.margin = margin(t = 2, r = 4, b = 2, l = 0))

p_geo_combined <- (p_geo_bar | p_geo_cards) + plot_layout(widths = c(1, 1.45))
top_row <- (p_phase | p_modality) + plot_layout(widths = c(1, 1.25))
fig4_combined <- (top_row / p_geo_combined) + plot_layout(heights = c(1, 1.05))

out_pdf <- file.path(fig_dir, "Figure4_Global_Clinical_Trial_Atlas_and_Geography.pdf")
out_png <- file.path(fig_dir, "Figure4_Global_Clinical_Trial_Atlas_and_Geography.png")
out_eps <- file.path(fig_dir, "Figure4_Global_Clinical_Trial_Atlas_and_Geography.eps")

cairo_pdf(out_pdf, width = 180 / 25.4, height = 125 / 25.4, family = "Arial")
print(fig4_combined)
dev.off()

cairo_ps(out_eps, width = 180 / 25.4, height = 125 / 25.4, family = "Arial")
print(fig4_combined)
dev.off()

ragg::agg_png(out_png, width = 180, height = 125, units = "mm", res = 500)
print(fig4_combined)
dev.off()

cat("Successfully generated Figure 4 in:", fig_dir, "\n")
