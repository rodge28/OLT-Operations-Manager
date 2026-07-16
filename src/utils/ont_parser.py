import re


class ONTParser:

    @staticmethod
    def parse(output):

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

            m = re.search(pattern, output)

            if m:
                data[key] = m.group(1).strip()

        data["found"] = "F/S/P" in output

        return data
