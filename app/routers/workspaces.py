import uuid

from fastapi import HTTPException, APIRouter, Depends
from app.database import get_session
from app.dependencies import get_current_user
from app.models import EventDB, UserDB, WorkspaceDB
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas import WorkspaceCreate, WorkspaceUpdate

router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"],
)


@router.get("/{workspace_id}")
def get_workspace(
    workspace_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    workspace = session.scalar(
        select(WorkspaceDB).where(
            WorkspaceDB.id == workspace_id, WorkspaceDB.owner_id == current_user.id
        )
    )

    if workspace is None:
        raise HTTPException(status_code=404, detail="No workspace found")

    return workspace


@router.post("", status_code=201)
def create_workspace(
    workspace: WorkspaceCreate,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    new_workspace = WorkspaceDB(
        name=workspace.name, color=workspace.color, owner_id=current_user.id
    )

    session.add(new_workspace)
    session.commit()
    session.refresh(new_workspace)

    return new_workspace


@router.get("")
def get_all_workspaces(
    name: str | None = None,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    statement = select(WorkspaceDB).where(WorkspaceDB.owner_id == current_user.id)

    if name is not None:
        statement = statement.where(WorkspaceDB.name == name)

    workspaces = session.scalars(statement).all()

    return workspaces


@router.delete("/{workspace_id}")
def delete_workspace(
    workspace_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    workspace = session.scalar(
        select(WorkspaceDB).where(
            WorkspaceDB.id == workspace_id, WorkspaceDB.owner_id == current_user.id
        )
    )

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    event = session.scalar(select(EventDB).where(EventDB.workspace_id == workspace_id))

    if event is not None:
        raise HTTPException(status_code=409, detail="Workspace still contains events")

    session.delete(workspace)
    session.commit()

    return {"message": "Workspace deleted"}


@router.patch("/{workspace_id}")
def update_workspace(
    workspace_id: uuid.UUID,
    workspace_update: WorkspaceUpdate,
    session: Session = Depends(get_session),
    current_user: UserDB = Depends(get_current_user),
):

    workspace = session.scalar(
        select(WorkspaceDB).where(
            WorkspaceDB.id == workspace_id, WorkspaceDB.owner_id == current_user.id
        )
    )

    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")

    updates = workspace_update.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided")

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
