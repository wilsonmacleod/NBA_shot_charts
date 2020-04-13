import os
from os import path
import json
import time

import requests
import pandas as pd
from tqdm import tqdm

from urls import Urls

def get_shotchart_data(player_id, season):
    url = Urls.shotchart_data(player_id, season)
    headers = Urls.headers()
    response = requests.get(url=url, headers=headers).json()
    column_headers = response['resultSets'][0]['headers']
    shots = response['resultSets'][0]['rowSet']
    shot_df = pd.DataFrame(shots, columns=column_headers)
    shot_df.drop(shot_df.columns[[0,1,2,5,6,8,9,10,11,12,13,14,15,16, 21]], axis=1, inplace=True)
    return shot_df

def parse_player_ids(season):
    basepath = path.dirname(__file__)
    finalpath = basepath + f'/data/player_details/{season}.json'
    with open(finalpath, 'r') as f:
        data = json.load(f)
    id_list = []
    for each in tqdm(data):
        id_list.append(each['id'])
    return id_list

def main(season):
    basepath = path.dirname(__file__)
    finalpath = basepath + f'/data/season_shotcharts/{season}/'
    count = 0
    for each in tqdm(parse_player_ids(season)):
        shot_df = get_shotchart_data(each, season)
        shot_df.to_json(finalpath + f'{each}.json')
        time.sleep(5)

if __name__ == "__main__": 
    #player_id=str(203932) ## AG
    season='2010-11'
    main(season)