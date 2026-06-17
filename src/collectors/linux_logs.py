from typing import List, Dict, Any
from loguru import logger
from pathlib import Path
from src.utils.parser import LogParser
from src.utils.event_normalizer import EventNormalizer

class LinuxLogCollector:
    """
    Simulates collection of Linux Syslog data.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.log_path = Path(config.get('log_sources', {}).get('linux_syslog', {}).get('path', './logs/collected/linux_syslog.log'))

    def collect(self) -> List[Dict[str, Any]]:
        logger.info(f"Collecting Linux syslog from {self.log_path}")
        if not self.log_path.exists():
            logger.warning(f"Linux syslog file not found: {self.log_path}")
            return []

        try:
            normalized_logs = []
            with open(self.log_path, 'r') as f:
                for line in f:
                    raw_event = LogParser.parse_syslog_line(line)
                    normalized_logs.append(EventNormalizer.normalize(raw_event, "linux_syslog"))
            
            logger.info(f"Successfully collected and normalized {len(normalized_logs)} Linux syslog events.")
            return normalized_logs
        except Exception as e:
            logger.error(f"Error collecting Linux logs: {e}")
            return []
