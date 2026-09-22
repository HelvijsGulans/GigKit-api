from pydantic import BaseModel, Field, ConfigDict
import datetime
import uuid


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

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    created_at: datetime.datetime