from dataclasses import dataclass


@dataclass
class MerakiNetwork:
    id: str
    organizationId: str
    name: str
    productTypes: list
    timeZone: str
    tags: list
    url: str
    notes: str
    configTemplateId: str
    isBoundToConfigTemplate: bool
