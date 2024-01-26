from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from pandas import DataFrame


def smooth_scatter(df, x, y, label, color="black"):
    return px.scatter(
        df,
        x=x,
        y=y,
        trendline="rolling",
        labels={y: label},
        trendline_options={"window": 8},
        color_discrete_sequence=[color],
    )


def heart_rate_plot(activity_df):
    fig = px.line(
        activity_df, x="time", y="heartrate", color_discrete_sequence=["red"],
    )
    fig.add_hrect(y0=160, y1=180, fillcolor="red", opacity=0.2)
    return fig


def run_plots(activity_dict):
    activity_df = DataFrame.from_dict(activity_dict)
    return [
        dbc.Row(html.Div("Running App")),
        dbc.Row(
            children=[
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=px.line(activity_df, x="time", y="pace",),
                            id="activity-pace-graph",
                        )
                    ],
                    width=True,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=heart_rate_plot(activity_df), id="activity-hr-graph",
                        )
                    ],
                    width=True,
                ),
            ]
        ),
    ]


X_DICT = {
    "Distance": "Cumulative Distance / km",
    "Duration": "Cumulative Duration / min",
    "Runs": "Number of runs",
}


def update_mini_plots(x, df_dict):
    x = X_DICT[x]
    df = DataFrame.from_records(df_dict, index=range(len(df_dict)))
    return [
        dbc.Row(html.Div("Running App")),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=smooth_scatter(
                                df, x=x, y="pace", label="Average Pace min/km",
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
                                y="average_heartrate",
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
                                y="average_cadence",
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
                                df, x=x, y="calories", label="Calories", color="red",
                            ),
                            id="vo2-graph",
                        )
                    ],
                    width=True,
                ),
            ]
        ),
    ]
