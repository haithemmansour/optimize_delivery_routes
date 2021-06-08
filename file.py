# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 23:50:56 2021

@author: Haythem
"""

import base64
import datetime
import io
import plotly.graph_objs as go

from jupyter_dash import JupyterDash
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
from datetime import date

import pandas as pd
from func import *
from Components import navbar , task

import arcgis
from arcgis.gis import GIS
import datetime
import getpass
from IPython.display import HTML

from arcgis import geocoding
from arcgis.features import Feature, FeatureSet
from arcgis.features import GeoAccessor, GeoSeriesAccessor

portal_url = 'https://www.arcgis.com'
#connect to your GIS
user_name = 'Mansour_Haythem_LearnArcGIS' # '<user_name>'
password = 'haithem1997' #'<password>'
my_gis = GIS(portal_url, user_name, password)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.title = "DASHBOARD"

#import location data 
data_df = pd.read_csv("data.csv")
routes_df = pd.read_csv('routes.csv')
depots_df = pd.read_csv('depots_df.csv')
x = "2021-03-20"

orders_df = orders_df_process(data_df, x)



colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

def update_data_df(routes_df, depots_df, data_df):

    out_stops_df= out_stops_df_process(depots_df,routes_df, orders_df, data_df, x )
    table = html.Div(
            [
                dash_table.DataTable(
                    data=out_stops_df.to_dict("rows"),
                    columns=[{"name": i, "id": i} for i in out_stops_df.columns],
                    page_size=12,
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[{
                                                'if': {'column_id': 'Region'},
                                                'textAlign': 'left'
                                            }],
                    style_table={'height': '300px','overflowY': 'auto'},
                ),
                html.Hr(),

            ]
        )

    return table
"""@app.callback(Output('Mygraph1', 'figure'), [
Input('upload-data', 'contents'),
Input('upload-data', 'filename') ])
def drawFigure(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])

        
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                        dcc.Graph(
            figure = go.Figure(data=[
            go.Bar(name=df.columns.values[0], x=pd.unique(df['Date']), y=df['TaskDurationSec'], text=df['Date'], textposition='auto'),
            ])
            ),  
            ])
        ),  
    ])
"""
def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])
# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2(["Text"], style = {'color' : 'red' }),
                ], style={'textAlign': 'left'}) 
            ])
        ),
    ])

# Data
df = px.data.iris()


# Build App
#app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])

app.layout = dbc.Container([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Col([navbar],style={
                                        "borderColor": "#8EA9C1",
                                       "boxShadow" : "0px 2px 5px 0px"})
                ], width=12),
               
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([

                    html.Div(id="output-optimase-upload") 
                ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginLeft": "15px",
                          "width": "600px",}),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    html.Div(id="output-route-upload") 
                ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginLeft": "15px",
                          "width": "600px",}),
            ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginLeft": "1.px",
                          "marginRight": "1px",
                          "padding" : "10px",}), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div(id="output-data-upload") 
                ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginRight": "15px",}, width=9),
                dbc.Col([
                    dbc.Col([task],style={
                                        "borderColor": "#8EA9C1",
                                       "boxShadow" : "0px 2px 5px 0px",})
                ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginLeft": "15px",
                          "width": "360px",
                          "height": "490px"}),
            ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginLeft": "1.px",
                          "marginRight": "1px",
                          "padding" : "10px",}),
            html.Br(),
             dbc.Row([
                dbc.Col([
                    html.H2("data frame :", className="card-title"),
                    html.Hr(),
                    #update_data_df(routes_df, depots_df, data_df)
                ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginRight": "15px",
                          "padding" : "10px"}, width=9),
                dbc.Col([
                    dbc.Col([task],style={
                                        "borderColor": "#8EA9C1",
                                       "boxShadow" : "0px 2px 5px 0px",})
                ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginLeft": "15px",
                          "width": "360px",
                          "height": "490px"}),
            ],style={ "borderColor": "#8EA9C1",
                          "boxShadow" : "0px 2px 5px 0px",
                          "marginLeft": "1.px",
                          "marginRight": "1px",
                          "padding" : "10px",}),
        ]), color = "#e9ecef"
    )
], fluid=True)
@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Input('date-picker', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%Y-%m-%d')
        return string_prefix + date_string

"""@app.callback(Output('MyMAP', 'figure'), [
Input('upload-data', 'contents'),
Input('upload-data', 'filename'),
])
def update_map (contents, filename):
    lon = []
    lat = []
    text = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        lon=df['pickup_longitude']
        lat=df['pickup_latitude']
        text=df['Round_Name']
    fig = go.Figure(data=go.Scattergeo(
    lon,
    lat, 
    text,
    mode='markers',
    ), 
    layout=go.Layout(height=1000, width=1200, 
                     title=go.layout.Title(text="task position map"))
        )

    fig.update_layout(
        geo_scope='europe',
        
        )
    return html.Div([
        dcc.Graph(id='example-map', figure=fig)
        ])"""

"""
@app.callback(Output('Mygraph', 'figure'), [
Input('upload-data', 'contents'),
Input('upload-data', 'filename'),
])
def update_graph(contents, filename):
    x = []
    y = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        x=df['Round_Name']
        y=df['distance']
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x, 
                y=y, 
                mode='lines+markers')
            ],
        layout=go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
        ))
    return fig
"""

def parse_data(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return df


@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents"), Input("upload-data", "filename"),Input('date-picker', 'date')],
)


def update_table(contents, filename , date_value):
    table = html.Div()
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%Y-%m-%d')
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.loc[df["Date"]  == date_string]
        df["Duration"]= cal_pred (df)
        df["depart_time"]= cal_depart_time(df)
        df['Arrive_time'] = cal_Arrive_time (df)
        table = html.Div(
            [
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_size=12,
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[{
                                                'if': {'column_id': 'Region'},
                                                'textAlign': 'left'
                                            }],
                    style_table={'height': '300px','overflowY': 'auto'},
                ),
                html.Hr(),

            ]
        )

    return table
@app.callback(
    Output("output-route-upload", "children"),
    [Input("upload-routes", "contents"), Input("upload-routes", "filename"),
     Input('date-picker', 'date')],
)


def update_routes(contents, filename, date_value):

    table1 = html.Div()
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%Y-%m-%d')

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.loc[df["Date"]  == date_string]

        table1 = html.Div(
            [
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_size=12,
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[{
                                                'if': {'column_id': 'Region'},
                                                'textAlign': 'left'
                                            }],
                    style_table={'height': '300px','overflowY': 'auto'},
                ),
                html.Hr(),
            ] 
        )

    return table1

@app.callback(
    Output("output-optimase-upload", "children"),
    [
    
     Input("upload-depots", "contents"), Input("upload-depots", "filename"),
    ]
)



def update_depots(contents, filename, ):
    table1 = html.Div()
    
        
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)


        table1 = html.Div(
            [
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_size=12,
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[{
                                                'if': {'column_id': 'Region'},
                                                'textAlign': 'left'
                                            }],
                    style_table={'height': '300px','overflowY': 'auto'},
                ),
                html.Hr(),
            ] 
        )

    return table1

if __name__ == "__main__":
    app.run_server(port=7000,debug=True)