from dataclasses import dataclass

@dataclass
class Subscriber:

    account_number: str

    customer_name: str

    serial: str

    fsp: str

    ont_id: int

    service_port: int

    vlan: int

    inbound_profile: str

    outbound_profile: str

    state: str
