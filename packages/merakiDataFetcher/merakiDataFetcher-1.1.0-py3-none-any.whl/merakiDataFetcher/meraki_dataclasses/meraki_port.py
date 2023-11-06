from dataclasses import dataclass


@dataclass
class MerakiPort:
    enabled: bool
    type: str
    vlan: int
    allowedVlans: str
