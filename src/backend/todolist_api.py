from flask import Flask, request, jsonify
from flask_cors import CORS
from src.backend.todolist import TodoList

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    todo_list = mytodo.get_all_tasks()
    return jsonify(todo_list)


@app.route('/add_task', methods=['POST'])
def add_task():
    new_task = request.get_json()
    mytodo.add_task(task=new_task['task'], detail=new_task['detail'], deadline=new_task['deadline'])
    return jsonify({'result': 'success'})


@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    mytodo.delete_task(task_id)
    return jsonify({'result': 'success'})


@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    mytodo.complete_task(task_id)
    return jsonify({'result': 'success'})


@app.route('/incomplete_task/<int:task_id>', methods=['POST'])
def incomplete_task(task_id):
    mytodo.incomplete_task(task_id)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    mytodo = TodoList()
    # mytodo.add_task("test1")
    app.run(debug=True, port=5001)
