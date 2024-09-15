import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.backend.sqlite_todo_list import SQLiteTodoList
from src.backend.mysql_todo_list import MySQLTodoList

app = Flask(__name__)
CORS(app, supports_credentials=True)
cfg_path = os.path.join(os.path.dirname(__file__), 'config.json')

with open(cfg_path, 'r') as f:
    config = json.load(f)

db_type = config['database']['type']
if db_type == 'sqlite':
    db_path = config['database']['sqlite_db']
    todo_list = SQLiteTodoList(db_path)
elif db_type == 'mysql':
    mysql_config = {
        'host': config['database']['mysql_host'],
        'user': config['database']['mysql_user'],
        'password': config['database']['mysql_password'],
        'database': config['database']['mysql_db']
    }
    todo_list = MySQLTodoList(mysql_config)
else:
    raise ValueError("Unsupported database type")


@app.route('/')
@app.route('/api/get_all_tasks')
def get_all_tasks():
    tasks = todo_list.get_all_tasks()
    return jsonify(tasks)


@app.route('/api/add_task', methods=['POST'])
def add_task():
    new_task = request.get_json()
    todo_list.add_task(task=new_task['task'],
                       detail=new_task['detail'],
                       deadline=new_task['deadline'],
                       priority=new_task['priority'])
    return jsonify({'result': 'success'}), 201


@app.route('/api/remove_task/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    todo_list.remove_task(task_id)
    return jsonify({'result': 'success'})


@app.route('/api/mark_task_done/<int:task_id>', methods=['POST'])
def mark_task_done(task_id):
    todo_list.mark_task_done(task_id)
    return jsonify({'result': 'success'})


@app.route('/api/mark_task_undone/<int:task_id>', methods=['POST'])
def mark_task_undone(task_id):
    todo_list.mark_task_undone(task_id)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
