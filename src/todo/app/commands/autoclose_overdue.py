from datetime import datetime
from sqlalchemy import and_
from todo.model.task import Task
from todo.model.enums import TaskStatus
from todo.repositories.task_repository import TaskRepository


def autoclose_overdue_tasks(task_repo: TaskRepository):
    try:
        now = datetime.now()
        overdue_tasks = (
            task_repo.db.query(Task)
            .filter(
                and_(
                    Task.deadline < now,
                    Task.status != TaskStatus.DONE.value
                )
            )
            .all()
        )

        closed_count = 0
        for task in overdue_tasks:
            print(f"Auto-closed overdue task: '{task.title}' (ID: {task.id})")
            closed_count += 1
            task.status = TaskStatus.DONE
            task_repo.update(task_id=task.id, status=TaskStatus.DONE)

        if closed_count > 0:
            print(f"Autoclose job completed: {closed_count} task(s) closed.")
        else:
            print("Autoclose job ran – no overdue tasks found.")

    except Exception as e:
        task_repo.db.rollback()
        print(f"Error in autoclose_overdue_tasks: {e}")