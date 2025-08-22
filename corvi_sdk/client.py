import requests
from typing import Optional

class Client:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.token = token

    def login(self, email: str, password: str):
        r = requests.post(f"{self.base_url}/auth/token", json={"email": email, "password": password})
        r.raise_for_status(); data = r.json(); self.token = data["access_token"]; return data

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def create_experiment(self, project_id: int, name: str, algorithm: str, backend: str, space: dict):
        r = requests.post(f"{self.base_url}/experiments/", json={"project_id": project_id, "name": name, "algorithm": algorithm, "backend": backend, "space": space}, headers=self._headers())
        r.raise_for_status(); return r.json()
