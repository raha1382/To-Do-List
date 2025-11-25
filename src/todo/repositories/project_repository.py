from typing import List, Optional
from todo.model.project import Project
from todo.model.project import Task
from todo.db.session import get_db

class ProjectRepository:
    def __init__(self):
        self.db = next(get_db())

    def create(self, name: str, description: Optional[str] = None) -> Project:
        if description is not None:
            description = description.strip()
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

    def update(self, name: Optional[str] = None, new_name: Optional[str] = None, description: Optional[str] = None) -> Optional[Project]:
        if new_name is not None:
            new_name = new_name.strip()
        if description is not None:
            description = description.strip()

        project = self.get_by_name(name)
        if not project:
            return None
        if new_name is not None:
            exists = self.db.query(Project).filter(Project.name == new_name).first()
            if not exists:
                project.name = new_name
        if description is not None:
            project.description = description
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, name: Optional[str] = None) -> bool:
        project = self.get_by_name(name)
        if not project:
            return False
        self.db.delete(project)
        self.db.commit()
        return True