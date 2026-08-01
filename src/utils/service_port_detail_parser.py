import re


class ServicePortDetailParser:

    @staticmethod
    def parse(output: str):

        patterns = {
            "service_port": r"Index\s*:\s*(\d+)",
            "vlan": r"VLAN ID\s*:\s*(\d+)",
            "frame": r"F/S/P\s*:\s*(\d+)/(\d+)/(\d+)",
            "ont_id": r"ONT ID\s*:\s*(\d+)",
            "gem": r"GEM port index\s*:\s*(\d+)",
            "rx": r"RX\s*:\s*(\d+)",
            "tx": r"TX\s*:\s*(\d+)",
            "inbound_profile": r"Inbound table name\s*:\s*(.+)",
            "outbound_profile": r"Outbound table name\s*:\s*(.+)",
            "admin_status": r"Admin status\s*:\s*(.+)",
            "state": r"State\s*:\s*(.+)",
            "description": r"Description\s*:\s*(.*)",
        }

        data = {}

        # Simple fields
        for key in (
            "service_port",
            "vlan",
            "ont_id",
            "gem",
            "rx",
            "tx",
            "inbound_profile",
            "outbound_profile",
            "admin_status",
            "state",
            "description",
        ):
            m = re.search(patterns[key], output)

            if m:
                value = m.group(1).strip()

                if key in (
                    "service_port",
                    "vlan",
                    "ont_id",
                    "gem",
                    "rx",
                    "tx",
                ):
                    value = int(value)

                data[key] = value

        # F/S/P
        m = re.search(patterns["frame"], output)

        if m:
            data["frame"] = int(m.group(1))
            data["slot"] = int(m.group(2))
            data["port"] = int(m.group(3))
            data["fsp"] = f"{m.group(1)}/{m.group(2)}/{m.group(3)}"

        return data
