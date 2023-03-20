from flask import Flask, redirect, url_for, request, render_template
from src.my_todo import TodoList

app = Flask(__name__)


@app.route('/')
def index():
    todo_list = mytodo.get_all_tasks()
    return render_template("index.html", todo_list=todo_list)


@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        new_task = request.form['new_task']
        description = request.form['description']
        mytodo.add_task(new_task, description)
        return redirect(url_for('index'))


if __name__ == '__main__':
    mytodo = TodoList()
    # mytodo.add_task("test1")
    app.run()
