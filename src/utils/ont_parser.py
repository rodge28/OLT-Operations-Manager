import re


class ONTParser:

    @staticmethod
    def parse_search(output: str) -> dict:
        """
        Parse:
            display ont info by-sn <serial>
        """

        if "F/S/P" not in output:
            return {
                "found": False
            }

        data = {
            "found": True
        }

        fields = {
            "fsp": r"F/S/P\s*:\s*(.+)",
            "ont_id": r"ONT-ID\s*:\s*(\d+)",
            "run_state": r"Run state\s*:\s*(.+)",
            "config_state": r"Config state\s*:\s*(.+)",
            "match_state": r"Match state\s*:\s*(.+)",
            "serial": r"SN\s*:\s*([A-Fa-f0-9]+)",
            "description": r"Description\s*:\s*(.+)",
            "line_profile_id": r"Line profile ID\s*:\s*(\d+)",
            "line_profile": r"Line profile name\s*:\s*(.+)",
            "last_down": r"Last down cause\s*:\s*(.+)",
            "online_duration": r"ONT online duration\s*:\s*(.+)",
            "distance": r"ONT distance\(m\)\s*:\s*(\d+)",
            "last_distance": r"ONT last distance\(m\)\s*:\s*(\d+)",
            "cpu": r"CPU occupation\s*:\s*(\d+)%",
            "memory": r"Memory occupation\s*:\s*(\d+)%",
            "temperature": r"Temperature\s*:\s*(\d+)",
        }

        for key, pattern in fields.items():

            match = re.search(pattern, output)

            if not match:
                continue

            value = match.group(1).strip()

            if key in (
                "ont_id",
                "distance",
                "last_distance",
                "cpu",
                "memory",
                "temperature",
                "line_profile_id",
            ):
                value = int(value)

            data[key] = value

        # Parse F/S/P
        if "fsp" in data:
            frame, slot, port = data["fsp"].split("/")

            data["frame"] = int(frame)
            data["slot"] = int(slot)
            data["port"] = int(port)

        # Parse Vendor / Model
        vendor_model = re.search(
            r"\(([A-Za-z0-9]+)-([A-Za-z0-9]+)\)",
            output,
        )

        if vendor_model:
            data["vendor"] = vendor_model.group(1)
            data["model"] = vendor_model.group(2)

        # Parse Description
        data.update(
            ONTParser.parse_description(
                data.get("description", "")
            )
        )

        return data

    @staticmethod
    def parse_description(description: str) -> dict:

        result = {
            "account_number": None,
            "customer_name": description,
        }

        if "/" not in description:
            return result

        account, customer = description.split("/", 1)

        result["account_number"] = account.strip()
        result["customer_name"] = customer.strip()

        return result
