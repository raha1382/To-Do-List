from apscheduler.schedulers.background import BackgroundScheduler
from todo.repositories.task_repository import TaskRepository
from todo.app.commands.autoclose_overdue import autoclose_overdue_tasks 
import threading


def start_scheduler(task_repo: TaskRepository):
    def run_scheduler():
        scheduler = BackgroundScheduler()

        scheduler.add_job(
            func=lambda: autoclose_overdue_tasks(task_repo),
            trigger="interval",
            minutes=2,
            id="autoclose_overdue",
            replace_existing=True,
            coalesce=True,
            max_instances=1
        )

        try:
            scheduler.start()
            print("\nScheduler started successfully (checking overdue tasks every 2 minutes)")
        except Exception as e:
            print(f"Failed to start scheduler: {e}")

    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()