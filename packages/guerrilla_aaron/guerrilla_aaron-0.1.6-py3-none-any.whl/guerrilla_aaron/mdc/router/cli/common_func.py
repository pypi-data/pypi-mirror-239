import os
import time

def telnet_login(session: object,
                 username: str,
                 password: str,
                 prompts_main: list,
                 prompts_config: list,
                 login_prompt: str = 'login'):
    """
    Log in to a telnet session with given username and password.

        Args:
            session (TelnetSession): Telnet session object.
            username (str): Username for login.
            password (str): Password for login.
            prompts (list): Prompts to expect after login.
            login_prompt (str, optional): Login prompt string, defaults to 'login: '. 
            
        Raises:
            ValueError: If cannot find login prompt or prompt after password. 
    """
    quick_timeout = 2

    # if login session existed, send enter to let prompt appear
    # print('try to get main prompt') #debug
    ret = session.command_expect('', prompts=prompts_main, timeout=quick_timeout)
    # consume prompts to make buffer clean
    # ret = session.command_expect(None, prompts=promtps, timeout=quick_timeout)
    if ret['matched']:
        return
    
    # print('try to get config prompt') #debug
    # if login session is config prompt, try to back to main prompt
    ret = session.command_expect('', prompts=prompts_config, timeout=quick_timeout)
    if ret['matched']:
        # print('config mode') #debug
        is_main_prompt = False
        for i in range(120):
            # print('try to login') #debug
            time.sleep(1)
            is_main_prompt = session.command_expect('exit', prompts=prompts_main, timeout=quick_timeout)['matched']
            if is_main_prompt:
                break
            # print('exit to main prompt') #debug
        return

    # try to press key to pass "Escape character is '^]'." if it occours
    # print('try to find login prompt 1') #debug
    ret = session.command_expect('',
                                 prompts=[login_prompt],
                                 exact_str=True,
                                 timeout=quick_timeout)
    if not ret['matched']:
        # print('try to find login prompt 2') #debug
        ret = session.command_expect('',
                                     prompts=[login_prompt],
                                     exact_str=True,
                                     timeout=quick_timeout)

    if not ret['matched']:
        raise ValueError(f'cannot find login prompt: "{login_prompt}" in {ret}')
    # print(f'input username: {username}') #debug
    session.command_expect(username,
                           prompts=['Password: '],
                           exact_str=True,
                           timeout=quick_timeout)
    # print(f'input password: {password}') #debug
    ret = session.command_expect(password, timeout=quick_timeout)
    if not ret['matched']:
        raise ValueError(f'cannot find prompt after password: {ret}')


def reload_factory_default(session: object,
                           prompts=[
                               'Proceed with reload to factory default? [Y/n]'
                           ]):
    """
    Reload the device to the factory default settings. 
        
        Args: 
            session (object): The session object for the device. 
            prompts (list): A list of strings that are expected from the device. 
    
    """
    session.command_expect('reload factory-default',
                           prompts=prompts,
                           exact_str=True)
    session.command_expect('Y')


def reload_factory_default_no_cert(session: object,
                           prompts=[
                               'Proceed with reload to factory default? [Y/n]'
                           ]):
    """
    Reload the device to the factory default settings.
    With no "Certificate Management" and "Authentication Certificate" configuration.
        
        Args: 
            session (object): The session object for the device. 
            prompts (list): A list of strings that are expected from the device. 
    
    """
    session.command_expect('reload factory-default no cert',
                           prompts=prompts,
                           exact_str=True)
    session.command_expect('Y')


def reload(session: object, prompts: list = ['Proceed with reload ? [Y/n]']):
    """
    Reload the device. 
        Args: 
            session (object): The session object for the device. 
            prompts (list): A list of strings that are expected from the device. 
    """
    session.command_expect('reload', prompts=prompts, exact_str=True)
    session.command_expect('Y')


def login(session: object,
          prompts1: list = ['Password:'],
          prompts2: list = ['#']):
    """
    Login to the device using admin credentials. 
        Args: 
            session (object): The session object for the device.  
            prompts1 (list): A list of strings that are expected from the device after entering 'admin'.  
            prompts2 (list): A list of strings that are expected from the device after entering 'moxa'.
    """
    session.command_expect('admin', prompts=prompts1, exact_str=True)
    session.command_expect('moxa', prompts=prompts2, exact_str=True)