from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import connect_to_db

app = FastAPI()


class Event(BaseModel):
    name: str
    date: str
    location: str
    description: str | None = None
    price: float | None = None


class UpdateEvent(BaseModel):
    name: str | None = None
    date: str | None = None
    location: str | None = None
    description: str | None = None
    price: float | None = None


@app.get("/events/{event_id}")
def get_event(event_id: int):

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))

    event = cur.fetchone()

    conn.close()
    cur.close()

    if event is None:
        raise HTTPException(status_code=404, detail="Item not found")

    else:
        return event


@app.post("/events")
def create_event(event: Event):

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO events 
        (name, date, location, description, price) 
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING *;
        """,
        (event.name, event.date, event.location, event.description, event.price))

    new_event = cur.fetchone()

    conn.commit()

    conn.close()
    cur.close()

    return new_event


@app.get("/events")
def get_all_events(location: str | None = None):

    conn = connect_to_db()
    cur = conn.cursor()

    if location is None:
        cur.execute("SELECT * FROM events;")
        events = cur.fetchall()

        conn.close()
        cur.close()

        return events

    cur.execute("SELECT * FROM events WHERE location = %s", (location,))

    found_events = cur.fetchall()

    conn.close()
    cur.close()

    return found_events


@app.delete("/events/{event_id}")
def delete_event(event_id: int):

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM events WHERE id = %s RETURNING *;", (event_id,))

    deleted_row = cur.fetchone()

    if deleted_row is None:
        conn.close()
        cur.close()
        raise HTTPException(status_code=404, detail="Event not found")

    conn.commit()

    conn.close()
    cur.close()

    return {"message": f"Deleted {deleted_row}"}


@app.patch("/events/{event_id}")
def update_event(event_id: int, event_update: UpdateEvent):

    conn = connect_to_db()
    cur = conn.cursor()

    updates = event_update.model_dump(exclude_unset=True)

    if not updates:
        cur.close()
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="No details provided"
        )

    set_clause = ", ".join(
        f"{column} = %s"
        for column in updates
    )

    values = list(updates.values())
    values.append(event_id)

    cur.execute(
        f"""
            UPDATE events SET {set_clause}
            WHERE id = %s
            RETURNING *
            """, 
            values
        )

    updated_event = cur.fetchone()

    if updated_event is None:
        conn.close()
        cur.close()
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    conn.commit()

    conn.close()
    cur.close()

    return updated_event

