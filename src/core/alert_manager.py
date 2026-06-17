from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from loguru import logger

class Alert(BaseModel):
    """Model representing a security alert."""
    id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    title: str
    description: str
    severity: str  # Low, Medium, High, Critical
    source: str
    mitre_attack_mapping: Optional[List[str]] = None
    affected_user: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    raw_event: Dict[str, Any]

class AlertManager:
    """
    Manages the creation, storage, and retrieval of security alerts.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alerts: List[Alert] = []

    def add_alert(self, alert_data: Dict[str, Any]):
        """Creates and stores a new alert."""
        try:
            alert = Alert(**alert_data)
            self.alerts.append(alert)
            logger.info(f"New Alert: [{alert.severity}] {alert.title} - Source: {alert.source}")
            self._log_to_file(alert)
        except Exception as e:
            logger.error(f"Failed to add alert: {e}")

    def get_all_alerts(self) -> List[Alert]:
        """Returns all generated alerts."""
        return self.alerts

    def get_alerts_by_severity(self, severity: str) -> List[Alert]:
        """Filters alerts by severity level."""
        return [a for a in self.alerts if a.severity.lower() == severity.lower()]

    def _log_to_file(self, alert: Alert):
        """Persists the alert to a log file for later analysis."""
        log_path = self.config.get('logging', {}).get('log_dir', './logs') + "/alerts.log"
        try:
            with open(log_path, 'a') as f:
                f.write(f"{alert.model_dump_json()}\n")
        except Exception as e:
            logger.error(f"Failed to log alert to file: {e}")
