from fastapi import FastAPI
from app.core.modules import make_middleware, init_routers


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


