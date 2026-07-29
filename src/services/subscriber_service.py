from drivers.huawei_driver import HuaweiDriver
from models.subscriber import Subscriber


class SubscriberService:

    def __init__(self, olt_service):
        self.olt_service = olt_service

    def find_by_serial(self, olt_id: int, serial: str) -> Subscriber | None:
        """
        Find a subscriber by serial number on the specified OLT.

        Returns:
            Subscriber object if found.
            None if subscriber does not exist.
        """

        olt = self.olt_service.get_by_id(olt_id)

        if olt is None:
            raise ValueError(f"OLT ID {olt_id} not found.")

        driver = HuaweiDriver(
            host=olt.ip_address,
            username=olt.username,
            password=olt.password,
        )

        driver.connect()

        try:
            # Search ONT by Serial Number
            info = driver.find_ont_by_serial(serial)

            if not info or not info.get("found"):
                return None

            # Retrieve Service-Port information
            service = driver.get_service_port(
                info["fsp"],
                info["ont_id"],
            )

            if service:
                info.update(service)

            # Convert dictionary into Subscriber model
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

                service_port=int(info.get("service_port", 0)),
                vlan=int(info.get("vlan", 0)),

                inbound_profile=info.get("inbound_profile", ""),
                outbound_profile=info.get("outbound_profile", ""),

                state=info.get("state", ""),
                admin_status=info.get("admin_status", ""),

                line_profile=info.get("line_profile", ""),

                distance=info.get("distance", 0),
                cpu=info.get("cpu", 0),
                memory=info.get("memory", 0),
                temperature=info.get("temperature", 0),
            )

        finally:
            driver.disconnect()
