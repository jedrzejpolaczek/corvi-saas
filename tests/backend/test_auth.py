def test_register_and_login(client):
    r = client.post("/auth/register", json={"email":"a@b.com","password":"x","org_name":"Org"})
    assert r.status_code == 200
    r2 = client.post("/auth/token", json={"email":"a@b.com","password":"x"})
    assert r2.status_code == 200
