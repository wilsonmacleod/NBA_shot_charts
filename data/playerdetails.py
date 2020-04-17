import json
import time
import os
from os import path

import requests
import pandas as pd
from tqdm import tqdm

from urls import Urls

def get(season):
    url = Urls.player_details(season)
    headers = Urls.headers()
    response = requests.get(url=url, headers=headers).json()
    column_headers = response['resultSets'][0]['headers']
    shots = response['resultSets'][0]['rowSet']
    df = pd.DataFrame(shots, columns=column_headers)
    df.drop(df.columns[5:], axis=1, inplace=True)
    df['SEASON'] = season
    return df

def main(season):
    basepath = path.dirname(__file__)
    finalpath = basepath + '/json_data/player_details/'
    df = get(season)
    data = [{'model': 'app.Player_id', 'fields': {j: row[j] for j in df.columns}} for i, row in df.iterrows()]
    with open(f'{finalpath}/{season}.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__": 
    count = 10
    pbar = tqdm(total = count+1)
    while count < 20:
        season = str(f'20{count}-{count+1}')
        main(season)
        count += 1
        pbar.update(1)
        time.sleep(5)


    