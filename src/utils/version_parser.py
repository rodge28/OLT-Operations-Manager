import re

class VersionParser:

    @staticmethod
    def parse(output: str):

        data = {
            "vendor": "Huawei",
            "model": "",
            "version": "",
            "patch": "",
            "uptime": "",
        }

        patterns = {
            "model": r"PRODUCT\s*:\s*(.+)",
            "version": r"VERSION\s*:\s*(.+)",
            "patch": r"PATCH\s*:\s*(.+)",
            "uptime": r"Uptime is (.+)",
        }

        for key, pattern in patterns.items():

            match = re.search(pattern, output)

            if match:
                data[key] = match.group(1).strip()

        return data
