from collections import deque
import datetime
import re
import subprocess
import time

import adafruit_mcp4725
from adafruit_seesaw.seesaw import Seesaw
import adafruit_scd30
import adafruit_tca9548a
import board
import busio
import dash
from dash.dependencies import Input, Output
from dash import dash_table, dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


class Haus:
    def __init__(self):
        self.data = {}
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
        self.dac = adafruit_mcp4725.MCP4725(self.i2c)
        self.scd = adafruit_scd30.SCD30(self.i2c)
        # create tca object based on i2c bus
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)
        for channel in range(8):
            time.sleep(1)
            if self.tca[channel].try_lock():
                addresses = self.tca[channel].scan()
                self.tca[channel].unlock()
        # create multiplexer object after unlocks
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)
        self.thermal = None

    def change_lighting(self, change_to, get_value=False):
        if get_value:
            return bool(self.dac.value)
        assert change_to in ['off', 'on']
        normalized_values = {'off': 0, 'on': 1}
        self.dac.normalized_value = normalized_values[change_to]

    def measure_air(self):
        """
        Measure CO2/temp/humidity of air
        """
        success = False
        while not self.scd.data_available:
            time.sleep(.1)
        while not success:
            try:
                co2 = self.scd.CO2
                temp = self.scd.temperature
                temp = ((temp*(9/5))+32) # convert C -> F degrees
                humidity = self.scd.relative_humidity
            except RuntimeError:
                time.sleep(.1)
                continue
            else:
                success = True 
        return pd.DataFrame({'co2': [round(co2, 4)], 'temp': [round(temp, 4)], 'humidity': [round(humidity, 4)]})
      
    def measure_soil(self, num_sensors=4):
        soil_sensors = []
        for i in range(num_sensors):
            if i in (0,1): ## this is a wiring error i need to fix
                continue
            try:
                soil_sensor = Seesaw(self.tca[i+2], addr=0x36)
                soil_sensors.append(soil_sensor)
            except (OSError, ValueError, RuntimeError) as e:
                #pass
                continue
                print(f'wiring error on sensor {i+1} (tca addr {i+2})')
        measurements = ['sensor_number', 'soil_moisture', 'soil_temp']
        soil_df = pd.DataFrame([(i, ss.moisture_read(), ss.get_temp()) for i, ss in enumerate(soil_sensors, start=1)], columns=measurements)
        return soil_df


headers = [html.H1(children='The Plants'), html.Div(children='Everything is "fine".'), html.A("Live Webcam", href="/live_cam")]


def init_dashboard(server):
    haus = Haus()
    dash_app = dash.Dash(
            server=server,
            routes_pathname_prefix='/plants/',
            external_stylesheets=['/static/css/custom.css',]
            )
    dash_app.layout = html.Div(children=headers+[
        dash_table.DataTable(haus.measure_air().to_dict('records'),[{"name": i, "id": i} for i in haus.measure_air().columns], id='tbl'),
        dash_table.DataTable(haus.measure_soil().to_dict('records'),[{"name": i, "id": i} for i in haus.measure_soil().columns], id='soil_tbl'),
        html.Div(children="light_status_emoji", id='lights'), 
        dcc.Interval(id="refresh", interval=5*1000, n_intervals=0)
        ])

    @dash_app.callback(
            [
                Output("tbl", "data"),
                Output("soil_tbl", "data"),
                Output("lights", "children")
                ],
            Input("refresh", "n_intervals"))
    def update(n_intervals):
        air = haus.measure_air().to_dict('records')
        soil = haus.measure_soil().to_dict('records')
        lights = haus.change_lighting(change_to=None, get_value=True)
        lights = "🌞" if lights else "🌙"
        return [air, soil, lights]

    return dash_app.server
