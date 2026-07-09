"""
Database Manager
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DatabaseManager:

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        db_file = project_root / "database" / "olt_manager.db"

        db_file.parent.mkdir(exist_ok=True)

        self.engine = create_engine(
            f"sqlite:///{db_file}",
            echo=False,
            future=True
        )

        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )

    def create_database(self):

        Base.metadata.create_all(self.engine)
