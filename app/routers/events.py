import uuid

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from app.database import get_session
from app.models import EventDB, WorkspaceDB
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import EventCreate, EventUpdate


router = APIRouter(
    prefix="/events",
    tags=["events"]
)



@router.get("/{event_id}")
def get_event(event_id: uuid.UUID, session: Session = Depends(get_session)):

    event = session.get(EventDB, event_id)

    if event is None:
        raise HTTPException(
            status_code=404, 
            detail="Event not found"
        )


    return event





@router.post("")
def create_event(event: EventCreate, session: Session = Depends(get_session)):

    workspace = session.get(WorkspaceDB, event.workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found",
        )

    new_event = EventDB(
            workspace_id = event.workspace_id,
            name = event.name,
            venue = event.venue,
            starts_at = event.starts_at,
            rider = event.rider,
            stage_icons = event.stage_icons,
            stage_layout = event.stage_layout
            
        )

    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return new_event




@router.get("")
def get_all_events(workspace_id: uuid.UUID | None = None, session: Session = Depends(get_session)):

    statement = select(EventDB)

    if workspace_id is not None:
        statement = statement.where(
            EventDB.workspace_id == workspace_id
        )

    events = session.scalars(statement).all()

    return events





@router.delete("/{event_id}")
def delete_event(event_id: uuid.UUID, session: Session = Depends(get_session)):

    event = session.get(EventDB, event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )
    
    
    session.delete(event)
    session.commit()

    return {"message" : "Event deleted"}




@router.patch("/{event_id}")
def update_event(event_id: uuid.UUID, event_update: EventUpdate, session: Session = Depends(get_session)):

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
            detail="Updates not provided",
        )

    non_nullable_fields = {
        "workspace_id",
        "name",
        "starts_at",
        "rider",
        "stage_icons",
    }

    for field in non_nullable_fields:
        if field in updates and updates[field] is None:
            raise HTTPException(
                status_code=400,
                detail=f"{field} cannot be null",
            )

    if "workspace_id" in updates:
        workspace = session.get(
            WorkspaceDB,
            updates["workspace_id"],
        )

        if workspace is None:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found",
            )

    for field, value in updates.items():
        setattr(event, field, value)

    session.commit()
    session.refresh(event)

    return event

        