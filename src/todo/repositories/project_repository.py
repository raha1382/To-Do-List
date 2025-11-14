from typing import List, Optional
from src.todo.model.project import Project
from src.todo.db.session import sessionlocal

class ProjectRepository:
    def __init__(self):
        self.db = next(sessionlocal())

    def create(self, name: str, description: Optional[str] = None) -> Project:
        # project_id = max((project_item.id for project_item in self.storage._projects.values()), default=-1) + 1
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.name == name).first()

    def get_all(self) -> List[Project]:
        return self.db.query(Project).all()

    def update(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Project]:
        project = self.get_by_id(project_id)
        if not project:
            return None
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> bool:
        project = self.get_by_id(project_id)
        if not project:
            return False
        self.db.delete(project)
        self.db.commit()
        return True