import requests
import json

user_settings = {
    "athlete_id": 0,
    "start_date": "2024-04-20",
    "end_date": "2024-04-20",
}
print(json.dumps(user_settings))
requests.post(
    "http://localhost:8000/user-settings",
    params={"token": "hi"},
    data=json.dumps(user_settings),
)
