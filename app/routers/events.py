import uuid

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from app.database import get_session
from app.dependencies import get_current_user
from app.models import EventDB, UserDB, WorkspaceDB
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import EventCreate, EventUpdate

router = APIRouter(prefix="/events", tags=["events"])
workspace_router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("/{event_id}")
def get_event(
    event_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    event = session.scalar(
        select(EventDB)
        .join(WorkspaceDB)
        .where(WorkspaceDB.owner_id == current_user.id, EventDB.id == event_id)
    )

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@workspace_router.post("/{workspace_id}/events")
def create_event(
    workspace_id: uuid.UUID,
    event: EventCreate,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    workspace = session.scalar(
        select(WorkspaceDB).where(
            WorkspaceDB.id == workspace_id, WorkspaceDB.owner_id == current_user.id
        )
    )

    if workspace is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found",
        )

    new_event = EventDB(
        workspace_id=workspace_id,
        name=event.name,
        venue=event.venue,
        starts_at=event.starts_at,
        rider=event.rider,
        stage_icons=event.stage_icons,
        stage_layout=event.stage_layout,
    )

    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return new_event


@workspace_router.get("/{workspace_id}/events")
def get_all_events(
    workspace_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    statement = (
        select(EventDB)
        .join(WorkspaceDB)
        .where(
            WorkspaceDB.owner_id == current_user.id,
            EventDB.workspace_id == workspace_id,
        )
    )

    events = session.scalars(statement).all()

    return events


@router.delete("/{event_id}")
def delete_event(
    event_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    event = session.scalar(
        select(EventDB)
        .join(WorkspaceDB)
        .where(EventDB.id == event_id, WorkspaceDB.owner_id == current_user.id)
    )

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    session.delete(event)
    session.commit()

    return {"message": "Event deleted"}


@router.patch("/{event_id}")
def update_event(
    event_id: uuid.UUID,
    event_update: EventUpdate,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    event = session.scalar(
        select(EventDB)
        .join(WorkspaceDB)
        .where(EventDB.id == event_id, WorkspaceDB.owner_id == current_user.id)
    )

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

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
        workspace = session.scalar(
            select(WorkspaceDB).where(
                WorkspaceDB.id == updates["workspace_id"],
                WorkspaceDB.owner_id == current_user.id,
            )
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
