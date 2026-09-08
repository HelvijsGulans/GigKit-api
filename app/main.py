from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class Event(BaseModel):
    event_name: str
    event_date: str
    event_location: str
    event_description: str | None = None
    event_price: float |  None = None

@app.get("/event/{event_id}")
def get_event(event_id: int):
    with open("app/database.json") as f:
        data = json.load(f)
    for event in data:
        if event["event_id"] == event_id:
            return event
        
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/events")
def create_event(event: Event):

    with open("app/database.json", "r") as f:
        data = json.load(f)

    new_event = event.model_dump()

    new_event["event_id"] = len(data) + 1

    data.append(new_event)

    with open("app/database.json", "w") as f:
        json.dump(data, f, indent=4)

    return new_event
    