from dataclasses import dataclass
from merakiDataFetcher.meraki_dataclasses.meraki_network import MerakiNetwork


@dataclass
class MerakiOrganization:
    id: str
    name: str
    url: str
    api: dict
    networks: list[MerakiNetwork] = None
