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