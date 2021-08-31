import pandas as pd
import numpy as np

data_dir = '/Users/annagreene/code/district-comparison/data/'
mapping = pd.read_csv(data_dir + 'raw/final_mapping.csv')
pd.options.mode.chained_assignment = None

#run main
def process_data():
    clean_map = clean_sheet(mapping)
    clean_map = clean_code(clean_map)
    create_csv(clean_map)

#get rid of unnecesary columns
def clean_sheet(mapping):
    cols = ["Object_code","Function_code", "Category_Edstruments","Major_Category_Edstruments","Title", "State"]
    clean_map = mapping[cols]
    clean_map = clean_map.fillna(0)
    
    return clean_map

#create new code column that is all ints and combines object & function codes
def clean_code(clean_map):
    clean_map["Code"] = ''
    clean_map["Code"] = np.where(clean_map["Object_code"] == 0, clean_map["Function_code"], clean_map["Object_code"])
    clean_map["Code"] = clean_map["Code"].astype(str)
    clean_map["Code"] = clean_map["Code"].str.strip()

    clean_map["Major_Category_Edstruments"] = clean_map["Major_Category_Edstruments"].replace('Purchased Professional and Technical Services', 'Professional and Technical Services')
    clean_map["Category_Edstruments"] = clean_map["Category_Edstruments"].replace('Purchased Professional Services', 'Professional Services')
    clean_map["Category_Edstruments"] = clean_map["Category_Edstruments"].replace('Other Employee Benefits', 'Other Benefits')
    clean_map["Category_Edstruments"] = clean_map["Category_Edstruments"].replace('Health Insurance/Health Related Benefits', 'Health Insurance/Benefits')

    return clean_map

#save/create csv
def create_csv(clean_map):
    clean_map.to_csv(data_dir + 'processed/mapping.csv')

if __name__ == '__main__':
    process_data()