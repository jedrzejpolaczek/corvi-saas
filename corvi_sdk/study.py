from dataclasses import dataclass
from .client import Client

@dataclass
class Study:
    client: Client
    project_id: int

    def optimize_dummy(self):
        space = {"budget": 10, "x": {"type": "int", "low": 0, "high": 10}}
        return self.client.create_experiment(self.project_id, "demo", "random", "local", space)
