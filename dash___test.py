# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 20:08:18 2018

@author: ls
"""
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import deque


def flat_list(l):
    return [item for sublist in l for item in sublist]

n_sliders = 6
max_len = 10

pwm_values = {str(i): deque([0]*max_len, maxlen=max_len) for i in range(n_sliders)}


app = dash.Dash()


sliders = [dcc.Slider(
    id='pwm-slider-{}'.format(i),
    min=0,
    max=100,
    value=0,
    marks={str(j): str(j) for j in range(0, 101, 10)}
) for i in range(n_sliders)]


app.layout = html.Div(flat_list([
    dcc.Graph(id='graph-with-slider'),
    sliders
]))


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers+lines',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()