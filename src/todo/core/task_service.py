from ..model.task import Task
from ..model.enums import TaskStatus
from ..storage.in_memory_storage import InMemoryStorage
from ..utils.utils import MAX_NUMBER_OF_TASKS, TASK_STATUS
from ..utils.validators import validate_name_of_task, validate_description_of_task, validate_status_of_task, validate_deadline
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self.project_repo = project_repo
        self.task_repo = task_repo

    def create_task(self, name: str, description: str = "", status: str = TaskStatus.TODO.value, deadline: str | None = None, project_name: str = None) -> Task:
        # Check max number of tasks
        all_tasks = self.task_repo.get_all()
        if len(all_tasks) >= MAX_NUMBER_OF_TASKS:
            raise ValueError(f"Maximum number of tasks ({MAX_NUMBER_OF_TASKS}) reached")

        # Check for duplicate task title
        if any(task.title == name for task in all_tasks):
            raise ValueError(f"Task with name '{name}' already exists")

        # Validate status
        status = validate_status_of_task(status)
        status_enum = TaskStatus(status) 

        # Validate and convert deadline
        deadline_datetime = validate_deadline(deadline)
        
        # Find or create project if project_name is provided
        project = None
        if project_name:
            project = self.project_repo.get_by_name(project_name)
            if not project:
                raise ValueError(f"Project '{project_name}' not found.")

        task = self.task_repo.create(
            title=name,
            project_name=project_name,
            description=description,
            status=status_enum,
            deadline=deadline_datetime
        )
        return task
    
    def get_task(self, name: str) -> Task | None:
        return next((task for task in self.task_repo.get_all() if task.title == name), None)
    
    def update_task(self, project_name: str, task_name: str, new_name: str, description: str, status: str, deadline: str | None = None) -> bool:
        # Validate project exists
        project = self.project_repo.get_by_name(project_name)
        if not project:
            return False

        # Find the task by title
        task = self.task_repo.get_by_project_name_and_title(project_name, task_name)
        if not task:
            return False

        # Validate inputs
        new_name = validate_name_of_task(new_name)
        validate_description_of_task(description)
        status = validate_status_of_task(status)
        status_enum = TaskStatus(status) 
        deadline_datetime = validate_deadline(deadline)

        return self.task_repo.update(
            task_id=task.id,
            title=new_name,
            description=description,
            status=status_enum,
            deadline=deadline_datetime
        )
    
    def delete_task(self, project_name: str, task_id: int) -> bool:
        project = self.project_repo.get_by_name(project_name)
        if not project:
            return False
        return self.task_repo.delete(task_id)
    
    def list_tasks(self, project_name: str) -> list[Task]:
        project = self.project_repo.get_by_name(project_name)
        if not project:
            raise ValueError(f"Project '{project_name}' not found.")
        return self.task_repo.get_by_project_name(project_name)
    
    def change_task_status(self, project_name: str, task_name: str, new_status: str) -> bool:
        task = self.task_repo.get_by_project_name_and_title(project_name, task_name)
        if not task:
            return False

        # Validate and update status
        validated_status = validate_status_of_task(new_status)
        status_enum = TaskStatus(validated_status) 
        return self.task_repo.update(task_id=task.id, status=status_enum)