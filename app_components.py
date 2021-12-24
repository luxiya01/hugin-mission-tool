from dash import html, dcc
import plotly.express as px
import datetime


def upload_mission_file_component(id='upload-mission-file'):
    return dcc.Upload(id=id,
                      children=['Drag and Drop or ',
                                html.A('Select Files')],
                      style={
                          'width': '80%',
                          'height': '20%',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'textAlign': 'center',
                          'margin': '10px'
                      })


def map_plot_component(df, filename, id='map-plot'):
    fig = px.line_geo(data_frame=df,
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
    fig.update_layout(height=800, width=1000, title=filename)

    return dcc.Graph(figure=fig, id=id)


def slider_component(df, id='slider'):
    # slider for waypoint index
    slider_marks = {
        i: f'{df.loc[i, "No"]}'
        for i in range(0, len(df), 10)  #if df.loc[i, 'Comment'].strip() != ''
    }
    return dcc.Slider(id=id,
                      min=0,
                      max=len(df.index) - 1,
                      step=1,
                      value=0,
                      marks=slider_marks,
                      tooltip={
                          'placement': 'bottom',
                          'always_visible': True
                      })


def mission_starttime_input(
        id=['mission-start-date', 'mission-start-time',
            'mission-time-submit']):
    time = datetime.datetime.now()

    return html.Div(children=[
        html.H5('Choose mission start time: \t', style={'margin': '5px'}),
        dcc.DatePickerSingle(id=id[0],
                             date=time.date(),
                             display_format='YYYY-MM-DD'),
        dcc.Input(id=id[1], type='text', value=time.strftime('%H:%M')),
        html.Button(id=id[2], children='Submit')
    ],
                    style={'display': 'flex'})
