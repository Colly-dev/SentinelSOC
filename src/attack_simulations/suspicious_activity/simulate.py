from datetime import datetime
from loguru import logger
from pathlib import Path

def simulate(output_path: str = "./logs/collected/auth_logs.log"):
    """
    Simulates suspicious activity in auth logs.
    """
    logger.info("Simulating Suspicious User Activity...")
    
    timestamp = datetime.now().strftime("%b %d %H:%M:%S")
    logs = [
        f"{timestamp} sentinel sshd[1234]: Failed password for invalid user root from 192.168.1.100 port 54321 ssh2\n",
        f"{timestamp} sentinel sshd[1234]: Failed password for invalid user root from 192.168.1.100 port 54322 ssh2\n",
        f"{timestamp} sentinel sshd[1234]: Accepted password for admin from 192.168.1.100 port 54323 ssh2\n"
    ]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'a') as f:
        f.writelines(logs)
    
    logger.info(f"Suspicious activity simulation complete. Logs written to {output_path}")
