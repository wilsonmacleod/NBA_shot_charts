import os
from os import path
import json
import time

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
    return df

def main(season):
    basepath = path.dirname(__file__)
    finalpath = basepath + '/data/player_details/'
    df = get(season)
    data = [{'id': row['PLAYER_ID'], 'metadata': {j: row[j] for j in df.columns if j != "PLAYER_ID"}} for i, row in df.iterrows()]
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


    