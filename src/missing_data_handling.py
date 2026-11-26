import pandas as pd
import numpy as np
from extract_data import data_extraction
import os

def main():
    #Set file directory
    directory = "data/processed/all_years"
    #Set desired taxa
    taxa = "Betu", "Poac"
    analysis_years = ["2018", "2019", "2020", "2021", "2023", "2024", "2025"]

    #Set Up Results List
    missingness = []

    #Go through each file in the all-years folder
    for filename in os.listdir(directory):
        #Find location
        location = filename.split("_")[0]

        #Find full file path
        path = os.path.join(directory, filename)
        #Extract Data
        data = pd.read_csv(path)
        #Format date column
        data["Date"] = pd.to_datetime(data["Date"], format="mixed")
        #Generate list of unique years within that file
        years = data["Date"].dt.year.astype(str).unique()
        #Keep only years used in UK-Ireland comparison
        years = [year for year in years
                if year in analysis_years]
        print(years)

        #Iterate through all years in the file
        for year in years:
            #Create copy of dataframe for that particular year
            df = data[data["Date"].dt.year == int(year)].copy()
            #Generate start and end dates
            monitoring_start = pd.to_datetime(f"01-03-{year}", format="%d-%m-%Y")
            monitoring_end = pd.to_datetime(f"30-09-{year}", format="%d-%m-%Y")
            #Filter dataframe by start and end date
            date_filtered_df = df.loc[(df["Date"] >= monitoring_start) & (df["Date"] <= monitoring_end)].copy()

            missing_dates, present_dates, num_expected_dates = date_coverage(date_filtered_df, monitoring_start, monitoring_end)

            
            for taxon in taxa:
                num_valid, num_NA = taxon_coverage(date_filtered_df, taxon)
                total_unavailable = num_NA + len(missing_dates)
                missingness_perc = total_unavailable/num_expected_dates * 100

                #Create record for current site, year and taxon
                record = {
                     "Site": location,
                     "Year": year,
                     "Taxon": taxon,
                     "No. Expected Dates": num_expected_dates,
                     "No. Absent Dates": len(missing_dates),
                     "No. Present Dates": len(present_dates),
                     "No. Valid Observations": num_valid,
                     "No. Invalid Observations": num_NA,
                     "Total Unavailable per Taxon": total_unavailable,
                     "Missingness (%)": round(missingness_perc, 2)
                }


                #Add record to missingness results
                missingness.append(record)

    #After all results have been recorded, turn missingness into a dataframe
    missingness_df = pd.DataFrame.from_dict(missingness)
    #Export data
    missingness_df.to_csv(f"data/processed/missingness/missingness.csv", index=False)


    ##Prepare summary table for export
    analysis_missingness = missingness_df.copy()
    #Group by year
    grouped_analysis_missingness = analysis_missingness.groupby(["Site", "Taxon"])["Missingness (%)"]
    #Calculate aggregate stats
    summary_df = grouped_analysis_missingness.agg([
        "mean", "std", "min", "max"
    ]).round(2).reset_index()
    summary_df = summary_df.rename(columns={
    "mean": "Mean missingness (%)",
    "std": "SD missingness (%)",
    "min": "Minimum missingness (%)",
    "max": "Maximum missingness (%)"
    })

    #Export data
    summary_df.to_csv(f"data/processed/missingness/summary.csv", index=False)


def date_coverage(data, monitoring_start, monitoring_end):
    
    ##Checking Date Coverage (how many dates are missing in every year for each site)
    #Set monitoring start and end dates
    expected_dates = pd.date_range(start=monitoring_start, end=monitoring_end, freq="D")
    actual_dates = data["Date"].unique()

    #Create empty lists for present and missing dates
    present_dates = []
    missing_dates = []

    for date in expected_dates:
            if date in actual_dates:
                present_dates.append(date)
            else:
                missing_dates.append(date)

    num_expected_dates = len(expected_dates)

    return missing_dates, present_dates, num_expected_dates

def taxon_coverage(data, taxon):
    #Create copy of data filtered by taxon
    df = data[["Date", taxon]].copy()
    
    #Count valid and NA values
    num_valid = (df[taxon] >= 0).sum()
    num_NA = (df[taxon].isna()).sum()

    return num_valid, num_NA
    

     

main()