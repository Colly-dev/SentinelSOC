from typing import List, Dict, Any
from loguru import logger
import uuid

class SuspiciousLoginDetector:
    """
    Detects suspicious login patterns (e.g., unusual times, unusual locations).
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def detect(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info("Running Suspicious Login Detection...")
        alerts = []

        for event in events:
            # Check for logins outside of business hours (mock logic)
            # In a real system, we'd parse the timestamp
            if event.get("original_source") == "auth_logs" and event.get("status") == "Success":
                # For demo purposes, we'll flag logins from specific 'suspicious' IPs
                if event.get("src_ip") == "192.168.1.100": # Mock suspicious IP
                    logger.warning(f"Login from suspicious IP: {event.get('src_ip')}")
                    alerts.append({
                        "id": str(uuid.uuid4()),
                        "title": "Suspicious Login Location",
                        "description": f"A successful login was detected from a flagged IP address: {event.get('src_ip')}",
                        "severity": "Medium",
                        "source": "SuspiciousLoginDetector",
                        "source_ip": event.get("src_ip"),
                        "affected_user": event.get("user"),
                        "mitre_attack_mapping": ["T1078 - Valid Accounts"],
                        "raw_event": event
                    })

        return alerts
