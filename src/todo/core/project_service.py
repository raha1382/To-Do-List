from ..storage.in_memory_storage import In_Memory_Storage
from ..utils.utils import MAX_NUMBER_OF_PROJECTS
from ..model.project import Project
from ..core.task_service import Task_Service


class Project_Service:
    def __init__(self, storage: In_Memory_Storage):
        self.storage = storage

    def Create_Project(self, name: str, description: str) -> Project:
        if len(self.storage.list_of_projects) > MAX_NUMBER_OF_PROJECTS:
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
                del self.storage._projects[name]
            return True
        return False
    
    def delete_project(self, name: str) -> bool:
        return self.storage.delete_project(name)
    
    def add_task_to_project(self, project_name: str, task_name: str, description: str = "") -> bool:
        project = self.storage.get_project(project_name)
        if project:
            task_service = Task_Service(self.storage)
            task = task_service.create_task(task_name, description)
            project.tasks.append(task)
            self.storage.add_project(project)
            return True
        return False
    
    def list_projects(self) -> list[Project]:
        return self.storage.list_projects()