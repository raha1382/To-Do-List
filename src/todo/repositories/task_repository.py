from typing import List, Optional
from datetime import datetime
from src.todo.model.task import Task, TaskStatus
from src.todo.db.session import sessionlocal


class TaskRepository:
    def __init__(self):
        self.db = next(sessionlocal())

    def create(self, title: str, project_name: str, description: Optional[str] = None,
               status: TaskStatus = TaskStatus.TODO, deadline: Optional[datetime] = None) -> Task:
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

    def get_by_project_name(self, project_name: str) -> List[Task]:
        return self.db.query(Task).filter(Task.project_name == project_name).all()

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