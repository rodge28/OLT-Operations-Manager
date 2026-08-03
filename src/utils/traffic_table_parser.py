import re


class TrafficTableParser:
    """
    Parser for Huawei MA5800 traffic tables.

    Supports:

        display traffic table ip from-index 500
        display traffic table ip index <id>
    """

    @staticmethod
    def parse_summary(output: str):

        tables = []

        for line in output.splitlines():

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            # Skip headers
            if len(parts) < 5:
                continue

            if not parts[0].isdigit():
                continue

            try:

                tables.append({

                    "index": int(parts[0]),
                    "cir": int(parts[1]),
                    "cbs": int(parts[2]),
                    "pir": int(parts[3]),
                    "pbs": int(parts[4]),

                })

            except Exception:
                continue

        return tables

    @staticmethod
    def parse_detail(output: str):

        patterns = {

            "index": r"Traffic Table Index\s*:\s*(\d+)",
            "name": r"Traffic Table Name\s*:\s*(.+)",

            "cir": r"CIR\s*:\s*(\d+)",
            "cbs": r"CBS\s*:\s*(\d+)",

            "pir": r"PIR\s*:\s*(\d+)",
            "pbs": r"PBS\s*:\s*(\d+)",

            "referenced": r"Referenced Status\s*:\s*(.+)",

        }

        data = {}

        for key, pattern in patterns.items():

            match = re.search(pattern, output)

            if not match:
                continue

            value = match.group(1).strip()

            if key in ("index", "cir", "cbs", "pir", "pbs"):
                value = int(value)

            elif key == "referenced":
                value = value.lower() == "used"

            data[key] = value

        return data
