from typing import Dict, List
from fastapi import WebSocket

class WSManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, experiment_id: str, ws: WebSocket):
        await ws.accept()
        self.connections.setdefault(experiment_id, []).append(ws)

    def disconnect(self, experiment_id: str, ws: WebSocket):
        conns = self.connections.get(experiment_id, [])
        if ws in conns:
            conns.remove(ws)

    async def broadcast(self, experiment_id: str, message: str):
        for ws in list(self.connections.get(experiment_id, [])):
            try:
                await ws.send_text(message)
            except Exception:
                self.disconnect(experiment_id, ws)

ws_manager = WSManager()
