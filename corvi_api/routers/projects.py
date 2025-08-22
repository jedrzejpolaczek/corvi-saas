from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..security import get_current_user
from ..models.project import Project
from ..feature_gating import enforce_feature, Feature

router = APIRouter(prefix="/projects", tags=["projects"]) 

@router.post("/")
def create_project(name: str, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(enforce_feature(Feature.MULTI_PROJECT))):
    p = Project(org_id=user.default_org_id, name=name)
    db.add(p); db.commit()
    return {"id": p.id, "name": p.name}

@router.get("/")
def list_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.query(Project).filter(Project.org_id==user.default_org_id).all()
    return [{"id": r.id, "name": r.name} for r in rows]
