
# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}




#app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
#    html.H1(
#        children='Hello Dash',
#        style={
#            'textAlign': 'center',
#            'color': colors['text']
#        }
#    ),
#
#    html.Div(children='Dash: A web application framework for Python.', style={
#        'textAlign': 'center',
#        'color': colors['text']
#    }),
#
#    dcc.Graph(
#        id='example-graph-2',
#        figure={
#            'data': [
#                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#            ],
#            'layout': {
#                'plot_bgcolor': colors['background'],
#                'paper_bgcolor': colors['background'],
#                'font': {
#                    'color': colors['text']
#                }
#            }
#        }
#    )
#])




app.layout = html.Div(children=[
    html.Label('Dropdown', style={
            'textAlign': 'center',
            'color': colors['text']
            }),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Multi-Select Dropdown', style={
            'textAlign': 'center',
            'color': colors['text']
            }),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF'],
        multi=True
    ),

    html.Label('Radio Items', style={
            'textAlign': 'center',
            'color': colors['text']
            }),
    dcc.RadioItems(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Checkboxes', style={
            'textAlign': 'center',
            'color': colors['text']
            }
    ),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        values=['MTL', 'SF']
    ),

    html.Label('Text Input', style={
            'textAlign': 'center',
            'color': colors['text']
            }),
    dcc.Input(value='MTL', type='text'),

    html.Label('PWM', style={
            'textAlign': 'center',
            'color': colors['text']
            }),
    dcc.Slider(
        min=0,
        max=100,
        marks={i: str(i) for i in range(0, 101, 10)},
        value=0,
    ),
], style={'columnCount': 1, 'backgroundColor': colors['background']})

if __name__ == '__main__':
    app.run_server(debug=True)
