from dataclasses import dataclass


@dataclass
class MerakiDevice:
    name: str
    lat: float
    lng: float
    serial: str
    mac: str
    model: str
    address: str
    notes: str
    tags: list
    networkId: str
    firmware: str
    floorPlanId: str
    url: str
    productType: str

