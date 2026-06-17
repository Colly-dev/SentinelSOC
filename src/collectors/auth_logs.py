from typing import List, Dict, Any
from loguru import logger
from pathlib import Path
from src.utils.parser import LogParser
from src.utils.event_normalizer import EventNormalizer

class AuthLogCollector:
    """
    Simulates collection of Authentication logs (e.g., /var/log/auth.log).
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.log_path = Path(config.get('log_sources', {}).get('auth_logs', {}).get('path', './logs/collected/auth_logs.log'))

    def collect(self) -> List[Dict[str, Any]]:
        logger.info(f"Collecting Auth logs from {self.log_path}")
        if not self.log_path.exists():
            return []

        try:
            normalized_logs = []
            with open(self.log_path, 'r') as f:
                for line in f:
                    # Basic extraction for auth logs
                    raw_event = {"message": line.strip(), "timestamp": line[:15]}
                    if "user" in line:
                        parts = line.split("user")
                        raw_event["user"] = parts[1].split()[0]
                    if "from" in line:
                        parts = line.split("from")
                        raw_event["rhost"] = parts[1].split()[0]
                        
                    normalized_logs.append(EventNormalizer.normalize(raw_event, "auth_logs"))
            
            return normalized_logs
        except Exception as e:
            logger.error(f"Error collecting Auth logs: {e}")
            return []
