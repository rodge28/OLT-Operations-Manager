from drivers.huawei_driver import HuaweiDriver
from db.database import DatabaseManager
from db.models import OLT
from sqlalchemy import select

class ONUService:

    def __init__(self):
        pass

    def search_on_olt(self, olt, serial):
        """
        Search for an ONU by serial number on a single OLT.

        Args:
            olt: OLT SQLAlchemy model
            serial: ONU serial number

        Returns:
            Raw CLI output
        """

        driver = HuaweiDriver(
            host=olt.ip_address,
            username=olt.username,
            password=olt.password,
            port=olt.ssh_port,
        )

        try:
            driver.connect()

            output = driver.find_ont_by_serial(serial)

            return output

        finally:
            driver.disconnect()

    def search_all(self, serial):

        database = DatabaseManager()
        session = database.get_session()

        olts = session.scalars(select(OLT)).all()

        for olt in olts:

            print(f"Searching {olt.hostname}...")

            try:
                output = self.search_on_olt(olt, serial)

                if "The number of required ONTs     : 1" in output:
                    return olt, output

            except Exception as e:
                    print(e)

        return None, None
