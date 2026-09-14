# GigKit API

Backend API for GigKit, a mobile application for managing gigs, technical riders, stage plans, and event information.

This project is built with FastAPI and PostgreSQL and serves as the backend foundation for GigKit. It currently provides workspace and event management through a REST API, with relational data stored in PostgreSQL and document-like event data stored using JSONB.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- psycopg
- pytest

## Features

- Workspace CRUD
- Event CRUD
- UUID-based resource identifiers
- Events grouped by workspace
- Event filtering by workspace
- PostgreSQL foreign key relationships
- JSONB storage for riders, stage icons, and stage layouts
- Database migrations with Alembic
- Request validation with Pydantic
- Automated API tests using an isolated PostgreSQL test database

## Data Model

A workspace can contain multiple events.

### Workspace

- `id` - UUID
- `name`
- `color`
- `created_at`
- `updated_at`

### Event

- `id` - UUID
- `workspace_id` - foreign key to a workspace
- `name`
- `venue`
- `starts_at`
- `rider` - JSONB
- `stage_icons` - JSONB
- `stage_layout` - JSONB
- `created_at`
- `updated_at`

Relational data such as workspace ownership is stored using normal PostgreSQL columns and foreign keys. More document-like data such as riders and stage layouts is stored as JSONB because these structures belong to an event and can contain nested data.

## API

The API currently exposes endpoints for managing workspaces and events.

```text
GET    /workspaces
GET    /workspaces/{workspace_id}
POST   /workspaces
PATCH  /workspaces/{workspace_id}
DELETE /workspaces/{workspace_id}

GET    /events
GET    /events/{event_id}
POST   /events
PATCH  /events/{event_id}
DELETE /events/{event_id}
```

Events can also be filtered by workspace:

```text
GET /events?workspace_id=<uuid>
```

Interactive API documentation is automatically available through FastAPI at:

```text
http://127.0.0.1:8000/docs
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/HelvijsGulans/GigKit-api.git
cd GigKit-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Create a local PostgreSQL database named:

```text
gigkit
```

For example:

```sql
CREATE DATABASE gigkit;
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and set your PostgreSQL password:

```env
DATABASE_PASSWORD=your_postgres_password
```

The current local configuration expects PostgreSQL to run on:

```text
localhost:5432
```

with the `postgres` user.

### 6. Apply database migrations

```bash
alembic upgrade head
```

### 7. Run the API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Tests

Tests run against a separate PostgreSQL database so development data is not modified.

Create:

```sql
CREATE DATABASE gigkit_test;
```

Then run:

```bash
python -m pytest
```

The test suite covers core API behaviour including workspace creation, event creation, event updates, event deletion, and invalid workspace references.

## Project Structure

```text
GigKit-api/
├── app/
│   ├── database.py
│   ├── main.py
│   └── models.py
├── alembic/
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

## Status

This backend is under active development and is intended to become the server-side API for the GigKit mobile application.