from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import config
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigNat(config.Config):
    """
    Class for configuring NAT service.

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
        index = self._args[0] if len(self._args) != 0 else None
        if index is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'ip nat {index}')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def original(self, in_iface: str, osi: str, osp: str, odi: str,
                    odp: str):
        """
        Set original parameters of the NAT rule.

            Args:
                in_iface (str): The commining interface.
                osi (str): The original source ip.
                osp (str): The original port.
                odi (str): The original destination ip.
                odp (str): The original destination port.
                
            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(
            f'original in-iface {in_iface} src-ip {osi} src-port {osp} dst-ip {odi} dst-port {odp}'
        )
        return self

    def translated(self, out_iface: str, tsi: str, tsp: str, tdi: str,
                    tdp: str):
        """
        Set translated parameters of the NAT rule.

            Args:
                out_iface (str): The outgoing interface.
                tsi (str): The translated source ip.
                tsp (str): The translated port.
                tdi (str): The translated destination ip.
                tdp (str): The translated destination port.
                
            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(
            f'translated out-iface {out_iface} src-ip {tsi} src-port {tsp} dst-ip {tdi} dst-port {tdp}'
        )
        return self

    def enable(self):
        """
        Enable the NAT rule.

            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(f'enable')
        return self

    def protocol(self, protocol):
        """
        Set protocol of the NAT rule.

            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(f'protocol {protocol}')
        return self

    def mode(self, mode: str):
        """
        Set mode of the NAT rule.

            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(f'mode {mode}')
        return self

    def desc(self, desc):
        """
        Set desc of the NAT rule.

            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(f'desc {desc}')
        return self

    def nat_loopback(self):
        """
        Enable nat_loopback of the NAT rule.

            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(f'nat-loopback')
        return self

    def double_nat(self):
        """
        Enable double_nat of the NAT rule.

            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(f'double-nat')
        return self

    # For debug
    def show(self):
        """
        Show the configured NAT rule.

            Returns:
                self: The instance of the object. 
        """
        ret = self._s.command_expect(f'show')
        print(ret['data'])
        return self

    def exit(self):
        """
        Exit configure mode of the NAT rule.

            Returns:
                self: The instance of the object. 
        """
        ret = self._s.command_expect('exit',
                                        prompts=[PROMPT_CONFIG],
                                        timeout=2)
        if ret['data'].find("You are setting") != -1:
            raise ValueError(f'Fail to set NAT rule\n{ret["data"]}')
        return self
