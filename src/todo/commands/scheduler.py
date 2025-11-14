# src/todo/scheduler.py
import time
from apscheduler.schedulers.background import BackgroundScheduler
from todo.commands.autoclose_overdue import autoclose_overdue_tasks

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=autoclose_overdue_tasks,
        trigger="interval",
        minutes=15,
        id='autoclose_overdue',
        name='Autoclose overdue tasks every 15 minutes',
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler started: autoclose every 15 minutes")
    
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()