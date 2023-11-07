from dataclasses import dataclass
from merakiDataFetcher.meraki_dataclasses.meraki_device import MerakiDevice
from merakiDataFetcher.meraki_dataclasses.meraki_port_switch import MerakiPortSwitch


@dataclass
class MerakiSwitch(MerakiDevice):
    lanIp: str
    switchProfileId: str
    ports: [MerakiPortSwitch] = None