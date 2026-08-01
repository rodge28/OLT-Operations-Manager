import re


class ServicePortParser:

    @staticmethod
    def find_by_ont(output: str, ont_id: int | str):

        ont_id = str(ont_id)

        for line in output.splitlines():

            line = line.strip()

            if not line:
                continue

            # Service-port table rows always start with the index
            if not re.match(r"^\d+", line):
                continue

            parts = line.split()

            if len(parts) < 11:
                continue

            try:
                service_port = int(parts[0])
                vlan = int(parts[1])

                # parts[4] = 0/1
                # parts[5] = /0
                frame_slot = parts[4]
                port = parts[5].replace("/", "")

                frame, slot = frame_slot.split("/")

                vpi = parts[6]          # ONT-ID
                gem = parts[7]
                flow = parts[9]
                rx = parts[10]
                tx = parts[11]
                state = parts[12]

            except Exception:
                continue

            if vpi == ont_id:

                return {
                    "service_port": service_port,
                    "vlan": vlan,
                    "frame": int(frame),
                    "slot": int(slot),
                    "port": int(port),
                    "ont_id": int(vpi),
                    "gem": int(gem),
                    "flow": int(flow),
                    "rx": int(rx),
                    "tx": int(tx),
                    "state": state,
                }

        return None
    @staticmethod
    def parse(output):

        fields = {
            "service_port": r"Index\s*:\s*(\d+)",
            "vlan": r"VLAN ID\s*:\s*(\d+)",
            "inbound_profile": r"Inbound table name\s*:\s*(.+)",
            "outbound_profile": r"Outbound table name\s*:\s*(.+)",
            "service_description": r"Description\s*:[ \t]*([^\r\n]*)",
            "state": r"State\s*:\s*(.+)",
            "admin_status": r"Admin status\s*:\s*(.+)",
        }

        data = {}

        for key, pattern in fields.items():

            m = re.search(pattern, output)

            if m:
                data[key] = m.group(1).strip()

        return data
