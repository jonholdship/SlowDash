import uvicorn
from dash_backend.config import ApiConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dash_backend.api.routers.user import router as user_router
from dash_backend.api.routers.activities import router as activities_router

if __name__ == "__main__":
    config = ApiConfig()
    
    app = FastAPI()

    # CORS settings: allow frontend (with cookies) to call the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(user_router)
    app.include_router(activities_router)

    uvicorn.run(app, port=config.port, host="0.0.0.0")
