# Dads Dash App

A simple plotly dash webapp which logs into your Garmin Connect account, downloads your runs between some dates, and gives you a UI to interact with them.

## Set Up

Use pip to install the required libraries

```
pip install requirements.txt
```
and then use the `example-config.yaml` file to produce your own file called `config.yaml`. Fill out the details specified in the example.

## Run

You can run with

```
python ./run.py
```
and then access the app at `localhost:8050` in your browser.