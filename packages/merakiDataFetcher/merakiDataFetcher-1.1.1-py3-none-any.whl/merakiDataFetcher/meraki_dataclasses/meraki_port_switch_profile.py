from dataclasses import dataclass


@dataclass
class MerakiPortSwitchProfile:
    enabled: bool
    id: str
    iname: str
