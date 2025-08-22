def test_corvi_opt_blocked_for_freemium(client):
    client.post("/auth/register", json={"email":"f@x.com","password":"p","org_name":"F"})
    tok = client.post("/auth/token", json={"email":"f@x.com","password":"p"}).json()["access_token"]
    headers={"Authorization": f"Bearer {tok}"}
    r = client.post("/experiments/", json={"project_id": 1, "name": "E", "algorithm":"corvi_opt","backend":"local","space":{"budget":2}}, headers=headers)
    assert r.status_code == 402
