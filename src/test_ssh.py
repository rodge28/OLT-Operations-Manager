from db.database import DatabaseManager
from services.olt_service import OLTService
from services.subscriber_service import SubscriberService

SERIAL = "4857544324F4ACAB"
OLT_ID = 1

db = DatabaseManager()
session = db.get_session()

try:
    olt_service = OLTService(session)
    subscriber_service = SubscriberService(olt_service)

    subscriber = subscriber_service.find_by_serial(
        OLT_ID,
        SERIAL,
    )

    if subscriber:
        print("\nSubscriber Found\n")
        print(subscriber)
    else:
        print("Subscriber not found.")

finally:
    session.close()
