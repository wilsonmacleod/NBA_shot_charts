import numpy as np
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go

from app.models import Player_id, Shot_data
from .draw_court import draw_plotly_court


def pull_from_db(player_id, season):
    player = Player_id.objects.filter(
        SEASON=season).filter(PLAYER_ID=player_id).first()
    player.AGE = player.AGE[0:2]
    raw_data = Shot_data.objects.filter(
        SEASON=season).filter(PLAYER_ID=player_id).all()
    return player, raw_data


def format_to_df(raw_data):
    clean_list = []
    for u in raw_data:
        attempts = int(u.TOTALS.split('/')[1])
        clean_list.append({
            'django_id': u.id,
            'PLAYER_ID': u.PLAYER_ID,
            'SHOT_DISTANCE': u.SHOT_DISTANCE,
            'LOC_X': u.LOC_X,
            'LOC_Y': u.LOC_Y,
            'SHOT_ATTEMPTED_FLAG': u.SHOT_ATTEMPTED_FLAG,
            'SHOT_MADE_FLAG': u.SHOT_MADE_FLAG,
            'ZONE_NAME': u.ZONE_NAME,
            'ACCURACY_FROM_ZONE': float(u.ACCURACY_FROM_ZONE),
            'ATTEMPTS': attempts,
            'TOTALS': u.TOTALS,
            'SEASON': u.SEASON
        })
    df = pd.DataFrame(clean_list)
    df.drop(df.columns[[0, 11]], axis=1, inplace=True)
    return df


def df_to_presentation(df):  # side data
    y = 0
    li = list(df.ZONE_NAME.unique())
    d = {i: 0 for i in li}
    for i, r in df.iterrows():
        x = int(r['TOTALS'].split('/')[1])
        if x > y:
            y = x
            row = r['ZONE_NAME']
    return_obj = {}
    return_obj['most_attempted_zone'] = f'{row} ({y} FGA.)'
    return_obj['highest_accuracy_zone'] = f'{df.iloc[df["ACCURACY_FROM_ZONE"].idxmax()]["ZONE_NAME"]} ({round(df["ACCURACY_FROM_ZONE"].max() * 100, 1)}%)'
    return_obj['average_distance'] = f'{round(df.SHOT_DISTANCE.mean(), 2)} ft.'
    return return_obj


def final_fig_gen(df, chart_type):
    fig = go.Figure()
    draw_plotly_court(fig)

    x = df['LOC_X']
    y = df['LOC_Y']
    if chart_type == 'default':
        color = df['ATTEMPTS']
        marker_cmin = df['ATTEMPTS'].min()
        marker_cmax = df['ATTEMPTS'].max()
        marker_cmean = df['ATTEMPTS'].mean()
        title_text = "<B>Attempts</B>"
    else:
        color = df['ACCURACY_FROM_ZONE'] * 100
        marker_cmin = df['ACCURACY_FROM_ZONE'].min() * 100
        marker_cmax = df['ACCURACY_FROM_ZONE'].max() * 100
        marker_cmean = df['ACCURACY_FROM_ZONE'].mean() * 100
        title_text = "<B>Accuracy</B>"

    ticktexts = ["Lowest", "Average", "Highest"]
    marker_text = [
        f'{str("Made" if df.SHOT_MADE_FLAG[i] == 1 else "Missed")} <BR>'
        f'<i>Distance: </i> {str(df.SHOT_DISTANCE[i])} ft.<BR>'
        f'<b>{str(df.ZONE_NAME[i])}</b><BR>'
        f'<i>Accuracy From Zone: </i> {str(round(df.ACCURACY_FROM_ZONE[i]*100, 1))}% ({str(df.TOTALS[i])})<BR>'
        for i in range(len(df.ACCURACY_FROM_ZONE))
    ]

    scat = go.Scatter(x=x, y=y,
                      mode='markers',
                      opacity=0.8,
                      marker=dict(
                          size=12,
                          color=color,
                          colorscale='YlOrRd',
                          colorbar=dict(
                              thickness=15,
                              x=0.82,
                              y=0.85,
                              yanchor='middle',
                              len=0.26,
                              title=dict(
                                  text=title_text,
                                  font=dict(
                                      size=14,
                                      color='#4d4d4d'
                                  ),
                              ),
                              tickvals=[marker_cmin,
                                        marker_cmean, marker_cmax],
                              ticktext=ticktexts,
                              tickfont=dict(
                                  size=11,
                                  color='black'
                              )
                          ),
                          line=dict(
                              width=1.5,
                              color='black'
                          ),
                          symbol='hexagon'
                      ),
                      text=marker_text,
                      hoverinfo='text'
                      )
    fig.add_trace(scat)
    plt_div = plot(fig, output_type='div', include_plotlyjs=False,
                   link_text="", config=dict(displayModeBar=False))
    return plt_div


def main(player_id, season, chart_type):
    player, raw_data = pull_from_db(player_id, season)
    df = format_to_df(raw_data)
    obj = df_to_presentation(df)
    return player, obj, final_fig_gen(df, chart_type)
