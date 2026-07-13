from db.database import DatabaseManager
from db.models import OLT
from db.repositories import OLTRepository


class OLTService:

    def __init__(self, session):

        self.session = session

        self.repository = OLTRepository(session)

    def get_all(self):
        return self.repository.get_all()

    def add(
        self,
        cluster_id,
        hostname,
        ip_address,
        username,
        password,
        ssh_port=22
    ):

        olt = OLT(
            cluster_id=cluster_id,
            hostname=hostname,
            ip_address=ip_address,
            ssh_port=ssh_port,
            username=username,
            password=password,
        )

        self.repository.add(olt)
