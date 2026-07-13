from sqlalchemy import select
from db.models import Cluster

DEFAULT_CLUSTERS = [
    "Lucena",
    "Pagbilao",
    "Tayabas",
    "Mauban",
    "Sariaya",
]

def seed_clusters(session):

    print("Running seed_clusters()")

    existing = session.scalars(select(Cluster)).all()

    print(f"Existing clusters: {len(existing)}")

    if existing:
        print("Clusters already exist.")
        return

    for name in DEFAULT_CLUSTERS:
        print(f"Adding {name}")
        session.add(
            Cluster(
                name=name,
                description=f"{name} Cluster"
            )
        )

    session.commit()

    print("Seed completed.")
