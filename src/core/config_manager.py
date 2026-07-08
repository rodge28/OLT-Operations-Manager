"""
Configuration Manager

Loads application settings from config/config.json
"""

from __future__ import annotations

import json
from pathlib import Path


class ConfigManager:
    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.config_file = project_root / "config" / "config.json"

        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found:\n{self.config_file}"
            )

        with self.config_file.open("r", encoding="utf-8") as file:
            self.config = json.load(file)

    def get(self, *keys, default=None):
        value = self.config

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default

        return value if value is not None else default
