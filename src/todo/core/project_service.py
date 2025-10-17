from ..storage.in_memory_storage import In_Memory_Storage
from ..utils.utils import MAX_NUMBER_OF_PROJECTS
from ..model.project import Project


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
    
    def get_project(self, project_id: int) -> Project | None:
        return self.storage.get_project(project_id)

    def update_project(self, project_id: int, name: str, description: str) -> bool:
        project = self.storage.get_project(project_id)
        if project:
            project.update(name, description)
            self.storage.save_project(project)
            return True
        return False
