import re


class ONTParser:
    """
    Parses Huawei MA5800 ONT command outputs.
    """

    @staticmethod
    def parse_search(output):

        fields = {
            "fsp": r"F/S/P\s*:\s*(.+)",
            "ont_id": r"ONT-ID\s*:\s*(.+)",
            "run_state": r"Run state\s*:\s*(.+)",
            "config_state": r"Config state\s*:\s*(.+)",
            "match_state": r"Match state\s*:\s*(.+)",
            "serial": r"SN\s*:\s*([A-Fa-f0-9]+)",
            "description": r"Description\s*:\s*(.+)",
            "line_profile": r"Line profile name\s*:\s*(.+)",
            "service_profile": r"Service profile name\s*:\s*(.+)",
            "last_down": r"Last down cause\s*:\s*(.+)",
            "online_duration": r"ONT online duration\s*:\s*(.+)",
        }

        data = {}

        for key, pattern in fields.items():
            match = re.search(pattern, output)

            if match:
                data[key] = match.group(1).strip()

        # ---------------------------------------
        # Parse F/S/P into individual values
        # ---------------------------------------

        fsp = data.get("fsp")

        if fsp:
            try:
                frame, slot, port = fsp.split("/")

                data["frame"] = int(frame)
                data["slot"] = int(slot)
                data["port"] = int(port)

            except ValueError:
                pass

        data["found"] = "F/S/P" in output

        return data

    @staticmethod
    def parse_info(output):
        return {}

    @staticmethod
    def parse_optical(output):
        return {}

    @staticmethod
    def parse_service_port(output):
        return {}
