#!/usr/bin/env Rscript
# ==============================================================================
# Figure 2: RAS mutation prevalence and KRAS allele spectrum (MSK-IMPACT 2017, derived by derive_figure2_data.py)
# Production Script for ESMO Open. 180 mm x 82 mm, Arial, smallest text 6.5 pt.
# Round 18 redesign: a, bubble matrix (circle area proportional to the share of samples, value printed in every
# cell, so that rates near zero stay readable); b, 100% bars of equal thickness with the share printed in each
# segment. Both panels use solid marks of similar weight and one palette shared with Figure 3.
# ==============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(tidyr)
  library(ggtext)
})

initial_options <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("--file=", initial_options, value = TRUE)
script_dir <- if (length(file_arg) > 0) dirname(normalizePath(sub("--file=", "", file_arg))) else getwd()
data_dir <- file.path(dirname(script_dir), "data")
fig_dir <- file.path(dirname(script_dir), "figures")
dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)

ink <- "#1A1A1A"
theme_fig <- function() {
  theme_minimal(base_size = 7, base_family = "Arial") %+replace%
    theme(
      panel.grid = element_blank(),
      axis.text = element_text(colour = ink, size = 7),
      axis.title = element_text(colour = ink, size = 7),
      plot.tag = element_text(colour = ink, face = "bold", size = 9),
      plot.tag.position = c(0, 1),
      plot.title = element_text(colour = ink, face = "bold", size = 7.5, hjust = 0, margin = margin(b = 4)),
      plot.title.position = "plot",
      legend.text = element_text(size = 7, colour = ink),
      legend.title = element_blank(),
      plot.margin = margin(t = 4, r = 6, b = 2, l = 6)
    )
}

# ---- a: bubble matrix (circles drawn as polygons in data units so that area is exactly proportional) ----
iso <- read.csv(file.path(data_dir, "pancancer_isoform_frequencies.csv"), stringsAsFactors = FALSE, check.names = FALSE)
short <- c("Pancreatic (PDAC)" = "Pancreatic", "Colorectal (CRC)" = "Colorectal")
iso$name <- ifelse(iso$cancer_type %in% names(short), short[iso$cancer_type], iso$cancer_type)
genes <- c("KRAS", "NRAS", "HRAS")
gene_col <- c(KRAS = "#B2182B", NRAS = "#2166AC", HRAS = "#E08214")
col_x <- c(KRAS = 1, NRAS = 3, HRAS = 5)            # columns two units apart, rows one unit apart
iso$y <- rev(seq_len(nrow(iso)))
iso_long <- pivot_longer(iso, all_of(genes), names_to = "gene", values_to = "pct") %>%
  mutate(cx = col_x[gene] - 0.35, r = 0.47 * sqrt(pct / 100),
         txt = ifelse(pct == 0, "0", sprintf("%.1f", pct)), inside = pct >= 60)
theta <- seq(0, 2 * pi, length.out = 73)
circ <- iso_long %>% filter(pct > 0) %>% rowwise() %>%
  reframe(gene = gene, id = paste(name, gene), x = cx + r * cos(theta), y = y + r * sin(theta))

p_a <- ggplot() +
  geom_rect(data = expand.grid(x = col_x, y = iso$y), aes(xmin = x - 0.92, xmax = x + 0.92, ymin = y - 0.48, ymax = y + 0.48),
            fill = "#F3F0EA", colour = NA) +
  geom_polygon(data = circ, aes(x, y, group = id, fill = gene), colour = "white", linewidth = 0.25) +
  geom_text(data = subset(iso_long, inside), aes(cx, y, label = txt), colour = "white", fontface = "bold",
            size = 7 / .pt, family = "Arial") +
  geom_text(data = subset(iso_long, !inside), aes(cx + pmax(r, 0.04) + 0.12, y, label = txt), colour = ink,
            size = 7 / .pt, family = "Arial", hjust = 0) +
  annotate("text", x = col_x, y = max(iso$y) + 0.85, label = genes, fontface = "bold.italic", size = 7.5 / .pt,
           family = "Arial", colour = gene_col[genes]) +
  annotate("text", x = -0.05, y = iso$y, label = iso$name, hjust = 1, size = 7 / .pt, family = "Arial", colour = ink) +
  annotate("text", x = -0.05 - 0.0, y = iso$y - 0.33, label = paste0("n = ", format(iso$n_samples, big.mark = ",", trim = TRUE)),
           hjust = 1, size = 6 / .pt, family = "Arial", colour = "#6B6B6B") +
  scale_fill_manual(values = gene_col, guide = "none") +
  coord_fixed(ratio = 1, xlim = c(-2.6, 5.95), ylim = c(0.45, max(iso$y) + 1.15), expand = FALSE, clip = "off") +
  labs(tag = "a") +
  theme_void(base_family = "Arial") +
  theme(plot.tag = element_text(colour = ink, face = "bold", size = 9), plot.tag.position = c(0, 1),
        plot.margin = margin(t = 4, r = 4, b = 2, l = 4))

# ---- b: 100% allele bars ------------------------------------------------------------------------
al <- read.csv(file.path(data_dir, "kras_allele_frequencies.csv"), stringsAsFactors = FALSE)
lev <- c("G12C", "G12D", "G12V", "G12R", "G13D", "Q61X", "Other")
al_col <- c(G12C = "#B2182B", G12D = "#2166AC", G12V = "#1B7837", G12R = "#762A83",
            G13D = "#E08214", Q61X = "#8C6D31", Other = "#BDBDBD")
tum <- c(PDAC = "Pancreatic", CRC = "Colorectal", NSCLC = "NSCLC")
al <- al %>% mutate(
  allele = factor(allele, levels = lev),
  row = sprintf("%s<br><span style='font-size:6pt;color:#6B6B6B'>n = %d</span>", tum[cancer_type], n_kras_mutations)
) %>% group_by(cancer_type) %>% arrange(allele, .by_group = TRUE) %>%
  mutate(xmax = cumsum(pct), xmin = xmax - pct, mid = (xmin + xmax) / 2) %>% ungroup()
al$row <- factor(al$row, levels = rev(unique(al$row[match(names(tum), al$cancer_type)])))
al <- al %>% mutate(lab = ifelse(pct >= 0.055, sprintf("%.0f", pct * 100), ""),
                    lab_col = ifelse(allele == "Other", ink, "white"))

p_b <- ggplot(al) +
  geom_rect(aes(xmin = xmin, xmax = xmax, ymin = as.numeric(row) - 0.36, ymax = as.numeric(row) + 0.36, fill = allele),
            colour = "white", linewidth = 0.5) +
  geom_text(aes(x = mid, y = as.numeric(row), label = lab, colour = lab_col), size = 7 / .pt, family = "Arial", fontface = "bold") +
  scale_colour_identity() +
  scale_fill_manual(values = al_col, breaks = lev, name = NULL) +
  scale_y_continuous(breaks = seq_along(levels(al$row)), labels = levels(al$row), expand = expansion(add = c(0.45, 0.45))) +
  scale_x_continuous(breaks = seq(0, 1, 0.25), labels = paste0(seq(0, 100, 25), "%"), expand = expansion(add = c(0, 0.01))) +
  guides(fill = guide_legend(nrow = 1, keywidth = unit(3.2, "mm"), keyheight = unit(3.2, "mm"))) +
  labs(tag = "b", x = "Share of <i>KRAS</i> missense mutations", y = NULL) +
  theme_fig() +
  theme(axis.text.y.left = element_markdown(hjust = 1, size = 7, lineheight = 1.1),
        axis.title.x = element_markdown(size = 7, margin = margin(t = 3)),
        axis.line.x = element_line(colour = ink, linewidth = 0.3),
        axis.ticks.x = element_line(colour = ink, linewidth = 0.3),
        axis.ticks.length.x = unit(1.2, "mm"),
        legend.position = "top", legend.justification = c(0, 1), legend.location = "plot",
        legend.margin = margin(b = 0, t = 0, l = 14), legend.box.spacing = unit(1.5, "mm"),
        legend.spacing.x = unit(1, "mm"))

fig2 <- (p_a | p_b) + plot_layout(widths = c(0.78, 1.22))

base <- file.path(fig_dir, "Figure2_RAS_Prevalence_and_KRAS_Alleles")
w <- 180; h <- 82
cairo_pdf(paste0(base, ".pdf"), width = w / 25.4, height = h / 25.4, family = "Arial"); print(fig2); invisible(dev.off())
cairo_ps(paste0(base, ".eps"), width = w / 25.4, height = h / 25.4, family = "Arial"); print(fig2); invisible(dev.off())
ragg::agg_png(paste0(base, ".png"), width = w, height = h, units = "mm", res = 500); print(fig2); invisible(dev.off())
cat("Successfully generated Figure 2 in:", fig_dir, "\n")
