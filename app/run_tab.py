from dash import html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px


def make_table(df):
    columns = [
        dict(id=col, name=col.capitalize(), format=dash_table.Format.Format())
        for col in df.columns
    ]
    return columns


def heart_rate_plot(activity_df):
    fig = px.line(
        activity_df,
        x="duration",
        y="directHeartRate",
        color_discrete_sequence=["red"],
    )
    fig.add_hrect(y0=160, y1=180, fillcolor="red", opacity=0.2)
    return fig


def run_plots(activity_df):
    return [
        dbc.Row(html.Div("Running App")),
        dbc.Row(
            children=[
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=px.line(
                                activity_df,
                                x="duration",
                                y=["pace", "elevationPace"],
                            ),
                            id="activity-pace-graph",
                        )
                    ],
                    width=True,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=heart_rate_plot(activity_df),
                            id="activity-hr-graph",
                        )
                    ],
                    width=True,
                ),
            ]
        ),
    ]


def runs_container(garmin_data):
    df = garmin_data.activity_summary
    header = make_table(df)
    return dbc.Container(
        [
            dbc.Row(
                id="single-activity-plots",
                children=run_plots(
                    garmin_data.get_activity_data(df.iloc[0]["activityId"])
                ),
            ),
            dash_table.DataTable(
                id="activity-selector-table",
                columns=header,
                data=df.to_dict("records"),
                page_size=30,
            ),
        ]
    )


def set_callbacks(garmin_data, app):
    @app.callback(
        Output("single-activity-plots", "children"),
        Input("activity-selector-table", "active_cell"),
        State("activity-selector-table", "data"),
        State("single-activity-plots", "children"),
    )
    def change_activity_plots(active_cell, data, old_plots):
        if active_cell:
            row = active_cell["row"]
            print(data[row])
            activity = data[row]["activityId"]
            return run_plots(garmin_data.get_activity_data(activity))
        else:
            return old_plots
