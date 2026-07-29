import re


class ServicePortParser:
    """
    Parses:
        display service-port port <fsp>

    Returns one entry per service-port.
    """

    @staticmethod
    def parse(output: str):

        entries = []

        pattern = re.compile(
            r"^\s*"
            r"(\d+)\s+"           # INDEX
            r"(\d+)\s+"           # VLAN
            r"\S+\s+"             # VLAN ATTR
            r"gpon\s+"            # PORT TYPE
            r"(\d+)/(\d+)\s*/(\d+)\s+"  # F/S/P
            r"(\d+)\s+"           # ONT ID (VPI)
            r"(\d+)\s+"           # GEM (VCI)
            r"\S+\s+"             # FLOW TYPE
            r"(\d+)\s+"           # FLOW PARA
            r"(\d+)\s+"           # RX
            r"(\d+)\s+"           # TX
            r"(\w+)",             # STATE
            re.MULTILINE,
        )

        for match in pattern.finditer(output):

            entries.append({

                "service_port": int(match.group(1)),
                "vlan": int(match.group(2)),

                "frame": int(match.group(3)),
                "slot": int(match.group(4)),
                "port": int(match.group(5)),

                "fsp": f"{match.group(3)}/{match.group(4)}/{match.group(5)}",

                "ont_id": int(match.group(6)),
                "gem": int(match.group(7)),

                "flow": int(match.group(8)),

                "rx": int(match.group(9)),
                "tx": int(match.group(10)),

                "state": match.group(11),

            })

        return entries

    @staticmethod
    def find_by_ont(output: str, ont_id: int):

        ports = ServicePortParser.parse(output)

        for port in ports:

            if port["ont_id"] == ont_id:
                return port

        return None
