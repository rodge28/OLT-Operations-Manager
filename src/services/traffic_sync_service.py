from services.package_service import PackageService
from utils.traffic_table_parser import TrafficTableParser


class TrafficSyncService:
    """
    Synchronizes Huawei Traffic Tables with the local Package database.
    """

    def __init__(
        self,
        driver,
        session,
    ):

        self.driver = driver
        self.package_service = PackageService(session)

    # ---------------------------------------------------------
    # Synchronize
    # ---------------------------------------------------------

    def synchronize(self, from_index=500):

        print("Downloading traffic table summary...")

        summary = self.driver.get_traffic_table_summary(
            from_index
        )

        tables = TrafficTableParser.parse_summary(summary)

        added = 0
        updated = 0
        unchanged = 0

        for table in tables:

            detail_output = self.driver.get_traffic_table_detail(
                table["index"]
            )

            detail = TrafficTableParser.parse_detail(
                detail_output
            )

            if not detail:
                continue

            package = self.package_service.get_by_table(
                detail["index"]
            )

            if package is None:

                self.package_service.create(
                    name=detail["name"],
                    speed=0,
                    profile_name=detail["name"],
                    traffic_table=detail["index"],
                )

                print(f"[ADD] {detail['index']}  {detail['name']}")

                added += 1

                continue

            changed = False

            if package.profile_name != detail["name"]:

                package.profile_name = detail["name"]
                package.name = detail["name"]

                changed = True

            if changed:

                self.package_service.update(package)

                print(f"[UPDATE] {detail['index']}  {detail['name']}")

                updated += 1

            else:

                unchanged += 1

        print()
        print("Synchronization Complete")
        print(f"Added      : {added}")
        print(f"Updated    : {updated}")
        print(f"Unchanged  : {unchanged}")

        return {
            "added": added,
            "updated": updated,
            "unchanged": unchanged,
        }
