from dataclasses import dataclass

from merakiDataFetcher.meraki_dataclasses.meraki_port import MerakiPort
from merakiDataFetcher.meraki_dataclasses.meraki_port_switch_profile import MerakiPortSwitchProfile


@dataclass
class MerakiPortSwitch(MerakiPort):
    serial: str
    portId: str
    name: str
    tags: [str]
    poeEnabled: bool
    voiceVlan: int
    isolationEnabled: bool
    rstpEnabled: bool
    stpGuard: str
    linkNegotiation: str
    linkNegotiationCapabilities: [str]
    portScheduleId: str
    udld: str
    accessPolicyType: str
    accessPolicyNumber: int
    macAllowList: [str]
    stickyMacAllowList: [str]
    stickyMacAllowListLimit: int
    stormControlEnabled: bool
    adaptivePolicyGroupId: str
    peerSgtCapable: bool
    flexibleStackingEnabled: bool
    daiTrusted: bool
    profile: MerakiPortSwitchProfile = None
