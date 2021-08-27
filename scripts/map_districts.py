import pandas as pd
import numpy as np

def create_map(district_1, district_2, dir):
    #load data
    district_data = pd.read_csv(dir + 'data/processed/district_data.csv', low_memory=False)
    district_data['nces_schoolID'] = district_data['nces_schoolID'].astype(str)
    mapping = pd.read_csv(dir + 'data/processed/mapping.csv')
    dist_1_og = pd.read_csv(dir + 'data/processed/' + district_1 + '.csv')
    dist_2_og = pd.read_csv(dir + 'data/processed/' + district_2 + '.csv')

    #run functions to do the mapping
    state_1, state_2 = get_states(district_data, district_1, district_2)
    maps = create_maps(mapping, state_1, state_2)
    dists = find_unmatched(dist_1_og, maps[0], dist_2_og, maps[1])
    merges = map(dists[0], maps[0], dists[1], maps[1], district_1, district_2)
    create_csv(merges, dir, district_1, district_2)
    sums = get_sums(merges[0], merges[1])
    return(sums)

def get_states(district_data, district_1, district_2):
    state_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'State Name [District] 2018-19_x'].iloc[0].capitalize()
    state_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'State Name [District] 2018-19_x'].iloc[0].capitalize()
    
    return state_1, state_2

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

def map(dist_1, dist_1_map, dist_2, dist_2_map, district_1, district_2):
    dist_1_merge = dist_1.merge(dist_1_map, how='left', on='Code')
    dist_2_merge = dist_2.merge(dist_2_map, how='left', on='Code')
    
    #add in district labels
    dist_1_merge['district'] = district_1
    dist_2_merge['district'] = district_2
    
    return [dist_1_merge, dist_2_merge]

def create_csv(merges, dir, district_1, district_2):
    #dist 1
    dist_1_merge = merges[0]
    dist_1_merge.to_csv(dir + 'data/processed/' + district_1 + '_mapped.csv')

    #dist 2
    dist_2_merge = merges[1]
    dist_2_merge.to_csv(dir + 'data/processed/' + district_2 + '_mapped.csv')

def get_sums(dist_1_merge, dist_2_merge):
    dist_1_sum = dist_1_merge['Transactions'].sum()
    dist_2_sum = dist_2_merge['Transactions'].sum()

    return [dist_1_sum, dist_2_sum]

if __name__ == '__main__':
    create_map()
