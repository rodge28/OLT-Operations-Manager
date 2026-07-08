from __future__ import annotations

from core.config_manager import ConfigManager
from core.logger import setup_logger


def main():

    logger = setup_logger()

    config = ConfigManager()

    logger.info("=" * 50)
    logger.info(config.get("application", "name"))
    logger.info(
        "Version: %s",
        config.get("application", "version"),
    )
    logger.info("=" * 50)

    print()
    print("Application initialized successfully.")
    print()


if __name__ == "__main__":
    main()
