from drivers.huawei_driver import HuaweiDriver


class SubscriberService:

    def __init__(self, driver: HuaweiDriver):
        self.driver = driver

    def find(self, serial: str):

        ont = self.driver.find_ont_by_serial(serial)

        if not ont:
            return None

        service = self.driver.get_service_port(
            ont["fsp"],
            ont["ont_id"],
        )

        if service:
            ont.update(service)

        return ont
