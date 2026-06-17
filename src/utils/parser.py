import json
import yaml
from typing import List, Dict, Any
from loguru import logger

class LogParser:
    """
    Parses different log formats (JSON, YAML, CSV, Syslog).
    """
    @staticmethod
    def parse_json(file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to parse JSON from {file_path}: {e}")
            return []

    @staticmethod
    def parse_yaml(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to parse YAML from {file_path}: {e}")
            return {}

    @staticmethod
    def parse_syslog_line(line: str) -> Dict[str, Any]:
        # Very basic syslog parser
        parts = line.split()
        if len(parts) < 5:
            return {"raw": line}
        return {
            "timestamp": f"{parts[0]} {parts[1]} {parts[2]}",
            "hostname": parts[3],
            "process": parts[4].strip(':'),
            "message": " ".join(parts[5:])
        }
