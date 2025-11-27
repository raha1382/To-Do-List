from fastapi import Depends
from sqlalchemy.orm import Session
from todo.db.session import get_db
from todo.repositories.project_repository import ProjectRepository
from todo.repositories.task_repository import TaskRepository
from todo.core.project_service import ProjectService
from todo.core.task_service import TaskService

def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return ProjectService(project_repo, task_repo)

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return TaskService(project_repo, task_repo)