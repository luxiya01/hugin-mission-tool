import dash
from dash import html
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign

cities = [dict(name='Aalborg', lat=57.026, lon=9.837, property1=1)]
geojson = dlx.dicts_to_geojson([{
    **c,
    **dict(tooltip=c['name'])
} for c in cities])
print(geojson)

app = dash.Dash()

server = app.server

point_to_layer = assign(
    "function(feature, latlng, context) {return L.circleMarker(latlng);}")
geojson_points = dl.GeoJSON(data=geojson,
                            options=dict(pointToLayer=point_to_layer))

app.layout = html.Div(dl.Map(children=[
    dl.TileLayer(
        url='https://maps.nbp.usap.gov/maptiles/osm-intl/{z}/{x}/{y}.png',
        maxZoom=9), geojson_points
]),
                      style={'height': '100vh'})

if __name__ == '__main__':
    app.run_server(debug=True)  #, dev_tools_props_check=False)
