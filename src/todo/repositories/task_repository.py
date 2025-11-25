# src/todo/repositories/task.py
from typing import List, Optional
from datetime import datetime
from todo.model.task import Task
from todo.model.enums import TaskStatus
from todo.db.session import get_db


class TaskRepository:

    def __init__(self):
        self.db = next(get_db())

    def create(
        self,
        title: str,
        project_name: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.TODO,
        deadline: Optional[datetime] = None
    ) -> Task:
        task = Task(
            title=title,
            project_name=project_name,
            description=description,
            status=status,
            deadline=deadline
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_project_name(self, project_name: str) -> List[Task]:
        return self.db.query(Task).filter(Task.project_name == project_name).all()

    def get_by_project_name_and_title(self, project_name: str, title: str) -> Optional[Task]:
        return self.db.query(Task).filter(
            Task.project_name == project_name,
            Task.title == title
        ).first()

    def get_all(self) -> List[Task]:
        return self.db.query(Task).all()

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        deadline: Optional[datetime] = None
    ) -> Optional[Task]:
        print("DEBUG STATUS TYPE:", status, type(status))

        task = self.get_by_id(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if deadline is not None:
            task.deadline = deadline
        print("DEBUG STATUS TYPE:", status, type(status))

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def get_overdue_todo_tasks(self) -> List[Task]:
        now = datetime.now()
        return (
            self.db.query(Task)
            .filter(
                Task.status == TaskStatus.TODO,
                Task.deadline.isnot(None),
                Task.deadline < now
            )
            .all()
        )