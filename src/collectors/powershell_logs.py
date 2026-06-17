import json
from typing import List, Dict, Any
from loguru import logger
from pathlib import Path
from src.utils.event_normalizer import EventNormalizer

class PowerShellLogCollector:
    """
    Simulates collection of PowerShell operational logs.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.log_path = Path(config.get('log_sources', {}).get('powershell_logs', {}).get('path', './logs/collected/powershell_logs.json'))

    def collect(self) -> List[Dict[str, Any]]:
        logger.info(f"Collecting PowerShell logs from {self.log_path}")
        if not self.log_path.exists():
            return []

        try:
            with open(self.log_path, 'r') as f:
                raw_logs = json.load(f)
            
            normalized_logs = [EventNormalizer.normalize(log, "powershell_logs") for log in raw_logs]
            return normalized_logs
        except Exception as e:
            logger.error(f"Error collecting PowerShell logs: {e}")
            return []
