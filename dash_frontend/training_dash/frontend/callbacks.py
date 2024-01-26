from dash import Input, Output, State
from flask import request as flask_request
import requests

from .layouts import app_layout, runs_container, training_container
from .plots import run_plots, update_mini_plots
from .config import AppConfig


def init_callbacks(dash_app):
    app_config = AppConfig()

    @dash_app.callback(
        Output("tabs-content-example-graph", "children"),
        Input("tabs-example-graph", "value"),
    )
    def render_content(tab):
        strava_token = flask_request.cookies["strava_token"]
        if tab == "overview-tab":
            return training_container
        elif tab == "run-tab":
            df_records = requests.get(
                app_config.api_url + "activities-summary/",
                params={"token": strava_token},
            ).json()
            return runs_container(df_records)

    @dash_app.callback(
        Output("mini-plots", "children"), Input("x-picker", "value"),
    )
    def training_tab_updater(x):
        strava_token = flask_request.cookies["strava_token"]
        df_dict = requests.get(
            app_config.api_url + "activities-summary/", params={"token": strava_token}
        ).json()
        return update_mini_plots(x, df_dict)

    @dash_app.callback(
        Output("single-activity-plots", "children"),
        Input("activity-selector-table", "active_cell"),
        State("activity-selector-table", "data"),
        State("single-activity-plots", "children"),
    )
    def change_activity_plots(active_cell, data, old_plots):
        strava_token = flask_request.cookies["strava_token"]
        if active_cell:
            row = active_cell["row"]
            activity_id = data[row]["id"]
            activity_dict = requests.get(
                app_config.api_url + "activity/",
                params={"activity_id": activity_id, "token": strava_token},
            ).json()
            return run_plots(activity_dict)
        else:
            return old_plots
