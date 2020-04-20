import json
import time
import os
from os import path

import requests
import pandas as pd
from tqdm import tqdm

from urls import Urls

#['GRID_TYPE' 'GAME_ID' 'GAME_EVENT_ID' 'PLAYER_ID' 'PLAYER_NAME' 'TEAM_ID'
# 'TEAM_NAME' 'PERIOD' 'MINUTES_REMAINING' 'SECONDS_REMAINING' 'EVENT_TYPE'
# 'ACTION_TYPE' 'SHOT_TYPE' 'SHOT_ZONE_BASIC' 'SHOT_ZONE_AREA'
# 'SHOT_ZONE_RANGE' 'SHOT_DISTANCE' 'LOC_X' 'LOC_Y' 'SHOT_ATTEMPTED_FLAG'
# 'SHOT_MADE_FLAG' 'GAME_DATE' 'HTM' 'VTM']

def get_shotchart_data(player_id, season):
    url = Urls.shotchart_data(player_id, season)
    headers = Urls.headers()
    response = requests.get(url=url, headers=headers).json()
    column_headers = response['resultSets'][0]['headers']
    shots = response['resultSets'][0]['rowSet']
    shot_df = pd.DataFrame(shots, columns=column_headers)
    shot_df.drop(shot_df.columns[[0,1,2,4,5,6,7,8,9,10,11,12,13,14,15, 16, 21,22,23]], axis=1, inplace=True)
    shot_df['SEASON'] = season
    shot_df.to_csv('shotdetail', sep='\t', encoding='utf-8')
    return shot_df

def parse_player_ids(season):
    basepath = path.dirname(__file__)
    finalpath = basepath + f'/json_data/player_details/{season}.json'
    with open(finalpath, 'r') as f:
        data = json.load(f)
    id_list = []
    for each in tqdm(data):
        id_list.append(each['fields']['PLAYER_ID'])
    return id_list

def main(season):
    basepath = path.dirname(__file__)
    finalpath = basepath + f'/json_data/season_shotcharts/{season}/'
    for each in tqdm(parse_player_ids(season)):
            shot_df = get_shotchart_data(each, season)
            data = [{'model': 'app.Shot_data', 'fields': {j: row[j] for j in shot_df.columns}} for i, row in shot_df.iterrows()]
            with open(finalpath + f'{each}.json', 'w') as f:
                json.dump(data, f)
            time.sleep(5)

if __name__ == "__main__": 
    count = 10
    pbar = tqdm(total = count+1)
    while count < 20:
        try:
            season = str(f'20{count}-{count+1}')
            main(season)
            pbar.update(1)
            time.sleep(5)   
            count += 1
        except:
            time.sleep(300)
            count = count
            continue