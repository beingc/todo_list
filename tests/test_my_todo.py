from unittest import TestCase
from src.my_todo import TodoList


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

    def test_delete_task(self):
        self.todo.delete_task(1)
        tasks = self.todo.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    def test_complete_task(self):
        self.todo.complete_task(1)
        task = self.todo.get_task(1)
        self.assertEqual(task['status'], True)

    def test_incomplete_task(self):
        self.todo.incomplete_task(1)
        task = self.todo.get_task(1)
        self.assertEqual(task['status'], False)
