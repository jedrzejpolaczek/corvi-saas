import random
from sqlalchemy.orm import Session
from corvi_api.models.job import Trial

def run_random(db: Session, exp, publish):
    space = exp.space or {}
    n = space.get("budget", 20)
    keys = [k for k in space.keys() if k != "budget"]
    best = None
    for _ in range(n):
        params = {}
        for k in keys:
            v = space[k]
            if isinstance(v, list):
                params[k] = random.choice(v)
            elif isinstance(v, dict) and v.get("type") == "int":
                params[k] = random.randint(v["low"], v["high"])
            elif isinstance(v, dict) and v.get("type") == "float":
                params[k] = random.uniform(v["low"], v["high"])
        t = Trial(experiment_id=exp.id, params=params, status="running")
        db.add(t); db.commit()
        value = sum([vv for vv in params.values() if isinstance(vv, (int,float))]) + random.random()
        t.value = value; t.status = "completed"; db.commit()
        if not best or value > best[0]:
            best = (value, params)
    if best:
        exp.best_value = str(best[0]); exp.best_metric = "dummy"; db.commit()
