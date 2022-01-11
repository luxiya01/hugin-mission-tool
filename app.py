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
from data import WayPoint

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                prevent_initial_callbacks=True)
server = app.server

#TODO: remove global variable for holding mission...
CURRENT_MISSION = None

#TODO: move id assignments to a components_id.py const file
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
            map_component(
                id=['map', 'geojson', 'polyline', 'map-callback-layer'])
        ],
                label='Mission Visualizer'),
        dbc.Tab([html.H5('TMP text')], label='utilities')
    ])
])


def mission_file_to_dataframe(contents, filename, start_time, time_fmt):
    """Given a content stream from dcc.Upload, filename, start_time and time_fmt,
    return a pandas dataframe with waypoints"""
    _, content_str = contents.split(',')
    try:
        m = MissionParser.parse_upload(filename=filename,
                                       content_str=content_str)
    except Exception as e:
        return None

    global CURRENT_MISSION
    CURRENT_MISSION = m
    df = pd.DataFrame(m.mission)
    df['lat'] = [x.latitude_in_dd for x in m.mission]
    df['lon'] = [x.longitude_in_dd for x in m.mission]
    df['timestamp'] = m.compute_mission_timestamps(start_time)
    df['reaching_time'] = [t.strftime(time_fmt) for t in df['timestamp']]
    df['reached'] = False
    df.loc[0, 'reached'] = True
    df = df[[
        'No', 'lat', 'lon', 'timestamp', 'reaching_time', 'reached', 'Comment'
    ]]
    return df


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

    if contents is not None:
        df = mission_file_to_dataframe(contents, filename, start_time,
                                       time_fmt)
        #TODO: handle when mission parsing fails
        map_center = (df.lat.mean(), df.lon.mean())

        # Compute Geojson based on waypoints from df
        dicts = df.to_dict('rows')
        for item in dicts:
            tooltip = f'Waypoint No.{item["No"]}<br/>Position: ({item["lat"]:.2f}, {item["lon"]:.2f})<br/>Reaching time: {item["reaching_time"]}'
            if item['Comment'] != '':
                tooltip = f'{tooltip}<br/>Comment: {item["Comment"]}'
            item['tooltip'] = tooltip
        geojson_data = dlx.dicts_to_geojson(dicts)

        # Compute polyline based on waypoints from df
        polyline_pos = [[lat, lon] for (lat, lon) in zip(df.lat, df.lon)
                        if not np.isnan(lat) and not np.isnan(lon)]
    return upload_mission_file_output, time_div, geojson_data, polyline_pos, map_center


@app.callback(
    Output('geojson-callback-layer', 'children'),
    [Input('geojson', 'n_clicks'),
     State('geojson', 'click_feature')])
def geojson_callback(n_clicks, click_feature):
    print(f'clicked feature: {click_feature}')
    lon, lat = click_feature['geometry']['coordinates']
    global CURRENT_MISSION
    CURRENT_MISSION.mission.append(
        WayPoint(Latitude=WayPoint.degree_decimals_to_degree_minutes(
            lat, is_lat=True),
                 Longitude=WayPoint.degree_decimals_to_degree_minutes(
                     lon, is_lat=False)))
    print(f'current mission length: {CURRENT_MISSION.length}')
    return [
        dl.CircleMarker(center=[lat, lon],
                        children=dl.Tooltip("{}".format(click_feature)),
                        color='red')
    ]


@app.callback(Output('map-callback-layer', 'children'),
              [Input('map', 'click_lat_lng')])
def map_click(click_lat_lng):
    return [
        dl.Marker(position=click_lat_lng,
                  children=dl.Tooltip(
                      "({:.3f}, {:.3f})".format(*click_lat_lng)))
    ]


if __name__ == '__main__':
    app.run_server(debug=True)  #, dev_tools_props_check=False)
