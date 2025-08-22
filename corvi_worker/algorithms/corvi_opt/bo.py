import random, math
from sqlalchemy.orm import Session
from corvi_api.models.job import Trial
from .pruning import should_prune

def expected_improvement(mu, best, sigma, xi=0.01):
    if sigma <= 1e-9: return 0.0
    z = (mu - best - xi) / sigma
    cdf = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    pdf = (1 / math.sqrt(2*math.pi)) * math.exp(-0.5 * z*z)
    return (mu - best - xi) * cdf + sigma * pdf

def run_bayes(db: Session, exp, publish):
    space = exp.space or {}
    budget = space.get("budget", 30)
    keys = [k for k in space.keys() if k != "budget"]
    observations = []
    best = None
    for i in range(budget):
        if len(observations) < max(5, len(keys)):
            params = {}
            for k in keys:
                v = space[k]
                if isinstance(v, list): params[k] = random.choice(v)
                elif isinstance(v, dict) and v.get("type") == "int": params[k] = random.randint(v["low"], v["high"])
                elif isinstance(v, dict) and v.get("type") == "float": params[k] = random.uniform(v["low"], v["high"])
        else:
            values = [v for _, v in observations]
            mu_seen = sum(values)/len(values)
            sd_seen = (sum((x - mu_seen)**2 for x in values)/len(values))**0.5 if values else 1.0
            cand_best, cand_params = -1e9, None
            for _ in range(20):
                params = {}
                for k in keys:
                    v = space[k]
                    if isinstance(v, list): params[k] = random.choice(v)
                    elif isinstance(v, dict) and v.get("type") == "int": params[k] = random.randint(v["low"], v["high"])
                    elif isinstance(v, dict) and v.get("type") == "float": params[k] = random.uniform(v["low"], v["high"])
                ei = expected_improvement(mu_seen, max(values), sd_seen)
                if ei > cand_best: cand_best, cand_params = ei, params
            params = cand_params
        t = Trial(experiment_id=exp.id, params=params, status="running")
        db.add(t); db.commit()
        # simple pruning sim
        progress = 0.0; pruned = False
        for step in range(5):
            progress += random.random()
            if should_prune(step, progress):
                t.status = "pruned"; db.commit(); pruned = True; break
        if not pruned:
            value = sum([vv for vv in params.values() if isinstance(vv, (int,float))]) + progress + random.random()
            t.value = value; t.status = "completed"; db.commit()
            observations.append((params, value))
            if not best or value > best[0]:
                best = (value, params)
    if best:
        exp.best_value = str(best[0]); exp.best_metric = "dummy"; db.commit()
