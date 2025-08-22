from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from corvi_api.models.base import Base
from corvi_api.models.experiment import Experiment, AlgoEnum
from corvi_worker.algorithms.grid_search import run_grid
from corvi_worker.algorithms.random_search import run_random

def test_grid_random_run(tmp_path):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine); db = Session()
    e1 = Experiment(project_id=1, name="g", algorithm=AlgoEnum.grid, space={"x":[1,2],"y":[3,4]})
    e2 = Experiment(project_id=1, name="r", algorithm=AlgoEnum.random, space={"budget":3, "x":{"type":"int","low":0,"high":2}})
    db.add_all([e1,e2]); db.commit()
    run_grid(db, e1, lambda *a, **k: None)
    run_random(db, e2, lambda *a, **k: None)
