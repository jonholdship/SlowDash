import uvicorn
from .api.api import app
from dash_backend.config import ApiConfig

if __name__ == "__main__":
    config = ApiConfig()
    uvicorn.run(app, port=config.port, host="0.0.0.0")
