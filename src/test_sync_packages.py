from db.database import DatabaseManager
from services.olt_service import OLTService
from services.traffic_sync_service import TrafficSyncService
from drivers.huawei_driver import HuaweiDriver


def main():

    db = DatabaseManager()
    session = db.get_session()

    olt_service = OLTService(session)

    # Master OLT (currently ID 1)
    olt = olt_service.get_by_id(1)

    if olt is None:
        print("No master OLT found.")
        return

    driver = HuaweiDriver(
        host=olt.ip_address,
        username=olt.username,
        password=olt.password,
    )

    print(f"Connecting to {olt.hostname} ({olt.ip_address})...")

    driver.connect()

    try:

        sync = TrafficSyncService(
            driver=driver,
            session=session,
        )

        result = sync.synchronize(500)

        print()
        print("========== SUMMARY ==========")
        print(f"Added      : {result['added']}")
        print(f"Updated    : {result['updated']}")
        print(f"Unchanged  : {result['unchanged']}")

    finally:

        driver.disconnect()
        session.close()


if __name__ == "__main__":
    main()
