import json
from datetime import datetime
from loguru import logger
from pathlib import Path

def simulate(output_path: str = "./logs/collected/sysmon_events.json"):
    """
    Simulates credential access (e.g., LSASS dumping).
    """
    logger.info("Simulating Credential Access...")
    
    events = [
        {
            "EventID": 10,
            "timestamp": datetime.now().isoformat(),
            "SourceImage": "C:\\Windows\\System32\\procdump.exe",
            "TargetImage": "C:\\Windows\\System32\\lsass.exe",
            "GrantedAccess": "0x1fffff",
            "User": "NT AUTHORITY\\SYSTEM"
        }
    ]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    # Append to existing sysmon logs if they exist
    existing_events = []
    if Path(output_path).exists():
        with open(output_path, 'r') as f:
            existing_events = json.load(f)
    
    existing_events.extend(events)
    with open(output_path, 'w') as f:
        json.dump(existing_events, f, indent=4)
    
    logger.info(f"Credential access simulation complete. Logs written to {output_path}")
