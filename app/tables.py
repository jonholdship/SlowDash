from dash import dash_table

TABLE_COLS = {
    "name": "Name",
    "start_date": "Date",
    "distance": "Distance",
    "pace": "Pace",
    "average_heartrate": "Average HR",
    "average_cadence": "Cadence",
    "moving_time": "Running Time",
    "elapsed_time": "Total Time",
    "total_elevation_gain": "Total Elevation Gain",
}


def make_table():
    columns = [
        dict(id=col, name=name, format=dash_table.Format.Format())
        for col, name in TABLE_COLS.items()
    ]
    return columns
