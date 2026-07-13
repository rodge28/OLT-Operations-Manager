from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.models import Cluster, OLT


class ClusterRepository:

    def __init__(self, session):
        self.session = session

    def get_all(self):

        stmt = (
            select(Cluster)
            .order_by(Cluster.name)
        )

        return self.session.scalars(stmt).all()


class OLTRepository:

    def __init__(self, session):
        self.session = session

    def get_all(self):

        stmt = (
            select(OLT)
            .options(joinedload(OLT.cluster))
            .order_by(OLT.hostname)
        )

        return self.session.scalars(stmt).all()

    def add(self, olt):

        self.session.add(olt)
        self.session.commit()
