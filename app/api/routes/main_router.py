from fastapi import APIRouter
from app.api.endpoints.event.event import router as event_router


router = APIRouter()
router.include_router(event_router)