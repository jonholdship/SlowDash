from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from app.plots import smooth_scatter


X_DICT = {
    "Distance": "Cumulative Distance / km",
    "Duration": "Cumulative Duration / min",
    "Runs": "Number of runs",
}


def training_container(df):
    return dbc.Container(
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


def set_callbacks(df, app):
    @app.callback(
        Output("mini-plots", "children"),
        Input("x-picker", "value"),
    )
    def miniplot(x):
        return update_mini_plots(X_DICT[x], df)


def update_mini_plots(x, df):
    print("hi")
    return [
        dbc.Row(html.Div("Running App")),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=smooth_scatter(
                                df,
                                x=x,
                                y="pace",
                                label="Average Pace min/km",
                            ),
                            id="pace-graph",
                        )
                    ],
                    width=True,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=smooth_scatter(
                                df,
                                x=x,
                                y="averageHR",
                                label="Average HR",
                                color="red",
                            ),
                            id="hr-graph",
                        )
                    ],
                    width=True,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=smooth_scatter(
                                df,
                                x=x,
                                y="averageRunningCadenceInStepsPerMinute",
                                label="Average Cadence steps/min",
                            ),
                            id="cadence-graph",
                        )
                    ],
                    width=True,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=smooth_scatter(
                                df,
                                x=x,
                                y="vO2MaxValue",
                                label="vO2 Max",
                                color="red",
                            ),
                            id="vo2-graph",
                        )
                    ],
                    width=True,
                ),
            ]
        ),
    ]
