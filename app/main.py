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

class UpdateEvent(BaseModel):
    event_name: str | None = None
    event_date: str | None = None
    event_location: str | None = None
    event_description: str | None = None
    event_price: float |  None = None



@app.get("/events/{event_id}")
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



@app.get("/events")
def get_all_events(location: str | None = None):

    with open("app/database.json", "r") as f:
        data = json.load(f)

    if location is None:
        return data

    found_events = []

    for event in data:
        if event["event_location"] == location:
            found_events.append(event)

    return found_events



@app.delete("/events/{event_id}")
def delete_event(event_id: int):

    with open("app/database.json", "r") as f:
        data = json.load(f)

    for event in data:
        if event["event_id"] == event_id:
            data.remove(event)
            with open("app/database.json", "w") as f:
                json.dump(data, f, indent=4)

            return "Event deleted sucessfully"
    

    raise HTTPException(status_code=404, detail="Item not found")
        
    

@app.patch("/events/{event_id}")
def update_event(event_id : int, event_update : UpdateEvent):

    with open("app/database.json", "r") as f:
        data = json.load(f)

    for event in data:
        if event["event_id"] == event_id:
            update = event_update.model_dump(exclude_unset = True)

            event.update(update)

            with open("app/database.json", "w") as f:
                json.dump(data, f, indent=4)

            return event

    raise HTTPException(status_code=404, detail="No event found")
