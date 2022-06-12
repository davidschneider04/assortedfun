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


def measure_air(scd30):
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



i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
"""
# create tca object based on i2c bus
tca = adafruit_tca9548a.TCA9548A(i2c)
for channel in range(8):
    time.sleep(1)
    if tca[channel].try_lock():
        addresses = tca[channel].scan()
        tca[channel].unlock()
# create multiplexer object after unlocks
tca = adafruit_tca9548a.TCA9548A(i2c)
"""
scd = adafruit_scd30.SCD30(i2c)

#data = pd.DataFrame(measure_air(scd))
#graphs = {metric:px.bar(data[data['metrics']==metric], x='metrics', y='values', barmode='group') 
#        for metric in data['metrics'].unique()}
#graphs_html = [dcc.Graph(id=f'{metric}-graph', figure=graph) for metric, graph in graphs.items()]
headers = [html.H1(children='The Plants'), html.Div(children='Everything is "fine".')]

metrics = ['co2', 'temp', 'humidity']
q = {metric: {'X': deque(maxlen=100), 'Y': deque(maxlen=100)} for metric in metrics}


def append_metric_val(metric, val):
    dttm = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
    q[metric]['X'].append(dttm)
    q[metric]['Y'].append(val)


def graph_from_metric(df, metric):
    filtered_df = df[df['metrics']==metric]
    yval = filtered_df['values'].iloc[0]
    append_metric_val(metric, yval)
    data = go.Scatter(x=list(q[metric]['X']), y=list(q[metric]['Y']), name=metric, showlegend=False, mode='lines')
    grph = {'data': [data],
            'layout': go.Layout(
                xaxis=dict(range=[min(q[metric]['X']), max(q[metric]['X'])]),
                yaxis=dict(range=[min(q[metric]['Y']), max(q[metric]['Y'])]),)}
    return grph


df = pd.DataFrame(measure_air(scd))
for metric in metrics:
    filt = df[df['metrics']==metric]
    val = filt['values'].iloc[0]
    append_metric_val(metric, val)



def init_dashboard(server):
    dash_app = dash.Dash(
            server=server,
            routes_pathname_prefix='/plants/',
            external_stylesheets=['/static/css/custom.css',]
            )
    dash_app.layout = html.Div(children=headers+[
        dash_table.DataTable(pd.read_csv("https://git.io/Juf1t").to_dict('records'),[{"name": i, "id": i} for i in pd.read_csv("https://git.io/Juf1t").columns], id='tbl'),
        dcc.Graph(id='co2-graph', animate=True),
        dcc.Graph(id='temp-graph', animate=True),
        dcc.Graph(id='humidity-graph', animate=True),
        dcc.Interval(id="refresh", interval=5*1000, n_intervals=0),
        ])

    @app.callback([Output("co2-graph", "figure"), Output("temp-graph", "figure"), Output("humidity-graph", "figure"), Output("tbl", "data")], Input("refresh", "n_intervals"))
    def update(n_intervals):
        df = pd.DataFrame(measure_air(scd))#.append(pd.DataFrame(measure_soil(tca)))
        graphs = [graph_from_metric(df, metric) for metric in metrics]
        co2, airtemp, humidity = graphs
        #df = pd.read_sql("select * from temp order by dttm desc limit 1", con) 
        dt = pd.read_csv("https://git.io/Juf1t").to_dict('records')
        return co2, airtemp, humidity, dt

    return dash_app.server
