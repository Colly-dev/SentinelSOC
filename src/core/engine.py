import yaml
from loguru import logger
from typing import Optional, List, Dict, Any
from pathlib import Path

from src.core.workflow import SOCWorkflow
from src.core.alert_manager import AlertManager
from src.core.correlation_engine import CorrelationEngine
from src.core.report_engine import ReportEngine

class SOCCoreEngine:
    """
    Main orchestration engine for SentinelSOC.
    Coordinates the workflow between collectors, detections, correlation, and reporting.
    """
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.workflow = SOCWorkflow(self.config)
        self.alert_manager = AlertManager(self.config)
        self.correlation_engine = CorrelationEngine(self.config)
        self.report_engine = ReportEngine(self.config)
        logger.info("SentinelSOC Core Engine initialized successfully.")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the YAML configuration file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_path}: {e}")
            raise

    def collect_logs(self, source: Optional[str] = None):
        """Orchestrates log collection from various sources."""
        logger.info(f"Starting log collection process for {source if source else 'all sources'}...")
        
        from src.collectors.windows_logs import WindowsLogCollector
        from src.collectors.auth_logs import AuthLogCollector
        from src.collectors.powershell_logs import PowerShellLogCollector
        from src.collectors.sysmon_collector import SysmonCollector
        
        all_events = []
        if not source or source == 'windows_events':
            all_events.extend(WindowsLogCollector(self.config).collect())
        if not source or source == 'auth_logs':
            all_events.extend(AuthLogCollector(self.config).collect())
        if not source or source == 'powershell_logs':
            all_events.extend(PowerShellLogCollector(self.config).collect())
        if not source or source == 'sysmon_logs':
            all_events.extend(SysmonCollector(self.config).collect())
            
        self.workflow.execute_step("Collect logs", source=source)
        return all_events

    def run_detections(self, rule: Optional[str] = None):
        """Applies detection rules to collected logs."""
        logger.info(f"Running detection rules for {rule if rule else 'all rules'}...")
        
        events = self.collect_logs()
        self.workflow.execute_step("Normalize events", events=events)
        
        from src.detections.brute_force_detection import BruteForceDetector
        from src.detections.powershell_abuse import PowerShellAbuseDetector
        from src.detections.malware_behavior import MalwareBehaviorDetector
        from src.detections.suspicious_logins import SuspiciousLoginDetector
        from src.detections.persistence_detection import PersistenceDetector
        from src.detections.lateral_movement import LateralMovementDetector
        
        detectors = [
            BruteForceDetector(self.config),
            PowerShellAbuseDetector(self.config),
            MalwareBehaviorDetector(self.config),
            SuspiciousLoginDetector(self.config),
            PersistenceDetector(self.config),
            LateralMovementDetector(self.config)
        ]
        
        all_alerts = []
        for detector in detectors:
            alerts = detector.detect(events)
            all_alerts.extend(alerts)
            
        self.workflow.execute_step("Apply detection rules", events=events, rule=rule)
        
        for alert in all_alerts:
            self.alert_manager.add_alert(alert)
        
        logger.info(f"Detections completed. Generated {len(all_alerts)} alerts.")

    def run_simulation(self, attack: Optional[str] = None):
        """Executes attack simulations to generate sample data."""
        logger.info(f"Executing attack simulations for {attack if attack else 'all attacks'}...")
        
        from src.attack_simulations.brute_force import simulate as brute_force_sim
        from src.attack_simulations.malware_execution import simulate as malware_sim
        from src.attack_simulations.powershell_attacks import simulate as powershell_sim
        from src.attack_simulations.credential_access import simulate as cred_sim
        from src.attack_simulations.suspicious_activity import simulate as suspicious_sim
        
        if not attack or attack == 'brute_force':
            brute_force_sim.simulate()
        if not attack or attack == 'malware_execution':
            malware_sim.simulate()
        if not attack or attack == 'powershell_attacks':
            powershell_sim.simulate()
        if not attack or attack == 'credential_access':
            cred_sim.simulate()
        if not attack or attack == 'suspicious_activity':
            suspicious_sim.simulate()
            
        self.workflow.execute_step("Simulate attacks", attack=attack)

    def generate_reports(self, report_type: str = 'html'):
        """Generates incident and detection reports."""
        logger.info(f"Generating {report_type} reports...")
        alerts = self.alert_manager.get_all_alerts()
        incidents = self.correlation_engine.correlate(alerts)
        self.report_engine.generate(alerts, incidents, report_type)

    def run_full_workflow(self):
        """Runs the complete SOC pipeline: collect -> detect -> correlate -> report."""
        logger.info("Starting full SOC workflow...")
        
        # 1. Collect
        self.collect_logs()
        
        # 2. Detect
        self.run_detections()
        
        # 3. Correlate and Report
        self.generate_reports()
        
        logger.info("Full SOC workflow completed successfully.")
