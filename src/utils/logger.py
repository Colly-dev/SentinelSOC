import sys
from loguru import logger
from pathlib import Path

def setup_logging(log_dir: str = "./logs", level: str = "INFO"):
    """Configures loguru for console and file output."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True
    )

    # Add file handler
    logger.add(
        log_path / "sentinelsoc.log",
        rotation="10 MB",
        retention="1 week",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

    # Add specialized alert log
    logger.add(
        log_path / "alerts.log",
        filter=lambda record: "New Alert:" in record["message"],
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {message}"
    )

    logger.info("Logging system initialized.")
