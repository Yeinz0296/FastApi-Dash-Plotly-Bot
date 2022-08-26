from dash import dash, html, dcc, Output, Input
import pandas as pd
from plotly import express as px
from datetime import date

dataframe = pd.read_csv("fastdata.csv")
# timestamp = dataframe['Timestamp']
# dataframe['Dates'] = pd.to_datetime(timestamp).dt.strftime('%m/%d/%Y')

app = dash.Dash(__name__, requests_pathname_prefix="/history/", title='Historical Dashboard',)
app.title = "fastApi to Google Sheet data with telegram bot"

app.layout = html.Div(
    
    children=[
    html.H1(children='FastApi to Google Sheet data with telegram bot by Hazrien Nazman'),

    html.Div(children='''
    HISTORICAL DATA
    '''),

    # Dropdown
    html.Div(
        children=[
            dcc.Dropdown(
            ['Temperature','Humidity'],
            'Temperature',
            id='dropdown'),
        ]
    ),

    # Date Picker
    html.Div(
        children=[
        dcc.DatePickerRange(
            id='daterange',
            # min_date_allowed=date(2022, 8, 1),
            # max_date_allowed=date(2022, 9, 1),
            # start_date=date(2022, 8, 21),
            # end_date=date(2022, 8, 24)
            min_date_allowed=dataframe['Timestamp'].min(),
            max_date_allowed=dataframe['Timestamp'].max(),
            start_date=date(2022, 8, 21),
            end_date=date(2022, 8, 26)
        ),
        ]
    ),
    
    # GRAPH SECTION
    html.Div(
        children=[
        dcc.Graph(id='TvT'),
        ]
    ),

    #Auto Refresh
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
    )
])

@app.callback(
    Output('TvT','figure'),
    #[Input('interval-component', 'n_intervals'),
    [Input('dropdown', 'value'),
    Input("daterange", "start_date"),
    Input("daterange", "end_date"),])
def update_graph(value, start_date, end_date):
    # timestamp = dataframe['Timestamp']

    # dataframe['Dates'] = pd.to_datetime(timestamp).dt.strftime('%m/%d/%Y')

    start_date_object = date.fromisoformat(start_date)
    start_date_string = start_date_object.strftime('%m/%d/%Y')
    
    end_date_object = date.fromisoformat(end_date)
    end_date_string = end_date_object.strftime('%m/%d/%Y')
    
    dataframe = pd.read_csv("fastdata.csv")
    mask = (dataframe['Timestamp'] >= start_date_string) & (dataframe['Timestamp'] <= end_date_string)
    # mask = (dataframe['Timestamp'] >= start_date) & (dataframe['Timestamp'] <= end_date)
    dataframe2 = dataframe.loc[mask]

    fig = px.line(dataframe2, x='Timestamp', y=value, title='{} vs time'.format(value))
    return fig
# app.run_server(debug=True, threaded=True)