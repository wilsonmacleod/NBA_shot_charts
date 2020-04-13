import os
from os import path

import requests
import pandas as pd

def get_shotchart_data(player_id, season):

    url = (
        "https://stats.nba.com/stats/shotchartdetail?Period=0&VsConference&LeagueID=00&"
        "LastNGames=0&TeamID=0&PlayerPosition&Location&Outcome&ContextMeasure=FGA&DateFrom&StartPeriod&"
        f"DateTo&OpponentTeamID=0&ContextFilter&RangeType&Season={season}&AheadBehind&PlayerID={player_id}&"
        "EndRange&VsDivision&PointDiff&RookieYear&GameSegment&Month=0&ClutchTime&EndPeriod&"
        "SeasonType=Regular+Season&SeasonSegment&GameID")
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
    shot_df = pd.DataFrame(shots, columns=column_headers)
    return shot_df, season

def main(player_id, season):
    shot_df, season = get_shotchart_data(player_id, season)
    basepath = path.dirname(__file__)
    finalpath = basepath + '/data/season_shotcharts/'
    shot_df.to_json(f'{finalpath}{player_id}_{season}.json')
    
if __name__ == "__main__": 
    player_id=str(203932)
    season='2018-19'
    main(player_id, season)