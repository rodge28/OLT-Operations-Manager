"""
Application Logger
"""

from __future__ import annotations

import logging
from pathlib import Path


def setup_logger() -> logging.Logger:

    project_root = Path(__file__).resolve().parents[2]

    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "application.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger("OLTManager")
