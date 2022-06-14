from collections import deque
import datetime
import re
import subprocess
import time

import adafruit_scd30
import adafruit_tca9548a
import board
import busio
import dash
from dash.dependencies import Input, Output
from dash import dash_table, dcc, html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd


def measure_air(scd30, out='raw'):
    """
    Measure CO2 in air
    """
    while not scd.data_available:
        print('waiting on data...')
        time.sleep(.5)
    co2 = scd.CO2
    temp = scd.temperature
    temp = ((temp*(9/5))+32) # convert C -> F degrees
    humidity = scd.relative_humidity
    if out=='raw':
        return pd.DataFrame({'co2': [co2], 'temp': [temp], 'humidity': [humidity]})
    data = {'metrics': ['co2', 'temp', 'humidity']
            , 'values': [co2, temp, humidity]}
    return data

def measure_soil(tca, num_sensors=4):
    soil_sensors = []
    for i in range(num_sensors):
        try:
            soil_sensor = Seesaw(tca[i+2], addr=0x36)
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


headers = [html.H1(children='The Plants'), html.Div(children='Everything is "fine".')]


def init_dashboard(server):
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)
    dash_app = dash.Dash(
            server=server,
            routes_pathname_prefix='/plants/',
            external_stylesheets=['/static/css/custom.css',]
            )
    dash_app.layout = html.Div(children=headers+[
        dash_table.DataTable(measure_air(scd).to_dict('records'),[{"name": i, "id": i} for i in measure_air(scd).columns], id='tbl'),
        dcc.Interval(id="refresh", interval=5*1000, n_intervals=0),
        ])

    @dash_app.callback([Output("tbl", "data")], Input("refresh", "n_intervals"))
    def update(n_intervals):
        dt = measure_air(scd).to_dict('records')
        return [dt]

    return dash_app.server
