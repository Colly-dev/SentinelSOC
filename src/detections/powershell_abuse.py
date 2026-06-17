from typing import List, Dict, Any
from loguru import logger
import uuid
import base64

class PowerShellAbuseDetector:
    """
    Detects suspicious PowerShell activity, including encoded commands.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def detect(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info("Running PowerShell Abuse Detection...")
        alerts = []

        for event in events:
            raw = event.get("raw", {})
            command_line = raw.get("CommandLine", "") or raw.get("message", "")
            
            # Check for encoded commands
            if "-EncodedCommand" in command_line or "-enc" in command_line.lower():
                logger.warning(f"Encoded PowerShell command detected: {command_line}")
                alerts.append({
                    "id": str(uuid.uuid4()),
                    "title": "Encoded PowerShell Command",
                    "description": "A PowerShell process was started with an encoded command, a common obfuscation technique.",
                    "severity": "High",
                    "source": "PowerShellAbuseDetector",
                    "source_ip": event.get("src_ip"),
                    "affected_user": event.get("user"),
                    "mitre_attack_mapping": ["T1059.001 - PowerShell", "T1027 - Obfuscated Files or Information"],
                    "raw_event": event
                })

            # Check for download strings
            if "Net.WebClient" in command_line or "Invoke-WebRequest" in command_line or "iwr" in command_line:
                logger.warning(f"PowerShell download cradle detected: {command_line}")
                alerts.append({
                    "id": str(uuid.uuid4()),
                    "title": "PowerShell Download Cradle",
                    "description": "PowerShell was used to download content from the internet, often used in malware delivery.",
                    "severity": "High",
                    "source": "PowerShellAbuseDetector",
                    "source_ip": event.get("src_ip"),
                    "affected_user": event.get("user"),
                    "mitre_attack_mapping": ["T1105 - Ingress Tool Transfer"],
                    "raw_event": event
                })

        return alerts
