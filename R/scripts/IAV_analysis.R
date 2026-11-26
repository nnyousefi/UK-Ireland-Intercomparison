#### Test import and preview data ####

#Load tidyverse
library(tidyverse)

#Import Betula IAV data
betu_iav <- read_csv("data/processed/analysis/IAV/betu_IAV.csv")
#Import Poaceae Data
poac_iav <- read_csv("data/processed/analysis/IAV/poac_IAV.csv")

#Combine Betula and Poaceae
iav_all <- bind_rows(betu_iav, poac_iav)

#Inspect dataset
glimpse(iav_all)

#Display first six rows
head(iav_all)


#### Main Code ####

### Relative Variation ###

#Reshape CV data into long format
all_cv <- iav_all |> pivot_longer(
    cols = c("%CV_APIn", "%CV_duration", "%CV_high_days"),
    names_to = "metric",
    values_to = "CV"
) |> 
mutate(
    taxon = recode(taxon, 
    "Betu" = "Birch",
    "Poac" = "Grass"),

    metric = recode(metric,
    "%CV_APIn" = "APIn",
    "%CV_duration" = "Season Duration",
    "%CV_high_days" = "High-Pollen Days"),

    metric = factor(
        metric,
        levels = c("APIn", "Season Duration", "High-Pollen Days")
    ),

    taxon = factor(taxon, levels = c("Birch", "Grass"))

)

#Create IAV coefficient of variation plot for both taxa
plot_CV <- ggplot(all_cv, aes(x = CV, y = site)) + 
geom_point(size = 3) +

#Separate metrics into columns and taxa into rows
facet_grid(taxon ~ metric) +

#Axis labels and title
labs(
    title = "Interannual Variability Across Monitoring Sites",
    subtitle = "Comparison of Birch and Grass pollen",
    x = "Coefficient of Variation (%)",
    y = "Monitoring Site"
) +

#Modify plot appearance
theme_minimal() +
theme(
    panel.border = element_rect(
        colour = "grey50",
        fill = NA,
        linewidth = 0.7
    ),
    panel.spacing = unit(1, "lines"),
    strip.background = element_rect(
        fill = "grey90",
        colour = "grey50"
    ),
    strip.text = element_text(face = "bold"),
    panel.grid.minor = element_blank()
)

# Save CV figure as PNG
ggsave(
  "outputs/figures/Betula_Grass_IAV_CV.png",
  plot = plot_CV,
  width = 12,
  height = 8,
  dpi = 300
)

### Absolute Variation ###

#Reshape start and end date SD data into long format
iav_timing <- iav_all |>
pivot_longer(
    cols = c("std_start_date_DOY", "std_end_date_DOY"),
    names_to = "timing_metric",
    values_to = "SD_days"
    )


#Improve labels and control panel ordering
iav_timing <- iav_timing |>
  mutate(
    taxon = recode(taxon,
                   "Betu" = "Birch",
                   "Poac" = "Grass"),

    timing_metric = recode(
      timing_metric,
      "std_start_date_DOY" = "Start date",
      "std_end_date_DOY" = "End date"
    ),

    timing_metric = factor(
      timing_metric,
      levels = c("Start date", "End date")
    ),

    taxon = factor(
      taxon,
      levels = c("Birch", "Grass")
    )
  )

iav_timing <- iav_timing |>
  select(site, taxon, timing_metric, SD_days)

head(iav_timing)


#Plot interannual variability in pollen season timing
plot_timing <- ggplot(iav_timing, aes(x = SD_days, y = site)) +
  geom_point(size = 3) +

  #Separate timing metrics into columns and taxa into rows
  facet_grid(taxon ~ timing_metric) +

  labs(
    title = "Interannual Variability in Pollen Season Timing",
    subtitle = "Comparison of Birch and Grass pollen",
    x = "Standard Deviation (days)",
    y = "Monitoring Site"
  ) +

  theme_minimal() +
  theme(
    panel.border = element_rect(
      colour = "grey50",
      fill = NA,
      linewidth = 0.7
    ),
    panel.spacing = unit(1, "lines"),
    strip.background = element_rect(
      fill = "grey90",
      colour = "grey50"
    ),
    strip.text = element_text(face = "bold"),
    panel.grid.minor = element_blank()
  )

# Save timing SD figure as PNG
ggsave(
  "outputs/figures/Betula_Grass_IAV_Timing_SD.png",
  plot = plot_timing,
  width = 10,
  height = 8,
  dpi = 300
)