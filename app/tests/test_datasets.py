import io, csv
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def auth_headers():
    client.post("/auth/register", json={"name":"Bob","email":"bob@example.com","password":"x"})
    r = client.post("/auth/login", json={"email":"bob@example.com","password":"x"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

def make_csv_bytes():
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["f1", "f2", "target"])
    for i in range(100):
        w.writerow([i, i*2, 1 if i%2==0 else 0])
    return io.BytesIO(buf.getvalue().encode())

def test_upload_dataset(monkeypatch, tmp_path):
    # Monkeypatch S3 to local writes
    from app.services import s3 as s3mod
    class Dummy:
        bucket = "dev"
        def sha256_of_fileobj(self, f): 
            import hashlib; 
            pos=f.tell(); f.seek(0); h=hashlib.sha256(f.read()).hexdigest(); f.seek(pos); 
            return h
        def upload_fileobj(self, fileobj, key, content_type="text/csv"):
            dest = tmp_path / key
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as out:
                fileobj.seek(0); out.write(fileobj.read())
        def download_to_path(self, key, path): 
            src = tmp_path / key
            with open(src, "rb") as inp, open(path, "wb") as out: out.write(inp.read())
    s3mod.s3_client = Dummy()

    headers = auth_headers()
    files = {"file": ("data.csv", make_csv_bytes(), "text/csv")}
    r = client.post("/datasets/upload", files=files, headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["id"]
    assert body["filename"] == "data.csv"
