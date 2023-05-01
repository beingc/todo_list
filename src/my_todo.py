# coding=utf8
# Date: 2023-03-18
# Desc: to-do list app

import sqlite3
from datetime import datetime


class TodoList:
    def __init__(self):
        # 报错: SQLite objects created in a thread can only be used in that same thread
        # 修改: check_same_thread=False
        self.conn = sqlite3.connect('todolist.db', check_same_thread=False)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS todolist
                             (task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              task TEXT NOT NULL,
                              detail TEXT,
                              status INTEGER NOT NULL DEFAULT 0,
                              deadline TEXT,
                              create_time TEXT,
                              update_time TEXT)''')

    def __del__(self):
        self.conn.close()

    def add_task(self, task, detail=None, deadline=None):
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute("INSERT INTO todolist (task, detail, deadline, create_time) VALUES (?, ?, ?, ?)",
                          (task, detail, deadline, create_time))
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM todolist WHERE task_id=?", (task_id,))
        self.conn.commit()

    def update_task(self, task_id, task=None, detail=None, status=None, deadline=None):
        params = []
        set_clause = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if task:
            set_clause.append("task = ?")
            params.append(task)
        if detail:
            set_clause.append("detail = ?")
            params.append(detail)
        if status:
            set_clause.append("status = ?")
            params.append(status)
        if deadline:
            set_clause.append("deadline = ?")
            params.append(deadline)
        if len(params) > 0:
            set_clause.append("update_time = ?")
            params.append(current_time)
        set_clause = ", ".join(set_clause)

        update_query = "UPDATE todolist SET {} WHERE task_id = ?".format(set_clause)
        params.append(task_id)

        self.conn.execute(update_query, tuple(params))
        self.conn.commit()

    def get_task(self, task_id):
        cursor = self.conn.execute("SELECT * FROM todolist WHERE task_id=?", (task_id,))
        row = cursor.fetchone()
        if row:
            return {'task_id': row[0], 'task': row[1], 'detail': row[2], 'status': row[3],
                    'deadline': row[4], 'create_time': row[5], 'update_time': row[6]}
        else:
            return None

    def get_all_tasks(self):
        cursor = self.conn.execute("SELECT * FROM todolist")
        rows = cursor.fetchall()
        task_list = []
        task_list = [{'task_id': row[0], 'task': row[1], 'detail': row[2], 'status': row[3], 'deadline': row[4],
                      'create_time': row[5], 'update_time': row[6]} for row in rows]
        return task_list

    def complete_task(self, task_id):
        self.update_task(task_id, status="1")

    def incomplete_task(self, task_id):
        self.update_task(task_id, status="0")

    def reset_db(self):
        self.conn.execute("DROP TABLE IF EXISTS todolist;")


if __name__ == '__main__':
    pass
