import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from corvi_api.models.experiment import Experiment, AlgoEnum
from .queue import QueueConsumer
from .algorithms.grid_search import run_grid
from .algorithms.random_search import run_random
from .algorithms.corvi_opt.bo import run_bayes
from .config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def handle_job(job: dict):
    db = SessionLocal()
    try:
        if job.get("kind") == "hpo":
            exp = db.query(Experiment).get(job["experiment_id"])  # type: ignore
            if not exp: return
            exp.status = "running"; db.commit()
            if exp.algorithm == AlgoEnum.grid:
                run_grid(db, exp, lambda *_: None)
            elif exp.algorithm == AlgoEnum.random:
                run_random(db, exp, lambda *_: None)
            else:
                run_bayes(db, exp, lambda *_: None)
            exp.status = "completed"; db.commit()
    finally:
        db.close()

def main():
    consumer = QueueConsumer()
    consumer.consume(handle_job)

if __name__ == "__main__":
    main()
