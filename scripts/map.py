import pandas as pd
import numpy as np
import sys

args = sys.argv[1:]
district_1 = args[0].lower()
state_1 = args[1].capitalize()
district_2 = args[2].lower()
state_2 = args[3].capitalize()

data_dir = '/Users/annagreene/code/district-comparison/data/'
mapping = pd.read_csv(data_dir + 'processed/mapping.csv')
dist_1_og = pd.read_csv(data_dir + 'processed/' + district_1 + '.csv')
dist_2_og = pd.read_csv(data_dir + 'processed/' + district_2 + '.csv')

def main():
    maps = create_maps(mapping, state_1, state_2)
    dists = find_unmatched(dist_1_og, maps[0], dist_2_og, maps[1])
    dist_1 = dists[0]
    dist_2 = dists[1]
    merges = map(dist_1, maps[0], dist_2, maps[1])
    create_csv(merges)

def create_maps(mapping, state_1, state_2):
    #first dist
    dist_1_map = mapping[mapping['State'] == state_1].reset_index()
    dist_1_map = dist_1_map.drop(columns=['index', 'Unnamed: 0', 'Object_code', 'Function_code'])
    dist_1_map.loc[len(dist_1_map.index)] = ['Miscellaneous', 'Other Financing Uses', '*Unable to assign to mapping tool*', state_1, 'XXXX']
    
    #second dist
    dist_2_map = mapping[mapping['State'] == state_2].reset_index()
    dist_2_map = dist_2_map.drop(columns=['index', 'Unnamed: 0', 'Object_code', 'Function_code'])
    dist_2_map.loc[len(dist_2_map.index)] = ['Miscellaneous', 'Other Financing Uses', '*Unable to assign to mapping tool*', state_2, 'XXXX']

    return [dist_1_map, dist_2_map]

def find_unmatched(dist_1, dist_1_map, dist_2, dist_2_map):
    #first dist
    dist_1['Code'] = dist_1['Code'].astype(str)
    dist_1_merge_diff = dist_1.merge(dist_1_map, how='left', on='Code', indicator=True)
    dist_1_merge_diff2 = dist_1_merge_diff[dist_1_merge_diff['_merge'] == 'left_only']
    dist_1_not_mapped = list(dist_1_merge_diff2['Code'])
    dist_1['Code'] = np.where(dist_1['Code'].isin(dist_1_not_mapped), dist_1['Code'] == 'False', dist_1['Code'])

    dist_1.loc[(dist_1.Code == False),'Code']='XXXX'
    dist_1 = dist_1.groupby(['Code'])['Transactions'].sum().reset_index()
    dist_1 = dist_1[dist_1['Transactions']>0]

    #second dist
    dist_2['Code'] = dist_2['Code'].astype(str)
    dist_2_merge_diff = dist_2.merge(dist_2_map, how='left', on='Code', indicator=True)
    dist_2_merge_diff2 = dist_2_merge_diff[dist_2_merge_diff['_merge'] == 'left_only']
    dist_2_not_mapped = list(dist_2_merge_diff2['Code'])
    dist_2['Code'] = np.where(dist_2['Code'].isin(dist_2_not_mapped), dist_2['Code'] == 'False', dist_2['Code'])

    dist_2.loc[(dist_2.Code == False),'Code']='XXXX'
    dist_2 = dist_2.groupby(['Code'])['Transactions'].sum().reset_index()
    dist_2 = dist_2[dist_2['Transactions']>0]

    return [dist_1, dist_2]

def map(dist_1, dist_1_map, dist_2, dist_2_map):
    dist_1_merge = dist_1.merge(dist_1_map, how='left', on='Code')
    dist_2_merge = dist_2.merge(dist_2_map, how='left', on='Code')
    #dist_1_subcategories = dist_1_merge.groupby("Category_Edstruments")['Transactions'].sum().reset_index()
    #dist_2_subcategories = dist_2_merge.groupby("Category_Edstruments")['Transactions'].sum().reset_index()

    return [dist_1_merge, dist_2_merge]

def create_csv(merges):
    #dist 1
    dist_1_merge = merges[0]
    dist_1_merge.to_csv(data_dir + 'processed/' + district_1 + '_mapped.csv')

    #dist 2
    dist_2_merge = merges[1]
    dist_2_merge.to_csv(data_dir + 'processed/' + district_2 + '_mapped.csv')

if __name__ == '__main__':
    main()
