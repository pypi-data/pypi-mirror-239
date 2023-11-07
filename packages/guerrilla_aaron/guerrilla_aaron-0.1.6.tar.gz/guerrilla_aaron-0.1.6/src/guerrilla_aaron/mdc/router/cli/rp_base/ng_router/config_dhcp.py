from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import config
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigDhcp(config.Config):
    """
    Class for configuring DHCP service.

        Args:
            session (object): The session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
            _args (list): A list of arguments passed to the function.
            _kwargs (dict): A dictionary of keyword arguments passed to the function.
    """

    def __init__(self, session: object, *args, **kwargs):
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        """
        Set the default prompts.
        """
        self._s.set_default_prompts([PROMPT_CONFIG])

    # Reserve flexibility for function override
    def _getin(self):
        """
        Get into the interface lan.
        """
        # default apply the first element as parameter
        if str(self._args[0]).isdigit():
            index = self._args[0] if len(self._args) != 0 else None
            self._index = index
            if index is None:
                raise Exception(f"Input parameter is empty!")
            self._s.command_expect(f'ip dhcp pool {index}')
        else:
            name = self._args[0] if len(self._args) != 0 else None
            self._name = name
            if name is None:
                raise Exception(f"Input parameter is empty!")
            self._s.command_expect(f'ip dhcp static pool {name}')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_dhcp_server(self,
                        lease: str = None,
                        dns_server_1: str = None,
                        dns_server_2: str = None,
                        ntp_server: str = None,
                        default_router: str = None,
                        network_begin: str = None,
                        network_end: str = None,
                        network_mask: str = None,
                        host: str = None,
                        host_mask: str = None,
                        hardware_address: str = None):
        """
        Set dhcp server.

            Args:
                lease (str): The lease time of dhcp server
                dns_server_1 (str): The ip address of first dhcp server.
                dns_server_2 (str): The ip address of second dhcp server.
                ntp_server (str): The ip address of ntp server.
                default_router (str): The ip address of default router.
                network_begin (str): The begining ip address of given ip address pool.
                network_end (str): The end ip address of given ip address pool.
                network_mask (str): The netmask of given ip address pool.
                host (str): The ip address to assign to a host.
                host_mask (str): The netmask to assign to a host.
                hardware_address (str): The hardware address which is specified to assign ip address.
                
            Returns:
                self: The instance of the object. 
        """
        if network_begin and network_end and network_mask:
            # print('network')
            self._s.command_expect(
                f'network {network_begin} {network_end} {network_mask}')
        if host and host_mask:
            # print('host')
            self._s.command_expect(f'host {host} {host_mask}')
        if hardware_address:
            # print('mac')
            self._s.command_expect(f'hardware-address {hardware_address}')
        if default_router:
            # print('gw')
            self._s.command_expect(f'default-router {default_router}')
        if dns_server_1:
            # print('dns1')
            self._s.command_expect(
                f'dns-server {dns_server_1} {dns_server_2}')
        if ntp_server:
            # print('dns2')
            self._s.command_expect(f'ntp-server {ntp_server}')
        if lease:
            # print('lease')
            self._s.command_expect(f'lease {lease}')
        return self

    def exit(self):
        """
        Exit configure mode of the dhcp server.

            Raises:
                ValueError: If fail to set DHCP rule.
        """
        ret = self._s.command_expect('exit',
                                        prompts=[PROMPT_CONFIG],
                                        timeout=2)
        if ret['data'].find("You are setting") != -1:
            raise ValueError(f'Fail to set DHCP rule\n{ret["data"]}')
