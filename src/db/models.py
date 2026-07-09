from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from db.database import Base


class Cluster(Base):

    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True)

    description = Column(String(200))


class OLT(Base):

    __tablename__ = "olts"

    id = Column(Integer, primary_key=True)

    cluster_id = Column(
        Integer,
        ForeignKey("clusters.id")
    )

    name = Column(String(100))

    ip = Column(String(50))

    port = Column(Integer)

    username = Column(String(100))

    password = Column(String(500))

    enabled = Column(Boolean, default=True)
