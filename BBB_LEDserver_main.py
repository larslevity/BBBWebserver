"""
To run on the BBB (-- without any virzuel enviroment)

Note: To log into BBB via ssh (in case of crash)
        ssh root@192.168.178.56

Sometimes, the FritzBox changes the static IP of the BBB for no reason.
Then, you can find ou the new IP by logging into the FritzBox as Admin
and scan all users of the LAN. BBB should be listed as beagleboard.


After running:

    visit the website in the local network on:
        192.168.178.56:8050


To start after a reboot, add a cronjob by editing the crontab:
	crontab -e
and add the following line:
	@reboot python ~/Git/BBBWebserver/BBB_LEDserver_main.py

"""

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
    print('can not import Adafruit')

#[11 12]
#[21 22]
#[31 32]
#[41 42]
#[51 52]
#[61 62]

pins = [
    "P8_10",  # bright orange 11
    "P8_14",  # light yellow 12
    "P8_12",  # kaputt
    "P8_8",   # bright yellow 22
    "P8_26",  # bright orange 31
    "P8_7",   # light red   32
    "P8_11",  # bright pink 41
    "P8_9",   # bright red 42
    "P8_17",  # light orange 51
    "P8_18",  # light red 52
    "P8_15",  # bright orange 61
    "P8_16",  # light green 62
   ]

pins_loop = [
    "P8_10",  # bright orange 11
    "P8_12",  # kaputt 21    
    "P8_26",  # bright orange 31    
    "P8_11",  # bright pink 41    
    "P8_17",  # light orange 51    
    "P8_15",  # bright orange 61
    "P8_16",  # light green 62
    "P8_18",  # light red 52
    "P8_9",   # bright red 42
    "P8_7",   # light red   32
    "P8_8",   # bright yellow 22
    "P8_14",  # light yellow 12
   ]


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
        children='Blinking Fischli',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(
        children='Select the mood of Fischli',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.RadioItems(
        id='radio-items',
        options=[
            {'label': 'OFF', 'value': 0},
            {'label': 'Knight', 'value': 1},
            {'label': 'Blink', 'value': 2},
            {'label': 'Loop', 'value': 3},
            {'label': 'Blitz', 'value': 4},
        ],
#        options = [{'label': 'pin '+str(i), 'value': i} for i in range(len(pins))],
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

#    def run(self):
#        """ run HUI """
#        while not self.exit_flag:
#
#            for i, pin in enumerate(pins):
#                if self.mode.value == i:
#                    GPIO.output(pin, GPIO.HIGH)
#                    time.sleep(.5)
#                    GPIO.output(pin, GPIO.LOW)
#            time.sleep(.2)

    def run(self):
        """ run HUI """
        while not self.exit_flag:
            if self.mode.value == 0:
                time.sleep(.5)
            elif self.mode.value in [1, 3]:
                for pin in pins if self.mode.value==1 else pins_loop:
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(.1)
                    GPIO.output(pin, GPIO.LOW)
            elif self.mode.value == 2:
                for pin in pins:
                    GPIO.output(pin, GPIO.HIGH)
                time.sleep(.1)
                for pin in pins:
                    GPIO.output(pin, GPIO.LOW)
                time.sleep(.2)
            elif self.mode.value == 4:
                for pin in pins:
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(.04)
                    GPIO.output(pin, GPIO.LOW)

    def kill(self):
        self.exit_flag = True


if __name__ == '__main__':
    gpio_thread = GPIOThread(modus)
    gpio_thread.start()

    try:
        app.run_server(debug=True, host='0.0.0.0', port=8050)
    finally:
        gpio_thread.kill()
