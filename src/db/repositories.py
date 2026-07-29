from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.models import Cluster, OLT, Package


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

    def get_by_id(self, olt_id: int):

        stmt = (
            select(OLT)
            .options(joinedload(OLT.cluster))
            .where(OLT.id == olt_id)
        )

        return self.session.scalar(stmt)

    def add(self, olt):

        self.session.add(olt)
        self.session.commit()

class PackageRepository:

    def __init__(self, session):
        self.session = session

    def get_all(self):

        stmt = (
            select(Package)
            .order_by(Package.speed)
        )

        return self.session.scalars(stmt).all()

    def get_by_id(self, package_id):

        stmt = (
            select(Package)
            .where(Package.id == package_id)
        )

        return self.session.scalar(stmt)

    def get_by_profile(self, profile_name):

        stmt = (
            select(Package)
            .where(Package.profile_name == profile_name)
        )

        return self.session.scalar(stmt)

    def add(self, package):

        self.session.add(package)
        self.session.commit()
