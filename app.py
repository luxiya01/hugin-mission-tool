import dash
from dash import html, dcc
import dash_leaflet as dl
import dash_leaflet.express as dlx
import plotly.express as px
from mission_parser import MissionParser
import pandas as pd

# Get mission data and produce a DataFrame
m = MissionParser.parse_file('NBP19_02_009.mp')
df = pd.DataFrame(m.mission)
df['lat'] = [x.latitude_in_dd for x in m.mission]
df['lon'] = [x.longitude_in_dd for x in m.mission]
df['timestamp'] = m.compute_mission_timestamps()
df['reaching_time'] = [t.strftime('%Y-%m-%d %H:%M') for t in df['timestamp']]
df['reached'] = False
df.loc[0, 'reached'] = True


# Line plot
def plot_figure(dff, highlight_idx):
    fig = px.line_geo(data_frame=dff,
                      lat='lat',
                      lon='lon',
                      text='No',
                      hover_name='No',
                      hover_data=['reaching_time', 'Comment'],
                      color='reached')
    fig.update_geos(fitbounds='locations',
                    lataxis_showgrid=True,
                    lonaxis_showgrid=True)
    fig.update_traces(textposition='top center')
    fig.update_layout(height=800, width=1000)
    return fig


# slider for waypoint index
slider_marks = {
    i: f'{df.loc[i, "No"]}'
    for i in range(0, len(df), 10)  #if df.loc[i, 'Comment'].strip() != ''
}
slider = dcc.Slider(id='slider',
                    min=0,
                    max=len(df.index) - 1,
                    step=1,
                    value=0,
                    marks=slider_marks,
                    tooltip={
                        'placement': 'bottom',
                        'always_visible': True
                    })

#TODO: checkout polyline decorator in dash-leaflet
app = dash.Dash()
fig = plot_figure(df, 0)
app.layout = html.Div([
    dcc.Graph(figure=fig, id='geo-plot'), slider,
    html.Div(id='slider-output-container')
])


@app.callback(dash.dependencies.Output('slider-output-container', 'children'),
              [dash.dependencies.Input('slider', 'value')])
def update_slider_output(value):
    return 'You have selected "{}"'.format(value)


@app.callback(dash.dependencies.Output('geo-plot', 'figure'),
              dash.dependencies.Input('slider', 'value'),
              dash.dependencies.Input('geo-plot', 'figure'))
def update_plot(value, figure):
    df.loc[:value, 'reached'] = True
    df.loc[value:, 'reached'] = False
    return plot_figure(df, value)


if __name__ == '__main__':
    app.run_server(debug=True)
