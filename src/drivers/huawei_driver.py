from drivers.huawei_keyboard_interactive import HuaweiOLTSSH


class HuaweiDriver:

    def __init__(self, host, username, password, port=22):

        self.device = {
            "device_type": "huawei_olt",
            "host": host,
            "username": username,
            "password": password,
            "port": port,
            "use_keys": False,
            "allow_agent": False,
            "fast_cli": False,
        }

        self.connection = None

    def connect(self):
        self.connection = HuaweiOLTSSH(**self.device)
        self.connection.enable()
        # Disable interactive prompts
        self.connection.send_command_timing("undo smart")

    def disconnect(self):
        try:
            # Restore the default CLI behavior
            self.connection.send_command_timing("smart")
        except Exception:
            pass

        if self.connection:
            try:
                self.connection.disconnect()
            except Exception:
                pass

    def enable(self):
        """Enter privileged mode."""
        self.connection.enable()

    def send_command(self, command, privilege=False):
        """
        Execute a command.

        If privilege=True, automatically enter enable mode first.
        """
        if privilege:
            self.enable()

        return self.connection.send_command(
            command,
            read_timeout=60
        )

    def get_version(self):
        return self.send_command("display version")

    def get_hostname(self):
        output = self.send_command(
            "display current-configuration | include sysname",
            privilege=True
        )

        return output

    def find_ont_by_serial(self, serial):

        return self.send_command(
            f"display ont info by-sn {serial}",
            privilege=True
        )


    def find_service_port(self, fspon):

        return self.send_command(
            f"display service-port port {fspon}",
            privilege=True
        )
