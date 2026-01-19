from fastapi import APIRouter


router = APIRouter(
    prefix='/tickets',
    tags=['tickets']
)


@router.get('/')
def get_tickets():
    return {"message": "List of available tickets"}

