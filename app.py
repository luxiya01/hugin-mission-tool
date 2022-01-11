import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.dependencies import Input, Output, State
from mission_parser import MissionParser
import datetime

import pandas as pd
import numpy as np

from app_components import (upload_mission_file_component,
                            mission_starttime_input, map_component)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([
    html.H2('Utility tool for Hugin missions'),
    dbc.Tabs([
        dbc.Tab([
            upload_mission_file_component(
                id=['upload-mission-file', 'upload-mission-file-output']),
            mission_starttime_input(id=[
                'mission-start-date', 'mission-start-time',
                'mission-time-submit'
            ]),
            html.Div(id='selected-datetime-text'),
            html.Div(id='map-plot-div'),
            map_component(id=['map', 'geojson', 'polyline'])
        ],
                label='Mission Visualizer'),
        dbc.Tab([html.H5('TMP text')], label='utilities')
    ])
])


@app.callback(Output('upload-mission-file-output', 'children'),
              Output('selected-datetime-text', 'children'),
              Output('geojson', 'data'), Output('polyline', 'positions'),
              Output('map', 'center'), Input('mission-time-submit',
                                             'n_clicks'),
              Input('upload-mission-file', 'contents'),
              State('upload-mission-file', 'filename'),
              State('mission-start-date', 'date'),
              State('mission-start-time', 'value'), State('map', 'center'))
def update_map_plot(n_clicks, contents, filename, date, time,
                    current_map_center):
    upload_mission_file_output = html.H5(f'Selected mission: {filename}')
    time_str = f'{date}, {time}'
    time_fmt = '%Y-%m-%d, %H:%M'
    time_div = html.H5(f'Selected mission start time: {time_str}')
    geojson_data = None
    polyline_pos = [[0, 0], [0, 0]]
    map_center = current_map_center

    start_time = datetime.datetime.strptime(time_str, time_fmt)

    error_div = html.Div([
        html.B(
            f'The selected file "{filename}" is not a valid .mp mission file!',
            style={'color': 'red'})
    ])

    if contents is not None:
        _, content_str = contents.split(',')
        try:
            m = MissionParser.parse_upload(filename=filename,
                                           content_str=content_str)
        except Exception as e:
            return error_div, time_div

        df = pd.DataFrame(m.mission)
        df['lat'] = [x.latitude_in_dd for x in m.mission]
        df['lon'] = [x.longitude_in_dd for x in m.mission]
        df['timestamp'] = m.compute_mission_timestamps(start_time)
        df['reaching_time'] = [t.strftime(time_fmt) for t in df['timestamp']]
        df['reached'] = False
        df.loc[0, 'reached'] = True
        df = df[[
            'No', 'lat', 'lon', 'timestamp', 'reaching_time', 'reached',
            'Comment'
        ]]
        map_center = (df.lat.mean(), df.lon.mean())
        dicts = df.to_dict('rows')
        for item in dicts:
            tooltip = f'Waypoint No.{item["No"]}<br/>Position: ({item["lat"]:.2f}, {item["lon"]:.2f})<br/>Reaching time: {item["reaching_time"]}'
            if item['Comment'] != '':
                tooltip = f'{tooltip}<br/>Comment: {item["Comment"]}'
            item['tooltip'] = tooltip
        geojson_data = dlx.dicts_to_geojson(dicts)
        polyline_pos = [[lat, lon] for (lat, lon) in zip(df.lat, df.lon)
                        if not np.isnan(lat) and not np.isnan(lon)]
    return upload_mission_file_output, time_div, geojson_data, polyline_pos, map_center


if __name__ == '__main__':
    app.run_server(debug=True)  #, dev_tools_props_check=False)
