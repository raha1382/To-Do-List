from ..model.task import Task, TaskStatus
from ..storage.in_memory_storage import InMemoryStorage
from ..utils.utils import MAX_NUMBER_OF_TASKS

class TaskService:
    
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_task(self, name: str, description: str = "", status: str = TaskStatus.TODO.value, deadline: str | None = None) -> Task:
        """Create a new task with validation."""
        if len(self.storage.list_tasks()) >= MAX_NUMBER_OF_TASKS:
            raise ValueError(f"Maximum number of tasks ({MAX_NUMBER_OF_TASKS}) reached")
        if name in self.storage._tasks:
            raise ValueError(f"Task with name '{name}' already exists")
        
        task = Task(id=0, title=name, description=description, status=status, deadline=deadline)
        self.storage.save_task(task)
        return task
    
    def get_task(self, name: str) -> Task | None:
        return self.storage.get_task(name)
    
    def update_task(self, name: str, new_name: str, description: str, status: str, deadline: str | None) -> bool:
        task = self.storage.get_task(name)
        if task:
            task.title = new_name
            task.description = description
            task.status = status
            task.deadline = deadline
            self.storage.save_task(task)
            if name != new_name:
                del self.storage._tasks[name]
            return True
        return False
    
    def delete_task(self, name: str) -> bool:
        return self.storage.delete_task(name)
    
    def list_tasks(self) -> list[Task]: 
        return self.storage.list_tasks()