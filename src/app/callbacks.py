from urllib.parse import parse_qs

from dash import Input, Output, State
from stravalib import Client

from . import settings
from .layouts import app_layout, strava_login_layout, runs_container, training_container
from .plots import run_plots, update_mini_plots
from .server import app
from .user import User
from .settings import START_DATE, END_DATE


@app.callback(
    output=[
        Output("body", "children"),
        Output("strava-auth", "data"),
    ],
    inputs=[Input("url", "search")],
    state=[State("strava-auth", "data")],
)
def display_page(query_string, strava_auth):
    if strava_auth is None:
        strava_auth = {}

    body = strava_login_layout

    if strava_auth.get("authenticated", False):
        body = app_layout
    elif query_string is not None:
        query = parse_qs(str(query_string[1:]))
        if "code" in query:
            client = Client()
            response = client.exchange_code_for_token(
                client_id=settings.STRAVA_CLIENT_ID,
                client_secret=settings.STRAVA_CLIENT_SECRET,
                code=query["code"],
            )
            strava_auth.update(response)
            strava_auth["authenticated"] = True
            body = app_layout

    return body, strava_auth


@app.callback(
    output=[
        Output("app-layout-body", "children"),
    ],
    inputs=[Input("strava-auth", "data")],
)
def app_layout_body(strava_auth):
    client = Client(access_token=strava_auth["access_token"])
    athlete = client.get_athlete()
    return [f"Welcome, dear {athlete.firstname} {athlete.lastname}"]


@app.callback(
    Output("tabs-content-example-graph", "children"),
    Input("tabs-example-graph", "value"),
    State("strava-auth", "data"),
)
def render_content(tab, strava_auth):
    if tab == "overview-tab":
        return training_container
    elif tab == "run-tab":
        user = User(strava_auth)
        df = user.get_activities_summary(settings.START_DATE, settings.END_DATE)
        return runs_container(df)


@app.callback(
    Output("mini-plots", "children"),
    Input("x-picker", "value"),
    State("strava-auth", "data"),
)
def training_tab_updater(x, strava_auth):
    user = User(strava_auth)
    df = user.get_activities_summary(settings.START_DATE, settings.END_DATE)
    return update_mini_plots(x, df)


@app.callback(
    Output("single-activity-plots", "children"),
    Input("activity-selector-table", "active_cell"),
    State("activity-selector-table", "data"),
    State("single-activity-plots", "children"),
    State("strava-auth", "data"),
)
def change_activity_plots(active_cell, data, old_plots, strava_auth):
    user = User(strava_auth)
    if active_cell:
        row = active_cell["row"]
        activity = data[row]["id"]
        df = user.get_activity_data(activity)
        print(df.iloc[0])
        return run_plots(df)
    else:
        return old_plots
