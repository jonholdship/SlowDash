# Import packages
from dash import Dash
import dash_bootstrap_components as dbc


# Initialize the app
# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]


app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
app.title = "Slow Running App"
app.config.suppress_callback_exceptions = True
