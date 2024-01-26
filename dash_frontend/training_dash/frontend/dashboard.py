from dash import Dash, html
from .callbacks import init_callbacks
from .layouts import base_layout, app_layout


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/dash/",
        external_stylesheets=["static/css/styles.css",],
    )
    dash_app.title = "Slow Running App"
    dash_app.config.suppress_callback_exceptions = True

    # Create Dash Layout
    dash_app.layout = app_layout
    init_callbacks(dash_app)
    return dash_app.server
