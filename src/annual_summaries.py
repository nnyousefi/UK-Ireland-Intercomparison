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
            #Create empty dictionary for yearly metrics results
            yearly_metrics = {}
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
                combined_metrics.pop("taxon", None)

                #Merge yearly metrics tables to include both taxa
                yearly_metrics[taxon] = combined_metrics
            #Create yearly metrics Dataframe
            yearly_metrics_df = pd.DataFrame(yearly_metrics)
            yearly_metrics_df.index.name = "Metric"
            yearly_metrics_df.loc["start_date"] = pd.to_datetime(yearly_metrics_df.loc["start_date"]).dt.strftime("%d-%m-%Y")
            yearly_metrics_df.loc["end_date"] = pd.to_datetime(yearly_metrics_df.loc["end_date"]).dt.strftime("%d-%m-%Y")
            yearly_metrics_df.to_csv(f"data/processed/yearly_metrics/annual_summaries/{location}/{year}_metrics.csv")

                
            

            

            

main()