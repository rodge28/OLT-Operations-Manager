from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from db.database import Base

from sqlalchemy.orm import relationship
class Cluster(Base):

    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True)

    description = Column(String(200))

    olts = relationship(
        "OLT",
        back_populates="cluster",
        cascade="all, delete-orphan"
    )

class OLT(Base):

    __tablename__ = "olts"

    id = Column(Integer, primary_key=True)

    cluster_id = Column(
        Integer,
        ForeignKey("clusters.id"),
        nullable=False
    )
    cluster = relationship(
        "Cluster",
        back_populates="olts"
    )
    hostname = Column(String(100), unique=True)

    ip_address = Column(String(50))

    ssh_port = Column(Integer, default=22)

    username = Column(String(100))

    password = Column(String(500))

    vendor = Column(String(50), default="Huawei")

    model = Column(String(100))

    software_version = Column(String(100))

    description = Column(String(200))

    enabled = Column(Boolean, default=True)

    last_ssh_test = Column(DateTime)

    last_login = Column(DateTime)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
