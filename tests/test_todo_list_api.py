import pytest
from datetime import datetime
from src.backend.todo_list_api import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_all_tasks(client):
    rv = client.get('/api/get_all_tasks')
    assert rv.status_code == 200
    assert rv.json == []


def test_add_task(client):
    rv = client.post('/api/add_task', json={
        'task': 'New Task',
        'detail': 'Details of the new task',
        'deadline': '2024-12-31',
        'priority': '1'
    })
    assert rv.status_code == 201
    assert rv.json['result'] == "success"
    # Clean up data
    rv = client.get('/api/clear_tasks')


def test_get_task(client):
    # Add task first
    client.post('/api/add_task', json={
        'task': 'Task1',
        'detail': 'Task1 details',
        'deadline': '2024-12-31',
        'priority': '1'
    })
    tasks = client.get('/api/get_all_tasks').json
    task_id = tasks[0]['task_id']
    # Get the task
    rv = client.get(f'/api/get_task/{task_id}')
    assert rv.status_code == 200
    assert rv.json['task_id'] == task_id
    assert rv.json['task'] == 'Task1'
    assert rv.json['detail'] == 'Task1 details'
    assert rv.json['deadline'] == '2024-12-31'
    assert rv.json['priority'] == 1
    assert rv.json['create_time'] == datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Clean up data
    rv = client.get('/api/clear_tasks')


def test_remove_task(client):
    # Add task first
    client.post('/api/add_task', json={
        'task': 'Task to be deleted',
        'detail': 'Task details',
        'deadline': '2024-12-31',
        'priority': '1'
    })
    tasks = client.get('/api/get_all_tasks').json
    task_id = tasks[0]['task_id']

    # Delete the task
    rv = client.delete(f'/api/remove_task/{task_id}')
    assert rv.status_code == 200
    assert rv.json['result'] == "success"


def test_edit_task(client):
    # Add task first
    client.post('/api/add_task', json={
        'task': 'Task to be updated',
        'detail': 'Task details',
        'deadline': '2024-12-30',
        'priority': '1'
    })
    tasks = client.get('/api/get_all_tasks').json
    task_id = tasks[0]['task_id']

    # Update the task
    rv = client.put(f'/api/edit_task/{task_id}', json={
        'task': 'Updated Task',
        'detail': 'Updated details',
        'status': 1,
        'deadline': '2024-12-31',
        'priority': '2'
    })
    assert rv.status_code == 200
    assert rv.json['result'] == "success"
    # Clean up data
    rv = client.get('/api/clear_tasks')


def test_clear_tasks(client):
    rv = client.get('/api/clear_tasks')
    assert rv.status_code == 200
    assert rv.json['result'] == "success"
