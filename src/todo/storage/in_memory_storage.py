from ..model.project import Project
from ..model.task import Task
from ..utils.utils import MAX_NUMBER_OF_PROJECTS, MAX_NUMBER_OF_TASKS

class In_Memory_Storage:
    def __init__(self):
        self._projects: dict[str, Project] = {}
        self._tasks: dict[str, Task] = {}

    def add_project(self, project: Project):
        self._projects[project.name] = project

    def get_project(self, name: str):
            project = self._projects[name]
            return project

    def delete_project(self, name: str) -> bool:
        if not name or not isinstance(name, str):
            raise ValueError("Project name must be a non-empty string.")
        if name in self._projects:
            del self._projects[name]
            self._tasks = {
                task_key: task 
                for task_key, task in self._tasks.items() 
                if getattr(task, 'project_name', '') != name
            }
            return True
        return False
    
    def list_projects(self) -> list[Project]:
        return list(self._projects.values())