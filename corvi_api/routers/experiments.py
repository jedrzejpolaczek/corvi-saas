from fastapi import APIRouter, Depends, HTTPException, WebSocket
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

router = APIRouter(prefix="/experiments", tags=["experiments"]) 

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
