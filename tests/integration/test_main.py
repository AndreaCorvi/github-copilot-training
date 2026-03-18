import pytest
from httpx import AsyncClient
from app.models import DeveloperTask, ProductivityReport, TaskStatus


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_status_returns_ok(client: AsyncClient) -> None:
    resp = await client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_returns_list(client: AsyncClient) -> None:
    resp = await client.get("/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_valid_schema(client: AsyncClient) -> None:
    resp = await client.get("/tasks")
    assert resp.status_code == 200
    for item in resp.json():
        DeveloperTask(**item)  # validates against Pydantic model


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_report_returns_valid_schema(client: AsyncClient) -> None:
    resp = await client.get("/report")
    assert resp.status_code == 200
    ProductivityReport(**resp.json())  # validates against Pydantic model


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_report_completion_rate_is_float(client: AsyncClient) -> None:
    resp = await client.get("/report")
    assert resp.status_code == 200
    assert isinstance(resp.json()["completion_rate"], float)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_creates_new_task(client: AsyncClient) -> None:
    payload = {"task_id": 0, "title": "New integration test task", "status": "pending", "hours_spent": 2.0}
    resp = await client.post("/log_task", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["message"] == "Task logged successfully."
    assert "task_id" in body


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_invalid_status_returns_422(client: AsyncClient) -> None:
    payload = {"task_id": 0, "title": "Bad task", "status": "invalid_status", "hours_spent": 0.0}
    resp = await client.post("/log_task", json=payload)
    assert resp.status_code == 422


# --- GET /task/{task_id}/status ---

@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_task_status_returns_status_for_known_id(client: AsyncClient) -> None:
    resp = await client.get("/task/1/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["task_id"] == 1
    assert "status" in body


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_task_status_returns_error_for_unknown_id(client: AsyncClient) -> None:
    resp = await client.get("/task/9999/status")
    assert resp.status_code == 200
    assert resp.json() == {"error": "Task not found"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_task_status_invalid_id_type_returns_422(client: AsyncClient) -> None:
    resp = await client.get("/task/not-an-int/status")
    assert resp.status_code == 422
