# Import packages
from dash import Dash, html, dcc, Output, Input

import dash_bootstrap_components as dbc
from app.training_tab import training_container, set_callbacks as set_training_callbacks
from app.run_tab import runs_container, set_callbacks as set_run_callbacks
from app.data import GarminHelper
import yaml

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Initialize the app
# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]


app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

garmin_helper = GarminHelper(**config)

# App layout
training_container = training_container(garmin_helper.activity_summary)
run_container = runs_container(garmin_helper)
set_training_callbacks(garmin_helper.activity_summary, app)
set_run_callbacks(garmin_helper, app)
app.layout = html.Div(
    [
        html.H1("Running Dashboard"),
        dcc.Tabs(
            id="tabs-example-graph",
            value="tab-1-example-graph",
            children=[
                dcc.Tab(label="My overview", value="overview-tab"),
                dcc.Tab(label="My Runs", value="run-tab"),
            ],
        ),
        html.Div(id="tabs-content-example-graph"),
    ]
)


@app.callback(
    Output("tabs-content-example-graph", "children"),
    Input("tabs-example-graph", "value"),
)
def render_content(tab):
    if tab == "overview-tab":
        return training_container
    elif tab == "run-tab":
        return run_container
