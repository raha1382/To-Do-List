from fastapi import FastAPI
from todo.app.api.routers import project, task
from todo.commands.scheduler import start_scheduler

app = FastAPI(
    title="ToDo List API - version",
    description="Web API format",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(project.router)
app.include_router(task.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    print("Background scheduler started")