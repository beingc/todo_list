# Generate by chatgpt

import unittest
from datetime import datetime
from src.backend.todolist import TodoList


class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.test_db_name = "test_todolist.db"
        self.test_todo = TodoList()

    def tearDown(self):
        self.test_todo.reset_db()
        self.test_todo.conn.close()

    def test_add_task(self):
        task_name = "Test task"
        detail = "Test detail"
        deadline = "2022-01-01 10:00:00"
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.test_todo.add_task(task_name, detail=detail, deadline=deadline)
        cursor = self.test_todo.conn.execute("SELECT * FROM todolist")
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], task_name)
        self.assertEqual(rows[0][2], detail)
        self.assertEqual(rows[0][4], deadline)
        self.assertEqual(rows[0][5], create_time)

    def test_update_task(self):
        task_name = "Test task"
        new_task_name = "Updated task"
        detail = "Test detail"
        new_detail = "Updated detail"
        status = 0
        new_status = 1
        deadline = "2022-01-01 10:00:00"
        new_deadline = "2022-12-31 23:59:59"

        self.test_todo.add_task(task_name, detail=detail, deadline=deadline)
        cursor = self.test_todo.conn.execute("SELECT * FROM todolist")
        task_id = cursor.fetchone()[0]

        self.test_todo.update_task(task_id, task=new_task_name, detail=new_detail, status=new_status,
                                   deadline=new_deadline)

        updated_task = self.test_todo.get_task(task_id)
        self.assertEqual(updated_task['task'], new_task_name)
        self.assertEqual(updated_task['detail'], new_detail)
        self.assertEqual(updated_task['status'], new_status)
        self.assertEqual(updated_task['deadline'], new_deadline)

    def test_delete_task(self):
        task_name = "Test task"
        detail = "Test detail"
        deadline = "2022-01-01 10:00:00"

        self.test_todo.add_task(task_name, detail=detail, deadline=deadline)
        cursor = self.test_todo.conn.execute("SELECT * FROM todolist")
        task_id = cursor.fetchone()[0]

        self.test_todo.delete_task(task_id)
        cursor = self.test_todo.conn.execute("SELECT * FROM todolist")
        rows = cursor.fetchall()

        self.assertEqual(len(rows), 0)

    def test_get_task(self):
        task_name = "Test task"
        detail = "Test detail"
        deadline = "2022-01-01 10:00:00"

        self.test_todo.add_task(task_name, detail=detail, deadline=deadline)
        cursor = self.test_todo.conn.execute("SELECT * FROM todolist")
        task_id = cursor.fetchone()[0]

        task = self.test_todo.get_task(task_id)
        self.assertEqual(task['task'], task_name)
        self.assertEqual(task['detail'], detail)
        self.assertEqual(task['deadline'], deadline)

    def test_get_all_tasks(self):
        tasks = [
            ("Task 1", "Detail 1", "2022-01-01 00:00:00"),
            ("Task 2", "Detail 2", "2022-02-01 00:00:00"),
            ("Task 3", "Detail 3", "2022-03-01 00:00:00")
        ]
        for task in tasks:
            self.test_todo.add_task(task[0], detail=task[1], deadline=task[2])

        all_tasks = self.test_todo.get_all_tasks()
        for i, task in enumerate(tasks):
            self.assertEqual(all_tasks[i]['task'], task[0])
            self.assertEqual(all_tasks[i]['detail'], task[1])
            self.assertEqual(all_tasks[i]['deadline'], task[2])

    def test_complete_task(self):
        task_name = "Test task"
        detail = "Test detail"
        deadline = "2022-01-01 10:00:00"

        self.test_todo.add_task(task_name, detail=detail, deadline=deadline)
        cursor = self.test_todo.conn.execute("SELECT * FROM todolist")
        task_id = cursor.fetchone()[0]

        self.test_todo.complete_task(task_id)
        completed_task = self.test_todo.get_task(task_id)

        self.assertEqual(completed_task['status'], 1)

    def test_incomplete_task(self):
        task_name = "Test task"
        detail = "Test detail"
        deadline = "2022-01-01 10:00:00"

        self.test_todo.add_task(task_name, detail=detail, deadline=deadline)
        cursor = self.test_todo.conn.execute("SELECT * FROM todolist")
        task_id = cursor.fetchone()[0]

        self.test_todo.incomplete_task(task_id)
        incomplete_task = self.test_todo.get_task(task_id)

        self.assertEqual(incomplete_task['status'], 0)


if __name__ == '__main__':
    unittest.main()
