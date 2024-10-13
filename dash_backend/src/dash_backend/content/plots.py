import pandas as pd


def training_summaries(activities: pd.DataFrame) -> dict:
    """Takes the activities summary dataframe
    and formats to the per point dictionaries needed
    for js plots.

    :param activities: DataFrame of models.Activity objects
    :return: dictionary for plotting
    """
    plots = {}
    activities["x"] = activities["start_date"]
    activities["y"] = activities["pace"]
    plots["pace_plot"] = activities[["x", "y"]].to_dict(orient="records")
    activities["y"] = activities["average_heartrate"]
    plots["hr_plot"] = activities[["x", "y"]].to_dict(orient="records")
    return plots
