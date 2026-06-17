import pytest
from src.detections.brute_force_detection import BruteForceDetector
from src.detections.powershell_abuse import PowerShellAbuseDetector

@pytest.fixture
def config():
    return {
        'detection_rules': {
            'brute_force': {'threshold': 3}
        }
    }

def test_brute_force_detection(config):
    detector = BruteForceDetector(config)
    events = [
        {"status": "Failure", "src_ip": "1.1.1.1", "user": "admin"},
        {"status": "Failure", "src_ip": "1.1.1.1", "user": "admin"},
        {"status": "Failure", "src_ip": "1.1.1.1", "user": "admin"}
    ]
    alerts = detector.detect(events)
    assert len(alerts) == 1
    assert alerts[0]["title"] == "Brute Force Attack Detected"
    assert alerts[0]["source_ip"] == "1.1.1.1"

def test_powershell_abuse_detection(config):
    detector = PowerShellAbuseDetector(config)
    events = [
        {"raw": {"CommandLine": "powershell.exe -enc SQBFAFM="}, "src_ip": "1.1.1.1"}
    ]
    alerts = detector.detect(events)
    assert len(alerts) == 1
    assert "Encoded PowerShell" in alerts[0]["title"]
