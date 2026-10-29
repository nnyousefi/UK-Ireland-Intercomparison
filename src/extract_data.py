#Import Modules
import pandas as pd
import numpy as np

def main():
    #Identify Desired Extracted Qualities
    ##Years of Interest
    years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    ##Sites of Interest
    locations = ["Invergowrie", "Leicester", "Cardiff", "Belfast"]
    ##Taxa of Interest 
    pollen_taxa = ["Betu", "Poac"]


    #For each location
    for location in locations:
        #Create Temporary Empty Location DataFrame
        location_df = pd.DataFrame() 
        #Get data per year
        for year in years:
            #Identify file path
            file_path = f"data/raw/PollenStationData_{year}.xlsx"
            #Import Excel File to Pandas DataFrame
            file = pd.read_excel(file_path, sheet_name=location, skiprows=2)
            #Create new filtered dataframe which extracts dates and pollen taxa for that year and location
            filtered_df = data_extraction(file, pollen_taxa, year)
            #Append Yearly Taxa Counts to Temp DB
            location_df = pd.concat([filtered_df, location_df])
        #Export final location dataframe
        location_df.to_csv(f"data/processed/{location}_allyears.csv", index=False)



def data_extraction(df, taxa, year):
    #Create Data Extraction function that takes full dataframe of Hirst counts 
    #at a specific site and returns filtered pandas dataframe
    
    #Set columns as date + desired taxa
    columns = ["Date"] + taxa

    #Ensure Date is datetime
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], format="mixed")
    
    #Filter dates so they are from March-April
    #Create datetime boundaries
    start_date = pd.Timestamp(year=int(year), month=3, day=1)
    end_date = pd.Timestamp(year=int(year), month=10, day=1)

    #Filter by date and selected columns
    filtered_df = df.loc[
        (df["Date"] >= start_date) & (df["Date"] < end_date),
        columns
    ].copy()
    
    #Swap all -1 values for 0 (ignores recording faults)
    filtered_df = filtered_df.replace(-1, np.nan)
    filtered_df = filtered_df.dropna()
    return filtered_df


if __name__ == "__main__":
    main()