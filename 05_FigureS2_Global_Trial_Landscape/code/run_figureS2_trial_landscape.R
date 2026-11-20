#!/usr/bin/env Rscript
# ==============================================================================
# Supplementary Figure S2 (Figure 4 in the first submission): Global Clinical Trial Landscape of RAS-Targeted Therapies
# Production Script for ESMO Open
# 180 mm x 150 mm, Arial, smallest text 6.5 pt. Round 18 redesign: a, b compact bars on top; c, world map of
# trial counts by country (a trial counts once in every country where it has a site) with region totals.
# Panel tags (a, b, c; lower case as in all figures and legends). All panels computed from trials_curated.csv (output of
# apply_classification_corrections.py): ras_tier == "RAS-targeted", excluding trials that enrol
# patients with haematological malignancies (n = 353);
# panel c region counts derived from site countries (a trial counts once in each region with >=1 site).
# ==============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(scales)
  library(maps)
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
targeted <- trials %>% filter(ras_tier == "RAS-targeted", !grepl("Haematologic", tumour_group))
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

region_of <- function(cc) {
  dplyr::case_when(
    cc %in% c("United States", "Canada", "Puerto Rico") ~ "North America",
    cc %in% c("China", "Japan", "South Korea", "Taiwan", "Hong Kong") ~ "East Asia",
    cc %in% c("Spain", "Italy", "France", "Germany", "United Kingdom", "Belgium", "Poland", "Netherlands", "Greece",
              "Denmark", "Switzerland", "Austria", "Hungary", "Portugal", "Romania", "Sweden", "Finland", "Norway",
              "Ukraine", "Czechia", "Ireland", "Bulgaria", "Russia", "Serbia", "Croatia", "Slovakia", "Estonia",
              "Latvia", "Lithuania", "Slovenia", "Iceland", "Georgia", "Turkey (T\u00fcrkiye)") ~ "Europe",
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

cat("Panel c region counts:\n"); print(geo_summary); cat("multi-region:", n_multi, " no-site:", n_nosite, "\n")

ink <- "#1A1A1A"; grey <- "#6B6B6B"
pt <- function(x) x / .pt
theme_bar <- function() {
  theme_minimal(base_size = 7, base_family = "Arial") %+replace%
    theme(panel.grid = element_blank(),
          axis.text.y = element_text(colour = ink, size = 7, hjust = 1),
          axis.text.x = element_blank(), axis.title = element_blank(),
          plot.tag = element_text(colour = ink, face = "bold", size = 9), plot.tag.position = c(0, 1),
          plot.title = element_text(colour = ink, face = "bold", size = 7.5, hjust = 0, margin = margin(b = 3, l = 9)),
          plot.title.position = "plot",
          legend.text = element_text(size = 7, colour = ink), legend.title = element_blank(),
          plot.margin = margin(t = 4, r = 6, b = 2, l = 4))
}

# ---- a: phase ----
phase_counts <- targeted %>% count(phase_clean) %>% mutate(pct = n / sum(n) * 100, lab = sprintf("%d (%.1f%%)", n, pct))
phase_counts$phase_clean <- factor(phase_counts$phase_clean, levels = rev(c("Phase 1", "Phase 1/2", "Phase 2", "Phase 2/3 or 3")))
cat("Panel a phases:\n"); print(phase_counts)
phase_col <- c("Phase 1" = "#C6D7EE", "Phase 1/2" = "#8FB3DE", "Phase 2" = "#4A7CC0", "Phase 2/3 or 3" = "#1F3F73")
p_a <- ggplot(phase_counts, aes(y = phase_clean, x = n, fill = phase_clean)) +
  geom_col(width = 0.72) +
  geom_text(aes(label = lab), hjust = -0.08, size = pt(7), family = "Arial", colour = ink) +
  scale_fill_manual(values = phase_col, guide = "none") +
  scale_x_continuous(limits = c(0, 205), expand = c(0, 0)) +
  labs(tag = "a", title = "Trials by phase (n = 353)") + theme_bar()

# ---- b: drug class ----
modality_counts <- targeted %>%
  filter(modality %in% c("KRAS(G12C) Inhibitor", "KRAS(G12D) Inhibitor", "Multi-RAS(ON) / Pan-RAS", "RAS Vaccine / TCR-T")) %>%
  count(modality, strategy) %>% group_by(modality) %>% mutate(total = sum(n)) %>% ungroup() %>% arrange(total)
cat("Panel b modality x strategy:\n"); print(modality_counts)
lab_mod <- c("KRAS(G12C) Inhibitor" = "KRAS G12C inhibitor", "KRAS(G12D) Inhibitor" = "KRAS G12D inhibitor",
             "Multi-RAS(ON) / Pan-RAS" = "Multi-RAS(ON) / pan-RAS", "RAS Vaccine / TCR-T" = "Vaccine / TCR-T / engager")
modality_counts$modality <- factor(modality_counts$modality, levels = unique(modality_counts$modality))
modality_counts$strategy <- factor(modality_counts$strategy, levels = c("Combination Regimen", "Monotherapy"))
tot <- modality_counts %>% distinct(modality, total)
p_b <- ggplot(modality_counts, aes(y = modality, x = n, fill = strategy)) +
  geom_col(width = 0.72, position = position_stack(reverse = TRUE)) +
  geom_text(data = tot, aes(y = modality, x = total, label = total), inherit.aes = FALSE, hjust = -0.25, size = pt(7),
            family = "Arial", colour = ink, fontface = "bold") +
  scale_fill_manual(values = c("Monotherapy" = "#1F3F73", "Combination Regimen" = "#8FB3DE"),
                    breaks = c("Monotherapy", "Combination Regimen"),
                    labels = c("1 registered intervention", "≥ 2 registered interventions")) +
  scale_y_discrete(labels = lab_mod) +
  scale_x_continuous(limits = c(0, 225), expand = c(0, 0)) +
  guides(fill = guide_legend(nrow = 1, keywidth = unit(3, "mm"), keyheight = unit(3, "mm"))) +
  labs(tag = "b", title = "Trials by principal drug class") + theme_bar() +
  theme(legend.position = "bottom", legend.justification = c(0, 0), legend.location = "plot",
        legend.margin = margin(t = 0, l = 0), legend.box.spacing = unit(1, "mm"))

# ---- c: world map ----
map_name <- c("United States" = "USA", "United Kingdom" = "UK", "Czechia" = "Czech Republic", "Turkey (Türkiye)" = "Turkey")
by_country <- targeted %>%
  mutate(country = strsplit(ifelse(is.na(countries), "", countries), "; ")) %>% tidyr::unnest(country) %>%
  filter(country != "") %>% distinct(nct_id, country) %>% count(country, name = "trials") %>% arrange(desc(trials))
by_country$map_region <- ifelse(by_country$country %in% names(map_name), map_name[by_country$country], by_country$country)
cat("Countries with >= 1 site:", nrow(by_country), "\n")
world <- map_data("world", wrap = c(-180, 180)) %>% filter(region != "Antarctica")
# Hong Kong is drawn as a sub-region of China in the map data; colour it by its own count
world$key <- ifelse(world$region == "China" & !is.na(world$subregion) & world$subregion == "Hong Kong", "Hong Kong", world$region)
world <- world %>% left_join(by_country %>% select(key = map_region, trials), by = "key")
cuts <- c(0, 4, 9, 24, 49, 99, Inf)
bins <- c("1–4", "5–9", "10–24", "25–49", "50–99", "≥100")
world$bin <- cut(world$trials, cuts, labels = bins)
# blue sequential scale that continues the phase palette of panel a (#C6D7EE, #8FB3DE, #4A7CC0, #1F3F73)
map_col <- setNames(c("#E1EAF6", "#C6D7EE", "#8FB3DE", "#4A7CC0", "#2A5596", "#13284D"), bins)
unmatched <- setdiff(by_country$map_region, unique(world$key)); if (length(unmatched)) cat("Not drawn on map:", unmatched, "\n")

gs <- setNames(geo_summary$trials, as.character(geo_summary$region))
reg_lab <- data.frame(
  lon = c(-145, -36, 160, 75),
  lat = c(20, 44, 22, -38),
  lab = c(sprintf("North America\n%d trials", gs["North America"]), sprintf("Europe\n%d trials", gs["Europe"]),
          sprintf("East Asia\n%d trials", gs["East Asia"]), sprintf("Other regions\n%d trials", gs["Other regions"])))

top <- head(by_country, 12)
top$lab <- ifelse(top$country == "Turkey (Türkiye)", "Türkiye", top$country)

p_map <- ggplot(world, aes(long, lat, group = group)) +
  geom_polygon(aes(fill = bin), colour = "white", linewidth = 0.08) +
  scale_fill_manual(values = map_col, na.value = "#E6E7E9", breaks = bins, drop = FALSE,
                    name = "Trials with ≥ 1 site") +
  geom_text(data = reg_lab, aes(lon, lat, label = lab), inherit.aes = FALSE, size = pt(7), family = "Arial",
            colour = ink, fontface = "bold", lineheight = 0.95) +
  coord_quickmap(xlim = c(-168, 180), ylim = c(-56, 80), expand = FALSE, clip = "off") +
  guides(fill = guide_legend(nrow = 1, title.position = "left", keywidth = unit(5, "mm"), keyheight = unit(2.6, "mm"),
                             label.position = "bottom")) +
  labs(tag = "c", title = sprintf("Trial sites by country or region (%d countries and regions; %d trials multinational)", nrow(by_country), sum(targeted$is_multinational == "yes"))) +
  theme_void(base_family = "Arial") +
  theme(plot.tag = element_text(colour = ink, face = "bold", size = 9), plot.tag.position = c(0, 1),
        plot.title = element_text(colour = ink, face = "bold", size = 7.5, hjust = 0, margin = margin(b = 2, l = 9)),
        legend.position = "bottom", legend.title = element_text(size = 7, colour = ink, margin = margin(r = 4)),
        legend.text = element_text(size = 6.5, colour = ink), legend.spacing.x = unit(0, "mm"),
        plot.margin = margin(t = 4, r = 2, b = 2, l = 4))

top$country_f <- factor(top$lab, levels = rev(top$lab))
top$bin <- cut(top$trials, cuts, labels = bins)
p_top <- ggplot(top, aes(y = country_f, x = trials, fill = bin)) +
  geom_col(width = 0.72) +
  geom_text(aes(label = trials), hjust = -0.2, size = pt(7), family = "Arial", colour = ink) +
  scale_fill_manual(values = map_col, guide = "none") +
  scale_x_continuous(limits = c(0, 235), expand = c(0, 0)) +
  labs(title = "Top 12 countries and regions") + theme_bar() +
  theme(plot.margin = margin(t = 6, r = 4, b = 14, l = 2))

fig <- wrap_plots(wrap_plots(p_a, p_b, widths = c(1, 1.15)), wrap_plots(p_map, p_top, widths = c(3.3, 1)),
                  ncol = 1, heights = c(0.5, 1))

base <- file.path(fig_dir, "FigureS2_Global_Clinical_Trial_Atlas_and_Geography")
w <- 180; h <- 112
cairo_pdf(paste0(base, ".pdf"), width = w / 25.4, height = h / 25.4, family = "Arial"); print(fig); invisible(dev.off())
cairo_ps(paste0(base, ".eps"), width = w / 25.4, height = h / 25.4, family = "Arial"); print(fig); invisible(dev.off())
ragg::agg_png(paste0(base, ".png"), width = w, height = h, units = "mm", res = 500); print(fig); invisible(dev.off())
cat("Successfully generated Supplementary Figure S2 in:", fig_dir, "\n")
