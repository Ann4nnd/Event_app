from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: str
    date: datetime
    available_spots: int

class EventCreate(EventBase):
    pass
