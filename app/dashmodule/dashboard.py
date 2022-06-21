from collections import deque
import datetime
import re
import subprocess
import time

import adafruit_mcp4725
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
            return self.dac.value
        assert change_to in ['off', 'on']
        normalized_values = {'off': 0, 'on': 1}
        self.dac.normalized_value = normalized_values[change_to]

    def measure_air(self):
        """
        Measure CO2/temp/humidity of air
        """
        while not self.scd.data_available:
            time.sleep(.1)
        co2 = self.scd.CO2
        temp = self.scd.temperature
        temp = ((temp*(9/5))+32) # convert C -> F degrees
        humidity = self.scd.relative_humidity
        return pd.DataFrame({'co2': [round(co2, 4)], 'temp': [round(temp, 4)], 'humidity': [round(humidity, 4)]})
      

    def measure_soil(self, num_sensors=4):
        soil_sensors = []
        for i in range(num_sensors):
            try:
                soil_sensor = Seesaw(self.tca[i+2], addr=0x36)
                soil_sensors.append(soil_sensor)
            except (OSError, ValueError) as e:
                print('wiring error')
        metrics = []
        values = []
        for i, ss in enumerate(soil_sensors):
            moisture = ss.moisture_read()
            temp = ss.get_temp()
            metrics.append(f'soil_moisture_{i}')
            values.append(moisture)
            metrics.append(f'soil_temp_{i}')
            values.append(temp)
        data = {'metrics': metrics, 'values': values}
        return data



    
#haus = Haus()


headers = [html.H1(children='The Plants'), html.Div(children='Everything is "fine".')]


def init_dashboard(server):
    haus = Haus()
    #i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    #scd = adafruit_scd30.SCD30(i2c)
    dash_app = dash.Dash(
            server=server,
            routes_pathname_prefix='/plants/',
            external_stylesheets=['/static/css/custom.css',]
            )
    dash_app.layout = html.Div(children=headers+[
        dash_table.DataTable(haus.measure_air().to_dict('records'),[{"name": i, "id": i} for i in haus.measure_air().columns], id='tbl'),
        dcc.Interval(id="refresh", interval=5*1000, n_intervals=0),
        ])

    @dash_app.callback([Output("tbl", "data")], Input("refresh", "n_intervals"))
    def update(n_intervals):
        dt = haus.measure_air().to_dict('records')
        return [dt]

    return dash_app.server
