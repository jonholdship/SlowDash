# SlowDash

A simple web app which allows users to log in with their Strava account and view stats and details.

## Run

To run the code, you'll need to set up a `.env` file. There's an example at `example.env` which is just missing the Strava client details.

You can then build and launch the app with docker

```
docker-compose build --parallel
docker-compose up
```

after which it should be available at `localhost:3000`.

## Code

### Backend

`dash_backend` is a FastAPI server which connects to the Strava API to get user activity data and stores it in a SQL database.

It is self contained with its own Dockerfile and can also be run locally using poetry.

### Frontend

`dash_frontend` is a react app which uses the backend to grab data and create plots of the user's training progress.
