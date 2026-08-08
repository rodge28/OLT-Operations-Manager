from drivers.huawei_driver import HuaweiDriver
from models.subscriber import Subscriber

class SubscriberService:

    def __init__(self, olt_service):
        self.olt_service = olt_service

    def find_by_serial(
        self,
        olt_id: int,
        serial: str,
    ) -> Subscriber | None:

        olt = self.olt_service.get_by_id(olt_id)

        if olt is None:
            raise ValueError(
                f"OLT ID {olt_id} not found."
            )

        driver = HuaweiDriver(
            host=olt.ip_address,
            username=olt.username,
            password=olt.password,
        )

        driver.connect()

        try:
            info = driver.find_ont_by_serial(serial)

            if not info or not info.get("found"):
                return None

            service = driver.get_service_port(
                info["fsp"],
                info["ont_id"],
            )

            if service:
                info.update(service)

            return Subscriber(
                account_number=info.get("account_number", ""),
                customer_name=info.get("customer_name", ""),
                serial=info.get("serial", ""),
                description=info.get("description", ""),

                fsp=info.get("fsp", ""),
                frame=info.get("frame", 0),
                slot=info.get("slot", 0),
                port=info.get("port", 0),
                ont_id=info.get("ont_id", 0),

                service_port=int(
                    info.get("service_port", 0)
                ),
                vlan=int(
                    info.get("vlan", 0)
                ),

                inbound_profile=info.get(
                    "inbound_profile", ""
                ),
                outbound_profile=info.get(
                    "outbound_profile", ""
                ),

                state=info.get("state", ""),
                admin_status=info.get(
                    "admin_status", ""
                ),

                line_profile=info.get(
                    "line_profile", ""
                ),

                distance=info.get("distance", 0),
                cpu=info.get("cpu", 0),
                memory=info.get("memory", 0),
                temperature=info.get(
                    "temperature", 0
                ),
            )

        finally:
            driver.disconnect()

    def change_package(
        self,
        olt_id: int,
        serial: str,
        package,
    ):
        """
        Change subscriber traffic profile and verify the result.
        """

        # --------------------------------------------------
        # Find subscriber
        # --------------------------------------------------

        subscriber = self.find_by_serial(
            olt_id,
            serial,
        )

        if subscriber is None:
            raise ValueError(
                "Subscriber not found."
            )

        # --------------------------------------------------
        # Get OLT
        # --------------------------------------------------

        olt = self.olt_service.get_by_id(
            olt_id
        )

        if olt is None:
            raise ValueError(
                f"OLT ID {olt_id} not found."
            )

        # --------------------------------------------------
        # Create driver
        # --------------------------------------------------

        driver = HuaweiDriver(
            host=olt.ip_address,
            username=olt.username,
            password=olt.password,
        )

        driver.connect()

        try:

            # --------------------------------------------------
            # Change package
            # --------------------------------------------------

            result = driver.change_traffic_profile(
                service_port=subscriber.service_port,
                profile_name=package.profile_name,
            )

            print(
                f"Change traffic profile result: {result!r}"
            )

            if result is not True:
                return False

            # --------------------------------------------------
            # Verify the change
            # --------------------------------------------------

            updated = driver.get_service_port_detail(
                subscriber.service_port
            )

            print(
                f"Updated service-port: {updated!r}"
            )

            if not isinstance(updated, dict):
                print(
                    "Package verification failed: "
                    "service-port detail is not a dictionary."
                )
                return False

            inbound = updated.get(
                "inbound_profile",
                "",
            ).strip()

            outbound = updated.get(
                "outbound_profile",
                "",
            ).strip()

            expected = package.profile_name.strip()

            print(
                f"Expected profile : {expected}"
            )

            print(
                f"Inbound profile  : {inbound}"
            )

            print(
                f"Outbound profile : {outbound}"
            )

            # --------------------------------------------------
            # Verification result
            # --------------------------------------------------

            return (
                inbound == expected
                and
                outbound == expected
            )

        finally:
            driver.disconnect()
