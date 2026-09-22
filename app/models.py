import datetime
from sqlalchemy import DateTime, ForeignKey, Text, func 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
import uuid



class Base(DeclarativeBase):
    pass

class EventDB(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    
    workspace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workspaces.id"))
    workspace: Mapped["WorkspaceDB"] = relationship(back_populates="events")

    name: Mapped[str] = mapped_column(Text)
    venue: Mapped[str | None] = mapped_column(Text)
    starts_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    rider: Mapped[list] = mapped_column(JSONB, default=list)
    stage_icons: Mapped[list] = mapped_column(JSONB, default=list,)
    stage_layout: Mapped[dict | None] = mapped_column(JSONB)

    created_at: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now()
    )


class WorkspaceDB(Base):
    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    events: Mapped[list["EventDB"]] = relationship(back_populates="workspace")    

    name: Mapped[str] = mapped_column(Text)
    color: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now()
    )

class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
