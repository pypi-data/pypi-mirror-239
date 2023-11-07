from dataclasses import dataclass
from merakiDataFetcher.meraki_dataclasses.meraki_device import MerakiDevice

@dataclass
class MerakiWireless(MerakiDevice):
    lanIp: str
    beaconIdParams: dict
