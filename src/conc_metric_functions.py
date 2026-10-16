#Functions for Calculating Common Concentration Metrics from Pandas Dataframes

#Import Modules
import numpy
import pandas as pd
from datetime import date


#Create results df
results = pd.DataFrame()

def season_metrics(df, taxon, integral_option):
    #Function for Calculating Season Start, End and Duration, APIn and SPIn
    APIn = int(df[taxon].sum())
    #Calculate Cumulative Total
    df["Cumulative_Total"] = df[taxon].cumsum()
    #Calculate Cumulative Percentage
    df["Cumulative_Percent"] = (df["Cumulative_Total"]/APIn) * 100
    #Identify Start Date
    start_date = df.loc[df["Cumulative_Percent"] >= 5, "Date"].iloc[0]
    #Identify End Date
    end_date = df.loc[df["Cumulative_Percent"] >= 95, "Date"].iloc[0]
    #Calculate Duration
    duration = (end_date - start_date).days
    #Calculate SPIn
    season_df = df[df["Date"].between(start_date, end_date)]
    SPIn = int(season_df[taxon].sum())

    #Basic Results Output
    results = {
                "taxon": taxon,
                "start_date": start_date,
                "end_date": end_date,
                "duration": duration
            }

    #Check to see if user wants to include APIn, SPIn or Both
    if integral_option == "APIn":
        results["APIn"] = APIn
        return results
    elif integral_option == "SPIn":
        results["SPIn"] = SPIn
        return results
    elif integral_option == "both":
        results["APIn"] = APIn
        results["SPIn"] = SPIn
        return results
    elif integral_option == None:
        return results
    else:
        raise ValueError(
            "integral_option must be 'APIn', 'SPIn', 'both' or None"
        )
    

def peak_metrics(df, taxon, high_days_threshold):
    #Identify peak concentration
    peak_conc = df[taxon].max()
    peak_date = df.loc[df[taxon] == peak_conc, "Date"].iloc[0].date()
    peak_days = df.loc[df[taxon] >= high_days_threshold]
    total_high_days = len(peak_days)
    results = {
        "taxon": taxon,
        "peak_conc": peak_conc,
        "peak_date": peak_date,
        "high_days": total_high_days
    }

    return results

if __name__ == "__main__":
    main()