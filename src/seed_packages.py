from db.database import DatabaseManager
from services.package_service import PackageService


db = DatabaseManager()
session = db.get_session()

service = PackageService(session)

packages = [
    ("20 Mbps", 20, "PRIVATE_FTTH-20Mb", 505),
    ("50 Mbps", 50, "PRIVATE_FTTH-50Mb", 506),
    ("100 Mbps", 100, "PRIVATE_FTTH-100Mb", 508),
    ("200 Mbps", 200, "PRIVATE_FTTH-200Mb", 509),
    ("500 Mbps", 500, "PRIVATE_FTTH-500Mb", 510),
    ("1 Gbps", 1000, "PRIVATE_FTTH-1Gb", 511),
]

for pkg in packages:

    if service.get_by_profile(pkg[2]):
        continue

    service.add(
        name=pkg[0],
        speed=pkg[1],
        profile_name=pkg[2],
        traffic_table=pkg[3],
    )

print("Packages seeded successfully.")
