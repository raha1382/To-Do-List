from datetime import datetime
from sqlalchemy import and_
from todo.db.session import SessionLocal
from todo.model.project import Project
from todo.model.task import Task
from todo.model.enums import TaskStatus
from ..repositories.task_repository import TaskRepository


def autoclose_overdue_tasks(task_repo: TaskRepository):
    db = SessionLocal()
    try:
        now = datetime.now()
        overdue_tasks = db.query(Task).filter(
            and_(
                Task.deadline < now,
                Task.status != TaskStatus.DONE
            )
        ).all()

        for task in overdue_tasks:
            task.status = TaskStatus.DONE
            task.closed_at = now
            task_repo.update(task_id=task.id, status=task.status)
            print(f"\n >Task '{task.title}' (ID: {task.id}) closed automatically.")

        db.commit()
        print(f"\n >Autoclose completed: {len(overdue_tasks)} tasks closed.")
    except Exception as e:
        db.rollback()
        print(f"\n >Error in autoclose: {e}")
    finally:
        db.close()

# if __name__ == "__main__":
#     repo = TaskRepository()
#     autoclose_overdue_tasks(repo)