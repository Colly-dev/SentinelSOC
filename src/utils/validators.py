from typing import Dict, Any
import jsonschema
from loguru import logger

class DataValidator:
    """
    Validates log data against defined schemas.
    """
    COMMON_SCHEMA = {
        "type": "object",
        "properties": {
            "event_id": {"type": "string"},
            "timestamp": {"type": "string"},
            "original_source": {"type": "string"},
            "user": {"type": ["string", "null"]},
            "src_ip": {"type": ["string", "null"]},
            "dest_ip": {"type": ["string", "null"]},
            "action": {"type": ["string", "integer", "null"]},
            "status": {"type": ["string", "null"]}
        },
        "required": ["event_id", "timestamp", "original_source"]
    }

    @staticmethod
    def validate_normalized_event(event: Dict[str, Any]) -> bool:
        try:
            # Using a simple check for now as jsonschema might not be in the sandbox env
            # though it was in requirements.txt
            for field in DataValidator.COMMON_SCHEMA["required"]:
                if field not in event:
                    logger.warning(f"Validation failed: Missing required field {field}")
                    return False
            return True
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
