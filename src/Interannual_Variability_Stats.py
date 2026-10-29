import pandas as pd

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
    "start_date_DOY": "std"
})

#Reformat column names
IAV_stats.columns = [f"{stat}_{metric}" for metric, stat in IAV_stats.columns]
IAV_stats.reset_index(inplace=True)

#Calculate Coefficient of Variation for each stat
IAV_stats["%CV_APIn"] = (IAV_stats["std_APIn"]/IAV_stats["mean_APIn"])*100
IAV_stats["%CV_duration"] = (IAV_stats["std_duration"]/IAV_stats["mean_duration"])*100
IAV_stats["%CV_high_days"] = (IAV_stats["std_high_days"]/IAV_stats["mean_high_days"])*100

#Reorder columns
IAV_stats = IAV_stats.reindex(columns = ["site", "taxon", 
                              "mean_APIn", "std_APIn", "%CV_APIn",
                              "mean_duration", "std_duration", "%CV_duration",
                              "mean_high_days", "std_high_days", "%CV_high_days",
                              "std_start_date_DOY"])

#Round values
IAV_stats = IAV_stats.round(2)

#Separate stats by taxa
betu_IAV = IAV_stats[IAV_stats["taxon"] == "Betu"].copy()
poac_IAV = IAV_stats[IAV_stats["taxon"] == "Poac"].copy()


#Export stats
betu_IAV.to_csv(f"data/processed/analysis/IAV/betu_IAV.csv", index=False)
poac_IAV.to_csv(f"data/processed/analysis/IAV/poac_IAV.csv", index=False)

            
            
            





    

    
