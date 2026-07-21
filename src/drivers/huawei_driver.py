from drivers.huawei_shell import HuaweiShell
from utils.version_parser import VersionParser
from utils.ont_parser import ONTParser


class HuaweiDriver:
    """
    High-level Huawei MA5800 driver.

    This class wraps HuaweiShell and exposes easy-to-use methods
    for the rest of the application.
    """

    def __init__(self, host, username, password, port=22):

        self.shell = HuaweiShell(
            host=host,
            username=username,
            password=password,
            port=port,
        )

    # ----------------------------
    # Connection
    # ----------------------------

    def connect(self):
        self.shell.connect()

    def disconnect(self):
        self.shell.disconnect()

    # ----------------------------
    # Generic command
    # ----------------------------

    def run(self, command):
        return self.shell.send_command(command)

    # ----------------------------
    # Information
    # ----------------------------

    def get_version(self):

        output = self.run("display version")

        return VersionParser.parse(output)

    def get_hostname(self):
        return self.run(
            "display current-configuration | include sysname"
        )

    # ----------------------------
    # ONU
    # ----------------------------
    def find_ont_by_serial(self, serial):

        output = self.run(
            f"display ont info by-sn {serial}"
        )

        return ONTParser.parse_search(output)


    def display_ont_info(self, fspon, ont_id):
        return self.run(
            f"display ont info {fspon} {ont_id}"
        )

    # ----------------------------
    # Service Port
    # ----------------------------

    def find_service_port(self, fspon):
        return self.run(
            f"display service-port port {fspon}"
        )

    # ----------------------------
    # Optical
    # ----------------------------

    def display_optical_info(self, fspon, ont_id):
        return self.run(
            f"display ont optical-info {fspon} {ont_id}"
        )
