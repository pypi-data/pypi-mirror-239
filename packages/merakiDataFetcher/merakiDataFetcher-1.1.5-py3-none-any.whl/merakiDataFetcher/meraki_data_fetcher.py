from pprint import pprint

import meraki
from meraki import APIError

from merakiDataFetcher.meraki_dataclasses.meraki_device import MerakiDevice
from merakiDataFetcher.meraki_dataclasses.meraki_device_appliance import MerakiAppliance
from merakiDataFetcher.meraki_dataclasses.meraki_device_camera import MerakiCamera
from merakiDataFetcher.meraki_dataclasses.meraki_device_sensor import MerakiSensor
from merakiDataFetcher.meraki_dataclasses.meraki_device_switch import MerakiSwitch
from merakiDataFetcher.meraki_dataclasses.meraki_device_wireless import MerakiWireless
from merakiDataFetcher.meraki_dataclasses.meraki_network import MerakiNetwork
from merakiDataFetcher.meraki_dataclasses.meraki_organization import MerakiOrganization
from merakiDataFetcher.meraki_dataclasses.meraki_port_appliance import MerakiPortAppliance
from merakiDataFetcher.meraki_dataclasses.meraki_port_switch import MerakiPortSwitch
from merakiDataFetcher.meraki_dataclasses.meraki_port_switch_profile import MerakiPortSwitchProfile


class MerakiDataFetcher:

    def __init__(self, apikey: str):
        """
        :param apikey:
        """
        api_key = apikey
        self.dashboard = meraki.DashboardAPI(api_key=api_key, suppress_logging=True)

    def apikey_validation(self) -> bool:
        """
        :return:
        """
        return bool(self._get_organizations())

    def _get_organizations(self):
        """
        :return:
        """
        try:
            organizations = self.dashboard.organizations.getOrganizations()
            return organizations
        except APIError:
            return None

    def _get_networks(self, organizationId: str):
        """
        :param organizationId:
        :return:
        """
        try:
            networks = self.dashboard.organizations.getOrganizationNetworks(organizationId=organizationId)
            return networks
        except APIError:
            return None

    def _get_device(self, deviceSerial: str):
        """
        :param deviceSerial:
        :return:
        """
        try:
            device = self.dashboard.devices.getDevice(serial=deviceSerial)
            return device
        except APIError:
            return None

    def _get_network(self, networkId: str):
        """
        :param networkId:
        :return:
        """
        try:
            network = self.dashboard.networks.getNetwork(networkId=networkId)
            return network
        except APIError:
            return None

    def _get_network_devices(self, networkId: str):
        """
        :param networkId:
        :return:
        """
        try:
            devices = self.dashboard.networks.getNetworkDevices(networkId=networkId)
            return devices
        except APIError:
            return None

    def _device_factory(self, device: dict) -> MerakiDevice:
        """
        :param device:
        :return:
        """
        device_data: MerakiDevice = None
        device_values = (device.get('name', ""),
                         device.get('lat', ""),
                         device.get('lng', ""),
                         device.get('serial', ""),
                         device.get('mac', ""),
                         device.get('model', ""),
                         device.get('address', ""),
                         device.get('notes', ""),
                         device.get('tags', ""),
                         device.get('networkId', ""),
                         device.get('firmware', ""),
                         device.get('floorPlanId', ""),
                         device.get('url', ""))

        if "MX" in device.get('model'):
            mx_values = ('Firewall', device.get('wan1Ip', ""), device.get('wan2Ip', ""))
            device_data = MerakiAppliance(*device_values, *mx_values)
        elif "MS" in device.get('model'):
            ms_values = ('Switch', device.get('lanIp', ""), device.get('switchProfileId', ""))
            device_data = MerakiSwitch(*device_values, *ms_values)
        elif "MR" in device.get('model'):
            mr_values = ('Access Point', device.get('lanIp', ""), device.get('beaconIdParams', ""))
            device_data = MerakiWireless(*device_values, *mr_values)
        elif "MT" in device.get('model'):
            mt_values = ('Sensor', device.get('lanIp'))
            device_data = MerakiSensor(*device_values, *mt_values)
        elif "MV" in device.get('model'):
            mv_values = ('Camera', device.get('lanIp'), device.get('wirelessMac'))
            device_data = MerakiCamera(*device_values, *mv_values)
        else:
            print(device)

        return device_data

    def _get_appliance_ports(self, networkId) -> [MerakiPortAppliance]:
        """
        :param networkId:
        :return:
        """
        try:
            appliance_ports = self.dashboard.appliance.getNetworkAppliancePorts(networkId=networkId)
            return appliance_ports
        except APIError:
            return None

    def _get_switch_ports(self, serial) -> [MerakiPortSwitch]:
        """
        :param serial:
        :return:
        """
        try:
            switch_ports = self.dashboard.switch.getDeviceSwitchPorts(serial=serial)
            return switch_ports
        except APIError:
            return None

    def get_organizations(self) -> [MerakiOrganization]:
        """
        :return:
        """
        organizations_data: [MerakiOrganization] = []
        for organization in self._get_organizations():
            organizations_data.append(
                MerakiOrganization(id=organization.get('id', ""), name=organization.get('name', ""),
                                   url=organization.get('url', ""), api=organization.get('api', ""))
            )
        return organizations_data

    def get_networks(self, organizationId: str) -> [MerakiNetwork]:
        """
        :param organizationId:
        :return:
        """
        networks_data: [MerakiNetwork] = []
        for network in self._get_networks(organizationId=organizationId):
            networks_data.append(MerakiNetwork(id=network.get('id', ""),
                                               organizationId=network.get('organizationId', ""),
                                               name=network.get('name', ""),
                                               productTypes=network.get('productTypes', ""),
                                               timeZone=network.get('timeZone', ""),
                                               tags=network.get('tags', ""),
                                               url=network.get('url', ""),
                                               notes=network.get('notes', ""),
                                               configTemplateId=network.get('configTemplateId', ""),
                                               isBoundToConfigTemplate=network.get('isBoundToConfigTemplate', ""),
                                               )
                                 )
        return networks_data

    def get_device(self, deviceSerial: str) -> MerakiDevice:
        """
        :param deviceSerial:
        :return:
        """
        device = self._get_device(deviceSerial=deviceSerial)
        device_data: MerakiDevice = self._device_factory(device)
        return device_data

    def get_network(self, networkId: str) -> MerakiNetwork:
        """
        :param networkId:
        :return:
        """
        network = self._get_network(networkId=networkId)
        network_data = MerakiNetwork(id=network.get('id', ""),
                                     organizationId=network.get('organizationId', ""),
                                     name=network.get('name', ""),
                                     productTypes=network.get('productTypes', ""),
                                     timeZone=network.get('timeZone', ""),
                                     tags=network.get('tags', ""),
                                     url=network.get('url', ""),
                                     notes=network.get('notes', ""),
                                     configTemplateId=network.get('configTemplateId', ""),
                                     isBoundToConfigTemplate=network.get('isBoundToConfigTemplate', ""))
        return network_data

    def get_network_devices(self, networkId: str, type='all') -> [MerakiDevice]:
        """
        :param networkId:
        :param type:
        :return:
        """
        devices = self._get_network_devices(networkId=networkId)
        device_data: [MerakiDevice] = []
        specific_devices: [MerakiDevice] = []

        for device in devices:
            device_data.append(self._device_factory(device))

        if type == 'all':
            return device_data

        for device in device_data:
            if device.productType == type:
                specific_devices.append(device)

        return specific_devices

    def get_appliance_ports(self, networkId: str):
        """
        :param networkId:
        :return:
        """
        ports = self._get_appliance_ports(networkId=networkId)
        appliance_ports: [MerakiPortAppliance] = []
        for port in ports:
            appliance_ports.append(
                MerakiPortAppliance(
                    enabled=port.get('enabled', ""),
                    type=port.get('type', ""),
                    vlan=port.get('vlan', ""),
                    allowedVlans=port.get('allowedVlans', ""),
                    number=port.get('number', ""),
                    dropUntaggedTraffic=port.get('dropUntaggedTraffic', ""),
                    accessPolicy=port.get('accessPolicy')
                )
            )
        return appliance_ports

    def get_switch_ports(self, serial: str):
        """
        :param serial:
        :return:
        """
        ports = self._get_switch_ports(serial=serial)
        switch_ports: [MerakiPortSwitch] = []
        for port in ports:
            switch_ports.append(
                MerakiPortSwitch(
                    serial=serial,
                    enabled=port.get('enabled', ""),
                    type=port.get('type', ""),
                    vlan=port.get('vlan', ""),
                    allowedVlans=port.get('allowedVlans', ""),
                    portId=port.get('portId', ""),
                    name=port.get('name', ""),
                    tags=port.get('tags', ""),
                    poeEnabled=port.get('poeEnabled', ""),
                    voiceVlan=port.get('voiceVlan', ""),
                    isolationEnabled=port.get('isolationEnabled', ""),
                    rstpEnabled=port.get('rstpEnabled', ""),
                    stpGuard=port.get('stpGuard', ""),
                    linkNegotiation=port.get('linkNegotiation', ""),
                    linkNegotiationCapabilities=port.get('linkNegotiationCapabilities', ""),
                    portScheduleId=port.get('portScheduleId', ""),
                    udld=port.get('udld', ""),
                    accessPolicyType=port.get('accessPolicyType', ""),
                    accessPolicyNumber=port.get('accessPolicyNumber', ""),
                    macAllowList=port.get('macAllowList', ""),
                    stickyMacAllowList=port.get('stickyMacAllowList', ""),
                    stickyMacAllowListLimit=port.get('stickyMacAllowListLimit', ""),
                    stormControlEnabled=port.get('stormControlEnabled', ""),
                    adaptivePolicyGroupId=port.get('adaptivePolicyGroupId', ""),
                    peerSgtCapable=port.get('peerSgtCapable', ""),
                    flexibleStackingEnabled=port.get('flexibleStackingEnabled', ""),
                    daiTrusted=port.get('daiTrusted', ""),
                    profile=MerakiPortSwitchProfile(
                        enabled=port.get('enabled', ""),
                        id=port.get('id', ""),
                        iname=port.get('iname', ""),
                    )
                )
            )
        return switch_ports
