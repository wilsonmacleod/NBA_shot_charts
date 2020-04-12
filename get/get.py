import requests
import pandas as pd
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

#player_id={203932}
url = "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2019-20&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight="
    #"https://stats.nba.com/stats/shotchartdetail?"
    #f"SeasonType=&TeamID=&PlayerID={player_id}&GameID=&Outcome=&Location=&Month=&SeasonSegment=&DateFrom=&DateTo=&"
    #"OpponentTeamID=&VsConference=&VsDivision=&Position=&RookieYear=&GameSegment=&Period=0&LastNGames=&ContextMeasure=&"
    #"PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2019-20&"
    #"PlayerPosition=")
response = requests.get(url=url, headers=headers)
print(response)

response = response.json()
column_headers = response['resultSets'][0]['headers']

shots = response['resultSets'][0]['rowSet']

shot_df = pd.DataFrame(shots, columns=column_headers)
print(shot_df)
shot_df.to_csv('output.csv', sep='\t', encoding='utf-8')