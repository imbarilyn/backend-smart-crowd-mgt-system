from fastapi import APIRouter
from app.api.endpoints.ticket.ticket import router as ticket_router


router = APIRouter()
router.include_router(ticket_router)