from apscheduler.schedulers.background import BackgroundScheduler
from todo.commands.autoclose_overdue import autoclose_overdue_tasks
from ..repositories.task_repository import TaskRepository

def start_scheduler(task_repo: TaskRepository):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: autoclose_overdue_tasks(task_repo),
        trigger="interval",
        minutes=15,
        id='autoclose_overdue',
        replace_existing=True
    )
    scheduler.start()
    print("\n >Scheduler started.")