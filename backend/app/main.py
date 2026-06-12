from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes_system import router as system_router
from app.api.routes_game import router as game_router
from app.api.routes_agents import router as agents_router


app = FastAPI(
    title=settings.app_name,
    description="Baymax AI-vs-AI Chess Arena Backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Baymax backend is running",
        "docs": "/docs",
        "health": "/system/health",
        "game_api": "/game/new",
        "agents_api": "/agents",
    }


app.include_router(system_router)
app.include_router(game_router)
app.include_router(agents_router)