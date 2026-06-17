import pandas as pd
from typing import List, Dict, Any
from loguru import logger
from pathlib import Path

class DataExporter:
    """
    Exports data to various formats using Pandas.
    """
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], output_path: str):
        try:
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
            logger.info(f"Data exported to CSV: {output_path}")
        except Exception as e:
            logger.error(f"CSV export failed: {e}")

    @staticmethod
    def to_excel(data: List[Dict[str, Any]], output_path: str):
        try:
            df = pd.DataFrame(data)
            df.to_excel(output_path, index=False)
            logger.info(f"Data exported to Excel: {output_path}")
        except Exception as e:
            logger.error(f"Excel export failed: {e}")
