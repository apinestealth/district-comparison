import pandas as pd
import numpy as np

#define variables
data_dir = '/Users/annagreene/code/district-comparison/data/'
raw_dist = pd.read_csv(data_dir + 'raw/atlantaExample.csv')
replace = [',', '$', '-', '(', ')']

#run main
def process_data():
    dist = clean_all(raw_dist)
    dist = get_code(dist)
    dist = clean_transactions(dist)
    create_csv(dist)

#remove uneccesary columns & rows and rename columns
def clean_all(raw_dist):
    dist = raw_dist[~raw_dist.DESCRIPTION.str.contains('TOTAL')]
    dist = dist.drop(columns=['Unnamed: 1', 'DESCRIPTION'])
    dist = dist.rename(columns={'ACCOUNT': 'Object_code', ' AMOUNT ': 'Transactions'})

    return dist

#isolate object code
def get_code(dist):
    dist['Object_code'] = dist['Object_code'].str[5:8]

    return dist

#make transactions into useable numbers
def clean_transactions(dist):
    dist['Transactions'] = dist['Transactions'].str.translate({ord(x): '' for x in replace})
    dist['Transactions'] = np.double(dist['Transactions'])
    dist = dist.groupby(['Object_code'])['Transactions'].sum().reset_index()
    dist = dist.round(2)

    return dist

def create_csv(dist):
    dist.to_csv(data_dir + 'processed/atlanta.csv')

if __name__ == '__main__':
    process_data()