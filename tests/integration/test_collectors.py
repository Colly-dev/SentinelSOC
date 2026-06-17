import json
from src.collectors.windows_logs import WindowsLogCollector

def test_windows_collector_with_file(tmp_path):
    log_file = tmp_path / "windows.json"
    sample_data = [{"EventID": 4624, "TargetUserName": "system"}]
    with open(log_file, 'w') as f:
        json.dump(sample_data, f)
        
    config = {'log_sources': {'windows_events': {'path': str(log_file)}}}
    collector = WindowsLogCollector(config)
    events = collector.collect()
    
    assert len(events) == 1
    assert events[0]["user"] == "system"
