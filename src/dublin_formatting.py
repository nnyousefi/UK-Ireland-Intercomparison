import pandas as pd
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

        ##Format Column Names in Each File
        #If the date column is already named correctly
        if "Date" in data.columns:
            #Reformat Only
            data["Date"] = pd.to_datetime(data["Date"], format="mixed").dt.strftime("%Y-%m-%d")
        #If date column is not named correctly
        elif "Day" in data.columns:
            #Create new, correctly named column and then reformat
            data["Date"] = pd.to_datetime(data["Day"], format="mixed").dt.strftime("%Y-%m-%d")
        #Capitalise columns
        data.columns = data.columns.str.capitalize()

        #Extract taxa and add to master dataframe\
        ##Extract data
        filtered_df = data_extraction(data, taxa)
        ##Shorten column names (match that of MetOffice data)
        filtered_df.columns = filtered_df.columns.str[:4]
        location_df = pd.concat([filtered_df, location_df])

    #Clean resultant dataframe
    #Remove empty rows (rows missing a date)
    location_df.dropna(how="all", inplace=True)
    #Replace empty counts with Os
    location_df = location_df.fillna("0")
    #Export final dataframe
    location_df.to_csv(f"data/processed/Dublin_allyears.csv", index=False)

main()
    

    
