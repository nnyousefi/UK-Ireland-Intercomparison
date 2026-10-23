import pandas as pd
import numpy as np
from extract_data import data_extraction
import os

def main():
    #Identify desired extracted qualities
    ##Set file directory
    directory = "data/raw/dublin"
    ##Set desired taxa
    taxa = ["Betula", "Poaceae"]
    ##Set empty all-years dataframe
    location_df = pd.DataFrame()

    ##Go through each file in the folder
    for filename in os.listdir(directory):
        #Find full file path
        file_path = os.path.join(directory, filename)
        #Determine file type and import file
        if filename.endswith(".xlsx"):
            data = pd.read_excel(file_path)
        elif filename.endswith(".csv"):
            data = pd.read_csv(file_path)
        else:
            raise ValueError(f"No date column found in {filename}")

        ##Format Column Names in Each File
        #If the date column is already named correctly
        if "Date" in data.columns:
            #Reformat Only
            data["Date"] = pd.to_datetime(data["Date"], format="mixed")
        #If date column is not named correctly
        elif "Day" in data.columns:
            #Create new, correctly named column and then reformat
            data["Date"] = pd.to_datetime(data["Day"], format="mixed")
        #Dataset cleaning
        #Capitalise columns
        data.columns = data.columns.str.capitalize()


        #Extract taxa and add to master dataframe
        #Check if current file has multiple years
        years = data["Date"].dt.year.dropna().astype(int).unique()
        for year in years:
        
            ##Extract data
            filtered_df = data_extraction(data, taxa, year)
            ##Clean date column
            filtered_df["Date"] = filtered_df["Date"].dt.strftime("%Y-%m-%d")
            ##Shorten column names (match that of MetOffice data)
            filtered_df.columns = filtered_df.columns.str[:4]
            location_df = pd.concat([filtered_df, location_df])


    #Export final dataframe
    location_df.to_csv(f"data/processed/Dublin_allyears.csv", index=False)

main()
    

    
