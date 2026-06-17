import pytest
from src.core.report_engine import ReportEngine
from src.core.alert_manager import Alert
from pathlib import Path

def test_report_generation(tmp_path):
    config = {
        'report_settings': {
            'output_dir': str(tmp_path),
            'json_report_enabled': True,
            'html_report_enabled': True
        }
    }
    engine = ReportEngine(config)
    alerts = [
        Alert(id="1", title="T", description="D", severity="High", source="S", raw_event={})
    ]
    engine.generate(alerts, [], 'json')
    
    assert (tmp_path / "report.json").exists()
    assert (tmp_path / "report.html").exists()
