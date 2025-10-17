from ..model.project import Project
from ..model.task import Task
from ..utils.utils import MAX_NUMBER_OF_PROJECTS, MAX_NUMBER_OF_TASKS

class In_Memory_Storage:
    def __init__(self):
        self._projects: dict[str, Project] = {}
        self._tasks: dict[str, Task] = {}

    def add_project(self, project: Project):
        self._projects[project.name] = project
        