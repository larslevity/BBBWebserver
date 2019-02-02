
# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import time

import threading

try:
    import Adafruit_BBIO.GPIO as GPIO
except ImportError:
    print 'can not import Adafruit'


pins = {
   "P8_10": {'name': 'pin10', 'state': GPIO.LOW},
   "P8_11": {'name': 'pin11', 'state': GPIO.LOW}
   }


class Modus(object):
    def __init__(self):
        self.value = 0


modus = Modus()


app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.RadioItems(
        id='radio-items',
        options=[
            {'label': 'Mode 1', 'value': 0},
            {'label': 'Mode 2', 'value': 1},
            {'label': 'Mode 3', 'value': 2}
        ],
        value=0,
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'padding': 10
        }
    ),

    html.Div(
        id='label-mode',
        children='',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

])


@app.callback(Output('label-mode', 'children'),
              [Input('radio-items', 'value')])
def radio_btn_clicked(value):
    modus.value = value
    return str(value)


class GPIOThread(threading.Thread):
    def __init__(self, modus):
        threading.Thread.__init__(self)
        self.mode = modus
        self.exit_flag = False

        # Set each pin as an output and make it low:
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def run(self):
        """ run HUI """
        while not self.exit_flag:
            if self.mode.val == 0:
                time.sleep(.5)
            elif self.mode.val == 1:
                for pin in pins:
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(.2)
                    GPIO.output(pin, GPIO.LOW)

    def kill(self):
        self.exit_flag = True


if __name__ == '__main__':
    gpio_thread = GPIOThread(modus)

    try:
        app.run_server(debug=True, host='0.0.0.0')
    finally:
        gpio_thread.kill()
