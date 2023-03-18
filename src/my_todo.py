# coding=utf8
# Date: 2023-03-18
# Desc: to-do list app

import sqlite3


class TodoList:
    def __init__(self):
        self.conn = sqlite3.connect('todolist.db')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS todolist
                             (task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              task TEXT NOT NULL,
                              description TEXT,
                              status BOOLEAN NOT NULL DEFAULT 0,
                              deadline TEXT,
                              create_time TEXT,
                              update_time TEXT)''')

    def __del__(self):
        self.conn.close()

    def add_task(self, task, description=None, deadline=None):
        self.conn.execute("INSERT INTO todolist (task, description, deadline) VALUES (?, ?, ?)",
                          (task, description, deadline))
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM todolist WHERE task_id=?", (task_id,))
        self.conn.commit()

    def update_task(self, task_id, task=None, description=None, status=None, deadline=None):
        update_query = "UPDATE todolist SET"
        if task:
            update_query += " task=?,"
        if description:
            update_query += " description=?,"
        if status is not None:
            update_query += " status=?,"
        if deadline:
            update_query += " deadline=?,"
        update_query = update_query.rstrip(',') + " WHERE task_id=?"

        params = []
        if task:
            params.append(task)
        if description:
            params.append(description)
        if status is not None:
            params.append(status)
        if deadline:
            params.append(deadline)
        params.append(task_id)

        self.conn.execute(update_query, tuple(params))
        self.conn.commit()

    def get_task(self, task_id):
        cursor = self.conn.execute("SELECT * FROM todolist WHERE task_id=?", (task_id,))
        row = cursor.fetchone()
        if row:
            return {'task_id': row[0], 'task': row[1], 'description': row[2], 'status': bool(row[3])}
        else:
            return None

    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT * FROM todolist")
        rows = cursor.fetchall()
        task_list = []
        for row in rows:
            task_list.append({'task_id': row[0], 'task': row[1], 'description': row[2], 'status': bool(row[3])})
        return task_list

    def complete_task(self, task_id):
        self.update_task(task_id, status=True)

    def incomplete_task(self, task_id):
        self.update_task(task_id, status=False)

    def reset_db(self):
        self.conn.execute("DROP TABLE IF EXISTS todolist;")


if __name__ == '__main__':
    todo_list = TodoList()
    todo_list.add_task('Buy groceries', 'Milk, bread, eggs')
    todo_list.add_task('Finish project')
    todo_list.complete_task(1)
    todo_list.incomplete_task(2)
    tasks = todo_list.get_all_tasks()
    print(tasks)
    todo_list.reset_db()
