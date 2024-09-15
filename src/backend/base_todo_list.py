from abc import ABC, abstractmethod


class BaseTodoList(ABC):
    @abstractmethod
    def add_task(self, task):
        """添加一个待办任务"""
        pass

    @abstractmethod
    def remove_task(self, task_id):
        """根据任务ID删除任务"""
        pass

    @abstractmethod
    def edit_task(self, task_id, task, detail, status, deadline, priority):
        """编辑指定任务"""
        pass

    @abstractmethod
    def get_task(self, task_id):
        """返回指定任务"""
        pass

    @abstractmethod
    def get_all_tasks(self):
        """返回所有任务"""
        pass

    @abstractmethod
    def mark_task_done(self, task_id):
        """将指定ID的任务标记为已完成"""
        pass

    @abstractmethod
    def mark_task_undone(self, task_id):
        """将指定ID的任务标记为未完成"""
        pass

    @abstractmethod
    def clear_tasks(self):
        """清除所有任务"""
        pass

    @abstractmethod
    def clear_completed_tasks(self):
        """清除已完成的任务"""
        pass
