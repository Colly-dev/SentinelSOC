import json
import csv
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pathlib import Path
from src.core.alert_manager import Alert
from src.core.correlation_engine import Incident

class ReportEngine:
    """
    Generates JSON, CSV, and HTML reports for security incidents and detections.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get('report_settings', {}).get('output_dir', './docs/reports'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, alerts: List[Alert], incidents: List[Incident], report_type: str = 'html'):
        """Generates the requested report types."""
        if report_type == 'json' or self.config.get('report_settings', {}).get('json_report_enabled'):
            self._generate_json(alerts, incidents)
        
        if report_type == 'csv' or self.config.get('report_settings', {}).get('csv_report_enabled'):
            self._generate_csv(alerts)
            
        if report_type == 'html' or self.config.get('report_settings', {}).get('html_report_enabled'):
            self._generate_html(alerts, incidents)

    def _generate_json(self, alerts: List[Alert], incidents: List[Incident]):
        report_data = {
            "summary": {
                "total_alerts": len(alerts),
                "total_incidents": len(incidents)
            },
            "alerts": [a.model_dump() for a in alerts],
            "incidents": [
                {
                    "id": i.id,
                    "severity": i.severity,
                    "summary": i.summary,
                    "alert_ids": [a.id for a in i.alerts]
                } for i in incidents
            ]
        }
        with open(self.output_dir / "report.json", 'w') as f:
            json.dump(report_data, f, indent=4, default=str)
        logger.info(f"JSON report generated at {self.output_dir / 'report.json'}")

    def _generate_csv(self, alerts: List[Alert]):
        if not alerts: return
        keys = alerts[0].model_dump().keys()
        with open(self.output_dir / "alerts.csv", 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            for alert in alerts:
                dict_writer.writerow(alert.model_dump())
        logger.info(f"CSV report generated at {self.output_dir / 'alerts.csv'}")

    def _generate_html(self, alerts: List[Alert], incidents: List[Incident]):
        # Simple HTML generation without a full template file for now
        # In a real project, we'd use Jinja2 with a separate .html template
        html_content = f"""
        <html>
        <head>
            <title>SentinelSOC Incident Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }}
                h1, h2 {{ color: #333; }}
                .summary {{ background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #007bff; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .severity-High {{ color: orange; font-weight: bold; }}
                .severity-Critical {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>SentinelSOC Incident Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Alerts: {len(alerts)}</p>
                <p>Total Correlated Incidents: {len(incidents)}</p>
            </div>
            
            <h2>Active Incidents</h2>
            <table>
                <tr><th>ID</th><th>Severity</th><th>Summary</th><th>Alert Count</th></tr>
                {"".join([f"<tr><td>{i.id}</td><td class='severity-{i.severity}'>{i.severity}</td><td>{i.summary}</td><td>{len(i.alerts)}</td></tr>" for i in incidents])}
            </table>

            <h2>All Alerts</h2>
            <table>
                <tr><th>Timestamp</th><th>Title</th><th>Severity</th><th>Source IP</th></tr>
                {"".join([f"<tr><td>{a.timestamp}</td><td>{a.title}</td><td class='severity-{a.severity}'>{a.severity}</td><td>{a.source_ip}</td></tr>" for a in alerts])}
            </table>
        </body>
        </html>
        """
        with open(self.output_dir / "report.html", 'w') as f:
            f.write(html_content)
        logger.info(f"HTML report generated at {self.output_dir / 'report.html'}")
