from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import EventDB
from sqlalchemy import select
import datetime

app = FastAPI()


class EventCreate(BaseModel):
    name: str
    date: datetime.date
    location: str
    description: str | None = None
    price: float | None = None


class UpdateEvent(BaseModel):
    name: str | None = None
    date: datetime.date| None = None
    location: str | None = None
    description: str | None = None
    price: float | None = None


@app.get("/events/{event_id}")
def get_event(event_id: int):

    with SessionLocal() as session:
        event = session.get(EventDB, event_id)

        if event is None:
            raise HTTPException(
                status_code=404, 
                detail="Item not found"
            )

    
        return event


@app.post("/events")
def create_event(event: EventCreate):

    with SessionLocal() as session:

        new_event = EventDB(
                name = event.name,
                location = event.location,
                date = event.date,
                description = event.description,
                price = event.price
            )

        session.add(new_event)
        session.commit()
        session.refresh(new_event)

        return new_event


@app.get("/events")
def get_all_events(location: str | None = None):

    with SessionLocal() as session:

        statement = select(EventDB)

        if location is not None:
            statement = statement.where(
                EventDB.location == location
            )

        events = session.scalars(statement).all()

        return events


@app.delete("/events/{event_id}")
def delete_event(event_id: int):

    with SessionLocal() as session:
        event = session.get(EventDB, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )
        
        
        session.delete(event)
        session.commit()

        return {"message" : "Event deleted"}




@app.patch("/events/{event_id}")
def update_event(event_id: int, event_update: UpdateEvent):

    with SessionLocal() as session:

        event = session.get(EventDB, event_id)

        if event is None:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        updates = event_update.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="Updates not provided"
            )

        for field, value in updates.items():
            setattr(event, field, value)
 
        session.commit()
        session.refresh(event)

        return event

        