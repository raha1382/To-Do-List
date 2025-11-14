from ..storage.in_memory_storage import InMemoryStorage
from ..utils.utils import MAX_NUMBER_OF_PROJECTS
from ..model.project import Project
from ..core.task_service import TaskService
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository


class ProjectService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo

    def create_project(self, name: str, description: str) -> Project:
        if len(self.project_repo.get_all()) >= MAX_NUMBER_OF_PROJECTS:
            raise ValueError(f"Maximum number of projects ({MAX_NUMBER_OF_PROJECTS}) reached")
        
        if self.project_repo.get_by_name(name):
            raise ValueError(f"Project with name '{name}' already exists. Please enter a different name.")
        
        return self.project_repo.create(name, description)
    
    def get_project(self, name: str) -> Project | None:
        return self.project_repo.get_by_name(name)

    def update_project(self, name: str, new_name: str, new_description: str) -> bool:
        # Check if the original project exists
        if not self.project_repo.get_by_name(name):
            return False

        # Check if the new name already exists
        if new_name and new_name != name and self.project_repo.get_by_name(new_name):
            raise ValueError(f"Project '{new_name}' already exists.")

        project = self.project_repo.update(name, new_name, new_description)
        return project is not None

    
    def delete_project(self, name: str) -> bool:
        return self.project_repo.delete(name)
    
    def add_task_to_project(self, project_name: str, task_name: str, description: str = "") -> bool:
        project = self.project_repo.get_by_name(project_name)
        if not project:
            return False
        self.task_repo.create(title=task_name, project_name=project_name, description=description)
        return True
    
    def list_projects(self) -> list[Project]:
        return self.project_repo.get_all()