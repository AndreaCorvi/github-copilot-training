import pytest
from app.main import fetch_all_tasks, generate_productivity_report, MOCK_TASKS
from app.models import TaskStatus


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_list() -> None:
    tasks = await fetch_all_tasks()
    assert isinstance(tasks, list)
    assert len(tasks) == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_fetch_all_tasks_contains_developer_tasks() -> None:
    from app.models import DeveloperTask
    tasks = await fetch_all_tasks()
    for task in tasks:
        assert isinstance(task, DeveloperTask)


@pytest.mark.asyncio
async def test_generate_productivity_report_total_tasks() -> None:
    report = await generate_productivity_report()
    assert report.total_tasks == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_generate_productivity_report_completed_tasks() -> None:
    report = await generate_productivity_report()
    expected = sum(1 for t in MOCK_TASKS.values() if t.status == TaskStatus.COMPLETE)
    assert report.completed_tasks == expected


@pytest.mark.asyncio
async def test_generate_productivity_report_completion_rate() -> None:
    report = await generate_productivity_report()
    expected_rate = round(report.completed_tasks / report.total_tasks, 2)
    assert report.completion_rate == expected_rate


@pytest.mark.asyncio
async def test_generate_productivity_report_total_hours() -> None:
    report = await generate_productivity_report()
    expected_hours = round(sum(t.hours_spent for t in MOCK_TASKS.values()), 2)
    assert report.total_hours_spent == expected_hours


# --- get_task_status ---

@pytest.mark.asyncio
async def test_get_task_status_returns_task_for_known_id() -> None:
    from app.main import get_task_status
    result = await get_task_status(1)
    assert result["task_id"] == 1
    assert result["status"] == TaskStatus.COMPLETE


@pytest.mark.asyncio
async def test_get_task_status_returns_error_for_unknown_id() -> None:
    from app.main import get_task_status
    result = await get_task_status(9999)
    assert result == {"error": "Task not found"}


@pytest.mark.asyncio
async def test_get_task_status_returns_pending_status() -> None:
    from app.main import get_task_status
    result = await get_task_status(3)
    assert result["status"] == TaskStatus.PENDING
