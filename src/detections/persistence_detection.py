from typing import List, Dict, Any
from loguru import logger
import uuid

class PersistenceDetector:
    """
    Detects persistence mechanisms like registry modifications or scheduled tasks.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def detect(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info("Running Persistence Detection...")
        alerts = []

        for event in events:
            raw = event.get("raw", {})
            # Check for registry Run key modifications (Event ID 13 for Sysmon)
            if event.get("original_source") == "sysmon_logs" and raw.get("EventID") == 13:
                target_obj = raw.get("TargetObject", "")
                if "Microsoft\\Windows\\CurrentVersion\\Run" in target_obj:
                    logger.warning(f"Persistence mechanism detected: {target_obj}")
                    alerts.append({
                        "id": str(uuid.uuid4()),
                        "title": "Registry Persistence Detected",
                        "description": f"A modification was made to a Windows Run key: {target_obj}",
                        "severity": "High",
                        "source": "PersistenceDetector",
                        "affected_user": event.get("user"),
                        "mitre_attack_mapping": ["T1547.001 - Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder"],
                        "raw_event": event
                    })

        return alerts
