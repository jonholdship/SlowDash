from fastapi import Request, HTTPException
from urllib.parse import urlencode

from dash_backend.api.api import app
from dash_backend.strava.strava_client import get_athlete_id


# @app.middleware("http")
# async def token_check(request: Request, call_next):
#     query_params = dict(request.query_params)
#     token = query_params.get("token", None)
#     if token:
#         try:
#             athlete_id = get_athlete_id(token)
#         except:
#             return HTTPException(401, "Token Expired")
#         query_params["athlete_id"] = athlete_id
#         request.scope["query_string"] = urlencode(query_params).encode("utf-8")
#     response = await call_next(request)
#     return response
