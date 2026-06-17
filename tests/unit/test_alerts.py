import pytest
from src.core.alert_manager import AlertManager

@pytest.fixture
def alert_manager():
    return AlertManager({})

def test_add_alert(alert_manager):
    alert_data = {
        "id": "test-1",
        "title": "Test Alert",
        "description": "Test Description",
        "severity": "High",
        "source": "TestDetector",
        "raw_event": {}
    }
    alert_manager.add_alert(alert_data)
    assert len(alert_manager.get_all_alerts()) == 1
    assert alert_manager.get_all_alerts()[0].title == "Test Alert"

def test_filter_by_severity(alert_manager):
    alert_manager.add_alert({"id": "1", "title": "A", "description": "D", "severity": "High", "source": "S", "raw_event": {}})
    alert_manager.add_alert({"id": "2", "title": "B", "description": "D", "severity": "Low", "source": "S", "raw_event": {}})
    
    high_alerts = alert_manager.get_alerts_by_severity("High")
    assert len(high_alerts) == 1
    assert high_alerts[0].id == "1"
