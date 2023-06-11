import plotly.express as px


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
