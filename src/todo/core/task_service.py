from ..model.task import Task
from ..storage.in_memory_storage import InMemoryStorage
from ..utils.utils import MAX_NUMBER_OF_TASKS, TASK_STATUS
from ..utils.validators import validate_name_of_task, validate_description_of_task, validate_status_of_task, validate_deadline

class TaskService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage

    def create_task(self, name: str, description: str = "", status: str = TASK_STATUS[0], deadline: str | None = None, project_name: str = None) -> Task:
        # Check max number of tasks
        if len(self.storage._tasks) >= MAX_NUMBER_OF_TASKS:
            raise ValueError(f"Maximum number of tasks ({MAX_NUMBER_OF_TASKS}) reached")

        # Check for duplicate task title
        if any(task.title == name for task in self.storage._tasks.values()):
            raise ValueError(f"Task with name '{name}' already exists")

        # Validate status
        status = validate_status_of_task(status)

        # Validate and convert deadline
        deadline_datetime = validate_deadline(deadline)
        
        # Find or create project if project_name is provided
        project = None
        if project_name:
            project = self.storage.get_project(project_name)
            if not project:
                raise ValueError(f"Project '{project_name}' not found.")

        # Create task with auto-incremented ID
        task_id = max((task.id for task in self.storage._tasks.values()), default=-1) + 1
        task = Task(
            id=task_id,
            title=name,
            description=description,
            status=status,
            deadline=deadline_datetime,
            project_name=project_name
        )

        # Add task to project if project_name is provided
        if project:
            project.tasks.append(task)

        # Add task to storage
        self.storage._tasks[task_id] = task
        return task
    
    def get_task(self, name: str) -> Task | None:
        return next((task for task in self.storage._tasks.values() if task.title == name), None)
    
    def update_task(self, project_name: str, task_name: str, new_name: str, description: str, status: str, deadline: str | None = None) -> bool:
        # Validate project exists
        if project_name not in self.storage._projects:
            return False

        project = self.storage._projects[project_name]
        # Find the task by title
        task = next((t for t in project.tasks if t.title == task_name), None)
        if not task:
            return False

        # Validate inputs
        new_name = validate_name_of_task(new_name)
        validate_description_of_task(description)
        status = validate_status_of_task(status)
        deadline_datetime = validate_deadline(deadline)

        # Update task attributes
        task.title = new_name
        task.description = description
        task.status = status
        task.deadline = deadline_datetime

        # No need to update storage dictionary since tasks are updated in place
        return True
    
    def delete_task(self, project_name: str, task_id: int) -> bool:
        if project_name not in self.storage._projects:
            return False
        project = self.storage._projects[project_name]
        task_to_delete = next((task for task in project.tasks if task.id == task_id), None)
        if task_to_delete is None:
            return False
        project.tasks.remove(task_to_delete)
        return True
    
    def list_tasks(self, project_name: str) -> list[Task]:
        if project_name not in self.storage._projects:
            raise ValueError(f"Project '{project_name}' not found.")
        project = self.storage._projects[project_name]
        return project.tasks if project.tasks else []
    
    def change_task_status(self, project_name: str, task_name: str, new_status: str) -> bool:
        # Find the project
        project = self.storage.get_project(project_name)
        if not project:
            return False

        # Find the task in the project's tasks
        task = next((t for t in project.tasks if t.title == task_name), None)
        if not task:
            return False

        # Validate and update status
        task.status = validate_status_of_task(new_status)
        return True