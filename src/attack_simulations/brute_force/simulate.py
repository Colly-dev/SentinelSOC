import json
import random
from datetime import datetime, timedelta
from loguru import logger
from pathlib import Path

def simulate(output_path: str = "./data/sample_targets/sample_windows_events.json"):
    """
    Simulates a brute force attack by generating failed login events.
    """
    logger.info("Simulating Brute Force Attack...")
    target_user = "admin"
    attacker_ip = "192.168.1.50"
    
    events = []
    base_time = datetime.now() - timedelta(minutes=10)
    
    # Generate 10 failed login attempts
    for i in range(10):
        event_time = base_time + timedelta(seconds=i * 2)
        events.append({
            "EventID": 4625,
            "timestamp": event_time.isoformat(),
            "TargetUserName": target_user,
            "IpAddress": attacker_ip,
            "Status": "0xC000006D",
            "SubStatus": "0xC000006A",
            "LogonType": 3,
            "Keywords": "0x8010000000000000"
        })
    
    # One successful login (optional)
    events.append({
        "EventID": 4624,
        "timestamp": (base_time + timedelta(seconds=25)).isoformat(),
        "TargetUserName": target_user,
        "IpAddress": attacker_ip,
        "LogonType": 3,
        "Keywords": "0x8020000000000000"
    })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(events, f, indent=4)
    
    logger.info(f"Brute force simulation complete. Logs written to {output_path}")
