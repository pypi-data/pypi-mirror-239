from guerrilla_aaron.session import SshSession
from guerrilla_aaron.utils.decorator import root_access_required

class PktMgmtService:
    """
    Class for manipulating TCP traffic.

        Args:
            ssh_session (SshSession): An SSH session object.
            sudo_paswd (str): The sudo password for the remote server.

        Attributes:
            _ssh (SshSession): SSH session.
            _sudo_pwd (str): Sudo password.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._sudo_pwd = sudo_paswd

    def _check_conneted(self):
        """
        Check if SSH session is connected.

        Raises:
            ValueError: If SSH session is not connected.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    def check_env(self):
        """
        Check if the environment have tcpreplay.

        Raises:
            ValueError: If the Command 'tcpreplay' is not found.
        """
        self._check_conneted()
        output = self._ssh.command('tcpreplay -V')
        if 'not found' in output:
            raise ValueError('Command "tcpreplay" not found')

    def rewrite(self,
                infile: str = "input.pcap",
                outfile: str = "output.pcap",
                sip: str = None,
                dip: str = None,
                smac: str = None,
                dmac: str = None):
        """
        Rewrite a given pcap file and send it through a given interface.

            Args:
                infile (str, optional): Path to the input pcap file. Defaults to None.
                outfile (str, optional): Path to the output pcap file. Defaults to None.
                sip (str, optional): Source IP address for rewriting. Defaults to None.
                dip (str, optional): Destination IP address for rewriting. Defaults to None.
                smac (str, optional): Source MAC address for rewriting. Defaults to None.
                dmac (str, optional): Destination MAC address for rewriting. Defaults to None. 
                intf (str, optional): Interface used for sending the pcap file through tcpreplay command . Defaults to None. 
                sendfile (str, optional): Path of the pcap file that needs to be sent through tcpreplay command . Defaults to None. 
                number (int, optional): Number of packets that needs to be sent through tcpreplay command . Defaults to None. 

            Returns: 
                ret(string) : Output of tshark command after sending the packet through tcpreplay command  

            Raises: 
                ValueError: If SSH session is not connected
        """
        self._check_conneted()

        cmd = 'tcprewrite '
        cmd += f'--infile={infile} '
        cmd += f'--outfile={outfile} '
        cmd += '' if sip is None else f'--srcipmap=0.0.0.0/0:{sip} '
        cmd += '' if dip is None else f'--dstipmap=0.0.0.0/0:{dip} '
        cmd += '' if smac is None else f'--enet-smac={smac} '
        cmd += '' if dmac is None else f'--enet-dmac={dmac} '
        cmd += '--fixcsum'

        print(cmd)

        self._ssh.command(cmd)

        capture_name = outfile.split('/')[-1].split('.')[0]
        self._ssh.command(f'tshark -r {outfile} -V > {capture_name}.log')

        ret = self._ssh.command(f'cat {capture_name}.log')
        print(ret)

        return ret

    @root_access_required
    def send(self, intf: str = None, sendfile: str = None, number: int = None):
        self._check_conneted()
        """
        Send a packet capture file to the target device. 
            
            Args: 
                intf (str): Interface to use for sending the packet capture file. Defaults to None. 
                sendfile (str): Path of the packet capture file to send. Defaults to None. 
                number (int): Number of packets to send. Defaults to None.  

            Raises: 
                Exception: If connection is not established or login as root fails.
        """
        # cmd = 'docker run --rm -t -v $(pwd):/data -i dgarros/tcpreplay /usr/bin/tcpreplay '
        cmd = 'tcpreplay '
        cmd += f'--intf1=eth1 ' if intf is None else f'--intf1={intf} '
        cmd += f'' if number is None else f'-l {number} '
        cmd += f'./home/autotwo/output.pcap ' if sendfile is None else f'{sendfile} '

        print(cmd)

        self._ssh.command(cmd)
