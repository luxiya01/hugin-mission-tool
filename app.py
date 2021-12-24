import dash
from dash import html
from dash.dependencies import Input, Output, State
from mission_parser import MissionParser
import datetime

import pandas as pd

from app_components import upload_mission_file_component, map_plot_component, mission_starttime_input

app = dash.Dash()
server = app.server
app.layout = html.Div([
    upload_mission_file_component(id='upload-mission-file'),
    mission_starttime_input(
        id=['mission-start-date', 'mission-start-time', 'mission-time-submit'
            ]),
    html.Div(id='selected-datetime-text'),
    html.Div(id='map-plot-div')
])


@app.callback(Output('map-plot-div', 'children'),
              Output('selected-datetime-text', 'children'),
              Input('mission-time-submit', 'n_clicks'),
              Input('upload-mission-file', 'contents'),
              State('upload-mission-file', 'filename'),
              State('mission-start-date', 'date'),
              State('mission-start-time', 'value'))
def update_map_plot(n_clicks, contents, filename, date, time):
    time_str = f'{date}, {time}'
    time_fmt = '%Y-%m-%d, %H:%M'
    time_div = html.H5(f'Selected mission start time: {time_str}')
    graph = None

    start_time = datetime.datetime.strptime(time_str, time_fmt)

    if contents is not None:
        content_type, content_str = contents.split(',')
        m = MissionParser.parse_upload(filename=filename,
                                       content_str=content_str)
        df = pd.DataFrame(m.mission)
        df['lat'] = [x.latitude_in_dd for x in m.mission]
        df['lon'] = [x.longitude_in_dd for x in m.mission]
        df['timestamp'] = m.compute_mission_timestamps(start_time)
        df['reaching_time'] = [t.strftime(time_fmt) for t in df['timestamp']]
        df['reached'] = False
        df.loc[0, 'reached'] = True

        graph = map_plot_component(df=df, id='map-plot', filename=filename)
    return html.Div([html.Div(html.H5(f'Mission file: {filename}')),
                     graph]), time_div


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_props_check=False)
