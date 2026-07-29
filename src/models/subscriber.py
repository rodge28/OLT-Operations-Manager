from dataclasses import dataclass


@dataclass
class Subscriber:
    account_number: str = ""
    customer_name: str = ""

    serial: str = ""

    fsp: str = ""
    frame: int = 0
    slot: int = 0
    port: int = 0
    ont_id: int = 0

    service_port: int = 0
    vlan: int = 0

    inbound_profile: str = ""
    outbound_profile: str = ""

    state: str = ""
    admin_status: str = ""

    description: str = ""

    line_profile: str = ""

    distance: int = 0
    cpu: int = 0
    memory: int = 0
    temperature: int = 0
