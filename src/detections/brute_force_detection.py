from typing import List, Dict, Any
from loguru import logger
from datetime import datetime
import uuid

class BruteForceDetector:
    """
    Detects brute force attacks by monitoring failed login attempts.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.threshold = config.get('detection_rules', {}).get('brute_force', {}).get('threshold', 5)

    def detect(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info("Running Brute Force Detection...")
        alerts = []
        
        # Group failed logins by source IP
        failed_logins: Dict[str, List[Dict[str, Any]]] = {}
        
        for event in events:
            # Check for failed login indicators (Event ID 4625 for Windows, or custom status)
            is_failed = False
            if event.get("original_source") == "windows_events" and event.get("action") == 4625:
                is_failed = True
            elif event.get("status") == "Failure":
                is_failed = True
                
            if is_failed and event.get("src_ip"):
                ip = event["src_ip"]
                if ip not in failed_logins:
                    failed_logins[ip] = []
                failed_logins[ip].append(event)

        # Generate alerts for IPs exceeding the threshold
        for ip, attempts in failed_logins.items():
            if len(attempts) >= self.threshold:
                logger.warning(f"Brute force detected from {ip} with {len(attempts)} failed attempts.")
                alerts.append({
                    "id": str(uuid.uuid4()),
                    "title": "Brute Force Attack Detected",
                    "description": f"Multiple failed login attempts ({len(attempts)}) from source IP {ip}.",
                    "severity": "High" if len(attempts) > 10 else "Medium",
                    "source": "BruteForceDetector",
                    "source_ip": ip,
                    "affected_user": attempts[0].get("user"),
                    "mitre_attack_mapping": ["T1110 - Brute Force"],
                    "raw_event": attempts[-1]
                })

        return alerts
