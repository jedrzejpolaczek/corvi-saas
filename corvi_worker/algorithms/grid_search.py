import itertools
from sqlalchemy.orm import Session
from corvi_api.models.job import Trial

def run_grid(db: Session, exp, publish):
    space = exp.space or {}
    keys = list(space.keys())
    values = [space[k] if isinstance(space[k], list) else [space[k]] for k in keys]
    best = None
    for combo in itertools.product(*values):
        params = {k: v for k, v in zip(keys, combo)}
        t = Trial(experiment_id=exp.id, params=params, status="running")
        db.add(t); db.commit()
        value = sum([v for v in params.values() if isinstance(v, (int,float))])
        t.value = value; t.status = "completed"; db.commit()
        if best is None or value > best[0]:
            best = (value, params)
    if best:
        exp.best_value = str(best[0]); exp.best_metric = "dummy"; db.commit()
