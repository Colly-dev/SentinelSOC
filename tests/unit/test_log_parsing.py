from src.utils.parser import LogParser
from src.utils.event_normalizer import EventNormalizer

def test_syslog_parsing():
    line = "Jan 01 10:00:00 host sshd: Failed password for root from 1.2.3.4"
    parsed = LogParser.parse_syslog_line(line)
    assert parsed["hostname"] == "host"
    assert parsed["process"] == "sshd"
    assert "Failed password" in parsed["message"]

def test_event_normalization():
    raw = {"TargetUserName": "admin", "IpAddress": "1.2.3.4", "EventID": 4625}
    normalized = EventNormalizer.normalize(raw, "windows_events")
    assert normalized["user"] == "admin"
    assert normalized["src_ip"] == "1.2.3.4"
    assert normalized["status"] == "Failure"
