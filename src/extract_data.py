#Import Modules
import pandas as pd

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
            filtered_df = data_extraction(file, pollen_taxa)
            #Append Yearly Taxa Counts to Temp DB
            location_df = pd.concat([filtered_df, location_df])
        #Export final location dataframe
        location_df.to_csv(f"data/processed/{location}_allyears.csv", index=False)



def data_extraction(df, taxa):
    #Create Data Extraction function that takes full dataframe of Hirst counts at a specific site and returns filtered pandas dataframe
    columns = ["Date"] + taxa
    filtered_df = df[columns]
    #Swap all -1 values for 0 (ignores recording faults)
    filtered_df = filtered_df.replace(-1, 0)
    return filtered_df


if __name__ == "__main__":
    main()