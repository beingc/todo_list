import time
from datetime import datetime
from unittest import TestCase
from src.backend.todolist import TodoList


class TestTodoList(TestCase):
    def setUp(self):
        self.todo = TodoList()
        self.todo.add_task('Test Task1')

    def tearDown(self):
        self.todo.reset_db()

    def test_add_task(self):
        self.todo.add_task('Test Task2')
        tasks = self.todo.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1]['task'], 'Test Task2')

    def test_add_task_with_detail(self):
        self.todo.add_task('Test Task2', 'detail2')
        tasks = self.todo.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1]['detail'], 'detail2')

    def test_add_task_with_deadline(self):
        self.todo.add_task('Test Task2', 'detail2', 'deadline2')
        tasks = self.todo.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[1]['deadline'], 'deadline2')

    def test_add_task_create_time(self):
        self.todo.add_task('Test Task2', 'detail2', 'deadline2')
        tasks = self.todo.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(tasks[1]['create_time'], create_time)

    def test_delete_task(self):
        self.todo.delete_task(1)
        tasks = self.todo.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    def test_complete_task(self):
        self.todo.complete_task(1)
        task = self.todo.get_task(1)
        self.assertEqual(task['status'], 1)

    def test_incomplete_task(self):
        self.todo.incomplete_task(1)
        task = self.todo.get_task(1)
        self.assertEqual(task['status'], 0)

    def test_update_task(self):
        self.todo.update_task(1, "test Task11")
        task = self.todo.get_task(1)
        self.assertEqual(task['task'], "test Task11")

    def test_update_task_with_detail(self):
        self.todo.update_task(1, "test Task12", "detail12")
        task = self.todo.get_task(1)
        self.assertEqual(task['detail'], "detail12")

    def test_update_task_with_deadline(self):
        self.todo.update_task(1, "test Task13", "detail13", deadline="deadline13")
        task = self.todo.get_task(1)
        self.assertEqual(task['deadline'], "deadline13")

    def test_update_task_with_update_time(self):
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1)
        self.todo.update_task(1, "test Task14", "detail14", deadline="deadline14")
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = self.todo.get_task(1)
        self.assertEqual(task['create_time'], create_time)
        self.assertEqual(task['update_time'], update_time)


if __name__ == '__main__':
    TestCase.run()
