from dataclasses import dataclass
from merakiDataFetcher.meraki_dataclasses.meraki_device import MerakiDevice
from merakiDataFetcher.meraki_dataclasses.meraki_port_appliance import MerakiPortAppliance


@dataclass
class MerakiAppliance(MerakiDevice):
    wan1Ip: str
    wan2Ip: str
    ports: [MerakiPortAppliance] = None
