from db.models import Package
from db.repositories import PackageRepository


class PackageService:

    def __init__(self, session):

        self.session = session
        self.repository = PackageRepository(session)

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, package_id):
        return self.repository.get_by_id(package_id)

    def get_by_profile(self, profile_name):
        return self.repository.get_by_profile(profile_name)

    def get_by_table(self, traffic_table):

        return (
            self.session.query(Package)
            .filter(Package.traffic_table == traffic_table)
            .first()
        )

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    def add(
        self,
        name,
        speed,
        profile_name,
        traffic_table,
    ):

        package = Package(
            name=name,
            speed=speed,
            profile_name=profile_name,
            traffic_table=traffic_table,
        )

        self.repository.add(package)

        return package

    def create(
        self,
        name,
        speed,
        profile_name,
        traffic_table,
    ):

        package = Package(
            name=name,
            speed=speed,
            profile_name=profile_name,
            traffic_table=traffic_table,
        )

        self.session.add(package)
        self.session.commit()

        return package

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update(self, package):

        self.session.add(package)
        self.session.commit()

        return package
