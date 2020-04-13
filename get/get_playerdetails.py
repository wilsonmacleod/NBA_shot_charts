import os
from os import path
import json
import time

import requests
import pandas as pd
from tqdm import tqdm

def get(season):
    url = (
        "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&"
        "DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&"
        "LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&"
        "PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&"
        f"PlusMinus=N&Rank=N&Season={season}&SeasonSegment=&SeasonType=Regular+Season&"
        "ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
        )
    headers = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://stats.nba.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }
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


    