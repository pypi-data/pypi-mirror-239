from datetime import datetime
from guerrilla_aaron.session import SshSession
import os

class ScapyService:
    """
    Class for controlling a scapy container on a remote host.

        Args:
            ssh_session (SshSession): An active SSH session to the remote host.
            sudo_paswd (str): The sudo password for the remote host.

        Attributes:
            _ssh (SshSession): SSH session object.
            image_name (str): The name of the scapy image to use. Defaults to 'calico/scapy'.
            image_tag (str): The tag of the scapy image to use. Defaults to 'v2.4.0'.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self.image_name = "calico/scapy"
        self.image_tag = "v2.4.0"
        self.scapy_dict_name = ""
        self.scapy_file_name = ""

    def _check_conneted(self):
        """
        Check if the SSH session is connected.

            Raises:
                ValueError: If the SSH session is not connected.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    def check_env(self):
        """
        Checks if the environment is set up correctly.

            Raises:
                ValueError: If the SSH session is not connected or if the docker image is not found.
        """
        self._check_conneted()
        output = self._ssh.command('docker images')
        if self.image_name not in output:
            raise ValueError(f'No docker image {self.image_name}')

    def send(self, scapy_syntax: str = '', dev: str = None, count: int = 1):
        """
        Send packet with Scapy.

            Args:
                scapy_syntax (str, optional): Scapy syntax for packet format. Defaults to ''.
                dev (str, optional): Device name. Defaults to None.
                count (int, optional): Number of packets to send. Defaults to 1.

            Returns:
                str: Output of the command execution. 
        """
        self._check_conneted()

        scapy_file_name = datetime.now().isoformat().replace(":", "_")[:19]
        scapy_dict_name = "scapy_script"

        self._ssh.command(f'mkdir -p $HOME/{scapy_dict_name}')
        if dev is not None:
            scapy_call = f'sendp({scapy_syntax}, iface="{dev}", count={count})'
        else:
            scapy_call = f'send({scapy_syntax}, count={count})'
        scapy_file_out_cmd = f'printf \'{scapy_call}\' >> $HOME/{scapy_dict_name}/{scapy_file_name}'
        self._ssh.command(scapy_file_out_cmd)

        # Descript packet format in `scapy_dict_name` and send packet with Scapy.
        docker_cmd = f'docker run --rm --net=host \
            -v $HOME/{scapy_dict_name}:/{scapy_dict_name} {self.image_name}:{self.image_tag} \
            scapy -c /{scapy_dict_name}/{scapy_file_name}'

        ret = self._ssh.command(docker_cmd)

        # Clean up
        print(docker_cmd)
        self._ssh.command(f"rm $HOME/{scapy_dict_name}/{scapy_file_name}")
    

    def generate_igmp_scapy_script(self, 
                                   sip: str, 
                                   dip: str, 
                                   padding_n: str, 
                                   igmp_type: str, 
                                   igmp_group_addr: str, 
                                   count: str, 
                                   iface: str):
        """
        Fill the igmp scapy script template with the given parameters
        Args:
            sip (str): Source IP
            dip (str): Destination IP
            padding_n (str): Padding number
            igmp_type (str): IGMP type
            igmp_group_addr (str): IGMP group address
            count (str): Number of packets to send
            iface (str): Interface name

        Returns:
            str: filled_script: The filled script with the given parameters.
        """
        with open(os.path.dirname(os.getcwd())+ '/lib/atb/service/scapy_template/igmp_script.py', "r") as script_file:
            script_content = script_file.read()

        filled_script = script_content.format(
            sip=sip,
            dip=dip,
            padding_n=padding_n,
            igmp_type=igmp_type,
            igmp_group_addr=igmp_group_addr,
            iface=iface,
            count=count
        )
        # print("filled_script",filled_script)
        return filled_script


    def generate_arp_scapy_script(self, 
                                  source_macs: list, 
                                  ips: list, 
                                  target_ip: str, 
                                  nic: str):
        """
        Fill the arp scapy script template with the given parameters
        Args:
            source_macs (list): list of source macs
            ips (list): list of ips
            target_ip (str): target ip
            nic (str): nic name

        Returns:
            str: filled_script: The filled script with the given parameters.
            
        """
        with open(os.path.dirname(os.getcwd())+ '/lib/atb/service/scapy_template/arp_script.py', "r") as script_file:
            script_content = script_file.read()

        filled_script = script_content.format(
            source_macs=source_macs,
            ips=ips,
            target_ip=target_ip,
            nic=nic
        )
        # print("filled_script",filled_script)
        return filled_script

    def generate_vrrp_scapy_script(self, 
                                   padding_n: int, 
                                   smac: str, 
                                   dmac: str, 
                                   sip: str, 
                                   dip: str, 
                                   version: int, 
                                   priority: int, 
                                   ip_address: str, 
                                   iface: str):
        """
        Fill the broadcast scapy script template with the given parameters
        Args:
            padding_n (int): Padding number
            smac (str): Source MAC
            dmac (str): Destination MAC
            sip (str): Source IP
            dip (str): Destination IP
            version (int): Version
            priority (int): Priority
            ip_address (str): IP address
            iface (str): Interface

        Returns:
            str: filled_script: The filled script with the given parameters.
        """
        with open(os.path.dirname(os.getcwd())+ '/lib/atb/service/scapy_template/vrrp_script.py', "r") as script_file:
            script_content = script_file.read()
        filled_script = script_content.format(
            padding_n=padding_n,
            smac=smac,
            dmac=dmac,
            sip=sip,
            dip=dip,
            version=version,
            priority=priority,
            ip_address=ip_address,
            iface=iface
        )
        # print("filled_script",filled_script)
        return filled_script

    def generate_broadcast_scapy_script(self, 
                                      sip: str, 
                                      dip: str, 
                                      dport: int, 
                                      iface: str,
                                      count: str):
        """
        Fill the broadcast scapy script template with the given parameters
        Args:
            sip (str): Source IP
            dip (str): Destination IP
            dport (int): Destination port
            iface (str): Interface
            count (str): Number of packets to send

        Returns:
            str: filled_script: The filled script with the given parameters.
        """
        with open(os.path.dirname(os.getcwd())+ '/lib/atb/service/scapy_template/broadcast_script.py', "r") as script_file:
            script_content = script_file.read()

        filled_script = script_content.format(
            sip=sip,
            dip=dip,
            dport=dport,
            iface=iface,
            count=count
        )
        # print("filled_script",filled_script)
        return filled_script
    
    def generate_rstp_scapy_script(self, 
                                   smac: int, 
                                   dmac: str, 
                                   brid: str, 
                                   iface: int,
                                   max_age: int,
                                   path_cost: int, 
                                   hello_time: int,
                                   fwd_delay: int,
                                   padding_n: int):
        """
        fill the vrrp scapy script template with the given parameters
        """
        with open(os.path.dirname(os.getcwd())+ '/lib/atb/service/scapy_template/rstp_script.py', "r") as script_file:
            script_content = script_file.read()
        filled_script = script_content.format(smac=smac,
                                              dmac=dmac,
                                              brid=brid,
                                              iface=iface,
                                              max_age=max_age,
                                              path_cost=path_cost, 
                                              hello_time=hello_time,
                                              fwd_delay=fwd_delay,
                                              padding_n=padding_n)
        # print("filled_script",filled_script)
        return filled_script
    
    def generate_rip_scapy_script(self, 
                                  rip_type: str,
                                  smac: int, 
                                  dmac: int, 
                                  sip: str, 
                                  dip: str, 
                                  iface: str,
                                  ripentries: list = None):
        
        with open(os.path.dirname(os.getcwd())+ '/lib/atb/service/scapy_template/rip_script.py', "r") as script_file:
            script_content = script_file.read()

        filled_script = script_content.format(
            rip_type=rip_type,
            smac=smac, 
            dmac=dmac, 
            sip=sip, 
            dip=dip, 
            iface=iface,
            ripentries=ripentries
        )
        # print("filled_script",filled_script)
        return filled_script

    def generate_multicast_scapy_script(self, 
                                        dst_mac: str, 
                                        src_mac: str, 
                                        nic: str, 
                                        pkt_count: str):
        """
        Fill the multicast scapy script template with the given parameters.
        Args:
            dst_mac (str): destination MAC address
            src_mac (str): source MAC address
            nic (str): nic name
            pkt_count (str): number of packets to send
        
        Return:
            str: filled_script: The filled script with the given parameters.
        """
        with open(os.path.dirname(os.getcwd())+ '/lib/atb/service/scapy_template/multicast_script.py', "r") as script_file:
            script_content = script_file.read()

        filled_script = script_content.format(dst_mac=dst_mac, src_mac=src_mac, nic=nic, pkt_count=int(pkt_count))

        return filled_script

    def do_script(self, scapy_file_name: str = ''):
        self._check_conneted()

        self.scapy_dict_name = "scapy_script"
        self.scapy_file_name = scapy_file_name

        self._ssh.command(f'mkdir -p $HOME/{self.scapy_dict_name}')
        self._ssh.command(f'mv $HOME/{self.scapy_file_name} $HOME/{self.scapy_dict_name}/')
        docker_cmd = f'docker run --rm --net=host \
            -v $HOME/{self.scapy_dict_name}:/{self.scapy_dict_name} {self.image_name}:{self.image_tag} \
            scapy -c /{self.scapy_dict_name}/{self.scapy_file_name}'

        ret = self._ssh.command(docker_cmd)

    def clean_up(self):
        # Clean up
        self._ssh.command(f"rm $HOME/{self.scapy_dict_name}/{self.scapy_file_name}")
