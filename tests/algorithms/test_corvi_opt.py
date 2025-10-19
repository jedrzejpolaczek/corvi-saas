from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from corvi_api.models.base import Base
from corvi_api.models.experiment import Experiment, AlgoEnum
from corvi_worker.algorithms.corvi_opt.bo import run_bayes

def test_bayes_run():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine); db = Session()
    e = Experiment(project_id=1, name="b", algorithm=AlgoEnum.corvi_opt, space={"budget":5, "x":{"type":"int","low":0,"high":3}})
    db.add(e); db.commit()
    run_bayes(db, e, lambda *a, **k: None)
