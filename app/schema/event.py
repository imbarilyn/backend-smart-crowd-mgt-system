from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time


class EventCreate(BaseModel):
    name: str
    date: datetime
    start_time: time
    end_time: time
    location: str
    description: str
    amount: float


class EventResponse(BaseModel):
    event_id: str
    name: str
    created_at: datetime
