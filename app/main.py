import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.database import SessionLocal
from app.models import EventDB, WorkspaceDB
from sqlalchemy import select
import datetime

app = FastAPI()


class WorkspaceCreate(BaseModel):
    name: str
    color: str

class WorkspaceUpdate(BaseModel):
    name: str | None = None
    color: str | None = None

class EventCreate(BaseModel):
    workspace_id: uuid.UUID
    name: str
    venue: str | None = None
    starts_at: datetime.datetime
    rider: list = Field(default_factory=list)
    stage_icons: list = Field(default_factory=list)
    stage_layout: dict | None = None

class EventUpdate(BaseModel):
    workspace_id: uuid.UUID | None = None
    name: str | None = None
    venue: str | None = None
    starts_at: datetime.datetime | None = None
    rider: list | None = None
    stage_icons: list | None = None
    stage_layout: dict | None = None



@app.get("/workspaces/{workspace_id}")  
def get_workspace(workspace_id: uuid.UUID):

    with SessionLocal() as session:
        workspace = session.get(WorkspaceDB, workspace_id)

        if workspace is None:
            raise HTTPException(
                status_code=404,
                detail="No workspace found"
            )

        return workspace


@app.get("/events/{event_id}")
def get_event(event_id: uuid.UUID):

    with SessionLocal() as session:
        event = session.get(EventDB, event_id)

        if event is None:
            raise HTTPException(
                status_code=404, 
                detail="Event not found"
            )

    
        return event

@app.post("/workspaces")
def create_workspace(workspace: WorkspaceCreate):

    with SessionLocal() as session:

        new_workspace = WorkspaceDB(
            name = workspace.name,
            color = workspace.color
        )

        session.add(new_workspace)
        session.commit()
        session.refresh(new_workspace)

        return new_workspace



@app.post("/events")
def create_event(event: EventCreate):

    with SessionLocal() as session:

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


@app.get("/workspaces")
def get_all_workspaces(name: str | None = None):
    with SessionLocal() as session:

        statement = select(WorkspaceDB)

        if name is not None:
            statement = statement.where(
                WorkspaceDB.name == name
            )

        workspaces = session.scalars(statement).all()

        return workspaces


@app.get("/events")
def get_all_events(workspace_id: uuid.UUID | None = None):

    with SessionLocal() as session:

        statement = select(EventDB)

        if workspace_id is not None:
            statement = statement.where(
                EventDB.workspace_id == workspace_id
            )

        events = session.scalars(statement).all()

        return events



@app.delete("/workspaces/{workspace_id}")
def delete_workspace(workspace_id: uuid.UUID):

    with SessionLocal() as session:
        workspace = session.get(WorkspaceDB, workspace_id)

        if workspace is None:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found"
            )

        session.delete(workspace)
        session.commit()

        return{"message" : "Workspace deleted"}



@app.delete("/events/{event_id}")
def delete_event(event_id: uuid.UUID):

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



@app.patch("/workspaces/{workspace_id}")
def update_workspace(workspace_id: uuid.UUID, workspace_update: WorkspaceUpdate):

    with SessionLocal() as session:

        workspace = session.get(WorkspaceDB, workspace_id)

        if workspace is None:
            raise HTTPException(
                status_code=404,
                detail="Workspace not found"
            )

        updates = workspace_update.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No updates provided"
            )

        for field in {"name", "color"}:
            if field in updates and updates[field] is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"{field} cannot be null",
                )

        for field, value in updates.items():
            setattr(workspace, field, value)

        session.commit()
        session.refresh(workspace)

        return workspace


@app.patch("/events/{event_id}")
def update_event(event_id: uuid.UUID, event_update: EventUpdate):

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

        