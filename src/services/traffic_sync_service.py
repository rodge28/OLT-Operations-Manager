from services.package_service import PackageService
from utils.traffic_table_parser import TrafficTableParser


class TrafficSyncService:
    """
    Synchronizes Huawei MA5800 traffic tables with the
    local Package database.

    Default synchronization range:
        TID 500 through 799
    """

    MIN_INDEX = 500
    MAX_INDEX = 799

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

    def synchronize(
        self,
        from_index=500,
        to_index=799,
    ):
        """
        Synchronize traffic tables from the OLT.

        Only traffic table indexes between from_index and
        to_index are synchronized.

        The OLT may have gaps in the index range. Missing
        indexes are ignored and are NOT created locally.
        """

        # -----------------------------------------------------
        # Validate range
        # -----------------------------------------------------

        from_index = max(
            from_index,
            self.MIN_INDEX,
        )

        to_index = min(
            to_index,
            self.MAX_INDEX,
        )

        if from_index > to_index:
            raise ValueError(
                f"Invalid traffic table range: "
                f"{from_index}-{to_index}"
            )

        print(
            f"Downloading traffic tables "
            f"{from_index}-{to_index}..."
        )

        # -----------------------------------------------------
        # Get summary
        # -----------------------------------------------------

        summary = self.driver.get_traffic_table_summary(
            from_index
        )

        tables = TrafficTableParser.parse_summary(
            summary
        )

        # -----------------------------------------------------
        # Filter requested range
        # -----------------------------------------------------

        tables = [
            table
            for table in tables
            if from_index
            <= table["index"]
            <= to_index
        ]

        print(
            f"Found {len(tables)} traffic tables "
            f"in range {from_index}-{to_index}"
        )

        # -----------------------------------------------------
        # Counters
        # -----------------------------------------------------

        added = 0
        updated = 0
        unchanged = 0
        skipped = 0

        # -----------------------------------------------------
        # Process tables
        # -----------------------------------------------------

        for table in tables:

            index = table["index"]

            print(
                f"Processing traffic table {index}..."
            )

            # -------------------------------------------------
            # Get detailed information
            # -------------------------------------------------

            try:

                detail_output = (
                    self.driver.get_traffic_table_detail(
                        index
                    )
                )

                detail = (
                    TrafficTableParser.parse_detail(
                        detail_output
                    )
                )

            except Exception as e:

                print(
                    f"[SKIP] {index} "
                    f"Unable to retrieve detail: {e}"
                )

                skipped += 1

                continue

            # -------------------------------------------------
            # Validate detail
            # -------------------------------------------------

            if not detail:

                print(
                    f"[SKIP] {index} "
                    f"No detail information returned."
                )

                skipped += 1

                continue

            # -------------------------------------------------
            # Make sure detail has an index
            # -------------------------------------------------

            detail_index = detail.get(
                "index",
                index,
            )

            # -------------------------------------------------
            # Safety check
            # -------------------------------------------------

            if not (
                from_index
                <= detail_index
                <= to_index
            ):

                print(
                    f"[SKIP] {index} "
                    f"Detail outside requested range."
                )

                skipped += 1

                continue

            # -------------------------------------------------
            # Traffic table name
            # -------------------------------------------------

            name = detail.get(
                "name"
            )

            if not name:

                print(
                    f"[SKIP] {index} "
                    f"Traffic table has no name."
                )

                skipped += 1

                continue

            # -------------------------------------------------
            # Find existing package
            # -------------------------------------------------

            package = (
                self.package_service.get_by_table(
                    detail_index
                )
            )

            # -------------------------------------------------
            # ADD
            # -------------------------------------------------

            if package is None:

                self.package_service.create(
                    name=name,
                    speed=0,
                    profile_name=name,
                    traffic_table=detail_index,
                )

                print(
                    f"[ADD] "
                    f"{detail_index}  {name}"
                )

                added += 1

                continue

            # -------------------------------------------------
            # UPDATE
            # -------------------------------------------------

            changed = False

            if package.profile_name != name:

                package.profile_name = name
                changed = True

            if package.name != name:

                package.name = name
                changed = True

            if changed:

                self.package_service.update(
                    package
                )

                print(
                    f"[UPDATE] "
                    f"{detail_index}  {name}"
                )

                updated += 1

            # -------------------------------------------------
            # UNCHANGED
            # -------------------------------------------------

            else:

                print(
                    f"[UNCHANGED] "
                    f"{detail_index}  {name}"
                )

                unchanged += 1

        # -----------------------------------------------------
        # Summary
        # -----------------------------------------------------

        total = (
            added
            + updated
            + unchanged
        )

        print()
        print("=" * 50)
        print("Traffic Table Synchronization Complete")
        print("=" * 50)
        print(
            f"Range      : "
            f"{from_index} - {to_index}"
        )
        print(
            f"OLT tables : {len(tables)}"
        )
        print(
            f"Processed  : {total}"
        )
        print(
            f"Added      : {added}"
        )
        print(
            f"Updated    : {updated}"
        )
        print(
            f"Unchanged  : {unchanged}"
        )
        print(
            f"Skipped    : {skipped}"
        )
        print("=" * 50)

        return {
            "from_index": from_index,
            "to_index": to_index,
            "total": total,
            "olt_tables": len(tables),
            "added": added,
            "updated": updated,
            "unchanged": unchanged,
            "skipped": skipped,
        }
