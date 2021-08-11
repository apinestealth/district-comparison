import pandas as pd

#define variables
data_dir = '/Users/annagreene/code/district-comparison/data/'
raw_dist = pd.read_csv(data_dir + 'raw/arizonaExample.csv')

#run main
def process_data():
    dist = get_code(raw_dist)
    dist = clean(dist)
    create_csv(dist)

#isolate out the object code
def get_code(raw_dist):
    raw_dist["Object_code"] = 0
    raw_dist["Object_code"] = raw_dist.Account.str.split(".").str[3]

    return raw_dist

#clean the district spreadsheet and make YTD Transactions useable data
def clean(dist):
    #filter only expenditures & remove unneccesary columns
    dist = dist[dist['Account Type']=="EXPENDITURE"]
    dist = dist.drop(columns=['Active', 'Account', 'Description', 'Account Type', 'Budget Control Group', 'Budget', 'Balance', 'Budget Balance', 'Encumbrance', 'Pre Encumbrance', 'Pending Invoices', 'Uncommitted Balance'])

    #convert transactions into numbers
    replace = [',', '$', '-', '(', ')']
    dist['YTD Transactions'] = dist['YTD Transactions'].str.translate({ord(x): '' for x in replace}).astype(float)

    #group duplicate object codes & rename transactions column
    dist = dist.groupby(['Object_code'])['YTD Transactions'].sum().reset_index()
    dist = dist.rename(columns={'YTD Transactions': 'Transactions'})

    #round to 2 decimal places
    dist = dist.round(2)

    return dist

def create_csv(dist):
    dist.to_csv(data_dir + 'processed/tolleson.csv')

if __name__ == '__main__':
    process_data()