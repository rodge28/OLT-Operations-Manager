from dataclasses import dataclass


@dataclass
class VersionInfo:
    version: str
    patch: str
    product: str
    uptime_days: int
