from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    type: str
    ts: datetime
    payload: dict

def emit(event: Event) -> None:
    # Placeholder for future event bus (Kafka, etc.)
    pass
