from fastapi import FastAPI
from app.routers import events, workspaces, users

app = FastAPI()

app.include_router(workspaces.router)
app.include_router(events.router)
app.include_router(users.router)