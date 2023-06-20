# Import packages
from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# Initialize the app
# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]

db = SQLAlchemy()

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)

app.title = "Slow Running App"
app.config.suppress_callback_exceptions = True

db_name = "data/user_data.db"

server = app.server
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name

server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# initialize the app with Flask-SQLAlchemy
db.init_app(server)
