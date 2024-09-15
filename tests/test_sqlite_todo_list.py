import os
import pytest
from src.backend.sqlite_todo_list import SQLiteTodoList


@pytest.fixture
def sqlite_todolist(tmp_path):
    db_path = os.path.join(tmp_path, "test_db.sqlite")
    return SQLiteTodoList(db_path)


def test_add_task(sqlite_todolist):
    sqlite_todolist.add_task("Task 1", "Detail for Task 1")
    tasks = sqlite_todolist.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]['task'] == "Task 1"


def test_remove_task(sqlite_todolist):
    sqlite_todolist.add_task("Task to be deleted")
    tasks = sqlite_todolist.get_all_tasks()
    task_id = tasks[0]['task_id']
    sqlite_todolist.remove_task(task_id)
    tasks = sqlite_todolist.get_all_tasks()
    assert tasks == []


def test_edit_task(sqlite_todolist):
    sqlite_todolist.add_task("Original Task")
    tasks = sqlite_todolist.get_all_tasks()
    task_id = tasks[0]['task_id']
    sqlite_todolist.edit_task(task_id, "Updated Task")
    edit_task = sqlite_todolist.get_all_tasks()
    print(edit_task)
    assert edit_task[0]['task'] == "Updated Task"
