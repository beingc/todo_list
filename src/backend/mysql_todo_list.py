import mysql.connector
from datetime import datetime
from src.backend.base_todo_list import BaseTodoList


class MySQLTodoList(BaseTodoList):
    def __init__(self, mysql_config):
        self.conn = mysql.connector.connect(**mysql_config)
        self.create_table()

    def __del__(self):
        if self.conn.is_connected():
            self.conn.close()

    def create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS todolist
                              (task_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                               task TEXT NOT NULL,
                               detail TEXT,
                               status INTEGER NOT NULL DEFAULT 0,
                               create_time TEXT,
                               update_time TEXT,
                               deadline TEXT,
                               priority INTEGER NOT NULL DEFAULT 0)''')
            self.conn.commit()

    def add_task(self, task, detail=None, status=0, deadline=None, priority=0):
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn.cursor() as cursor:
            cursor.execute(
                '''INSERT INTO todolist (task, detail, status, deadline, create_time, priority)
                VALUES (%s, %s, %s, %s, %s, %s)''',
                (task, detail, status, deadline, create_time, priority))
            self.conn.commit()

    def remove_task(self, task_id):
        with self.conn.cursor() as cursor:
            cursor.execute("DELETE FROM todolist WHERE task_id = %s", (task_id,))
            self.conn.commit()

    def edit_task(self, task_id, task=None, detail=None, status=None, deadline=None, priority=None):
        update_fields = {
            "task": task,
            "detail": detail,
            "status": status,
            "deadline": deadline,
            "priority": priority
        }

        set_clause = [f"{key} = %s" for key, value in update_fields.items() if value is not None]
        params = [value for value in update_fields.values() if value is not None]

        if not set_clause:
            return

        set_clause.append("update_time = %s")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        update_query = f"UPDATE todolist SET {', '.join(set_clause)} WHERE task_id = %s"
        params.append(task_id)

        with self.conn.cursor() as cursor:
            cursor.execute(update_query, tuple(params))
            self.conn.commit()

    def get_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM todolist where task_id = %s", (task_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return {
                'task_id': row[0],
                'task': row[1],
                'detail': row[2],
                'status': row[3],
                'create_time': row[4],
                'update_time': row[5],
                'deadline': row[6],
                'priority': row[7]
            }
        return {}

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM todolist")
        rows = cursor.fetchall()
        cursor.close()
        if rows:
            return [
                {
                    'task_id': row[0],
                    'task': row[1],
                    'detail': row[2],
                    'status': row[3],
                    'create_time': row[4],
                    'update_time': row[5],
                    'deadline': row[6],
                    'priority': row[7]
                }
                for row in rows]
        else:
            return []

    def _update_task_status(self, task_id, status):
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn.cursor() as cursor:
            cursor.execute("update todolist set status = %s, update_time = %s where task_id = %s", (status, update_time, task_id))
            self.conn.commit()

    def mark_task_done(self, task_id):
        self._update_task_status(task_id, 1)

    def mark_task_undone(self, task_id):
        self._update_task_status(task_id, 0)

    def clear_tasks(self):
        with self.conn.cursor() as cursor:
            cursor.execute("delete from todolist")
            self.conn.commit()

    def clear_completed_tasks(self):
        with self.conn.cursor() as cursor:
            cursor.execute("delete from todolist where status='1'")
            self.conn.commit()
