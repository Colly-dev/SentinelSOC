from typing import List, Dict, Any
from datetime import timedelta
from loguru import logger
from src.core.alert_manager import Alert

class Incident:
    """Represents a correlated group of related alerts."""
    def __init__(self, incident_id: str, alerts: List[Alert]):
        self.id = incident_id
        self.alerts = alerts
        self.start_time = min(a.timestamp for a in alerts)
        self.end_time = max(a.timestamp for a in alerts)
        self.severity = self._calculate_severity()
        self.summary = self._generate_summary()

    def _calculate_severity(self) -> str:
        severities = [a.severity for a in self.alerts]
        if "Critical" in severities: return "Critical"
        if "High" in severities: return "High"
        if "Medium" in severities: return "Medium"
        return "Low"

    def _generate_summary(self) -> str:
        titles = set(a.title for a in self.alerts)
        return f"Incident involving: {', '.join(titles)}"

class CorrelationEngine:
    """
    Correlates related alerts based on time, IP, and user.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.time_window = timedelta(minutes=30)

    def correlate(self, alerts: List[Alert]) -> List[Incident]:
        """Performs correlation on a list of alerts to group them into incidents."""
        if not alerts:
            return []

        logger.info(f"Starting correlation for {len(alerts)} alerts...")
        incidents: List[Incident] = []
        
        # Simple IP-based correlation
        ip_groups: Dict[str, List[Alert]] = {}
        for alert in alerts:
            if alert.source_ip:
                if alert.source_ip not in ip_groups:
                    ip_groups[alert.source_ip] = []
                ip_groups[alert.source_ip].append(alert)

        for ip, group in ip_groups.items():
            if len(group) > 1:
                incident_id = f"INC-IP-{ip.replace('.', '-')}"
                incidents.append(Incident(incident_id, group))
                logger.info(f"Correlated {len(group)} alerts into incident {incident_id}")

        # Simple User-based correlation
        user_groups: Dict[str, List[Alert]] = {}
        for alert in alerts:
            if alert.affected_user:
                if alert.affected_user not in user_groups:
                    user_groups[alert.affected_user] = []
                user_groups[alert.affected_user].append(alert)

        for user, group in user_groups.items():
            if len(group) > 1:
                incident_id = f"INC-USER-{user}"
                incidents.append(Incident(incident_id, group))
                logger.info(f"Correlated {len(group)} alerts into incident {incident_id}")

        return incidents
