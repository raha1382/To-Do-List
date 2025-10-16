from ..storage.in_memory_storage import In_Memory_Storage
from ..utils.utils import MAX_NUMBER_OF_PROJECTS
from ..model.project import Project


class Project_Service:
    def __init__(self, storage: In_Memory_Storage):
        self.storage = storage

    def Create_Project(self, name: str, description: str):
        if len(self.storage.list_of_projects) > MAX_NUMBER_OF_PROJECTS:
            raise ValueError(f"Maximum number of projects ({MAX_NUMBER_OF_PROJECTS}) reached")
        
        if name in self.storage._projects:
            raise ValueError(f"Project with name '{name}' already exists. Please enter a different name.")
        
        project = Project(name, description)
        self.storage.add_project(project)
        return project

