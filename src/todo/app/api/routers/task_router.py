from fastapi import APIRouter, Depends, HTTPException, status
from todo.app.api.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate
from todo.app.dependencies import get_task_service
from todo.core.task_service import TaskService
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, service: TaskService = Depends(get_task_service)):
    try:
        task = service.create_task(
            name=payload.title,
            description=payload.description or "",
            deadline=payload.deadline,
            project_name=payload.project_name
        )
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(project_name: str, service: TaskService = Depends(get_task_service)):
    try:
        return service.list_tasks(project_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, payload: TaskUpdate, service: TaskService = Depends(get_task_service)):
    task = service.get_task_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    try:
        updated = service.update_task(
            task_id=task_id,
            new_name=payload.title or task.title,
            description=payload.description or task.description,
            status=payload.status,
            deadline=payload.deadline or task.deadline
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_status(task_id: int, payload: TaskStatusUpdate, service: TaskService = Depends(get_task_service)):
    task = service.get_task_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    try:
        updated = service.update_task(
            task_id=task_id,
            new_name=None,
            description=None,
            status=payload.status,
            deadline=None
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    if not service.delete_task(None, task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    