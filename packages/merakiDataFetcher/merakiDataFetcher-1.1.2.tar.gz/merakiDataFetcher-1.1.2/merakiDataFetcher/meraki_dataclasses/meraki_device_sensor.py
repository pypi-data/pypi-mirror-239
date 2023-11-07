from dataclasses import dataclass
from merakiDataFetcher.meraki_dataclasses.meraki_device import MerakiDevice

@dataclass
class MerakiSensor(MerakiDevice):
    lanIp: str
