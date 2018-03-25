# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 20:08:18 2018

@author: ls
"""
import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import deque
import time


def flat_list(l):
    return [item for sublist in l for item in sublist]

n_sliders = 6
max_len = 10

pwm_values = {
    str(i): deque([0]*max_len, maxlen=max_len) for i in range(n_sliders)}
timestamp = {
    str(i): deque(range(max_len), maxlen=max_len) for i in range(n_sliders)}
timestamp['start'] = time.time()

app = dash.Dash()


sliders = flat_list([[html.Label('0', id='pwm-label-{}'.format(i)),
                      dcc.Slider(
                            id='pwm-slider-{}'.format(i),
                            min=0,
                            max=100,
                            value=0,
                            marks={str(j): str(j) for j in range(0, 101, 10)})
                      ] for i in range(n_sliders)])


app.layout = html.Div(flat_list([
    [dcc.Graph(id='live-graph', animate=True),
     dcc.Interval(id='graph-update', interval=1000)],
    sliders
]))


for i in range(n_sliders):
    @app.callback(Output('pwm-label-{}'.format(i), 'children'),
                  [Input('pwm-slider-{}'.format(i), 'value')])
    def slider_callback(val, idx=i):
        global timestamp
        global pwm_values
        pwm_values[str(idx)].append(val)
        timestamp[str(idx)].append(time.time()-timestamp['start'])
        return val


@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph():
    global pwm_values
    global timestamp

    traces = []
    minis = []
    maxis = []
    for key in pwm_values:
        minis.append(min(list(timestamp[key])))
        maxis.append(max(list(timestamp[key])))
        data = go.Scatter(
            x=list(timestamp[key]),
            y=list(pwm_values[key]),
            name=key,
            mode='markes+lines')
        traces.append(data)
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'range': [min(minis), max(maxis)]},
            yaxis={'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10}
        )
    }


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5000, debug=True)
