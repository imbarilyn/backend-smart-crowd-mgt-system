from fastapi import APIRouter
from app.api.endpoints.event.event import router as event_router
from app.api.endpoints.payments.payments import router as payments_router


router = APIRouter()
all_routes = [event_router, payments_router]
for i in all_routes:
    router.include_router(i)