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
    
    def save_task(self, task: Task) -> int:
        if not task.id:
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
        """Return all tasks."""
        return list(self._tasks.values())