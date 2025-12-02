from fastapi import FastAPI
from todo.app.api.routers import project_router, task_router
from todo.app.commands.scheduler import start_scheduler
from todo.repositories.task_repository import TaskRepository
from todo.db.session import SessionLocal

app = FastAPI(
    title="ToDo List API - version",
    description="Web API format",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(project_router.router)
app.include_router(task_router.router)

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    task_repo = TaskRepository(db)
    start_scheduler(task_repo)   
    print("Application startup complete")