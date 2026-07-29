from sqlalchemy import Column, Integer, String
from db.database import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)          # 50 Mbps
    speed = Column(Integer, nullable=False)            # 50
    profile_name = Column(String(100), nullable=False) # PRIVATE_FTTH-50Mb
    traffic_table = Column(Integer, nullable=False)    # 506

    def __repr__(self):
        return f"<Package {self.name}>"
