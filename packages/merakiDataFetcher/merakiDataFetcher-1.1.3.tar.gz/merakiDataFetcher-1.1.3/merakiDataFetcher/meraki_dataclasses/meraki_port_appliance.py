from dataclasses import dataclass

from merakiDataFetcher.meraki_dataclasses.meraki_port import MerakiPort


@dataclass
class MerakiPortAppliance(MerakiPort):
    number: int
    dropUntaggedTraffic: bool
    accessPolicy: str
