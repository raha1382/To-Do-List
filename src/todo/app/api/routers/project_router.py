from fastapi import APIRouter, Depends, HTTPException, status
from todo.app.api.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from todo.app.dependencies import get_project_service
from todo.core.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    try:
        project = service.create_project(payload.name, payload.description or "")
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProjectResponse])
async def list_projects(service: ProjectService = Depends(get_project_service)):
    return service.list_projects()

@router.get("/{name}", response_model=ProjectResponse)
async def get_project(name: str, service: ProjectService = Depends(get_project_service)):
    project = service.get_project(name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{name}", response_model=ProjectResponse)
async def update_project(name: str, payload: ProjectUpdate, service: ProjectService = Depends(get_project_service)):
    success = service.update_project(name, payload.name or name, payload.description or "")
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return service.get_project(payload.name or name)

@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(name: str, service: ProjectService = Depends(get_project_service)):
    if not service.delete_project(name):
        raise HTTPException(status_code=404, detail="Project not found")