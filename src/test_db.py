from db.database import DatabaseManager
from db.repositories import ClusterRepository

db = DatabaseManager()
session = db.get_session()

repo = ClusterRepository(session)

clusters = repo.get_all()

print(f"Total Clusters: {len(clusters)}")

for cluster in clusters:
    print(cluster.id, cluster.name)
