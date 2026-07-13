from db.repositories import ClusterRepository


class ClusterService:

    def __init__(self, session):

        self.repository = ClusterRepository(session)

    def get_all(self):
        return self.repository.get_all()
