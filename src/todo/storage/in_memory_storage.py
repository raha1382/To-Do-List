from ..model.project import Project
from ..model.task import Task
from typing import Dict, List

class InMemoryStorage:
    def __init__(self):
        self._projects: dict[str, Project] = {}
        self._tasks: dict[int, Task] = {}
        self._next_task_id = 0

    def add_project(self, project: Project) -> None:
        self._projects[project.name] = project

    def get_project(self, name: str) -> Project | None:
        return self._projects.get(name)

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
    
    def add_task(self, task: Task) -> int:
        if task.id is None or task.id == 0:
            task.id = self._next_task_id
            self._next_task_id += 1
        self._tasks[task.id] = task
        return task.id
    
    def get_task(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def list_tasks(self) -> List[Task]:
        return list(self._tasks.values())