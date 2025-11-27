# todo/app/background/autoclose.py
from datetime import datetime
from sqlalchemy import and_
from todo.model.task import Task
from todo.model.enums import TaskStatus


def autoclose_overdue_tasks(task_repo):
    try:
        now = datetime.now()
        overdue_tasks = (
            task_repo.db.query(Task)
            .filter(
                and_(
                    Task.deadline < now,
                    Task.status != TaskStatus.DONE
                )
            )
            .all()
        )

        closed_count = 0
        for task in overdue_tasks:
            was_changed = False
            if task.status != TaskStatus.DONE:
                task.status = TaskStatus.DONE
                was_changed = True
            if task.closed_at is None:
                task.closed_at = now
                was_changed = True

            if was_changed:
                task_repo.update(task_id=task.id, status=TaskStatus.DONE, closed_at=now)
                print(f"Auto-closed overdue task: '{task.title}' (ID: {task.id})")
                closed_count += 1

        if closed_count > 0:
            task_repo.db.commit()
            print(f"Autoclose job completed: {closed_count} task(s) closed.")
        else:
            print("Autoclose job ran – no overdue tasks found.")

    except Exception as e:
        task_repo.db.rollback()
        print(f"Error in autoclose_overdue_tasks: {e}")