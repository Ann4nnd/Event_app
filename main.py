from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Event
from schemas import EventCreate
from typing import List

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Booking API!"}

# Получить список всех мероприятий
@app.get("/events", response_model=List[EventCreate])
def read_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

# Создать новое мероприятие
@app.post("/events", response_model=EventCreate)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    new_event = Event(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event
from fastapi import Path

# Получить детальную информацию о мероприятии
@app.get("/events/{event_id}", response_model=EventCreate)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Обновить мероприятие
@app.put("/events/{event_id}", response_model=EventCreate)
def update_event(event_id: int, updated_event: EventCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in updated_event.dict().items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

# Удалить мероприятие
@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}

# Пример списка мероприятий
events = []

@app.get("/events", response_model=List[dict])
def get_events():
    return events