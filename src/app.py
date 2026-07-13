from __future__ import annotations

from core.config_manager import ConfigManager
from core.logger import setup_logger
from gui.main_window import MainWindow
from db.database import DatabaseManager
import db.models

def main():

    logger = setup_logger()

    config = ConfigManager()
    database = DatabaseManager()
    database.create_database()
    session = database.get_session()

    from db.seed import seed_clusters

    seed_clusters(session)

    logger.info("=" * 50)
    logger.info(config.get("application", "name"))
    logger.info("Version: %s", config.get("application", "version"))
    logger.info("=" * 50)

    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
