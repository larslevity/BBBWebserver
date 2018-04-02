# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 20:08:18 2018

@author: ls
"""
import dash
from dash.dependencies import Input, Output, Event, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from collections import deque
import time
import os
import flask


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


d_ref_values = {
    str(i): 0 for i in range(n_btns)}

minus_clicks_ref = {
    str(i): 0 for i in range(n_sliders)}

plus_clicks_ref = {
    str(i): 0 for i in range(n_sliders)}


timestamp = {
    str(i): deque(range(max_len), maxlen=max_len) for i in range(n_sliders)}
timestamp['start'] = time.time()

ref_timestamp = {
    str(i): deque(range(max_len), maxlen=max_len) for i in range(n_sliders)}
ref_timestamp['start'] = time.time()

mes_timestamp = {
    str(i): deque(range(max_len), maxlen=max_len) for i in range(n_sliders)}
ref_timestamp['start'] = time.time()

app = dash.Dash()
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True


# -----------------------------------------------------------------------------
# CSS Stylesheets
# -----------------------------------------------------------------------------


# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
css_directory = os.getcwd()
stylesheets = ['style.css']
static_css_route = '/static/'


@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                stylesheet
            )
        )
    return flask.send_from_directory(css_directory, stylesheet)


for stylesheet in stylesheets:
    app.css.append_css({"external_url": "/static/{}".format(stylesheet)})


#
##app.css.append_css({
##    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
##})
#dcc._css_dist[0]['relative_package_path'].append('style.css')
#
##    html.I(id='submit-button', n_clicks=0, className='fa fa-send'),


# -----------------------------------------------------------------------------
# PWM CONTROL - Html layout
# -----------------------------------------------------------------------------

lbls = [[html.Label('0', id='ref-label-{}'.format(i))
         ] for i in range(n_sliders)]

btns = [[
        html.Button(id='-ref-btn-{}'.format(i), children='-'),
        html.Button(id='+ref-btn-{}'.format(i), children='+')
        ] for i in range(n_sliders)]

sldrs = [[
        dcc.Slider(id='ref-slider-{}'.format(i),
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


dlbls = [[html.Button(children='F{}'.format(i), id='d-ref-btn-{}'.format(i))
          ] for i in range(n_btns)]

dsldrs = [[dcc.Slider(id='d-ref-slider-{}'.format(i),
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


refctr = html.Div([
        html.H1('Pressure Control'),
        html.Div([
            html.Div(sliders, className='eight columns'),
            html.Div(dsliders, className='three columns')
        ], className='row')
    ])


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


pwmctr = html.Div([
        html.H1('PWM Control'),
        html.Div([
            html.Div(sliders, className='eight columns'),
            html.Div(dsliders, className='three columns')
        ], className='row')
    ])

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

PATTusr = [[0.00, 0.00, 0.00, 0.0, 0.25, 0.00, False, True, True, False, 5.0],
           [0.00, 0.00, 0.00, 0.0, 0.25, 0.00, True, True, True, True, 2.0],
           [0.00, 0.00, 0.00, 0.0, 0.25, 0.00, True, False, False, True, 1.0],
           [0.00, 0.0, 0.0, 0.00, 0.00, 0.25, True, False, False, True, 5.0],
           [0.00, 0.0, 0.0, 0.00, 0.00, 0.25, True, True, True, True, 2.0],
           [0.00, 0.0, 0.0, 0.00, 0.00, 0.25, False, True, True, False, 1.0]]


def generate_ptrn_dict(data):
    return {
        'ptrn_t_move': data[0][-1],
        'ptrn_t_fix': data[1][-1],
        'ptrn_t_defix': data[2][-1],
        'ptrn_p_0': data[3][0],
        'ptrn_p_01': data[0][0],
        'ptrn_p_1': data[0][1],
        'ptrn_p_11': data[3][1],
        'ptrn_p_2': data[0][2],
        'ptrn_p_21': data[3][2],
        'ptrn_p_3': data[3][3],
        'ptrn_p_31': data[0][3],
        'ptrn_p_4': data[3][4],
        'ptrn_p_41': data[0][4],
        'ptrn_p_5': data[0][5],
        'ptrn_p_51': data[3][5]}


def generate_pattern(ptrn_t_move, ptrn_t_fix, ptrn_t_defix, ptrn_p_0,
                     ptrn_p_01, ptrn_p_1, ptrn_p_11, ptrn_p_2, ptrn_p_21,
                     ptrn_p_3, ptrn_p_31, ptrn_p_4, ptrn_p_41, ptrn_p_5,
                     ptrn_p_51):
    data = [
        [ptrn_p_01, ptrn_p_1, ptrn_p_2, ptrn_p_31, ptrn_p_41, ptrn_p_5,
         False, True, True, False, ptrn_t_move],
        [ptrn_p_01, ptrn_p_1, ptrn_p_2, ptrn_p_31, ptrn_p_41, ptrn_p_5,
         True, True, True, True, ptrn_t_fix],
        [ptrn_p_01, ptrn_p_1, ptrn_p_2, ptrn_p_31, ptrn_p_41, ptrn_p_5,
         True, False, False, True, ptrn_t_defix],
        [ptrn_p_0, ptrn_p_11, ptrn_p_21, ptrn_p_3, ptrn_p_4, ptrn_p_51,
         True, False, False, True, ptrn_t_move],
        [ptrn_p_0, ptrn_p_11, ptrn_p_21, ptrn_p_3, ptrn_p_4, ptrn_p_51,
         True, True, True, True, ptrn_t_fix],
        [ptrn_p_0, ptrn_p_11, ptrn_p_21, ptrn_p_3, ptrn_p_4, ptrn_p_51,
         False, True, True, False, ptrn_t_defix]]
    return data


ptrnctr_dic = {key: generate_ptrn_dict(data)
               for key, data in zip(['v3.0', 'v2.6', 'own-ptrn'],
                                    [PATT3_0, PATT2_6, PATTusr])
               }


ptrn_inputs_t = [
    ['{}{} :'.format(key.split('_')[1], key.split('_')[2][:3]),
     dcc.Input(id=key, type='number', min=0,
               max=100 if key.split('_')[1] == 'p' else 1000,
               value=ptrnctr_dic['own-ptrn'][key]*100, style={'width': 65})]
    for key in sorted(ptrnctr_dic[ptrnctr_dic.keys()[0]].iterkeys())
    if key != 'data']
ptrn_inputs = [html.Div([
        html.Div(item[0], className='five columns'),
        html.Div(item[1], className='seven columns')
    ], className='row') for item in ptrn_inputs_t]


pttrnctr = html.Div([
    html.H1('Walking'),
    html.Div(dcc.Dropdown(
        id='ptrn-dropdown',
        options=[{'label': key, 'value': key} for key in ptrnctr_dic],
        value=ptrnctr_dic.keys()[0]
        ), className='row'),
    html.Div([html.Button(id='ptrn-start', children='Start'),
              html.Button(id='ptrn-stop', children='Stop')
              ], className='row'),
    html.Div([
        html.Div(id='ptrn-scope', className='eight columns'),
        html.Div([
            html.Div([
                html.Div(
                    ptrn_inputs[:8], className='six columns'),
                html.Div(flat_list([
                    ptrn_inputs[8:],
                    [html.Div([
                        html.Button(id='ptrn-submit-btn', children='Submit')
                        ], className='row')]
                ]), className='six columns'),
            ], className='row')
        ], className='four columns')
    ], className='row')
])


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
    [dcc.Tabs(
        tabs=[
            {'label': i[1], 'value': i[0]} for i in
            [('PAUSE', 'Pause'),
             ('REFERENCE_TRACKING', 'Walking'),
             ('USER_CONTROL', 'PWM Ctr'),
             ('USER_REFERENCE', 'Prsr Ctr'),
             ('EXIT', 'Quit')]
        ],
        value='PAUSE',
        id='tabs'),
     html.Div(id='tab-output')]
]), style={
    'width': '90%',
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto'
})


# -----------------------------------------------------------------------------
# Callbacks - Tabs Content
# -----------------------------------------------------------------------------


@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    if value == 'REFERENCE_TRACKING':
        return pttrnctr
    elif value == 'USER_CONTROL':
        return pwmctr
    elif value == 'USER_REFERENCE':
        return refctr
    elif value == 'PAUSE':
        return html.H1('PAUSE')
    elif value == 'EXIT':
        return 'Not Implemented'
    else:
        return 'Not Implemented'

# -----------------------------------------------------------------------------
# Callbacks - PWM CTR
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


# -----------------------------------------------------------------------------
# Callbacks - REF CTR
# -----------------------------------------------------------------------------

for i in range(n_sliders):
    @app.callback(Output('ref-label-{}'.format(i), 'children'),
                  [Input('ref-slider-{}'.format(i), 'value')])
    def ref_slider_callback(val, idx=i):
        global ref_values
        if ref_values[str(idx)][-1] != val:
            global ref_timestamp
            ref_values[str(idx)].append(val)
            ref_timestamp[str(idx)].append(time.time()-timestamp['start'])
        return str(val)

    @app.callback(Output('ref-slider-{}'.format(i), 'value'),
                  [Input('-ref-btn-{}'.format(i), 'n_clicks'),
                   Input('+ref-btn-{}'.format(i), 'n_clicks')])
    def ref_slider_update(minus, plus, idx=i):
        global ref_values
        global minus_clicks_ref
        global plus_clicks_ref
        val = ref_values[str(idx)][-1]
        if minus > minus_clicks_ref[str(idx)]:
            minus_clicks_ref[str(idx)] += 1
            if val - 1 >= 0:
                val -= 1
        if plus > plus_clicks_ref[str(idx)]:
            plus_clicks_ref[str(idx)] += 1
            if val + 1 <= 100:
                val += 1
        return val


for i in range(n_btns):
    @app.callback(Output('d-ref-slider-{}'.format(i), 'value'),
                  [Input('d-ref-btn-{}'.format(i), 'n_clicks')])
    def d_ref_btn_callback(event, idx=i):
        global d_ref_values
        if event:
            state = event % 2
        else:
            state = 0
        d_ref_values[str(idx)] = state
        return state

# -----------------------------------------------------------------------------
# Callbacks - Ptrn
# -----------------------------------------------------------------------------


@app.callback(Output('ptrn-scope', 'children'),
              inputs=[Input('ptrn-dropdown', 'value'),
                      Input('ptrn-submit-btn', 'n_clicks')],
              state=[State(key, 'value') for key in sorted(
                          ptrnctr_dic[ptrnctr_dic.keys()[0]].iterkeys())
                     if key != 'data'])
def update_ptrn_graph(dropdown_val, submit, *args):
    global ptrnctr_dic
    if dropdown_val == 'own-ptrn':
        ptrnctr_dic['own-ptrn'] = {
            key: min(abs(float(args[idx])), 100)*.01
            if key.split('_')[1] == 'p' else abs(float(args[idx]))*.01
            for idx, key in enumerate(
                sorted(ptrnctr_dic['own-ptrn'].iterkeys()))}
    traces = []
    ptrn = generate_pattern(**ptrnctr_dic[dropdown_val])
    for key in pwm_values:
        y = [p[int(key)] for p in ptrn]
        t_m, t_a, t_d = (ptrnctr_dic[dropdown_val]['ptrn_t_move'],
                         ptrnctr_dic[dropdown_val]['ptrn_t_fix'],
                         ptrnctr_dic[dropdown_val]['ptrn_t_defix'])
        x = [0, t_m, t_m+t_a, t_m+t_a+t_d, 2*t_m+t_a+t_d, 2*t_m+2*t_a+t_d]
        data = go.Scatter(
            x=x,
            y=y,
            name=key,
            mode='lines+markers')
        traces.append(data)

    ptrn_lbls_t = [
        ['{}{} : '.format(key.split('_')[1], key.split('_')[2]),
         html.Label(children=ptrnctr_dic[dropdown_val][key])]
        for key in sorted(ptrnctr_dic[dropdown_val].iterkeys())
        if key != 'data']
    ptrn_lbls = [html.Div([
            html.Div(item[0], className='six columns'),
            html.Div(item[1], className='six columns')
            ], className='row') for item in ptrn_lbls_t]

    figure = {
            'data': traces,
            'layout': go.Layout(
                xaxis={'range': [0, 2*t_m+2*t_a+t_d]},
                yaxis={'range': [0, 1]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                height=300
                )
        }
    return [html.Div(ptrn_lbls, className='three columns'),
            html.Div([
                html.Div([
                    dcc.Graph(id='ptrn-graph',
                              figure=figure, config={'staticPlot': True})
                    ], className='nine columns')
                ])]


# -----------------------------------------------------------------------------
# Callbacks - Main
# -----------------------------------------------------------------------------


@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph():
    traces = []
    minis = []
    maxis = []
    for key in pwm_values:
        minis.append(min(list(timestamp[key])))
        maxis.append(max(list(timestamp[key])))
        data = go.Scatter(
            x=list(timestamp[key]),
            y=list(pwm_values[key]),
            name='PWM {}'.format(key),
            mode='lines+markers')
        traces.append(data)
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'range': [min(minis), max(maxis)]},
            yaxis={'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10}
        )
    }


@app.callback(Output('pressure-ref-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_ref_graph():
    traces = []
    minis = []
    maxis = []
    for key in ref_values:
        minis.append(min(list(ref_timestamp[key])))
        maxis.append(max(list(ref_timestamp[key])))
        data = go.Scatter(
            x=list(ref_timestamp[key]),
            y=list(ref_values[key]),
            name='Ref {}'.format(key),
            mode='lines+markers')
        traces.append(data)
    for key in mes_values:
        minis.append(min(list(mes_timestamp[key])))
        maxis.append(max(list(mes_timestamp[key])))
        data = go.Scatter(
            x=list(mes_timestamp[key]),
            y=list(mes_values[key]),
            name='Mes {}'.format(key),
            mode='lines+markers')
        traces.append(data)
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'range': [min(minis), max(maxis)]},
            yaxis={'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10}
        )
    }


def run_server():
    app.run_server(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run_server()
