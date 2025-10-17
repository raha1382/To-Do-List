from ..model.task import Task
from ..storage.in_memory_storage import InMemoryStorage
from ..utils.utils import MAX_NUMBER_OF_TASKS, TASK_STATUS

class TaskService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_task(self, name: str, description: str = "", status: str = TASK_STATUS[0], deadline: str | None = None, project_name: str = None) -> Task:
        if len(self.storage._tasks) >= MAX_NUMBER_OF_TASKS:
            raise ValueError(f"Maximum number of tasks ({MAX_NUMBER_OF_TASKS}) reached")
        if name in [task.title for task in self.storage._tasks.values()]:
            raise ValueError(f"Task with name '{name}' already exists")
        
        task = Task(id=0, title=name, description=description, status=status, deadline=deadline, project_name=project_name)
        self.storage.add_task(task)
        return task
    
    def get_task(self, name: str) -> Task | None:
        return next((task for task in self.storage._tasks.values() if task.title == name), None)
    
    def update_task(self, name: str, new_name: str, description: str, status: str, deadline: str | None) -> bool:
        task = self.get_task(name)
        if task:
            if status not in TASK_STATUS:
                raise ValueError(f"Status must be one of {', '.join(TASK_STATUS)}.")
            task.title = new_name
            task.description = description
            task.status = status
            task.deadline = deadline
            self.storage.add_task(task)
            if name != new_name:
                # Remove old reference if title changes
                pass 
            return True
        return False
    
    def delete_task(self, name: str) -> bool:
        task = self.get_task(name)
        if task and task.id in self.storage._tasks:
            del self.storage._tasks[task.id]
            return True
        return False
    
    def list_tasks(self) -> list[Task]: 
        return list(self.storage._tasks.values())