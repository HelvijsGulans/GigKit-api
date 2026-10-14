import uuid


def test_api_starts(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_create_workspace(client):
    client.post(
        "/users",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    login = client.post(
        "/users/login",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/workspaces",
        json={
            "name": "Test Workspace",
            "color": "Green",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Workspace"
    assert data["color"] == "Green"
    assert "id" in data


def test_create_event(client):
    client.post(
        "/users",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    login = client.post(
        "/users/login",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    workspace_response = client.post(
        "/workspaces",
        json={"name": "Test Workspace 2", "color": "Blue"},
        headers=headers,
    )

    workspace_id = workspace_response.json()["id"]

    response = client.post(
        f"/workspaces/{workspace_id}/events",
        json={
            "name": "Test event",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Dzintari",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test event"
    assert data["venue"] == "Dzintari"
    assert data["workspace_id"] == workspace_id


def test_create_event_with_missing_workspace(client):
    client.post(
        "/users",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    login = client.post(
        "/users/login",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    fake_workspace_uuid = str(uuid.uuid4())

    response = client.post(
        f"/workspaces/{fake_workspace_uuid}/events",
        json={
            "name": "Test event",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Dzintari",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        },
        headers=headers,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Workspace not found"


def test_update_event(client):
    client.post(
        "/users",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    login = client.post(
        "/users/login",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    workspace_response = client.post(
        "/workspaces",
        json={
            "name": "Test Workspace",
            "color": "Blue",
        },
        headers=headers,
    )

    assert workspace_response.status_code == 201

    workspace_id = workspace_response.json()["id"]

    event_response = client.post(
        f"/workspaces/{workspace_id}/events",
        json={
            "name": "Original name",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Original venue",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        },
        headers=headers,
    )

    assert event_response.status_code == 200

    event_id = event_response.json()["id"]

    response = client.patch(
        f"/events/{event_id}",
        json={
            "name": "Different test name",
            "venue": "Different venue",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Different test name"
    assert data["venue"] == "Different venue"


def test_delete_event(client):
    client.post(
        "/users",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    login = client.post(
        "/users/login",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    workspace_response = client.post(
        "/workspaces",
        json={
            "name": "Test Workspace",
            "color": "Blue",
        },
        headers=headers,
    )

    workspace_id = workspace_response.json()["id"]

    assert workspace_response.status_code == 201

    event_create = client.post(
        f"/workspaces/{workspace_id}/events",
        json={
            "name": "Original name",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Original venue",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        },
        headers=headers,
    )

    event_id = event_create.json()["id"]

    response = client.delete(f"/events/{event_id}", headers=headers)

    assert response.status_code == 200

    get_response = client.get(f"/events/{event_id}", headers=headers)

    assert get_response.status_code == 404


def test_cannot_delete_workspace_with_events(client):
    client.post(
        "/users",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    login = client.post(
        "/users/login",
        json={
            "email": "user1@gmail.com",
            "password": "password1",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    workspace_response = client.post(
        "/workspaces", json={"name": "testName", "color": "red"}, headers=headers
    )

    workspace_id = workspace_response.json()["id"]

    client.post(
        f"/workspaces/{workspace_id}/events",
        json={
            "name": "Original name",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Original venue",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        },
        headers=headers,
    )

    response = client.delete(f"/workspaces/{workspace_id}", headers=headers)

    assert response.status_code == 409

    data = response.json()

    assert data["detail"] == "Workspace still contains events"

    exists = client.get(f"/workspaces/{workspace_id}", headers=headers)

    assert exists.status_code == 200


def test_new_login(client):
    client.post("/users", json={"email": "freddy@yahoo.lv", "password": "secure69"})

    response = client.post(
        "/users/login", json={"email": "freddy@yahoo.lv", "password": "secure69"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"


def test_wrong_email(client):
    client.post("/users", json={"email": "freddy@yahoo.lv", "password": "secure69"})

    response = client.post(
        "/users/login", json={"email": "freddy@gmail.lv", "password": "secure69"}
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


def test_wrong_password(client):
    client.post("/users", json={"email": "freddy@yahoo.lv", "password": "secure69"})

    response = client.post(
        "/users/login", json={"email": "freddy@yahoo.lv", "password": "reallysafe 20"}
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


def test_ownership_of_workspaces(client):
    client.post("/users", json={"email": "user1@gmail.com", "password": "password1"})
    client.post("/users", json={"email": "user2@gmail.com", "password": "password2"})

    login1 = client.post(
        "/users/login", json={"email": "user1@gmail.com", "password": "password1"}
    )

    token1 = login1.json()["access_token"]
    headers1 = {"Authorization": f"bearer {token1}"}

    assert login1.json()["token_type"] == "bearer"

    login2 = client.post(
        "/users/login", json={"email": "user2@gmail.com", "password": "password2"}
    )

    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"bearer {token2}"}
    assert login2.json()["token_type"] == "bearer"

    workspace = client.post(
        "/workspaces",
        json={
            "name": "workspace1",
            "color": "blue",
        },
        headers=headers1,
    )

    workspace_id = workspace.json()["id"]

    response = client.get(
        f"/workspaces/{workspace_id}",
        headers=headers1,
    )

    assert response.status_code == 200

    workspace_invalid_get = client.get(
        f"/workspaces/{workspace_id}",
        headers=headers2,
    )

    assert workspace_invalid_get.status_code == 404

    workspace_invalid_patch = client.patch(
        f"/workspaces/{workspace_id}",
        json={
            "name": "workspace1",
            "color": "blue",
        },
        headers=headers2,
    )

    assert workspace_invalid_patch.status_code == 404

    workspace_invalid_delete = client.delete(
        f"/workspaces/{workspace_id}",
        headers=headers2,
    )

    assert workspace_invalid_delete.status_code == 404
