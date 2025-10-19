from fastapi import APIRouter, Depends, HTTPException, WebSocket, UploadFile, File, Form
from sqlalchemy.orm import Session
import json
from db import get_db
from security import get_current_user
from models.experiment import Experiment, AlgoEnum, BackendEnum
from models.subscription import UsageQuota
from models.job import Job, Trial
from feature_gating import enforce_feature, Feature, enforce_quota
from websocket_manager import ws_manager
from config import settings
import pika, redis
from typing import Optional

router = APIRouter(tags=["experiments"]) 

def _publish(job: dict):
    if settings.QUEUE_BACKEND == "rabbitmq":
        params = pika.URLParameters(settings.RABBITMQ_URL)
        conn = pika.BlockingConnection(params)
        ch = conn.channel(); ch.queue_declare(queue="corvi_jobs", durable=True)
        ch.basic_publish(exchange="", routing_key="corvi_jobs", body=json.dumps(job))
        conn.close()
    else:
        r = redis.Redis.from_url(settings.REDIS_URL)
        r.lpush("corvi_jobs", json.dumps(job))

@router.post("/")
def create_experiment_with_files(
    dataset: UploadFile = File(...),
    model: Optional[UploadFile] = File(None),
    predefined_model: Optional[str] = Form(None),
    settings: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Create experiment with file uploads from frontend
    """
    try:
        # Parse the settings JSON
        experiment_settings = json.loads(settings)
        
        # Determine the algorithm based on the settings
        algorithm = experiment_settings.get('optimization_algorithm', 'random_search')
        if algorithm == 'random_search' or algorithm == 'random':
            algo_enum = AlgoEnum.random
        elif algorithm == 'grid_search' or algorithm == 'grid':
            algo_enum = AlgoEnum.grid
        elif algorithm == 'corvi_opt':
            algo_enum = AlgoEnum.corvi_opt
        else:
            algo_enum = AlgoEnum.random
        
        # Create experiment name based on dataset filename
        experiment_name = f"Experiment {dataset.filename} - {algorithm}"
        
        # For demo purposes, we'll use a default project_id of 1
        # In production, this should come from the user's context
        project_id = 1
        
        # Create the experiment
        exp = Experiment(
            project_id=project_id, 
            name=experiment_name, 
            algorithm=algo_enum, 
            backend=BackendEnum.local, 
            space=experiment_settings, 
            status="queued"
        )
        db.add(exp)
        db.commit()
        
        # Create job for worker
        job = {
            "kind": "hpo", 
            "experiment_id": exp.id,
            "dataset_filename": dataset.filename,
            "model_filename": model.filename if model else None,
            "predefined_model": predefined_model,
            "settings": experiment_settings
        }
        _publish(job)
        
        return {"experiment_id": exp.id, "status": exp.status, "message": "Experiment started successfully"}
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid settings JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create experiment: {str(e)}")

@router.post("/legacy")
def create_experiment(project_id: int, name: str, algorithm: AlgoEnum, backend: BackendEnum = BackendEnum.local, space: dict = {}, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(enforce_quota("experiments_per_month"))):
    if algorithm == AlgoEnum.corvi_opt:
        enforce_feature(Feature.CORVI_OPT)(db=db, user=user)
    exp = Experiment(project_id=project_id, name=name, algorithm=algorithm, backend=backend, space=space, status="queued")
    db.add(exp); db.commit()
    q = db.query(UsageQuota).filter(UsageQuota.org_id==user.default_org_id, UsageQuota.key=="experiments_per_month").first()
    if q:
        q.used += 1; db.commit()
    job = {"kind": "hpo", "experiment_id": exp.id}
    _publish(job)
    return {"id": exp.id, "status": exp.status}

@router.post("/{id}/pause")
def pause_experiment(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    exp = db.query(Experiment).get(id)
    exp.status = "paused"; db.commit(); return {"status":"paused"}

@router.post("/{id}/stop")
def stop_experiment(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    exp = db.query(Experiment).get(id)
    exp.status = "stopped"; db.commit(); return {"status":"stopped"}

@router.websocket("/ws/jobs/{experiment_id}")
async def ws_jobs(ws: WebSocket, experiment_id: str):
    await ws.accept()
    # Demo echo for local; real worker may publish via Redis/Rabbit fanout -> for simplicity just keepalive
    try:
        while True:
            await ws.receive_text()
            await ws.send_text(json.dumps({"event":"ping","exp":experiment_id}))
    except Exception:
        pass
    finally:
        await ws.close()
