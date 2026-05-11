import json
import os
import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger("session_recorder")

class SessionRecorder:
    """
    Registrador de sessões minimalista e determinístico (JSONL).
    Garante persistência atômica de eventos de orquestração.
    """

    def __init__(self, session_id: str, base_dir: str = ".sessions"):
        self.session_id = session_id
        self.log_path = os.path.join(base_dir, f"{session_id}.jsonl")
        os.makedirs(base_dir, exist_ok=True)

    def record(self, event_type: str, data: Dict[str, Any]):
        """Grava um evento atômico no arquivo JSONL."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "session_id": self.session_id,
            "data": data
        }
        
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
                f.flush() # Garantia de persistência imediata
                os.fsync(f.fileno()) # Garantia de escrita no disco
        except Exception as e:
            logger.error(f"Falha ao persistir evento {event_type}: {e}")
            # Fail-fast/Fail-silent: persistência falha, mas o runtime continua
