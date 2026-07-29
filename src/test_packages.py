from db.database import DatabaseManager
from services.package_service import PackageService

db = DatabaseManager()
session = db.get_session()

service = PackageService(session)

for pkg in service.get_all():
    print(pkg)
