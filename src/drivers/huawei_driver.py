from drivers.huawei_shell import HuaweiShell
from utils.version_parser import VersionParser
from utils.ont_parser import ONTParser
from utils.service_port_parser import ServicePortParser
from utils.service_port_detail_parser import ServicePortParser
from utils.service_port_detail_parser import ServicePortDetailParser

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

    def get_service_port(self, fsp: str, ont_id: int):
        """
        Returns complete service-port information for an ONT.
        """

        # Command 1
        output = self.run(
            f"display service-port port {fsp}"
        )

        service = ServicePortParser.find_by_ont(
            output,
            ont_id,
        )

        if not service:
            return None

        # Command 2
        output = self.run(
            f"display service-port {service['service_port']}"
        )

        details = ServicePortParser.parse_details(output)

        service.update(details)

        return service
        # ----------------------------
    # Optical
    # ----------------------------

    def display_optical_info(self, fspon, ont_id):
        return self.run(
            f"display ont optical-info {fspon} {ont_id}"
        )

    # ----------------------------
    # Traffic Profile
    # ----------------------------

    def change_traffic_profile(
        self,
        service_port: int,
        profile_name: str,
    ):
        raise NotImplementedError
    def change_traffic_profile(
        self,
        service_port: int,
        profile_name: str,
    ):
        """
        Change both inbound and outbound traffic profiles
        of a service-port.
        """

        self.run(
            f"service-port {service_port} "
            f"inbound traffic-table name {profile_name}"
        )

        self.run(
            f"service-port {service_port} "
            f"outbound traffic-table name {profile_name}"
        )

        return True
    def get_service_port_details(self, service_port: int):
        """
        Returns service-port details.
        """

        output = self.run(
            f"display service-port {service_port}"
        )

        return ServicePortParser.parse_details(output)

    def change_service_port_profile(
        self,
        service_port: int,
        inbound_profile: str,
        outbound_profile: str,
    ):
        """
        Change inbound/outbound traffic table.
        """

        self.send_command("system-view")

        output = self.send_command(
            f"service-port {service_port} "
            f"inbound traffic-table name {inbound_profile} "
            f"outbound traffic-table name {outbound_profile}"
        )

        self.send_command("commit")
        self.send_command("quit")

        return output

    def get_service_port_detail(self, service_port):
        output = self.send_command(
            f"display service-port {service_port}"
        )

        return parse_service_port_detail(output)

    def get_service_port_detail(self, service_port: int):

        output = self.send_command(
            f"display service-port {service_port}"
        )

        return ServicePortDetailParser.parse(output)
