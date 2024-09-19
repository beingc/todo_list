from abc import ABC, abstractmethod


class BaseTodoList(ABC):
    @abstractmethod
    def add_task(self, task):
        pass

    @abstractmethod
    def remove_task(self, task_id):
        pass

    @abstractmethod
    def edit_task(self, task_id, task, detail, status, deadline, priority):
        pass

    @abstractmethod
    def get_task(self, task_id):
        pass

    @abstractmethod
    def get_all_tasks(self):
        pass

    @abstractmethod
    def mark_task_done(self, task_id):
        pass

    @abstractmethod
    def mark_task_undone(self, task_id):
        pass

    @abstractmethod
    def clear_tasks(self):
        pass

    @abstractmethod
    def clear_completed_tasks(self):
        pass
