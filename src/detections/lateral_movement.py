from typing import List, Dict, Any
from loguru import logger
import uuid

class LateralMovementDetector:
    """
    Detects lateral movement indicators like remote service creation or PsExec.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def detect(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info("Running Lateral Movement Detection...")
        alerts = []

        for event in events:
            raw = event.get("raw", {})
            # Check for service installation (Event ID 7045 for Windows)
            if event.get("original_source") == "windows_events" and raw.get("EventID") == 7045:
                service_name = raw.get("ServiceName", "")
                if "PSEXESVC" in service_name or "winexesvc" in service_name:
                    logger.warning(f"Lateral movement tool detected: {service_name}")
                    alerts.append({
                        "id": str(uuid.uuid4()),
                        "title": "Lateral Movement Tool Detected",
                        "description": f"A remote execution service was installed: {service_name}",
                        "severity": "High",
                        "source": "LateralMovementDetector",
                        "affected_user": event.get("user"),
                        "mitre_attack_mapping": ["T1021.002 - Remote Services: SMB/Windows Admin Shares"],
                        "raw_event": event
                    })

        return alerts
