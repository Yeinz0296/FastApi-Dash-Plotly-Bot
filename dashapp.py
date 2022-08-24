from dash import dash, html, dcc, Output, Input
import pandas as pd, numpy as np
from plotly import graph_objects as go, express as px


app = dash.Dash(__name__, requests_pathname_prefix="/dashboard/", title='Dashboard',)
app.title = "fastApi to Google Sheet data with telegram bot"

# def server_layout():
    
#     return html.Div(
#             children=[
#                 html.H1(children='FastApi to Google Sheet data with telegram bot'),
#                 html.Div(children='''FastApi to Google Sheet data with telegram bot by Hazrien'''),
#                 dcc.Graph(id='TvT'),
#                 dcc.Interval(id='interval-component',interval=1*1000,n_intervals=0)
#             ])

# app.layout = server_layout

app.layout = html.Div(
    children=[
    html.H1(children='FastApi to Google Sheet data with telegram bot'),

    html.Div(children='''
        FastApi to Google Sheet data with telegram bot
        
        by Hazrien
    '''),
    
    # GRAPH SECTION
    dcc.Dropdown(
        ['Temperature','Humidity'],
        'Temperature',
        id='dropdown'
    ),
    dcc.Graph(id='TvT'),

    dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
    )
])

@app.callback(
    Output('TvT','figure'),
    [Input('interval-component', 'n_intervals'),
    Input('dropdown', 'value'),])
def update_graph(interval, value):
    dataframe = pd.read_csv("fastdata.csv")
    fig = px.line(dataframe, x='Timestamp', y=value, title='{} vs time'.format(value))
    return fig
# app.run_server(debug=True, threaded=True)