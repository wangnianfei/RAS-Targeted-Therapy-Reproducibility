#!/usr/bin/env Rscript
# ==============================================================================
# Figure 3: PFS and OS hazard ratios across seven phase III RCTs (descriptive forest plots)
# Production Script for ESMO Open. 180 mm x 92 mm, Arial, smallest text 6.5 pt.
# Round 19: no panel letters; each block is headed by its endpoint.
# Round 18 redesign: one table-forest. Each trial is one row; the PFS and OS blocks sit side by side and share the
# trial, setting and n columns. Colour = tumour type; filled square = 95% CI excludes 1, open = includes 1;
# square area proportional to n. No pooled estimate. Drawn in a single coordinate system (x in mm) so that
# row bands and columns line up exactly.
# ==============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
})

initial_options <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("--file=", initial_options, value = TRUE)
script_dir <- if (length(file_arg) > 0) dirname(normalizePath(sub("--file=", "", file_arg))) else getwd()
data_dir <- file.path(dirname(script_dir), "data")
fig_dir <- file.path(dirname(script_dir), "figures")
dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)

ink <- "#1A1A1A"; grey <- "#6B6B6B"
pt <- function(x) x / .pt                       # font size in pt -> ggplot size
d <- read.csv(file.path(data_dir, "phase3_rct_outcomes.csv"), stringsAsFactors = FALSE)
d$y <- rev(seq_len(nrow(d)))
d$tumour <- sub(",.*", "", d$setting)
d$comparator <- sub(".*\\(vs ", "vs ", sub("\\)$", "", d$setting))
d$line <- trimws(sub("^[^,]*, *([^ ]*).*", "\\1", d$setting))
d$sub <- sprintf("%s, %s, %s", d$tumour, d$line, d$comparator)
tum_col <- c(NSCLC = "#1F4E8C", mCRC = "#1B7F5C", mPDAC = "#B2182B", Melanoma = "#7A4E9C")

# ---- x layout (mm) ----
X <- list(trial = 3.2, n = 59.5, f1 = c(63, 98), t1 = 99.5, f2 = c(121, 156), t2 = 157.5)
lo <- log(0.25); hi <- log(1.6)
mapx <- function(hr, f) f[1] + (log(hr) - lo) / (hi - lo) * (f[2] - f[1])
brks <- c(0.25, 0.5, 1, 1.5)

ci_txt <- function(h, l, u) ifelse(is.na(h), "", sprintf("%.2f (%.2f–%.2f)", h, l, u))
mk <- function(h, l, u, f, ep) data.frame(trial = d$trial_id, y = d$y, tumour = d$tumour, n = d$n_pts, ep = ep,
  x = mapx(h, f), xl = mapx(l, f), xu = mapx(u, f), sig = !is.na(u) & u < 1, txt = ci_txt(h, l, u), ok = !is.na(h))
pts <- rbind(mk(d$pfs_hr, d$pfs_low, d$pfs_high, X$f1, "PFS"), mk(d$os_hr, d$os_low, d$os_high, X$f2, "OS"))
pts$tx <- ifelse(pts$ep == "PFS", X$t1, X$t2)
pts$fill <- ifelse(pts$sig, tum_col[pts$tumour], "white")

top <- nrow(d) + 0.5
axis_y <- 0.35
axes <- rbind(data.frame(f = "a", hr = brks, x = mapx(brks, X$f1)), data.frame(f = "b", hr = brks, x = mapx(brks, X$f2)))
grp_breaks <- c(4.5, 2.5, 1.5)   # NSCLC | mCRC | mPDAC | melanoma

p <- ggplot() +
  # row bands
  geom_rect(data = d, aes(xmin = 0, xmax = 180, ymin = y - 0.5, ymax = y + 0.5),
            fill = ifelse(d$y %% 2 == 0, "#F4F1EC", "white"), colour = NA) +
  geom_segment(aes(x = 0, xend = 180, y = grp_breaks, yend = grp_breaks), colour = "#BFB8AC", linewidth = 0.3) +
  # tumour colour bar
  geom_rect(data = d, aes(xmin = 0, xmax = 1.3, ymin = y - 0.44, ymax = y + 0.44, fill = I(tum_col[tumour]))) +
  # null lines
  annotate("segment", x = mapx(1, X$f1), xend = mapx(1, X$f1), y = axis_y, yend = top, colour = grey, linewidth = 0.35, linetype = "22") +
  annotate("segment", x = mapx(1, X$f2), xend = mapx(1, X$f2), y = axis_y, yend = top, colour = grey, linewidth = 0.35, linetype = "22") +
  # CIs and squares
  geom_segment(data = subset(pts, ok), aes(x = xl, xend = xu, y = y, yend = y, colour = I(tum_col[tumour])), linewidth = 0.7, lineend = "butt") +
  geom_point(data = subset(pts, ok), aes(x = x, y = y, size = n, fill = I(fill), colour = I(tum_col[tumour])), shape = 22, stroke = 0.8) +
  scale_size_area(max_size = 4.2, guide = "none") +
  # HR text
  geom_text(data = subset(pts, ok), aes(x = tx, y = y, label = txt, fontface = ifelse(sig, "bold", "plain")),
            hjust = 0, size = pt(7), family = "Arial", colour = ink) +
  annotate("text", x = X$t2, y = d$y[is.na(d$os_hr)], label = "OS immature", hjust = 0, size = pt(6.5), family = "Arial",
           colour = grey, fontface = "italic") +
  # trial and setting columns
  geom_text(data = d, aes(x = X$trial, y = y + 0.17, label = trial_id), hjust = 0, size = pt(7.2), family = "Arial", fontface = "bold", colour = ink) +
  geom_text(data = d, aes(x = X$trial, y = y - 0.21, label = sub), hjust = 0, size = pt(6.5), family = "Arial", colour = grey) +
  geom_text(data = d, aes(x = X$n, y = y, label = n_pts), hjust = 1, size = pt(7), family = "Arial", colour = ink) +
  # headers
  annotate("text", x = c(X$trial, X$n), y = top + 0.42, label = c("Trial and setting", "n"), hjust = c(0, 1),
           size = pt(7), family = "Arial", fontface = "bold", colour = ink) +
  # endpoint headers: each spans its forest and HR columns, with a coloured rule underneath
  annotate("text", x = c(X$f1[1], X$f2[1]), y = top + 1.05, label = c("Progression-free survival (PFS)", "Overall survival (OS)"),
           hjust = 0, size = pt(8), family = "Arial", fontface = "bold", colour = ink) +
  annotate("segment", x = c(X$f1[1], X$f2[1]), xend = c(X$t1 + 20, X$t2 + 20), y = top + 0.74, yend = top + 0.74,
           colour = ink, linewidth = 0.35) +
  annotate("text", x = c(X$t1, X$t2), y = top + 0.42, label = "HR (95% CI)", hjust = 0, size = pt(7), family = "Arial",
           fontface = "bold", colour = ink) +
  annotate("segment", x = 0, xend = 180, y = top, yend = top, colour = ink, linewidth = 0.45) +
  # x axes
  annotate("segment", x = c(X$f1[1], X$f2[1]), xend = c(X$f1[2], X$f2[2]), y = axis_y, yend = axis_y, colour = ink, linewidth = 0.4) +
  geom_segment(data = axes, aes(x = x, xend = x, y = axis_y, yend = axis_y - 0.12), colour = ink, linewidth = 0.4) +
  geom_text(data = axes, aes(x = x, y = axis_y - 0.32, label = c("0.25", "0.5", "1", "1.5")[match(hr, brks)]), size = pt(6.8), family = "Arial", colour = ink) +
  annotate("text", x = c(mapx(1, X$f1) - 1.2, mapx(1, X$f2) - 1.2), y = axis_y - 0.72, label = "← Favours RAS-pathway inhibitor",
           hjust = 1, size = pt(6.5), family = "Arial", colour = ink) +
  annotate("text", x = c(mapx(1, X$f1) + 1.2, mapx(1, X$f2) + 1.2), y = axis_y - 0.72, label = "Control →",
           hjust = 0, size = pt(6.5), family = "Arial", colour = grey) +
  # key
  annotate("point", x = c(3.5, 31), y = axis_y - 0.32, shape = 22, size = 2.6, stroke = 0.8, colour = ink, fill = c(ink, "white")) +
  annotate("text", x = c(5.5, 33), y = axis_y - 0.32, label = c("95% CI excludes 1", "includes 1"), hjust = 0,
           size = pt(6.5), family = "Arial", colour = ink) +
  annotate("text", x = 3.2, y = axis_y - 0.72, label = "Square area proportional to n; HR on log scale", hjust = 0,
           size = pt(6.5), family = "Arial", colour = grey) +
  scale_x_continuous(limits = c(0, 180), expand = c(0, 0)) +
  scale_y_continuous(limits = c(axis_y - 0.95, top + 1.4), expand = c(0, 0)) +
  theme_void(base_family = "Arial") + theme(plot.margin = margin(2, 2, 2, 2))

base <- file.path(fig_dir, "Figure3_Phase3_RCT_PFS_OS_Forest")
w <- 180; h <- 92
cairo_pdf(paste0(base, ".pdf"), width = w / 25.4, height = h / 25.4, family = "Arial"); print(p); invisible(dev.off())
cairo_ps(paste0(base, ".eps"), width = w / 25.4, height = h / 25.4, family = "Arial"); print(p); invisible(dev.off())
ragg::agg_png(paste0(base, ".png"), width = w, height = h, units = "mm", res = 500); print(p); invisible(dev.off())
cat("Successfully generated Figure 3 in:", fig_dir, "\n")
