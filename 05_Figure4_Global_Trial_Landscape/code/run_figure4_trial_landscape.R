#!/usr/bin/env Rscript
# ==============================================================================
# Figure 4: Global Clinical Trial Landscape of RAS-Targeted Therapies
# Production Script for ESMO Open
# Strictly 180.0 mm double-column width, 125.0 mm height, TrueType Arial font
# Panel tags (A, B, C). All panels computed from trials_curated.csv (output of
# apply_classification_corrections.py): ras_tier == "RAS-targeted", excluding trials that enrol only
# patients with haematological malignancies (n = 367);
# panel C region counts derived from site countries (a trial counts once in each region with >=1 site).
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

data_file <- file.path(data_dir, "trials_curated.csv")
trials <- read.csv(data_file, stringsAsFactors = FALSE)
targeted <- trials %>% filter(ras_tier == "RAS-targeted", tumour_group != "Haematologic malignancy")
cat("Analysis set n =", nrow(targeted), "\n")
targeted <- targeted %>%
  mutate(phase_clean = case_when(
    phase %in% c("Phase 1", "Early Phase 1") ~ "Phase 1",
    phase %in% c("Phase 1/Phase 2") ~ "Phase 1/2",
    phase %in% c("Phase 2") ~ "Phase 2",
    phase %in% c("Phase 2/Phase 3", "Phase 3") ~ "Phase 2/3 or 3",
    TRUE ~ NA_character_
  ), modality = case_when(
    grepl("KRAS G12C", target_class) ~ "KRAS(G12C) Inhibitor",
    grepl("KRAS G12D", target_class) ~ "KRAS(G12D) Inhibitor",
    grepl("pan-RAS / multi-selective RAS\\(ON\\)", target_class) ~ "Multi-RAS(ON) / Pan-RAS",
    grepl("vaccine|immunotherapy", target_class) ~ "RAS Vaccine / TCR-T",
    grepl("farnesyl", target_class) ~ "FTase Inhibitor",
    TRUE ~ "Other Targeted"
  ), strategy = ifelse(grepl("\\|", interventions), "Combination Regimen", "Monotherapy"))
# strategy = number of registered interventions (>= 2 vs 1); control-arm agents count as interventions

phase_counts <- targeted %>% count(phase_clean) %>% mutate(pct = n / sum(n) * 100, pct_label = sprintf("%d (%.1f%%)", n, pct))
phase_counts$phase_clean <- factor(phase_counts$phase_clean, levels = rev(c("Phase 1", "Phase 1/2", "Phase 2", "Phase 2/3 or 3")))

p_phase <- ggplot(phase_counts, aes(y = phase_clean, x = n, fill = phase_clean)) +
  geom_bar(stat = "identity", width = 0.62, color = "#FFFFFF", linewidth = 0.25) +
  geom_text(aes(label = pct_label), hjust = -0.1, size = 2.1, color = "#222222", family = "Arial", fontface = "bold") +
  scale_fill_manual(values = c("Phase 1" = "#2C3E50", "Phase 1/2" = "#16A085", "Phase 2" = "#2980B9", "Phase 2/3 or 3" = "#C0392B"), guide = "none") +
  scale_x_continuous(limits = c(0, max(phase_counts$n) * 1.45), breaks = seq(0, 200, by = 50)) +
  labs(tag = "A", x = "Number of trials (all statuses)", y = "") +
  theme_esmo_tight()

modality_counts <- targeted %>%
  filter(modality %in% c("KRAS(G12C) Inhibitor", "KRAS(G12D) Inhibitor", "Multi-RAS(ON) / Pan-RAS", "RAS Vaccine / TCR-T")) %>%
  count(modality, strategy) %>% group_by(modality) %>% mutate(total = sum(n)) %>% ungroup() %>% arrange(total)
modality_counts$modality <- factor(modality_counts$modality, levels = unique(modality_counts$modality))
modality_counts$strategy <- factor(modality_counts$strategy, levels = c("Combination Regimen", "Monotherapy"))

p_modality <- ggplot(modality_counts, aes(y = modality, x = n, fill = strategy)) +
  geom_bar(stat = "identity", position = "stack", width = 0.62, color = "#FFFFFF", linewidth = 0.25) +
  scale_fill_manual(values = c("Combination Regimen" = "#E67E22", "Monotherapy" = "#2980B9"), labels = c("\u2265 2 registered interventions", "Single registered intervention")) +
  scale_x_continuous(limits = c(0, 220), breaks = seq(0, 200, by = 50)) +
  labs(tag = "B", x = "Number of trials", y = "") +
  theme_esmo_tight() +
  theme(legend.position = "top", legend.justification = "right", legend.margin = margin(b = -6, t = 0))

region_of <- function(cc) {
  dplyr::case_when(
    cc %in% c("United States", "Canada", "Puerto Rico") ~ "North America",
    cc %in% c("China", "Japan", "South Korea", "Taiwan", "Hong Kong") ~ "East Asia",
    cc %in% c("Spain", "Italy", "France", "Germany", "United Kingdom", "Belgium", "Poland", "Netherlands", "Greece",
              "Denmark", "Switzerland", "Austria", "Hungary", "Portugal", "Romania", "Sweden", "Finland", "Norway",
              "Ukraine", "Czechia", "Ireland", "Bulgaria", "Russia", "Serbia", "Croatia", "Slovakia", "Estonia",
              "Latvia", "Slovenia", "Iceland", "Georgia", "Turkey (T\u00fcrkiye)") ~ "Europe",
    TRUE ~ "Other regions"
  )
}
site_rows <- targeted %>%
  mutate(country = strsplit(ifelse(is.na(countries), "", countries), "; ")) %>%
  tidyr::unnest(country) %>%
  filter(country != "") %>%
  mutate(region = region_of(country)) %>%
  distinct(nct_id, region)
n_multi <- site_rows %>% count(nct_id) %>% filter(n > 1) %>% nrow()
n_nosite <- sum(is.na(targeted$countries) | targeted$countries == "")
geo_summary <- site_rows %>% count(region, name = "trials")
geo_summary$region <- factor(geo_summary$region, levels = rev(c("North America", "East Asia", "Europe", "Other regions")))

p_geo_combined <- ggplot(geo_summary, aes(y = region, x = trials)) +
  geom_bar(stat = "identity", fill = "#34495E", width = 0.62) +
  geom_text(aes(label = trials), hjust = -0.2, size = 2.1, color = "#222222", fontface = "bold", family = "Arial") +
  scale_x_continuous(limits = c(0, max(geo_summary$trials) * 1.25), breaks = seq(0, 250, by = 50)) +
  labs(tag = "C", x = "Trials with \u2265 1 site in region", y = "") +
  theme_esmo_tight()
cat("Panel C region counts:\n"); print(geo_summary); cat("multi-region:", n_multi, " no-site:", n_nosite, "\n")
cat("Panel A phases:\n"); print(phase_counts)
cat("Panel B modality x strategy:\n"); print(modality_counts)

top_row <- (p_phase | p_modality) + plot_layout(widths = c(1, 1.25))
fig4_combined <- (top_row / (p_geo_combined | plot_spacer() + theme_void()) + plot_layout(heights = c(1, 0.8))) 

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
