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


# -----------------------------------------------------------------------------
# Initialize
# -----------------------------------------------------------------------------


n_sliders = 6
n_btns = 4
max_len = 10

pwm_values = {
    str(i): deque([0]*max_len, maxlen=max_len) for i in range(n_sliders)}

ref_values = {
    str(i): deque([0]*max_len, maxlen=max_len) for i in range(n_sliders)}

mes_values = {
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


# -----------------------------------------------------------------------------
# PWM CONTROL - Html layout
# -----------------------------------------------------------------------------

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
                html.Div(btns[i], className="four columns"),
                html.Div(sldrs[i], className="seven columns"),
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
                html.Div(dsldrs[i], className="six columns")
                ], className="row")
              ] for i in range(n_btns)])


pwmctr = [html.Div([
            html.Div(sliders, className='eight columns'),
            html.Div(dsliders, className='three columns')
        ], className='row')]

# -----------------------------------------------------------------------------
# Pattern CONTROL - Html tab Layout
# -----------------------------------------------------------------------------

PATT3_0 = [[0.0, 0.99, 0.97, 0.0, 0.25, 0.71, False, True, True, False, 5.0],
           [0.0, 0.99, 0.97, 0.0, 0.25, 0.71, True, True, True, True, 2.0],
           [0.0, 0.99, 0.97, 0.0, 0.25, 0.71, True, False, False, True, 1.0],
           [0.77, 0.0, 0.0, 0.93, 0.70, 0.25, True, False, False, True, 5.0],
           [0.77, 0.0, 0.0, 0.93, 0.70, 0.25, True, True, True, True, 2.0],
           [0.77, 0.0, 0.0, 0.93, 0.70, 0.25, False, True, True, False, 1.0]]

PATT2_6 = [[0.0, 0.95, 0.91, 0.0, 0.25, 0.71, False, True, True, False, 5.0],
           [0.0, 0.95, 0.91, 0.0, 0.25, 0.71, True, True, True, True, 2.0],
           [0.0, 0.95, 0.91, 0.0, 0.25, 0.71, True, False, False, True, 1.0],
           [0.7, 0.0, 0.0, 0.92, 0.76, 0.25, True, False, False, True, 5.0],
           [0.7, 0.0, 0.0, 0.92, 0.76, 0.25, True, True, True, True, 2.0],
           [0.7, 0.0, 0.0, 0.92, 0.76, 0.25, False, True, True, False, 1.0]]


def generate_pattern(t_move, t_fix, t_defix, p0, p1, p2, p3, p4, p41, p5, p51):
    pattern = [[0.0, p1, p2, 0.0, p41, p5, False, True, True, False, t_move],
               [0.0, p1, p2, 0.0, p41, p5, True, True, True, True, t_fix],
               [0.0, p1, p2, 0.0, p41, p5, True, False, False, True, t_defix],
               [p0, 0.0, 0.0, p3, p4, p51, True, False, False, True, t_move],
               [p0, 0.0, 0.0, p3, p4, p51, True, True, True, True, t_fix],
               [p0, 0.0, 0.0, p3, p4, p51, False, True, True, False, t_defix]]
    return pattern


pttrnctr_dic = {'v3.0': {'data': PATT3_0,
                         'ptrn-t-move': PATT3_0[0][-1],
                         'ptrn-t-fix': PATT3_0[1][-1],
                         'ptrn-t-defix': PATT3_0[2][-1],
                         'ptrn-p-0': PATT3_0[3][0],
                         'ptrn-p-1': PATT3_0[0][1],
                         'ptrn-p-2': PATT3_0[0][2],
                         'ptrn-p-3': PATT3_0[3][3],
                         'ptrn-p-4': PATT3_0[3][4],
                         'ptrn-p-41': PATT3_0[0][4],
                         'ptrn-p-5': PATT3_0[0][5],
                         'ptrn-p-51': PATT3_0[3][5]},
                'v2.6': {'data': PATT2_6,
                         't_move': PATT2_6[0][-1],
                         't_fix': PATT2_6[1][-1],
                         't_defix': PATT2_6[2][-1],
                         'p_0': PATT2_6[3][0],
                         'p_1': PATT2_6[0][1],
                         'p_2': PATT2_6[0][2],
                         'p_3': PATT2_6[3][3],
                         'p_4': PATT2_6[3][4],
                         'p_41': PATT2_6[0][4],
                         'p_5': PATT2_6[0][5],
                         'p_51': PATT2_6[3][5]}
                }

pttrnctr = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(id='ptrn-graph')
            ], className='row')
        ], className='eight columns'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div(['p0: \t\t', dcc.Input(id='ptrn-p-0',
                                                    type='text',
                                                    style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['p1: \t\t', dcc.Input(id='ptrn-p-1',
                                                    type='text',
                                                    style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['p2: \t\t', dcc.Input(id='ptrn-p-2',
                                                    type='text',
                                                    style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['p3: \t\t', dcc.Input(id='ptrn-p-3',
                                                    type='text',
                                                    style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['p4: \t\t', dcc.Input(id='ptrn-p-4',
                                                    type='text',
                                                    style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['p5: \t\t', dcc.Input(id='ptrn-p-5',
                                                    type='text',
                                                    style={'width': 60})])
                    ], className='row')
            ], className='six columns'),
            html.Div([
                html.Div([
                    html.Div(['p41: \t\t', dcc.Input(id='ptrn-p-41',
                                                     type='text',
                                                     style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['p51: \t\t', dcc.Input(id='ptrn-p-51',
                                                     type='text',
                                                     style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['t_m: \t\t', dcc.Input(id='ptrn-t-move',
                                                     type='text',
                                                     style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['t_a: \t\t', dcc.Input(id='ptrn-t-fix',
                                                     type='text',
                                                     style={'width': 60})])
                    ], className='row'),
                html.Div([
                    html.Div(['t_d: \t\t', dcc.Input(id='ptrn-t-defix',
                                                     type='text',
                                                     style={'width': 60})])
                    ], className='row')
            ], className='six columns'),
        ], className='row')
    ], className='four columns')
], className='row')


# -----------------------------------------------------------------------------
# Pressure CONTROL - Html Tab Layout
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Overall - Html Layout
# -----------------------------------------------------------------------------

app.layout = html.Div(flat_list([
    [html.Div([
        html.Div(dcc.Graph(id='pressure-ref-graph', animate=True),
                 className="six columns"),
        html.Div(dcc.Graph(id='live-graph', animate=True),
                 className="six columns")
        ], className='row'),
     dcc.Interval(id='graph-update', interval=1000)],
    pwmctr,
    [pttrnctr]
]))


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


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
