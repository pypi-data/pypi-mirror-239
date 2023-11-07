from session import SshSession
from utils.decorator import root_access_required

class BirdService:
    """
    A class to manage bird server.

        Attributes:
            _ssh (SshSession): An instance of SshSession.
            _sudo_pwd (str): Password for sudo user.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._dir = "$HOME/bird"
        self._sudo_pwd = sudo_paswd

    def _check_conneted(self):
        """
        Check if the environment is valid.

            Raises:
                ValueError: If the SSH session is not connected or if no docker image cincan/tshark is found.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')
        
    def check_env(self):
        self._check_conneted()
        output = self._ssh.command('docker images')
        if 'pierky/bird' not in output:
            self._ssh.command('docker pull pierky/bird:1.6.3', 
                              exact_prompts=['Downloaded newer image for pierky/bird:1.6.3'], 
                              timeout=120)
        output = self._ssh.command('ls')
        if 'bird' not in output:
            self._ssh.command(f'mkdir {self._dir}')
        self.clean_up()

    def start(self):
        docker_cmd = f'docker run --name bird --privileged --rm -dit --network=host \
            -v $HOME/bird:/etc/bird pierky/bird'
        self._ssh.command(docker_cmd)

    def clean_up(self):
        self._ssh.command("docker ps") 
        try:
            self._ssh.command("docker stop bird", 
                              exact_prompts=['bird'],
                              timeout=60)
        except:
            print("bird container is no actived")

    def set_ospf_config(self, 
                    router_id: str = "192.168.128.100", 
                    intf: str = "eth1", 
                    area_id: str = "0.0.0.0", 
                    priority: int = 1,
                    hello_interval: int = 10, 
                    dead_interval: int = 40):
        ospf_config= '''
protocol kernel {{
        scan time 60;
        import none;
        export all;   # Actually insert routes into the kernel routing table
}}

protocol device {{
        scan time 60;
}}

router id {};

protocol ospf {{
 export all;
 import all;
 area {} {{
  interface "{}" {{
   hello {};
   retransmit 5;
   cost 10;
   transmit delay 1;
   dead count 4;
   wait {};
   type broadcast;
   priority {};
   authentication none;
   #authentication cryptographic; password "ixnfo.com";
  }};
 }};
}}
'''.format(router_id, area_id, intf, hello_interval, dead_interval, priority)
        self._ssh.command(f"cat <<EOF > {self._dir}/bird.conf\n{ospf_config}\nEOF")
