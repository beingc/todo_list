import os
import pytest
from src.backend.sqlite_todo_list import SQLiteTodoList


@pytest.fixture
def sqlite_todolist(tmp_path):
    db_path = os.path.join(tmp_path, "test_db.sqlite")
    return SQLiteTodoList(db_path)


def test_add_task(sqlite_todolist):
    sqlite_todolist.add_task("Task 1", "Detail for Task 1", status=0, priority=3)
    tasks = sqlite_todolist.get_all_tasks()

    assert len(tasks) == 1
    task = tasks[0]
    assert task['task'] == "Task 1"
    assert task['detail'] == "Detail for Task 1"
    assert task['status'] == 0
    assert task['priority'] == 3
    assert task['create_time'] is not None
    assert task['update_time'] is None
    assert task['deadline'] is None


def test_remove_task(sqlite_todolist):
    sqlite_todolist.add_task("Task to be deleted")
    tasks = sqlite_todolist.get_all_tasks()
    assert len(tasks) == 1

    task_id = tasks[0]['task_id']
    sqlite_todolist.remove_task(task_id)

    tasks = sqlite_todolist.get_all_tasks()
    assert tasks == []


def test_edit_task(sqlite_todolist):
    sqlite_todolist.add_task("Original Task", "Original Detail", priority=1)
    tasks = sqlite_todolist.get_all_tasks()
    assert len(tasks) == 1

    task_id = tasks[0]['task_id']
    original_update_time = tasks[0]['update_time']

    sqlite_todolist.edit_task(task_id, detail="Updated Detail", priority=5)
    updated_task = sqlite_todolist.get_task(task_id)

    assert updated_task['task'] == "Original Task"
    assert updated_task['priority'] == 5
    assert updated_task['detail'] == "Updated Detail"
    assert updated_task['update_time'] != original_update_time


def test_mark_task_done(sqlite_todolist):
    sqlite_todolist.add_task("Task to be done", status=0)
    tasks = sqlite_todolist.get_all_tasks()
    task_id = tasks[0]['task_id']

    sqlite_todolist.mark_task_done(task_id)
    updated_task = sqlite_todolist.get_task(task_id)

    assert updated_task['status'] == 1
    assert updated_task['update_time'] is not None


def test_mark_task_undone(sqlite_todolist):
    sqlite_todolist.add_task("Task to be undone", status=1)
    tasks = sqlite_todolist.get_all_tasks()
    task_id = tasks[0]['task_id']

    sqlite_todolist.mark_task_undone(task_id)
    updated_task = sqlite_todolist.get_task(task_id)

    assert updated_task['status'] == 0
    assert updated_task['update_time'] is not None


def test_clear_tasks(sqlite_todolist):
    sqlite_todolist.add_task("Task 1")
    sqlite_todolist.add_task("Task 2")
    sqlite_todolist.add_task("Task 3")

    assert len(sqlite_todolist.get_all_tasks()) == 3

    sqlite_todolist.clear_tasks()
    assert sqlite_todolist.get_all_tasks() == []


def test_clear_completed_tasks(sqlite_todolist):
    sqlite_todolist.add_task("Task 1", status=1)
    sqlite_todolist.add_task("Task 2", status=0)

    assert len(sqlite_todolist.get_all_tasks()) == 2

    sqlite_todolist.clear_completed_tasks()

    tasks = sqlite_todolist.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]['task'] == "Task 2"
