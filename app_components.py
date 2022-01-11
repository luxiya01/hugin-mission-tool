from dash import html, dcc
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import plotly.express as px
import datetime


def upload_mission_file_component(id='upload-mission-file'):
    return dcc.Upload(
        id=id,
        children=['Drag and Drop or ',
                  html.A('Select a Mission File (.mp)')],
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


def map_component(id=['map', 'geojson']):
    return html.Div(dl.Map(children=[
        dl.LayersControl([
            dl.BaseLayer(dl.TileLayer(
                url=
                'https://maps.nbp.usap.gov/maptiles/osm-intl/{z}/{x}/{y}.png',
                maxZoom=13),
                         name='OpenStreetMap',
                         checked=True)
        ] + [
            dl.Overlay(dl.TileLayer(
                url=
                'https://maps.nbp.usap.gov/maptiles/ocean_tiles/{z}/{y}/{x}.png',
                maxZoom=13),
                       name='Ocean Features Layer',
                       checked=True),
            dl.Overlay(dl.TileLayer(
                url=
                'https://maps.nbp.usap.gov/maptiles/label_tiles/{z}/{y}/{x}.png',
                maxZoom=13),
                       name='Labels Layer',
                       checked=True),
            dl.Overlay(dl.TileLayer(
                url=
                'https://maps.nbp.usap.gov/maptiles/Bathymetry/{z}/{x}/{y}.png',
                maxZoom=13),
                       name='Bathymetry',
                       checked=True),
            dl.Overlay(dl.GeoTIFFOverlay(url='./assets/20220107_MODIS.tiff'),
                       name='MODIS',
                       checked=False),
            dl.Overlay(dl.GeoTIFFOverlay(
                url='./assets/Antarctic_AMSR2_2022_01_09.tif'),
                       name='AMSR2',
                       checked=False),
        ],
                         id=id[0]),
        dl.GeoJSON(data=None, id=id[1])
    ],
                           zoom=1,
                           center=(-60, -70)),
                    style={'height': '100vh'},
                    id='map-div')


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
        dbc.Col(html.H5('Choose mission start time: \t',
                        style={'margin': '5px'}),
                width=12),
        dbc.Row([
            dbc.Col(dcc.DatePickerSingle(
                id=id[0], date=time.date(), display_format='YYYY-MM-DD'),
                    width=2),
            dbc.Col(dcc.Input(
                id=id[1], type='text', value=time.strftime('%H:%M')),
                    width=2),
            dbc.Col(html.Button(id=id[2], children='Submit'), width=1)
        ])
    ])
