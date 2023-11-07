import json
from datetime import datetime

def create_debug_output(option: bool, name_prefix: str, con_type: str,
                        host: str, port):
    """
    Creates debug output for a session. 

        Args: 
            option (bool or file object): If True, session information and output will be logged. If False, nothing will be logged. Or set a file object for writing console output only. 
            name_prefix (str): Prefix for the debug output files. 
            con_type (str): Type of connection used in the session. 
            host (str): Host address used in the session. 
            port (int): Port number used in the session. 
            
        Returns: 
            output_logfile (file object): File object of the logfile created if option is True or set to a file object; None otherwise.
    """
    time_str = datetime.now().isoformat()
    name = f'{name_prefix}_{time_str}'

    if option is True:
        # create debug info
        with open(f'{name}.info.json', 'w', encoding='utf8') as f:
            json.dump(
                {
                    'start_time': time_str,
                    'connection_type': con_type,
                    'host': host,
                    'port': port
                },
                f,
                indent=2)
        # create logfile object
        # pylint: disable=consider-using-with
        output_logfile = open(f'{name}.output.txt', 'w', encoding='utf8')
    elif option:
        output_logfile = option
    else:
        output_logfile = None
    return output_logfile
