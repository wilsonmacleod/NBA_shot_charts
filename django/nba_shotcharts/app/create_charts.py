import numpy as np
import pandas as pd 
from plotly.offline import plot
import plotly.graph_objs as go

from .models import Season, Player_id, Shot_data

def pull_from_db(player_id, season):
    player = Player_id.objects.filter(SEASON=season).filter(PLAYER_ID=player_id).first()
    raw_data = Shot_data.objects.filter(SEASON=season).filter(PLAYER_ID=player_id).all()
    return player, raw_data

def format_to_df(raw_data):
    df = pd.DataFrame(list(raw_data.values()), columns=[
        'django_id', 
        'PLAYER_ID', 
        'SHOT_DISTANCE',
        'LOC_X', 
        'LOC_Y',
        'SHOT_ATTEMPTED_FLAG',
        'SHOT_MADE_FLAG',
        'SEASON'])
    df.drop(df.columns[[0,7]], axis=1, inplace=True)
    df.to_csv('out.csv', index=False) 
    return df

def draw_plotly_court(fig, fig_width=600, margins=10):
        
    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[-250 - margins, 250 + margins])
    fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

    threept_break_y = 89.47765084
    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=2),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=2),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=2),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=2),
                # fillcolor='#dddddd',
                layer='below'
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=2),
                layer='below'
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=2),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=2),
            ),
            dict(
                type="line", x0=-35, y0=-12.5, x1=35, y1=-12.5,
                line=dict(color="black", width=2),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=2), layer='below'),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=2), layer='below'),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=2), layer='below'
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=2), layer='below'
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=2), layer='below'),

        ]
    )

def final_fig_gen(df):
    
    fig = go.Figure()
    draw_plotly_court(fig)

    made_x = df[df['SHOT_MADE_FLAG'] == 1]['LOC_X']
    made_y = df[df['SHOT_MADE_FLAG'] == 1]['LOC_Y']

    made = go.Scatter(x=made_x, y=made_y,
                        mode='markers', name='Made',
                        opacity=0.7, marker_color='#6395E5',
                        marker=dict(
                            size=10,
                            line=dict(width=2, color='black'), 
                            symbol='hexagon'),
                            text='',
                            hoverinfo=None #'text'
                        )      
    fig.add_trace(made)

    missed_x = df[df['SHOT_MADE_FLAG'] == 0]['LOC_X']
    missed_y = df[df['SHOT_MADE_FLAG'] == 0]['LOC_Y']

    missed = go.Scatter(x=missed_x, y=missed_y,
                        mode='markers', name='Missed',
                        opacity=0.7, marker_color='#C8B51B',
                        marker=dict(
                            size=10,
                            line=dict(width=2, color='black'), 
                            symbol='hexagon'),
                            text='',
                            hoverinfo=None #'text'
                        )      
    fig.add_trace(missed)

    plt_div = plot(fig, output_type='div', include_plotlyjs=False, link_text="", config=dict(displayModeBar=False))
    return plt_div

class Return_Data_and_Charts():
    def main(player_id, season):
        player, raw_data = pull_from_db(player_id, season)
        df = format_to_df(raw_data)
        return player, final_fig_gen(df)
        


# low paint [width(x) -80 to +80, height(y) is +60 to -52.5]
# high paint [width(x)  -80 to +80, height(y) is +140 to  +60]
# straight mid range [width(x) -80 to +80, height(y) is +230 to  +140]
# straight threes [width(x) -80 to +80, height(y) is +417 to  +230]
# L wing mid range [width(x) -250 to -80, height(y) is +225 to  +50]
# R wing mid range [width(x) +250 to +80, height(y) is +225 to  +50]
# L wing threes [width(x) -250 to -80, height(y) is +417 to  +175]
# R wing threes [width(x) +250 to +80, height(y) is +417 to  +175]
# L baseline mid range [width(x) -210 to -80, height(y) is +50 to  -52.5]
# R baseline mid range [width(x) 210 to 80, height(y) is +50 to  -52.5]
# L corner threes [width(x) -250 to -210, height(y) is +50 to  -52.5]
# R corner threes [width(x) 250 to 210, height(y) is +50 to  -52.5]

