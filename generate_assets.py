import os
import subprocess
import time
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.terminal_theme import MONOKAI

console = Console(record=True, width=100)

def run_command(description, command):
    print(f"\n>>> Generating: {description}")
    print(f"Command: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

def capture_banner():
    banner = Text()
    banner.append("\n  ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      \n", style="bold orange1")
    banner.append("  ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║      \n", style="bold orange1")
    banner.append("  ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║      \n", style="bold orange1")
    banner.append("  ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║      \n", style="bold orange1")
    banner.append("  ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗  \n", style="bold orange1")
    banner.append("  ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝  \n", style="bold orange1")
    banner.append("                      SOC Platform v1.0.0 | by Colly-dev\n", style="dim")
    console.print(Panel(banner, border_style="orange1", padding=(0, 2)))
    console.save_svg("docs/screenshots/banner_terminal.svg", theme=MONOKAI)
    print("Banner SVG generated at docs/screenshots/banner_terminal.svg")

def main():
    # Ensure directories exist
    os.makedirs("docs/screenshots", exist_ok=True)
    os.makedirs("docs/diagrams", exist_ok=True)
    os.makedirs("docs/reports", exist_ok=True)

    print("--- SentinelSOC Asset Generator ---")
    
    # 1. Capture Banner
    capture_banner()

    # 2. Run Full SOC Pipeline for Detection Output
    run_command("Detection Output", "python3 main.py full")
    print("Action: Take a screenshot of the terminal output above and save it as docs/screenshots/detection_output.png")

    # 3. Generate Alert Table
    run_command("Alert Table", "python3 main.py detect")
    print("Action: Take a screenshot of the alert summary table and save it as docs/screenshots/alert_table.png")

    # 4. Generate HTML Report
    run_command("HTML Report", "python3 main.py report --type html")
    print("Action: Open the generated report in docs/reports/ and take a screenshot, save as docs/screenshots/html_report.png")

    print("\n--- Summary of Commands to Run ---")
    print("1. Banner: (Generated automatically as SVG)")
    print("2. Detection Output: python3 main.py full")
    print("3. Alert Table: python3 main.py detect")
    print("4. HTML Report: python3 main.py report --type html")
    print("5. Architecture Diagram: (Manual creation or use Mermaid live editor)")

if __name__ == "__main__":
    main()
