import io, csv, time
from fastapi.testclient import TestClient
from app.main import app
from app.workers.celery_app import celery

# Run Celery tasks eagerly in tests
celery.conf.task_always_eager = True

client = TestClient(app)

def auth_headers():
    client.post("/auth/register", json={"name":"Eve","email":"eve@example.com","password":"x"})
    r = client.post("/auth/login", json={"email":"eve@example.com","password":"x"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

def make_csv_bytes():
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["a","b","target"])
    for i in range(200):
        w.writerow([i, i*0.5, 1 if i%2==0 else 0])
    return buf.getvalue().encode()

def test_experiment_flow(monkeypatch, tmp_path):
    # Fake S3 local
    from app.services import s3 as s3mod
    class Dummy:
        bucket = "dev"
        def sha256_of_fileobj(self, f): 
            import hashlib; pos=f.tell(); f.seek(0); h=hashlib.sha256(f.read()).hexdigest(); f.seek(pos); return h
        def upload_fileobj(self, fileobj, key, content_type="text/csv"):
            dest = tmp_path / key; dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as out: fileobj.seek(0); out.write(fileobj.read())
        def download_to_path(self, key, path): 
            src = tmp_path / key
            with open(src, "rb") as inp, open(path, "wb") as out: out.write(inp.read())
    s3mod.s3_client = Dummy()

    headers = auth_headers()
    files = {"file": ("train.csv", io.BytesIO(make_csv_bytes()), "text/csv")}
    r = client.post("/datasets/upload", files=files, headers=headers)
    ds_id = r.json()["id"]

    payload = {
        "dataset_id": ds_id,
        "task_type": "classification",
        "objective_metric": "accuracy",
        "budget_trials": 10,
        "time_limit_minutes": 1
    }
    r = client.post("/experiments", json=payload, headers=headers)
    assert r.status_code in (200,201)
    exp = r.json()
    exp_id = exp["id"]

    # Since tasks are eager, trials should appear quickly
    time.sleep(0.1)
    r = client.get(f"/experiments/{exp_id}/status", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in ("running","finished","stopped")

    r = client.get(f"/experiments/{exp_id}", headers=headers)
    assert r.status_code == 200
    data = r.json()
    # Either first_useful_result present, or trials exist
    if data["first_useful_result"]:
        assert data["first_useful_result"]["trials_used"] >= 1
