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
    l_wing_mid_range = {'x_loc': range(-200, -81), 'y_loc': range(50, 221), 'name': 'Left-wing Mid-range'} # 4
    r_wing_mid_range = {'x_loc': range(80,201), 'y_loc': range(50, 221), 'name': 'Right-wing Mid-range'} # 5
    l_wing_threes = {'x_loc': range(-250, -81), 'y_loc': range(51, 418), 'name': 'Left-wing 3'} # 6
    r_wing_threes = {'x_loc': range(80, 251), 'y_loc': range(51, 418), 'name': 'Right-wing 3 '} # 7
    l_baseline_mid_range = {'x_loc': range(-210, -81), 'y_loc': range(-53, 51), 'name': 'Left Baseline Mid-range'} # 8
    r_baseline_mid_range = {'x_loc': range(80, 211), 'y_loc': range(-53, 51), 'name': 'Right Baseline Mid-range'} # 9
    l_corner_threes = {'x_loc': range(-250, -211), 'y_loc': range(-53, 51), 'name': 'Left Corner 3'} # 10
    r_corner_threes = {'x_loc': range(210, 251), 'y_loc': range(-53, 51), 'name': 'Right Corner 3'} # 11
    shot_zones = [low_paint, high_paint, straight_mid_range, straight_threes, l_wing_mid_range,
                  r_wing_mid_range, l_wing_threes, r_wing_threes, l_baseline_mid_range,
                  r_baseline_mid_range, l_corner_threes, r_corner_threes]
    
    new_df_dict = {}
    for index, row in df.iterrows(): 
        for i in shot_zones:
            if row['LOC_X'] in i['x_loc'] and row['LOC_Y'] in i['y_loc']:
                try:
                    new_df_dict[shot_zones.index(i)] = {
                        'ZONE': shot_zones.index(i),
                        'ZONE_NAME': i['name'],
                        'LOC_X': i['x_loc'],
                        'LOC_Y': i['y_loc'],
                        'SHOT_ATTEMPTED_FLAG': int(new_df_dict[shot_zones.index(i)]['SHOT_ATTEMPTED_FLAG']) + int(row['SHOT_ATTEMPTED_FLAG']),
                        'SHOT_MADE_FLAG': int(new_df_dict[shot_zones.index(i)]['SHOT_MADE_FLAG']) + int(row['SHOT_MADE_FLAG']),
                        'SHOT_MISSED': int(new_df_dict[shot_zones.index(i)]['SHOT_ATTEMPTED_FLAG']) - int(new_df_dict[shot_zones.index(i)]['SHOT_MADE_FLAG'])
                    }
                except KeyError: #inital entry
                    new_df_dict[shot_zones.index(i)] = {
                        'ZONE': shot_zones.index(i),
                        'ZONE_NAME': i['name'],
                        'LOC_X': i['x_loc'],
                        'LOC_Y': i['y_loc'],
                        'SHOT_ATTEMPTED_FLAG': 1,
                        'SHOT_MADE_FLAG': int(row['SHOT_MADE_FLAG']),   
                        'SHOT_MISSED': 1 - int(row['SHOT_MADE_FLAG']) 
                    }

    fin_list = []
    for i in new_df_dict.values():
        i['ZONE_ACCURACY'] = i['SHOT_MADE_FLAG']/i['SHOT_ATTEMPTED_FLAG']
        fin_list.append(i)

    zone_df = pd.DataFrame(fin_list)
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
    final_df_dict = {}
    for index, row in df.iterrows():
        for i, r in zone_df.iterrows():
            if row['LOC_X'] in r['LOC_X'] and row['LOC_Y'] in r['LOC_Y']:
                try:
                    final_df_dict[f"{row['LOC_X']}, {row['LOC_Y']}"] = {
                        'PLAYER_ID': row['PLAYER_ID'],
                        'SHOT_DISTANCE': row['SHOT_DISTANCE'],
                        'LOC_X': row['LOC_X'],
                        'LOC_Y': row['LOC_Y'],
                        'SHOT_ATTEMPTED_FLAG': row['SHOT_ATTEMPTED_FLAG'],
                        'SHOT_MADE_FLAG': row['SHOT_MADE_FLAG'],
                        'ZONE_NAME': r['ZONE_NAME'],
                        'ACCURACY_FROM_ZONE': r['ZONE_ACCURACY']
                    }
                except KeyError:
                        final_df_dict[f"{row['LOC_X']}, {row['LOC_Y']}"] = {
                        'PLAYER_ID': row['PLAYER_ID'],
                        'SHOT_DISTANCE': row['SHOT_DISTANCE'],          
                        'LOC_X': row['LOC_X'],
                        'LOC_Y': row['LOC_Y'],
                        'SHOT_ATTEMPTED_FLAG': row['SHOT_ATTEMPTED_FLAG'],
                        'SHOT_MADE_FLAG': row['SHOT_MADE_FLAG'],
                        'ZONE_NAME': r['ZONE_NAME'],
                        'ACCURACY_FROM_ZONE': r['ZONE_ACCURACY']
                    }                        
    final_df_list = []
    for each in final_df_dict.values():
        final_df_list.append(each)

    fin_df = pd.DataFrame(final_df_list)
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
    df['SEASON'] = season
    data = [{'model': 'app.Shot_data', 'fields': {j: row[j] for j in df.columns}} for i, row in df.iterrows()]
    finalpath = f'json_data/season_shotcharts/cleaned_data/'
    with open(finalpath + f'{df.PLAYER_ID[0]}-{season}.json', 'w') as f:
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
                no_data_files.append(f'{each}')
    print(no_data_files)

if __name__ == "__main__": 
    count = 10
    pbar = tqdm(total = count+1)
    while count < 20:
        season = str(f'20{count}-{count+1}')
        main(season)
        pbar.update(1)
        count += 1