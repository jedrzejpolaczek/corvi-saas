def test_upload_csv_and_start_experiment(client):
    client.post("/auth/register", json={"email":"u@x.com","password":"p","org_name":"O"})
    tok = client.post("/auth/token", json={"email":"u@x.com","password":"p"}).json()["access_token"]
    headers={"Authorization": f"Bearer {tok}"}
    # create project (may be gated; ignore failure in freemium)
    client.post("/projects/", params={"name":"P"}, headers=headers)
    pid = 1
    # upload dataset
    data = "a,b\n1,2\n3,4\n".encode()
    files={"file": ("toy.csv", data, "text/csv")}
    r = client.post("/datasets/upload", params={"project_id": pid}, files=files, headers=headers)
    assert r.status_code == 200
    # start experiment random (allowed in freemium)
    r2 = client.post("/experiments/", json={"project_id": pid, "name": "E", "algorithm":"random","backend":"local","space":{"budget":3, "x":{"type":"int","low":0,"high":1}}}, headers=headers)
    assert r2.status_code == 200
