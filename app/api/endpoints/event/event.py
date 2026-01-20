from fastapi import APIRouter, HTTPException
from app.core.dependencies import sessionDependency
from asyncpg import Connection, UniqueViolationError, PostgresError
from app.schema.event import EventResponse, EventCreate

router = APIRouter(
    prefix='/event',
    tags=['event']
)


@router.get('/all')
async def get_events(conn: Connection = sessionDependency):
    """Fetch all the event"""
    try:
        rows = await conn.fetch("""
              SELECT * FROM events
          """)
        # Convert records to list of dict
        event = [dict(row) for row in rows]
        return event
    except PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get('/{event_id}')
async def get_event_byId(event_id: int, conn: Connection = sessionDependency):
    """Fetch event by ID"""
    try:
        row = await conn.fetchrow("""
              SELECT * FROM events WHERE event_id = $1
          """, event_id)
        if row:
            return dict(row)
        else:
            raise HTTPException(status_code=404, detail="Event not found")
    except PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.post('/create')
async def create_event(event: EventCreate, conn: Connection = sessionDependency):
    """Create a new event"""
    query = """
    INSERT INTO events (name, description, amount, start_time, end_time, date, location)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    """

    try:
        await conn.execute(
            query,
            event.name,
            event.description,
            event.amount,
            event.start_time,
            event.end_time,
            event.date,
            event.location
        )
    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="Event with the same name already exists.")
    except PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    return {"message": "Event created successfully"}
