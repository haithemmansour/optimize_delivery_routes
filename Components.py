# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 18:22:30 2021

@author: Haythem
"""

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash

from datetime import datetime as dt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

navbar = dbc.Navbar(
    [
        
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Transporter Route", className="layout_title")),     
                    dbc.Col(dcc.Upload( id="upload-data",
                                        children=dbc.Button("Upload Tasks Table", outline=True, color="info",
                                                                className="btn btn-outline-primary", size = 'sm',
                                                                style ={'width': '150px',
                                                                        'height': '60px'}),
                                         style={
                                            'width': '100%',
                                            'height': '80%',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'margin': '10px',
                                            'paddingLeft' : '10px'
                                            },
                                        # Allow multiple files to be uploaded
                                        multiple=True,
                                                    ),),
                    dbc.Col(dcc.Upload( id="upload-routes",
                                        children=dbc.Button("Upload routes Table", outline=True, color="info",
                                                                className="btn btn-outline-primary", size = 'sm',
                                                                style ={'width': '150px',
                                                                        'height': '60px'}),
                                         style={
                                            'width': '100%',
                                            'height': '80%',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'margin': '10px',
                                            'paddingLeft' : '10px'
                                            },
                                        # Allow multiple files to be uploaded
                                        multiple=True,
                                                    ),),
                    dbc.Col(dcc.Upload( id="upload-depots",
                                        children=dbc.Button("Upload depots Table", outline=True, color="info",
                                                                className="btn btn-outline-primary", size = 'sm',
                                                                style ={'width': '150px',
                                                                        'height': '60px'}),
                                         style={
                                            'width': '100%',
                                            'height': '80%',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'margin': '10px',
                                            'paddingLeft' : '10px'
                                            },
                                        # Allow multiple files to be uploaded
                                        multiple=True,
                                                    ),),
                    
                                            ],
                                            align="center",
                                            no_gutters=True,
                                        ),
                    dbc.Col(
                            [html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2021, 1, 1),
                                    max_date_allowed=dt(2021, 3, 31),
                                    initial_visible_month=dt(2021, 1, 1),
                                    date=dt(2021, 1, 1).date(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                ),
                                html.Div(id='output-container-date-picker-single')
                            ],
                        ),],
                                  style={
                                           'width': '400px',}),
                    dbc.Col([html.Img(src=app.get_asset_url('redlean.jfif'), height="50px", className="rounded float-right"  )] ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    className = "layout-header",
    
)
html.Div(id="output-data-upload")
task = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title"),
            html.H6("Card subtitle", className="card-subtitle"),
            html.P(
                "Some quick example text to build on the card title and make "
                "up the bulk of the card's content.",
                className="card-text",
            ),
            #html.Div(id="output-data-upload"),
            #dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
    style={"width": "100%", },
    className="rounded float-right",
    color = "#e9ecef"
    )