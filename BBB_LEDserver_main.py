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
    print 'can not import Adafruit'


pins = {
    "P8_7": {'name': 'pin7', 'state': GPIO.LOW},
    "P8_8": {'name': 'pin8', 'state': GPIO.LOW},
    "P8_9": {'name': 'pin9', 'state': GPIO.LOW},
    "P8_10": {'name': 'pin10', 'state': GPIO.LOW},
    "P8_11": {'name': 'pin11', 'state': GPIO.LOW},
    "P8_12": {'name': 'pin12', 'state': GPIO.LOW},
    "P8_14": {'name': 'pin14', 'state': GPIO.LOW},
    "P8_16": {'name': 'pin16', 'state': GPIO.LOW},
    "P8_15": {'name': 'pin15', 'state': GPIO.LOW},
    "P8_17": {'name': 'pin17', 'state': GPIO.LOW},
    "P8_18": {'name': 'pin18', 'state': GPIO.LOW},
    "P8_26": {'name': 'pin26', 'state': GPIO.LOW}
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
            {'label': 'Blinking', 'value': 1},
            {'label': 'Fast Blinking', 'value': 2}
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
            if self.mode.value == 0:
                time.sleep(.5)
            elif self.mode.value == 1:
                for pin in pins:
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

    def kill(self):
        self.exit_flag = True


if __name__ == '__main__':
    gpio_thread = GPIOThread(modus)
    gpio_thread.start()

    try:
        app.run_server(debug=True, host='0.0.0.0', port=8050)
    finally:
        gpio_thread.kill()
