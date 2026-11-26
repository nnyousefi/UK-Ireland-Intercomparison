import pandas as pd
import numpy as np

#Import annual metrics master table
annual_metrics = pd.read_csv("data/processed/yearly_metrics/all_annual_metrics.csv")
#Convert season dates into usable numeric values (calculate day of year)
date_cols = ["start_date", "end_date", "peak_date"]
#Loop through each date column
for col in date_cols:
    #Convert column to datetime format
    annual_metrics[col] = pd.to_datetime(annual_metrics[col], format="%Y-%m-%d")
    #Extract day of year from datetime series
    annual_metrics[col + "_DOY"] = annual_metrics[col].dt.dayofyear

#Group metrics by site and by taxon
grouped_annual_metrics = annual_metrics.groupby(["site", "taxon"])
#Calculate stats required for IAV analysis
IAV_stats = grouped_annual_metrics.agg({
    "APIn": ["mean", "std"],
    "duration": ["mean", "std"],
    "high_days": ["mean", "std"],
    "start_date_DOY": ["mean", "std"],
    "end_date_DOY": ["mean", "std"]
})

#Reformat column names
IAV_stats.columns = [f"{stat}_{metric}" for metric, stat in IAV_stats.columns]
IAV_stats.reset_index(inplace=True)

#Calculate Coefficient of Variation for each metric
CoV_metrics = ["APIn", "duration", "high_days"]
for metric in CoV_metrics:
    #Set CV to NaN by default
    IAV_stats[f"%CV_{metric}"] = np.nan
    #Identify rows where mean is not 0
    non_zero_mean = IAV_stats[f"mean_{metric}"] != 0
    #Calculate CV for only those rows
    IAV_stats.loc[non_zero_mean, f"%CV_{metric}"] = (
        IAV_stats.loc[non_zero_mean, f"std_{metric}"]/
        IAV_stats.loc[non_zero_mean, f"mean_{metric}"] * 100
    )

#Reorder columns
IAV_stats = IAV_stats.reindex(columns = ["site", "taxon", 
                              "mean_APIn", "std_APIn", "%CV_APIn",
                              "mean_duration", "std_duration", "%CV_duration",
                              "mean_high_days", "std_high_days", "%CV_high_days",
                              "mean_start_date_DOY", "std_start_date_DOY", 
                              "mean_end_date_DOY", "std_end_date_DOY"])

#Add sample size column
IAV_stats["n"] = annual_metrics["year"].nunique()

#Round values
IAV_stats = IAV_stats.round(2)

#Separate stats by taxa
betu_IAV = IAV_stats[IAV_stats["taxon"] == "Betu"].copy()
poac_IAV = IAV_stats[IAV_stats["taxon"] == "Poac"].copy()


#Export stats
betu_IAV.to_csv(f"data/processed/analysis/IAV/betu_IAV.csv", index=False)
poac_IAV.to_csv(f"data/processed/analysis/IAV/poac_IAV.csv", index=False)

            
            
            





    

    
