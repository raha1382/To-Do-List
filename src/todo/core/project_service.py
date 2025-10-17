from ..storage.in_memory_storage import InMemoryStorage
from ..utils.utils import MAX_NUMBER_OF_PROJECTS
from ..model.project import Project
from ..core.task_service import TaskService

class ProjectService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_project(self, name: str, description: str) -> Project:
        if len(self.storage._projects) >= MAX_NUMBER_OF_PROJECTS:
            raise ValueError(f"Maximum number of projects ({MAX_NUMBER_OF_PROJECTS}) reached")
        
        if name in self.storage._projects:
            raise ValueError(f"Project with name '{name}' already exists. Please enter a different name.")
        
        project = Project(name, description)
        self.storage.add_project(project)
        return project
    
    def get_project(self, name: str) -> Project | None:
        return self.storage.get_project(name)

    def update_project(self, name: str, new_name: str, description: str) -> bool:
        project = self.storage.get_project(name)
        if project:
            project.name = new_name
            project.description = description
            self.storage.add_project(project)
            if name != new_name:
                if name in self.storage._projects:
                    del self.storage._projects[name]
            return True
        return False
    
    def delete_project(self, name: str) -> bool:
        return self.storage.delete_project(name)
    
    def add_task_to_project(self, project_name: str, task_name: str, description: str = "") -> bool:
        project = self.storage.get_project(project_name)
        if project:
            task_service = TaskService(self.storage)  
            task = task_service.create_task(task_name, description)
            project.tasks.append(task)
            self.storage.add_project(project)
            return True
        return False
    
    def list_projects(self) -> list[Project]:
        return list(self.storage._projects.values())