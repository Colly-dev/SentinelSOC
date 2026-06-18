
import argparse
import sys
from loguru import logger
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

from src.core.engine import SOCCoreEngine
from src.utils.logger import setup_logging

console = Console()

def display_banner():
    """Displays the SentinelSOC ASCII art banner."""
    banner = Text()
    banner.append("\n  ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗      \n", style="bold deep_sky_blue1")
    banner.append("  ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║      \n", style="bold deep_sky_blue1")
    banner.append("  ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║      \n", style="bold deep_sky_blue1")
    banner.append("  ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║      \n", style="bold deep_sky_blue1")
    banner.append("  ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗  \n", style="bold deep_sky_blue1")
    banner.append("  ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝  \n", style="bold deep_sky_blue1")
    banner.append("                      SOC Platform v1.0.0 | by Colly-dev\n", style="dim")
    console.print(Panel(banner, border_style="deep_sky_blue1", padding=(0, 2)))

def main():
    """Main entry point for SentinelSOC CLI."""
    display_banner()
    setup_logging()

    parser = argparse.ArgumentParser(description="SentinelSOC - Open-Source Security Operations Center Simulation")
    parser.add_argument('--config', type=str, default='config/config.yaml', help='Path to the configuration file')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Collect command
    collect_parser = subparsers.add_parser('collect', help='Collect security logs')
    collect_parser.add_argument('--source', type=str, help='Specific log source to collect (e.g., windows_events)')

    # Detect command
    detect_parser = subparsers.add_parser('detect', help='Apply detection rules and generate alerts')
    detect_parser.add_argument('--rule', type=str, help='Specific detection rule to apply (e.g., brute_force)')

    # Simulate command
    simulate_parser = subparsers.add_parser('simulate', help='Simulate attack scenarios')
    simulate_parser.add_argument('--attack', type=str, help='Specific attack to simulate (e.g., brute_force)')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate incident and detection reports')
    report_parser.add_argument('--type', type=str, default='html', help='Report type (json, csv, html)')

    # Full command
    full_parser = subparsers.add_parser('full', help='Run full SOC workflow (collect -> detect -> report)')

    args = parser.parse_args()

    engine = SOCCoreEngine(args.config)

    try:
        if args.command == 'collect':
            logger.info(f"Starting log collection for source: {args.source if args.source else 'all'}")
            engine.collect_logs(args.source)
        elif args.command == 'detect':
            logger.info(f"Starting detection for rule: {args.rule if args.rule else 'all'}")
            engine.run_detections(args.rule)
        elif args.command == 'simulate':
            logger.info(f"Starting attack simulation for: {args.attack if args.attack else 'all'}")
            engine.run_simulation(args.attack)
        elif args.command == 'report':
            logger.info(f"Generating {args.type} reports...")
            engine.generate_reports(args.type)
        elif args.command == 'full':
            logger.info("Running full SentinelSOC workflow...")
            engine.run_full_workflow()
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"An error occurred during command execution: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
