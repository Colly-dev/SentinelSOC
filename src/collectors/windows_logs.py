import json
from typing import List, Dict, Any
from loguru import logger
from pathlib import Path
from src.utils.event_normalizer import EventNormalizer

class WindowsLogCollector:
    """
    Simulates collection of Windows Event Logs.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.log_path = Path(config.get('log_sources', {}).get('windows_events', {}).get('path', './data/sample_targets/sample_windows_events.json'))

    def collect(self) -> List[Dict[str, Any]]:
        logger.info(f"Collecting Windows logs from {self.log_path}")
        if not self.log_path.exists():
            logger.warning(f"Windows log file not found: {self.log_path}. Returning empty list.")
            return []

        try:
            with open(self.log_path, 'r') as f:
                raw_logs = json.load(f)
            
            normalized_logs = [EventNormalizer.normalize(log, "windows_events") for log in raw_logs]
            logger.info(f"Successfully collected and normalized {len(normalized_logs)} Windows events.")
            return normalized_logs
        except Exception as e:
            logger.error(f"Error collecting Windows logs: {e}")
            return []
