#Import Modules
import pandas as pd
import numpy
from conc_metric_functions import season_metrics, peak_metrics

def main():

    #Identify Desired Extracted Qualities
    ##Years of Interest
    years = ["2018", "2019", "2020", "2021", "2023", "2024", "2025"]
    ##Sites of Interest
    locations = ["Invergowrie", "Leicester", "Cardiff", "Belfast", "Dublin"]
    ##Taxa of Interest 
    taxa = ["Betu", "Poac"]

    #Create annual metrics df
    annual_metrics = pd.DataFrame()

    for location in locations:
        #Identify file path
        file_path = f"data/processed/{location}_allyears.csv"
        #Import concentration data for that location
        conc_data = pd.read_csv(file_path)
        #Ensure correct datetime formatting
        conc_data["Date"] = pd.to_datetime(conc_data["Date"], format="%Y-%m-%d")
        #Filter dataframe for each year
        for year in years:
            #Filter concentration data by year
            yearly_conc_data = conc_data[
                conc_data["Date"].dt.year == int(year)]
            #Loop by taxa
            for taxon in taxa:
                #Identify threshold for "High Days"
                if taxon == "Betu":
                    high_days_threshold = 80
                elif taxon == "Poac":
                    high_days_threshold = 50

                #Calculate APIn; Season Start, End and Duration; and SPIn
                season_data = season_metrics(yearly_conc_data, taxon, integral_option="both")
                #Calculate Peak Concentration, Date for Peak Conc, Number of High Days
                peak_data = peak_metrics(yearly_conc_data, taxon, high_days_threshold)

                #Combine calculated metrics + remove taxon
                combined_metrics = {
                    **season_data,
                    **peak_data
                }
                combined_metrics["year"] = year
                combined_metrics["site"] = location
                #combined_metrics_df = pd.DataFrame.from_dict(combined_metrics)
                combined_metrics = pd.DataFrame(combined_metrics, index=[0])

                #Merge combined metrics per site and year into master df
                annual_metrics = pd.concat([annual_metrics, combined_metrics], ignore_index=True)

    annual_metrics = annual_metrics.reindex(columns=["site", "year", "taxon", "start_date", "end_date", "peak_date", "peak_conc", "high_days",  "duration", "APIn", "SPIn"])

    #Code for splitting up year from month-day
    """
    annual_metrics["peak_date"] = pd.to_datetime(annual_metrics["peak_date"]) 
    print(annual_metrics.info())
    date_cols = ["start_date", "end_date", "peak_date"]
    for col in date_cols:
        annual_metrics[col] = annual_metrics[col].dt.strftime("%m-%d")
    print(annual_metrics.head())
    """ 

    #Export
    annual_metrics.to_csv(f"data/processed/yearly_metrics/all_annual_metrics.csv", index=False)
    
      

            

main()