# Import packages
from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime
import flask
import json
import requests

from .config import AppConfig
from .dashboard import init_dashboard

app_config = AppConfig()

# Initialize the app
# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
server = flask.Flask(__name__, static_folder="static/")
server = init_dashboard(server)


@server.route("/")
def login_check():
    if "strava_token" in flask.request.cookies:
        return flask.redirect("/dash")
    else:
        return flask.redirect("/login")


@server.route("/login")
def login_page():
    resp = requests.get(app_config.api_url + "strava-url/")
    strava_authorization_url = resp.json()["strava_url"]
    return flask.render_template(
        "login.html", strava_url=strava_authorization_url, title=app_config.app_title
    )


@server.route("/login-success")
def login_success():
    access_code = flask.request.args.get("code")
    resp = requests.get(
        app_config.api_url + "login/", params={"access_code": access_code}
    )
    token = resp.json()["token"]

    redirect_resp = flask.make_response(flask.redirect("/dash"))
    redirect_resp.set_cookie(key="strava_token", value=token)
    return redirect_resp


@server.route("/static/<path:filepath>")
def serve_res(filepath):
    return flask.send_from_directory("./", filepath)


@server.route("/user-settings", methods=["GET", "POST"])
def user_settings():
    if "strava_token" not in flask.request.cookies:
        server.logger.info("No token found, redirect to login")
        return flask.redirect("/login")
    resp = requests.get(
        app_config.api_url + "user-settings/",
        params={"token": flask.request.cookies["strava_token"]},
    )
    server.logger.info(resp)
    user_settings = resp.json()
    server.logger.info(user_settings)
    if flask.request.method == "GET":
        return flask.render_template(
            "settings.html",
            title=app_config.app_title,
            start_date=user_settings["start_date"],
            end_date=user_settings["end_date"],
        )
    else:
        form = flask.request.form
        server.logger.info(form)
        user_settings["start_date"] = datetime.fromisoformat(
            form["start_date"]
        ).isoformat()
        user_settings["end_date"] = datetime.fromisoformat(form["end_date"]).isoformat()
        server.logger.info(json.dumps(user_settings))
        resp = requests.post(
            app_config.api_url + "user-settings/",
            params={
                "token": flask.request.cookies["strava_token"],
            },
            data=json.dumps(user_settings),
        )
        return flask.redirect("/dash")
