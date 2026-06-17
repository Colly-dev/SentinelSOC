from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class EventNormalizer:
    """
    Normalizes raw log data from various sources into a common schema.
    """
    @staticmethod
    def normalize(raw_data: Dict[str, Any], source_type: str) -> Dict[str, Any]:
        """Maps source-specific fields to the SentinelSOC common schema."""
        normalized = {
            "event_id": str(uuid.uuid4()),
            "original_source": source_type,
            "timestamp": raw_data.get("timestamp", datetime.now().isoformat()),
            "user": None,
            "src_ip": None,
            "dest_ip": None,
            "action": None,
            "status": None,
            "raw": raw_data
        }

        if source_type == "windows_events":
            normalized["user"] = raw_data.get("TargetUserName") or raw_data.get("SubjectUserName")
            normalized["src_ip"] = raw_data.get("IpAddress")
            normalized["action"] = raw_data.get("EventID")
            normalized["status"] = "Success" if raw_data.get("Keywords") == "0x8020000000000000" else "Failure"

        elif source_type == "linux_syslog":
            normalized["user"] = raw_data.get("user")
            normalized["src_ip"] = raw_data.get("src_ip")
            normalized["action"] = raw_data.get("process")

        elif source_type == "auth_logs":
            normalized["user"] = raw_data.get("user")
            normalized["src_ip"] = raw_data.get("rhost")
            normalized["action"] = "login"
            normalized["status"] = "Success" if "Accept" in raw_data.get("message", "") else "Failure"

        return normalized
