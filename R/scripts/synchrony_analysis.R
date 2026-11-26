# Synchrony analysis heatmaps
#### Import and preview data ####

# Load packages
library(tidyverse)
library(patchwork)

# Create output directory
dir.create(
  "outputs/figures/synchrony",
  recursive = TRUE,
  showWarnings = FALSE
)


#### Function for creating correlation heatmaps ####

create_corr_heatmap <- function(taxon, metric, method) {

  # Construct the filename
  file_path <- file.path(
    "data/processed/analysis/synchrony",
    method,
    paste0(taxon, "_", metric, "_", method, "_corrmatrix.csv")
  )

  # Check that the file exists
  if (!file.exists(file_path)) {
    stop(paste("File not found:", file_path))
  }

  # Read the correlation matrix
  corr_matrix <- read_csv(
    file_path,
    show_col_types = FALSE
  )

  # Store the original site order
  site_order <- corr_matrix$site

  # Convert matrix from wide to long format
  corr_long <- corr_matrix |>
    pivot_longer(
      cols = -site,
      names_to = "site_2",
      values_to = "correlation"
    ) |>
    mutate(
      site = factor(site, levels = rev(site_order)),
      site_2 = factor(site_2, levels = site_order)
    )

  # Translate metric names into plain English
  metric_labels <- c(
    "APIn" = "APIn",
    "duration" = "Duration",
    "high_days" = "No. of High Days",
    "start_DOY" = "Season Start DoY",
    "end_DOY" = "Season End DoY"
  )

  # Create the heatmap
  p <- ggplot(
    corr_long,
    aes(x = site_2, y = site, fill = correlation)
  ) +
    geom_tile(
      colour = "white",
      linewidth = 0.3
    ) +
    geom_text(
      aes(label = sprintf("%.2f", correlation)),
      colour = "black",
      size = 3
    ) +
    scale_fill_gradient2(
      low = "blue",
      mid = "white",
      high = "red",
      midpoint = 0,
      limits = c(-1, 1),
      name = "Correlation"
    ) +
    coord_equal() +
    labs(
      title = metric_labels[[metric]],
      x = NULL,
      y = NULL
    ) +
    theme_minimal() +
    theme(
      axis.text.x = element_text(
        angle = 45,
        hjust = 1,
        size = 8
      ),
      axis.text.y = element_text(size = 8),
      plot.title = element_text(
        face = "bold",
        size = 11
      ),
      legend.position = "right",
      legend.title = element_text(size = 8),
      legend.text = element_text(size = 7),
      panel.grid = element_blank(),
      plot.margin = margin(3, 3, 3, 3)
    )

  return(p)
}


#### Define metrics and correlation methods ####

metrics <- c(
  "APIn",
  "duration",
  "high_days",
  "start_DOY",
  "end_DOY"
)

methods <- c("pearson", "spearman")


#### Generate heatmaps ####


#### Birch - Pearson ####

# Generate plots
betu_pearson_plots <- map(
  metrics,
  ~ create_corr_heatmap("Betu", .x, "pearson")
)

# Arrange plots
betu_pearson_figure <- wrap_plots(
  c(betu_pearson_plots, list(guide_area())),
  ncol = 2,
  nrow = 3
) +
  plot_layout(guides = "collect") +
  plot_annotation(
    title = "Inter-site Synchrony: Birch (Betula)",
    subtitle = "Pearson Correlation"
  ) &
  theme(
    plot.title = element_text(face = "bold", size = 16),
    plot.subtitle = element_text(size = 11),
    legend.position = "right"
  )

# Save figure
ggsave(
  "outputs/figures/synchrony/Betula_Pearson.png",
  plot = betu_pearson_figure,
  width = 29.7,
  height = 21,
  units = "cm",
  dpi = 300
)


#### Birch - Spearman ####

# Generate plots
betu_spearman_plots <- map(
  metrics,
  ~ create_corr_heatmap("Betu", .x, "spearman")
)

# Arrange plots
betu_spearman_figure <- wrap_plots(
  c(betu_spearman_plots, list(guide_area())),
  ncol = 2,
  nrow = 3
) +
  plot_layout(guides = "collect") +
  plot_annotation(
    title = "Inter-site Synchrony: Birch (Betula)",
    subtitle = "Spearman Correlation"
  ) &
  theme(
    plot.title = element_text(face = "bold", size = 16),
    plot.subtitle = element_text(size = 11),
    legend.position = "right"
  )

# Save figure
ggsave(
  "outputs/figures/synchrony/Betula_Spearman.png",
  plot = betu_spearman_figure,
  width = 29.7,
  height = 21,
  units = "cm",
  dpi = 300
)


#### Grass - Pearson ####

# Generate plots
poac_pearson_plots <- map(
  metrics,
  ~ create_corr_heatmap("Poac", .x, "pearson")
)

# Arrange plots
poac_pearson_figure <- wrap_plots(
  c(poac_pearson_plots, list(guide_area())),
  ncol = 2,
  nrow = 3
) +
  plot_layout(guides = "collect") +
  plot_annotation(
    title = "Inter-site Synchrony: Grass (Poaceae)",
    subtitle = "Pearson Correlation"
  ) &
  theme(
    plot.title = element_text(face = "bold", size = 16),
    plot.subtitle = element_text(size = 11),
    legend.position = "right"
  )

# Save figure
ggsave(
  "outputs/figures/synchrony/Poaceae_Pearson.png",
  plot = poac_pearson_figure,
  width = 29.7,
  height = 21,
  units = "cm",
  dpi = 300
)


#### Grass - Spearman ####

# Generate plots
poac_spearman_plots <- map(
  metrics,
  ~ create_corr_heatmap("Poac", .x, "spearman")
)

# Arrange plots
poac_spearman_figure <- wrap_plots(
  c(poac_spearman_plots, list(guide_area())),
  ncol = 2,
  nrow = 3
) +
  plot_layout(guides = "collect") +
  plot_annotation(
    title = "Inter-site Synchrony: Grass (Poaceae)",
    subtitle = "Spearman Correlation"
  ) &
  theme(
    plot.title = element_text(face = "bold", size = 16),
    plot.subtitle = element_text(size = 11),
    legend.position = "right"
  )

# Save figure
ggsave(
  "outputs/figures/synchrony/Poaceae_Spearman.png",
  plot = poac_spearman_figure,
  width = 29.7,
  height = 21,
  units = "cm",
  dpi = 300
)
