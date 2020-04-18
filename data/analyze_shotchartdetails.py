import os
from os import path
import json

import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
from tqdm import tqdm

### IMPROVE  ZONES
def zone_sort(df):
    """
    SORT COORDS INTO ZONES
    AND TALLY MADE/MISSED TO 
    CALC ACC PER ZONE
    """
    low_paint = {'x_loc': range(-80,81), 'y_loc': range(-53, 61), 'name': 'Low Paint'} # 0
    high_paint = {'x_loc': range(-80,81), 'y_loc': range(60, 141), 'name': 'High Paint'} # 1
    straight_mid_range = {'x_loc': range(-80,81), 'y_loc': range(140, 231), 'name': 'Straight-on Mid-range'} # 2
    straight_threes = {'x_loc': range(-80,81), 'y_loc': range(231, 418), 'name': 'Straight-on 3'} # 3
    r_wing_mid_range = {'x_loc': range(-190, -81), 'y_loc': range(50, 201), 'name': 'Right-wing Mid-range'} # 4
    l_wing_mid_range = {'x_loc': range(80,191), 'y_loc': range(50, 201), 'name': 'Left-wing Mid-range'} # 5
    r_baseline_mid_range = {'x_loc': range(-210, -81), 'y_loc': range(-53, 51), 'name': 'Right Baseline Mid-range'} # 6
    l_baseline_mid_range = {'x_loc': range(80, 211), 'y_loc': range(-53, 51), 'name': 'Left Baseline Mid-range'} # 7
    r_corner_threes = {'x_loc': range(-250, -211), 'y_loc': range(-53, 51), 'name': 'Right Corner 3'} # 8
    l_corner_threes = {'x_loc': range(210, 251), 'y_loc': range(-53, 51), 'name': 'Left Corner 3'} # 9
    r_wing_threes = {'x_loc': range(-250, -81), 'y_loc': range(50, 418), 'name': 'Right-wing 3'} # 10
    l_wing_threes = {'x_loc': range(80, 251), 'y_loc': range(50, 418), 'name': 'Left-wing 3'} # 11
    shot_zones = [low_paint, high_paint, straight_mid_range, straight_threes, 
        r_wing_mid_range, l_wing_mid_range, r_baseline_mid_range, l_baseline_mid_range,
        r_corner_threes, l_corner_threes, r_wing_threes, l_wing_threes]
    
    new_df_dict = {}
    for index, row in df.iterrows(): 
        for i in shot_zones:
            if row['LOC_X'] in i['x_loc'] and row['LOC_Y'] in i['y_loc']:
                try:
                    new_df_dict[shot_zones.index(i)] = {
                        'ZONE': shot_zones.index(i),
                        'ZONE_NAME': i['name'],
                        'LOC_X': f'{i["x_loc"][0]}/{i["x_loc"][-1]}',
                        'LOC_Y': f'{i["y_loc"][0]}/{i["y_loc"][-1]}',
                        'SHOT_ATTEMPTED_FLAG': int(new_df_dict[shot_zones.index(i)]['SHOT_ATTEMPTED_FLAG']) + int(row['SHOT_ATTEMPTED_FLAG']),
                        'SHOT_MADE_FLAG': int(new_df_dict[shot_zones.index(i)]['SHOT_MADE_FLAG']) + int(row['SHOT_MADE_FLAG']),
                        'SHOT_MISSED': int(new_df_dict[shot_zones.index(i)]['SHOT_ATTEMPTED_FLAG']) - int(new_df_dict[shot_zones.index(i)]['SHOT_MADE_FLAG'])
                    }
                    break
                except KeyError: #inital entry
                    new_df_dict[shot_zones.index(i)] = {
                        'ZONE': shot_zones.index(i),
                        'ZONE_NAME': i['name'],
                        'LOC_X': f'{i["x_loc"][0]}/{i["x_loc"][-1]}',
                        'LOC_Y': f'{i["y_loc"][0]}/{i["y_loc"][-1]}',
                        'SHOT_ATTEMPTED_FLAG': 1,
                        'SHOT_MADE_FLAG': int(row['SHOT_MADE_FLAG']),   
                        'SHOT_MISSED': 1 - int(row['SHOT_MADE_FLAG']) 
                    }
                    break
    fin_list = []
    for i in new_df_dict.values():
        i['ZONE_ACCURACY'] = i['SHOT_MADE_FLAG']/i['SHOT_ATTEMPTED_FLAG']
        fin_list.append(i)

    zone_df = pd.DataFrame(fin_list)
    zone_df = zone_df.sort_values('ZONE')
    return zone_df

def clean_df_per_hex(df, zone_df):
    """
    return DF with
    PER SHOT
    PLAYER_ID,
    LOC_X, LOC_Y,
    MADE/ATTEMPT
    and per zone accuracy
    """
    def return_range(stored_str): # clean ranges stored as str in zone_df
        min_x = int(stored_str.split('/')[0])
        max_x = int(stored_str.split('/')[1])
        return range(min_x, max_x)

    final_df_dict = {}
    df.to_csv('df.csv')
    zone_df.to_csv('zone_df.csv')
    for index, row in df.iterrows():
        for i, r in zone_df.iterrows():
            zone_df_LOC_X = return_range(r['LOC_X'])
            zone_df_LOC_Y = return_range(r['LOC_Y'])         
            if row['LOC_X'] in zone_df_LOC_X and row['LOC_Y'] in zone_df_LOC_Y:
                final_df_dict[f"{row['LOC_X']}, {row['LOC_Y']}"] = {
                    'PLAYER_ID': row['PLAYER_ID'],
                    'SHOT_DISTANCE': row['SHOT_DISTANCE'],
                    'LOC_X': row['LOC_X'],
                    'LOC_Y': row['LOC_Y'],
                    'SHOT_ATTEMPTED_FLAG': row['SHOT_ATTEMPTED_FLAG'],
                    'SHOT_MADE_FLAG': row['SHOT_MADE_FLAG'],
                    'ZONE_NAME': r['ZONE_NAME'],
                    'ACCURACY_FROM_ZONE': r['ZONE_ACCURACY'],
                    'TOTALS': str(r["SHOT_MADE_FLAG"]) + '/' + str(r['SHOT_ATTEMPTED_FLAG'])
                }
                break

    fin_df = pd.DataFrame(final_df_dict.values())
    return fin_df

#C:\Users\wilso\Desktop\nba_shotcharts\data\json_data\season_shotcharts\2010-11
def format_json(data):
    data = pd.DataFrame.from_dict(json_normalize(data), orient='columns')
    data.drop(data.columns[[0]], axis=1, inplace=True)
    data.columns = [
            'PLAYER_ID', 
            'SHOT_DISTANCE', 
            'LOC_X', 
            'LOC_Y', 
            'SHOT_ATTEMPTED_FLAG', 
            'SHOT_MADE_FLAG',
            'SEASON']
    return data

def write_json(df, season):
    df.to_csv('df-fail.csv')
    df['SEASON'] = season
    data = [{'model': 'app.Shot_data', 'fields': {j: row[j] for j in df.columns}} for i, row in df.iterrows()]
    finalpath = f'json_data/season_shotcharts/cleaned_data/'
    with open(finalpath + f'{df["PLAYER_ID"][0]}-{season}.json', 'w') as f:
        json.dump(data, f)

def main(season):
    no_data_files = [season]
    files =  os.listdir(f'json_data/season_shotcharts/{season}/')
    for each in tqdm(files):
        path = f'json_data/season_shotcharts/{season}/{each}'
        with open(path, 'r') as f:
            data = json.load(f)
            if len(data) > 0:
                df = format_json(data)
                zone_df = zone_sort(df)
                fin = clean_df_per_hex(df, zone_df)
                write_json(fin, season)
            else:
                no_data_files.append(f'{each}') # empty downloaded json returned from nba

if __name__ == "__main__": 
    count = 19
    pbar = tqdm(total = count+1)
    while count < 20:
        season = str(f'20{count}-{count+1}')
        main(season)
        pbar.update(1)
        count += 1