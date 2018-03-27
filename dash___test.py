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
n_btns = 4
max_len = 10

pwm_values = {
    str(i): deque([0]*max_len, maxlen=max_len) for i in range(n_sliders)}
d_values = {
    str(i): 0 for i in range(n_btns)}
minus_clicks = {
    str(i): 0 for i in range(n_sliders)}
plus_clicks = {
    str(i): 0 for i in range(n_sliders)}
timestamp = {
    str(i): deque(range(max_len), maxlen=max_len) for i in range(n_sliders)}
timestamp['start'] = time.time()

app = dash.Dash()


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


#    html.I(id='submit-button', n_clicks=0, className='fa fa-send'),


lbls = [[html.Label('0', id='pwm-label-{}'.format(i))
         ] for i in range(n_sliders)]

btns = [[
        html.Button(id='--btn-{}'.format(i), children='-'),
        html.Button(id='+-btn-{}'.format(i), children='+')
        ] for i in range(n_sliders)]

sldrs = [[
        dcc.Slider(id='pwm-slider-{}'.format(i),
                   min=0,
                   max=100,
                   value=0,
                   marks={str(j): str(j) for j in range(0, 101, 10)}
                   )
        ] for i in range(n_sliders)]


sliders = flat_list(
            [[html.Div([
                html.Div(lbls[i], className="one column"),
                html.Div(btns[i], className="three columns"),
                html.Div(sldrs[i], className="eight columns"),
                ], className="row")
              ] for i in range(n_sliders)])


dlbls = [[html.Button(children='F{}'.format(i), id='d-btn-{}'.format(i))
          ] for i in range(n_btns)]

dsldrs = [[dcc.Slider(id='d-slider-{}'.format(i),
                      min=0,
                      max=1,
                      value=0,
                      marks={j: str(bool(j)) for j in range(2)}
                      )
           ] for i in range(n_btns)]

dsliders = flat_list(
            [[html.Div([
                html.Div(dlbls[i], className="six columns"),
                html.Div(dsldrs[i], className="six columns"),
                ], className="row")
              ] for i in range(n_btns)])


userctr = [html.Div([
            html.Div(sliders, className='eight columns'),
            html.Div(dsliders, className='three columns')
        ], className='row')]


app.layout = html.Div(flat_list([
    [dcc.Graph(id='live-graph', animate=True),
     dcc.Interval(id='graph-update', interval=1000)],
    userctr
]))


for i in range(n_sliders):
    @app.callback(Output('pwm-label-{}'.format(i), 'children'),
                  [Input('pwm-slider-{}'.format(i), 'value')])
    def slider_callback(val, idx=i):
        global pwm_values
        if pwm_values[str(idx)][-1] != val:
            global timestamp
            pwm_values[str(idx)].append(val)
            timestamp[str(idx)].append(time.time()-timestamp['start'])
        return str(val)

    @app.callback(Output('pwm-slider-{}'.format(i), 'value'),
                  [Input('--btn-{}'.format(i), 'n_clicks'),
                   Input('+-btn-{}'.format(i), 'n_clicks')])
    def slider_update(minus, plus, idx=i):
        global pwm_values
        global minus_clicks
        global plus_clicks
        val = pwm_values[str(idx)][-1]
        if minus > minus_clicks[str(idx)]:
            minus_clicks[str(idx)] += 1
            if val - 1 >= 0:
                val -= 1
        if plus > plus_clicks[str(idx)]:
            plus_clicks[str(idx)] += 1
            if val + 1 <= 100:
                val += 1
        return val


for i in range(n_btns):
    @app.callback(Output('d-slider-{}'.format(i), 'value'),
                  [Input('d-btn-{}'.format(i), 'n_clicks')])
    def d_btn_callback(event, idx=i):
        global d_values
        if event:
            state = event % 2
        else:
            state = 0
        d_values[str(idx)] = state
        return state







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
