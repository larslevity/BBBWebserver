
'''
https://stackoverflow.com/questions/36695902/beaglebone-black-to-the-gpio-control-over-python-flask-webserver-html
'''
import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_45", GPIO.OUT)
GPIO.setup("P8_46", GPIO.OUT)

from flask import Flask
from flask import render_template
from flask import request
from jinja2 import Environment, PackageLoader

app =Flask(__name__)
env = Environment(loader=PackageLoader('flask-test', 'templates'))

@app.route("/", methods = ['GET', 'POST'])
def main():
    if request.method == 'GET':
        template = env.get_template('click.html')
        return template.render(val = "nothing")
    else:
        switch_name = None
        for led_name in request.form.keys():
            led_status = request.form.get(led_name, None)
            if led_name == "led1" and led_status == "On":
                GPIO.output("P8_45", GPIO.HIGH)
                GPIO.output("P8_46", GPIO.LOW)
                switch_name = "SWITCH 1"
            elif led_name == "led2" and led_status == "On":
                GPIO.output("P8_45", GPIO.LOW)
                GPIO.output("P8_46", GPIO.HIGH)
                switch_name = "SWITCH 2"
            else:
                GPIO.output("P8_46", GPIO.LOW)
                GPIO.output("P8_45", GPIO.LOW)
        template = env.get_template('click.html')
        return template.render(val=switch_name)
        time.sleep(5)

app.debug = True
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
