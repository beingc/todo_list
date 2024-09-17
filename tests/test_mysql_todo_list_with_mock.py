import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.backend.mysql_todo_list import MySQLTodoList

mysql_config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'test_db'
}


@pytest.fixture
def mock_mysql():
    with patch('mysql.connector.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        # 模拟 `with self.conn.cursor() as cursor` 中的游标行为
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        yield mock_conn, mock_cursor


def test_create_table(mock_mysql):
    mock_conn, mock_cursor = mock_mysql

    todo_list = MySQLTodoList(mysql_config)

    mock_cursor.execute.assert_called_once_with('''CREATE TABLE IF NOT EXISTS todolist
                              (task_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                               task TEXT NOT NULL,
                               detail TEXT,
                               status INTEGER NOT NULL DEFAULT 0,
                               create_time TEXT,
                               update_time TEXT,
                               deadline TEXT,
                               priority INTEGER NOT NULL DEFAULT 0)''')
    mock_conn.commit.assert_called_once()


@patch('src.backend.mysql_todo_list.datetime')
def test_add_task(mock_datetime, mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    fixed_time = datetime(2024, 9, 17, 10, 20, 46)
    mock_datetime.now.return_value = fixed_time

    todo_list = MySQLTodoList(mysql_config)
    task_name = "Test Task"
    task_detail = "This is a test task"
    task_deadline = "2024-12-31"
    task_priority = 1

    todo_list.add_task(task_name, detail=task_detail, deadline=task_deadline, priority=task_priority)

    # print(mock_cursor.execute.call_args_list)
    mock_cursor.execute.assert_any_call('''INSERT INTO todolist (task, detail, status, deadline, create_time, priority)
                VALUES (%s, %s, %s, %s, %s, %s)''',
                                        (task_name, task_detail, 0, task_deadline,
                                         fixed_time.strftime("%Y-%m-%d %H:%M:%S"), task_priority))
    assert mock_conn.commit.call_count == 2


def test_remove_task(mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    todo_list = MySQLTodoList(mysql_config)
    task_id = 1

    todo_list.remove_task(task_id)

    mock_cursor.execute.assert_any_call("DELETE FROM todolist WHERE task_id = %s", (task_id,))
    assert mock_conn.commit.call_count == 2


@patch('src.backend.mysql_todo_list.datetime')
def test_edit_task(mock_datetime, mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    fixed_time = datetime(2024, 9, 17, 10, 20, 46)
    mock_datetime.now.return_value = fixed_time

    todo_list = MySQLTodoList(mysql_config)
    task_id = 1
    updated_task = "Updated Task"
    updated_detail = "Updated Detail"

    todo_list.edit_task(task_id, task=updated_task, detail=updated_detail)

    mock_cursor.execute.assert_any_call(
        "UPDATE todolist SET task = %s, detail = %s, update_time = %s WHERE task_id = %s",
        (updated_task, updated_detail, fixed_time.strftime("%Y-%m-%d %H:%M:%S"), task_id)
    )
    assert mock_conn.commit.call_count == 2


def test_get_task(mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    todo_list = MySQLTodoList(mysql_config)
    task_id = 1
    mock_cursor.fetchone.return_value = (1, "Test Task", "Test Detail", 0, "2024-09-17", None, "2024-12-31", 1)

    result = todo_list.get_task(task_id)

    mock_cursor.execute.assert_any_call("SELECT * FROM todolist where task_id = %s", (task_id,))
    assert result == {
        'task_id': 1,
        'task': "Test Task",
        'detail': "Test Detail",
        'status': 0,
        'create_time': "2024-09-17",
        'update_time': None,
        'deadline': "2024-12-31",
        'priority': 1
    }


def test_get_all_tasks(mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    todo_list = MySQLTodoList(mysql_config)

    mock_cursor.fetchall.return_value = [
        (1, "Task 1", "Detail 1", 0, "2024-09-17", None, "2024-12-31", 1),
        (2, "Task 2", "Detail 2", 1, "2024-09-17", None, None, 0)
    ]

    result = todo_list.get_all_tasks()

    mock_cursor.execute.assert_any_call("SELECT * FROM todolist")
    assert result == [
        {
            'task_id': 1,
            'task': "Task 1",
            'detail': "Detail 1",
            'status': 0,
            'create_time': "2024-09-17",
            'update_time': None,
            'deadline': "2024-12-31",
            'priority': 1
        },
        {
            'task_id': 2,
            'task': "Task 2",
            'detail': "Detail 2",
            'status': 1,
            'create_time': "2024-09-17",
            'update_time': None,
            'deadline': None,
            'priority': 0
        }
    ]


@patch('src.backend.mysql_todo_list.datetime')
def test_mark_task_done(mock_datetime, mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    fixed_time = datetime(2024, 9, 17, 10, 20, 46)
    mock_datetime.now.return_value = fixed_time
    todo_list = MySQLTodoList(mysql_config)
    task_id = 1

    todo_list.mark_task_done(task_id)

    mock_cursor.execute.assert_any_call(
        "update todolist set status = %s, update_time = %s where task_id = %s",
        (1, fixed_time.strftime("%Y-%m-%d %H:%M:%S"), task_id)
    )
    assert mock_conn.commit.call_count == 2


@patch('src.backend.mysql_todo_list.datetime')
def test_mark_task_undone(mock_datetime, mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    todo_list = MySQLTodoList(mysql_config)
    fixed_time = datetime(2024, 9, 17, 10, 20, 46)
    mock_datetime.now.return_value = fixed_time
    task_id = 1
    todo_list.mark_task_undone(task_id)

    mock_cursor.execute.assert_any_call(
        "update todolist set status = %s, update_time = %s where task_id = %s",
        (0, fixed_time.strftime("%Y-%m-%d %H:%M:%S"), task_id)
    )
    assert mock_conn.commit.call_count == 2


def test_clear_tasks(mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    todo_list = MySQLTodoList(mysql_config)

    todo_list.clear_tasks()

    mock_cursor.execute.assert_any_call("delete from todolist")
    assert mock_conn.commit.call_count == 2


def test_clear_completed_tasks(mock_mysql):
    mock_conn, mock_cursor = mock_mysql
    todo_list = MySQLTodoList(mysql_config)

    todo_list.clear_completed_tasks()

    mock_cursor.execute.assert_any_call("delete from todolist where status='1'")
    assert mock_conn.commit.call_count == 2
