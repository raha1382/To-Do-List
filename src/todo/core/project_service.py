from ..storage.in_memory_storage import InMemoryStorage
from ..utils.utils import MAX_NUMBER_OF_PROJECTS
from ..model.project import Project
from ..core.task_service import TaskService
from ..utils.validators import validate_name_of_project, validate_description_of_project

class ProjectService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_project(self, name: str, description: str) -> Project:
        if len(self.storage._projects) >= MAX_NUMBER_OF_PROJECTS:
            raise ValueError(f"Maximum number of projects ({MAX_NUMBER_OF_PROJECTS}) reached")
        
        if name in self.storage._projects:
            raise ValueError(f"Project with name '{name}' already exists. Please enter a different name.")
        
        validate_name_of_project(name)
        validate_description_of_project(description)
        
        project_id = max((project_item.id for project_item in self.storage._projects.values()), default=-1) + 1
        project = Project(id=project_id, name=name, description=description)
        self.storage.add_project(project)
        return project
    
    def get_project(self, name: str) -> Project | None:
        return self.storage.get_project(name)

    def update_project(self, name: str, new_name: str, new_description: str) -> bool:
        # Check if the original project exists
        if name not in self.storage._projects:
            return False

        # Check if the new name already exists
        if new_name and new_name != name and new_name in self.storage._projects:
            raise ValueError(f"Project '{new_name}' already exists.")

        # Get the project
        project = self.storage._projects[name]
        # Update attributes
        project.name = new_name or name  
        project.description = new_description or project.description  

        # Remove old reference and add with new name if changed
        if name != new_name:
            del self.storage._projects[name]
            self.storage._projects[new_name] = project

        return True
    
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