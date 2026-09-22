import uuid

def test_api_starts(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_create_workspace(client):
    response = client.post(
        "/workspaces",
        json={
            "name" : "Test Workspace",
            "color" : "Green"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Workspace"
    assert data["color"] == "Green"
    assert "id" in data


def test_create_event(client):
    workspace_response = client.post(
        "/workspaces",
        json={
            "name" : "Test Workspace 2",
            "color" : "Blue"
        }
    )

    workspace_id = workspace_response.json()["id"]

    response = client.post(
        "/events",
        json={
            "workspace_id" : workspace_id,
            "name" : "Test event",
            "starts_at" : "2026-09-20T20:00:00+03:00",
            "venue" : "Dzintari",
            "rider" : [],
            "stage_icons" : [],
            "stage_layout" : None
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test event"
    assert data["venue"] == "Dzintari"
    assert data["workspace_id"] == workspace_id


def test_create_event_with_missing_workspace(client):

    fake_workspace_uuid = str(uuid.uuid4())

    response = client.post(
        "/events",
        json={
            "workspace_id" : fake_workspace_uuid,
            "name" : "Test event",
            "starts_at" : "2026-09-20T20:00:00+03:00",
            "venue" : "Dzintari",
            "rider" : [],
            "stage_icons" : [],
            "stage_layout" : None
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Workspace not found"


def test_update_event(client):
    workspace_response = client.post(
        "/workspaces",
        json={
            "name": "Test Workspace",
            "color": "Blue",
        },
    )

    assert workspace_response.status_code == 200

    workspace_id = workspace_response.json()["id"]

    event_response = client.post(
        "/events",
        json={
            "workspace_id": workspace_id,
            "name": "Original name",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Original venue",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        },
    )

    assert event_response.status_code == 200

    event_id = event_response.json()["id"]

    response = client.patch(
        f"/events/{event_id}",
        json={
            "name": "Different test name",
            "venue": "Different venue",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Different test name"
    assert data["venue"] == "Different venue"


def test_delete_event(client):

    workspace_response = client.post(
            "/workspaces",
            json={
                "name": "Test Workspace",
                "color": "Blue",
            },
        )
    
    workspace_id = workspace_response.json()["id"]

    event_response = client.post(
        "/events",
        json={
            "workspace_id": workspace_id,
            "name": "Original name",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Original venue",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        },
    )

    event_id = event_response.json()["id"]

    response = client.delete(
        f"/events/{event_id}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/events/{event_id}"
    )

    assert get_response.status_code == 404

    
def test_cannot_delete_workspace_with_events(client):
    workspace_response = client.post(
        "/workspaces",
        json={
            "name" : "testName",
            "color" : "red"
        }
    )

    workspace_id = workspace_response.json()["id"]

    client.post(
        "/events",
        json={
            "workspace_id": workspace_id,
            "name": "Original name",
            "starts_at": "2026-09-20T20:00:00+03:00",
            "venue": "Original venue",
            "rider": [],
            "stage_icons": [],
            "stage_layout": None,
        }
    )

    response = client.delete(
        f"/workspaces/{workspace_id}"
    )

    assert response.status_code == 409

    data = response.json()

    assert data["detail"] == "Workspace still contains events"

    exists = client.get(
        f"/workspaces/{workspace_id}"
    )

    assert exists.status_code == 200


