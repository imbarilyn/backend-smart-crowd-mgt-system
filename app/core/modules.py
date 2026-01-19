from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import FastAPI
from app.api.routes.main_router import router
def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def make_middleware() -> List[Middleware]:
    origins = ["http://localhost:5173", "*"]
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
    return middleware
