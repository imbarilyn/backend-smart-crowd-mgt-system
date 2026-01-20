from fastapi import FastAPI
from app.core.modules import make_middleware, init_routers
from app.core.database import db


def create_app() -> FastAPI:
    print("Creating FastAPI application...")
    app_ = FastAPI(
        title="Smart Crowd Management System",
        verision="1.0.0",
        middleware=make_middleware()
    )
    init_routers(app_=app_)
    return app_


app = create_app()


@app.on_event("startup")
async def on_startup():
    print("Application startup tasks completed.")
    await db.connect()


@app.on_event("shutdown")
async def on_shutdown():
    print("Application shutdown tasks completed.")
    await db.disconnect()
