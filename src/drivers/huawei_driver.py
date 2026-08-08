from drivers.huawei_shell import HuaweiShell

from utils.service_port_parser import ServicePortParser
from utils.version_parser import VersionParser
from utils.ont_parser import ONTParser
from utils.service_port_detail_parser import ServicePortDetailParser


class HuaweiDriver:
    """
    High-level Huawei MA5800 Driver.
    """

    def __init__(self, host, username, password, port=22):

        self.shell = HuaweiShell(
            host=host,
            username=username,
            password=password,
            port=port,
        )

    # ==========================================================
    # Connection
    # ==========================================================

    def connect(self):
        self.shell.connect()

    def disconnect(self):
        self.shell.disconnect()

    # ==========================================================
    # Generic Command
    # ==========================================================

    def run(self, command: str):
        """
        Send any command to the OLT.
        """
        return self.shell.send_command(command)

    # ==========================================================
    # System Information
    # ==========================================================

    def get_version(self):

        output = self.run("display version")

        return VersionParser.parse(output)

    def get_hostname(self):

        return self.run(
            "display current-configuration | include sysname"
        )

    # ==========================================================
    # ONU
    # ==========================================================

    def find_ont_by_serial(self, serial):

        output = self.run(
            f"display ont info by-sn {serial}"
        )

        return ONTParser.parse_search(output)

    def display_ont_info(self, fspon, ont_id):

        return self.run(
            f"display ont info {fspon} {ont_id}"
        )

    def display_optical_info(self, fspon, ont_id):

        return self.run(
            f"display ont optical-info {fspon} {ont_id}"
        )

    # ==========================================================
    # Service Port
    # ==========================================================

    def get_service_port(self, fsp: str, ont_id: int):
        """
        Returns complete service-port information for an ONT.
        """

        output = self.run(
            f"display service-port port {fsp}"
        )

        service = ServicePortParser.find_by_ont(
            output,
            ont_id,
        )

        if not service:
            return None

        output = self.run(
            f"display service-port {service['service_port']}"
        )

        details = ServicePortDetailParser.parse_details(output)

        service.update(details)

        return service

    def get_service_port_detail(self, service_port: int):
        """
        Returns parsed service-port detail.
        """

        output = self.run(
            f"display service-port {service_port}"
        )

        return ServicePortDetailParser.parse_details(output)

    # ==========================================================
    # Traffic Tables
    # ==========================================================

    def get_traffic_table_summary(self, from_index=500):
        """
        Returns all traffic tables starting from the supplied index.
        """

        return self.run(
            f"display traffic table ip from-index {from_index}"
        )

    def get_traffic_table_detail(self, index):
        """
        Returns one traffic table.
        """

        return self.run(
            f"display traffic table ip index {index}"
        )

    # ==========================================================
    # Provisioning
    # ==========================================================

    def change_traffic_profile(
        self,
        service_port: int,
        profile_name: str,
    ):
        """
        Change inbound and outbound traffic profiles
        of a service-port.

        Huawei MA5800 workflow:

            LCN-xxx#
                |
                | config
                v
            LCN-xxx(config)#
                |
                | inbound traffic-table
                | outbound traffic-table
                v
            LCN-xxx(config)#
                |
                | quit
                v
            LCN-xxx#
        """

        # ------------------------------------------------------
        # Enter configuration mode
        # ------------------------------------------------------

        self.shell.enter_config_mode()

        try:

            # --------------------------------------------------
            # Change inbound traffic profile
            # --------------------------------------------------

            self.run(
                f"service-port {service_port} "
                f"inbound traffic-table name {profile_name}"
            )

            # --------------------------------------------------
            # Change outbound traffic profile
            # --------------------------------------------------

            self.run(
                f"service-port {service_port} "
                f"outbound traffic-table name {profile_name}"
            )

        finally:

            # --------------------------------------------------
            # Always leave configuration mode
            # --------------------------------------------------

            self.shell.exit_config_mode()

        return True
