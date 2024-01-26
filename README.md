# Dads Dash App

A simple plotly dash webapp which logs into your Garmin Connect account, downloads your runs between some dates, and gives you a UI to interact with them.



## Run
To run the code, you'll need to set up a `.env`` file. There's an example at `example.env` which is just missing the Strava client details.

You can then launch the app with docker

```
docker-compose up
```

after which it should be available at `localhost:5000`.

## Code

### Backend
`dash_backend` is a FastAPI server which connects to the Strava API to get user activity data and stores it in a SQL database.

It is self contained with its own Dockerfile and can also be run locally using poetry.

### Frontend
`dash_frontend` is a Flask/Dash app which uses the backend to grab data and create plots of the user's training progress.


## To Do
**User Preferences** - start and end dates should be added to the user table on the backend so the user can look at training over a period. We need a section in the front end to select this as well as set things like the normal HR range for the user.