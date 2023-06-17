from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from stravalib import Client

from . import settings
from .server import app
from .tables import make_table


app.layout = html.Div(
    [
        dcc.Store(id="strava-auth", storage_type="session"),
        dcc.Location(id="url", refresh=False),
        html.H1(children="Slow Running App"),
        html.Div(id="body"),
    ]
)

app_layout = html.Div(
    [
        html.H1("Running Dashboard"),
        dcc.Tabs(
            id="tabs-example-graph",
            value="overview-tab",
            children=[
                dcc.Tab(label="My overview", value="overview-tab"),
                dcc.Tab(label="My Runs", value="run-tab"),
            ],
        ),
        html.Div(id="tabs-content-example-graph"),
    ]
)

client = Client()
strava_authorization_url = client.authorization_url(
    client_id=settings.STRAVA_CLIENT_ID,
    redirect_uri=settings.APP_URL,
    state="strava-dash-app",
)

strava_login_layout = html.Div(
    [
        html.A(
            html.Img(src="static/btn_strava_connectwith_orange.png"),
            "Connect with Strava",
            href=strava_authorization_url,
        )
    ]
)


def runs_container(df):
    return dbc.Container(
        [
            dbc.Row(
                id="single-activity-plots",
            ),
            dash_table.DataTable(
                id="activity-selector-table",
                columns=make_table(df),
                data=df.to_dict("records"),
                page_size=30,
            ),
        ]
    )


training_container = dbc.Container(
    [
        dbc.Row(html.Div("Running App")),
        dcc.RadioItems(
            options=["Distance", "Duration", "Runs"],
            value="Distance",
            inline=True,
            id="x-picker",
        ),
        html.Div(id="mini-plots"),
    ]
)
