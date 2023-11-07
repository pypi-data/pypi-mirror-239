import re

from guerrilla_aaron.session import SshSession
from guerrilla_aaron.utils.decorator import root_access_required
from guerrilla_aaron.utils.input_chk import chk_valid_mac, chk_valid_ip

class ShellCmdService:
    """
    Class for using utility in Host.

        Args:
            ssh_session (SshSession): SSH session object.
            sudo_paswd (str): Password for sudo access.

        Attributes:
            _ssh (SshSession): SSH session object.
            _sudo_pwd (str): Password for sudo access.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._sudo_pwd = sudo_paswd

    def check_env(self):
        """
        Check if the host is alive.

            Raises:
                ValueError: If the host is not alive.
        """
        if not self._ssh:
            raise ValueError('host is not alive')

    @root_access_required
    def unzip_file(self, unzip_file, unzip_filepath, unzip_path):
        """
         The path to the file to unzip. Must be a gzipped tar file
         
         Args:
         	 unzip_filepath: The path to the unzip file
         	 unzip_path: The path to the unzip file
        """
        print(f'tar zxvf {unzip_filepath}/{unzip_file}.tar.gz -C {unzip_path}')
        ret = self._ssh.command(
            f'tar zxvf {unzip_filepath}/{unzip_file}.tar.gz -C {unzip_path}')

    @root_access_required
    def arp(self, count, ip):
        """
         Send ARP request to IP. This is a blocking call. The return value is a list of IP addresses that were sent to the IP.
         
            Args:
                count: Number of ARP requests to send. If this is less than 1 it is a zero - length list
                ip: IP address to send ARP request
            
            Returns: 
                A list of IP addresses that were sent to the
        """
        ret = self._ssh.command(f'arping -c {count} {ip}', timeout=5)
        return ret

    def tcpdump(self, itf, filter_type):
        """
         Get the PID of the tcpdump process. It is possible to filter by type but not by type
         
            Args:
                itf: ITERATOR or ITF name ( ex : i386_8 )
                filter_type: TCPDUMP_NONE or TCPDUMP_STANDARDEFF
            
            Returns: 
                PID of the tcpdump
        """
        self._ssh.login_as_root()
        ret = self._ssh.command(
            f'tcpdump -i {itf} {filter_type} > tcpdumpfile 2>&1 &')
        pid = re.findall("\[[\d\]]] \d+", ret)[0].split(' ')[1]
        return pid

    def get_tcpdumpfile(self, pid):
        """
         Get tcpdumpfile for process with pid. This is useful for debugging the process
         
            Args:
                pid: pid of the process to get tcpdumpfile for
            
            Returns: 
                string containing tcpdumpfile for the process with pid
        """
        self._ssh.command(f'kill {pid}')
        ret = self._ssh.command(f'cat tcpdumpfile')
        print(f"DUMP{ret}DUMPEND")
        self._ssh.command(f'rm tcpdumpfile')
        self._ssh.logout_from_root()
        return ret

    def dig(self, domain_name: str = None):
        """
        A tool to dig the URL.
            
            Args:
                domain_name: A domain name which is required to analyze
                
            Raises:
                ValueError: If the host is not alive.
        """
        ret = self._ssh.command(f'dig {domain_name} | grep {domain_name}.')
        return ret

    def show_network(self, dev=None):
        """
        Show network information.

            Args:
                dev (str, optional): The device name. Defaults to None.

            Returns:
                str: The network information. 
        """
        if dev is None:
            return self._ssh.command(f'ip addr')
        else:
            return self._ssh.command(f'ip addr show {dev}')
        
    @root_access_required
    def set_network(self, dev: str = 'eth1', ip: str = '', mask: str = '24'):
        """
        Set network for a device.

            Args:
                dev (str, optional): The device name. Defaults to 'eth1'.
                ip (str, optional): The IP address. Defaults to ''.
                mask (str, optional): The subnet mask. Defaults to '24'.
        """

        # Configure network setting via edit config file
        config=f"auto {dev}\niface {dev} inet static\naddress {ip}\nnetmask {mask}"

        self._ssh.command(f'ip addr flush {dev}')
        self._ssh.command('echo "source-directory /etc/network/interfaces.d" > /etc/network/interfaces')
        self._ssh.command(f'echo "{config}" > /etc/network/interfaces.d/{dev}')
        self._restart_network(dev)

    @root_access_required
    def restart_network(self, dev):
        self._restart_network(dev)
    
    def _restart_network(self, dev):
        """
        Restart network for a device.
        """
        self._ssh.command(f"ifdown {dev}")
        self._ssh.command(f"ifup {dev}")

    @root_access_required
    def set_networks(self, dev: str = 'eth1', ip: list = [], mask: list = []):
        """
        Set multiple networks for a device.

            Args: 
                dev (str, optional): The device name. Defaults to 'eth1'. 
                ip (list, optional): A list of IP addresses. Defaults to []. 
                mask (list, optional): A list of subnet masks. Defaults to []. 

            Raises: 
                ValueError: If the number of IPs and masks are not equal.  
        """
        if len(ip) != len(mask):
            raise ValueError('number of ip and mask are not equal')
        self._ssh.command(f'ip addr flush dev {dev}')

        config=f"auto {dev}\niface {dev} inet static\naddress {ip[0]}\nnetmask {mask[0]}"
        self._ssh.command('echo "source-directory /etc/network/interfaces.d" > /etc/network/interfaces')
        self._ssh.command(f'echo "{config}" > /etc/network/interfaces.d/{dev}')

        for i in range(1, len(ip)):
            self._ssh.command(f'echo "up ip addr add {ip[i]}/{mask[i]} dev {dev}" >> /etc/network/interfaces.d/{dev}')

    @root_access_required
    def set_mac_addr(self, dev: str = 'eth1', mac: str = ''):
        """
        Set the MAC address of a device.

            Args:
                dev (str): The device to set the MAC address for. Default is 'eth1'.
                mac (str): The MAC address to set. Must be a valid MAC address.

            Returns:
                str: The output of the command used to set the MAC address. 
        """
        chk_valid_mac(mac)
        ret = self._ssh.command(f'ip link set {dev} address {mac}')

    @root_access_required
    def remove_arp_entry(self, dev: str = 'eth1', ip: str = ''):
        """
        Remove an ARP entry from the device.

            Args:
                dev (str): The device name (default: 'eth1').
                ip (str): The IP address of the ARP entry to be removed.

            Returns: 
                str: The output of the command. 
        """
        chk_valid_ip(ip)
        ret = self._ssh.command(f'ip neigh del {ip} dev {dev}')

    @root_access_required
    def enable_dhcp_client(self, dev: str = 'eth1'):
        """
        Enable DHCP client on a given device.

            Args:
                dev (str): The device to enable DHCP client on. Defaults to 'eth1'.. Prints the output of the commands executed on the remote machine. 
        """
        print(self._ssh.command(f'ip addr flush {dev}'))
        print(self._ssh.command(f'dhclient {dev}', timeout=10))

    @root_access_required
    def add_route(self,
                  dev: str = 'eth1',
                  dip: str = '',
                  gw: str = '',
                  mask: str = ''):
        """
        Log in as root and add a route to the device. 

            Args: 
                dev (str): Name of the device. Default is 'eth1'. 
                dip (str): Destination IP address. 
                gw (str): Gateway IP address. 
                mask (str): Subnet mask. 
            Returns: 
                ret (list): List of routes on the device.  
        """

        # Configure routing rule via edit config file
        self._ssh.command(f'ip addr flush {dev}')
        self._ssh.command(f'echo "post-up ip route add {dip}/{mask} via {gw}" >> /etc/network/interfaces.d/{dev}')
        self._restart_network(dev)

    def show_route(self):
        """
        Show the route of the current device.

            Returns:
                str: The output of the command 'ip route'. 
        """
        return self._ssh.command('ip route')

    @root_access_required
    def remove_residual_artifact(self):
        self._ssh.command("rm *.log")