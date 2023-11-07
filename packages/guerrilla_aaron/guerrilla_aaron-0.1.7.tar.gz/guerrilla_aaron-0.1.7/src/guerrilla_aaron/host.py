import time

from guerrilla_aaron.mdc import Router
from abc import ABC, abstractmethod
from guerrilla_aaron.atb.const import get_control_class
from guerrilla_aaron.session import SshSession, TelnetSession, SerialSession
from guerrilla_aaron.utils.error_detector import cli_error_detector


class HostAbstract(ABC):

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def check_env(self):
        pass


class AtbHost(HostAbstract):

    def __init__(self, session: object, credential: dict, controls: list):
        self._s = session
        self._cred = credential
        self._ctrls = {}
        self._init_controls(controls)

    def _init_controls(self, controls):
        for ctrl in controls:
            ctrl_obj = ControlFactory.create(ctrl, self._s, self._cred)
            print(f'**************ctrl_obj: {ctrl_obj}**************')
            setattr(self, ctrl['name'], ctrl_obj)
            self._ctrls[ctrl['name']] = ctrl_obj

    def login(self):
        self._s.login(self._cred['username'], self._cred['password'])

    def logout(self):
        self._s.logout()

    def check_env(self):
        for _, obj in self._ctrls.items():
            print(f'**************check service: {_}**************')
            obj.check_env()

class SessionFactory:

    @staticmethod
    def create_ssh(conf: dict, auto_prompt_reset: bool = False):
        if conf['con_type'] == 'ssh':
            return SshSession(conf, auto_prompt_reset=auto_prompt_reset)
        else:
            raise ValueError(f'session type not supported: {conf["type"]}')
        
    @staticmethod
    def create_telnet(conf: dict, debug_output: bool = False):
        if conf['con_type'] == 'telnet':
            session = TelnetSession(conf, cli_error_detector, debug_output)
            session.open()
            return session
        else:
            raise ValueError(f'session type not supported: {conf["type"]}')

    @staticmethod
    def create_serial(conf: dict, debug_output: bool = False):
        if conf['con_type'] == 'serial':
            session = SerialSession(conf, cli_error_detector, debug_output)
            session.open()
            return session
        else:
            raise ValueError(f'session type not supported: {conf["type"]}')


class ControlFactory:

    @staticmethod
    def create(ctrl: dict, session: object, cred: dict):
        try:
            _type = ctrl['type']
            ctrl_cls = get_control_class(_type)
        except KeyError as e:
            raise ValueError('bad control config') from e

        return ctrl_cls(session, cred['password'])


class HostFactory:

    @staticmethod
    def create_atb(conf: dict):
        if conf['session']['con_type'] == 'ssh':
            session = SessionFactory.create_ssh(conf['session'], auto_prompt_reset=True)
        elif conf['session']['con_type'] == 'telnet':
            raise ValueError(f'Its not supported yet: {conf["session"]["con_type"]}')
        
        host_obj = AtbHost(session, conf['session']['credential'],
                                 conf['controls'])
        return host_obj
    
    @staticmethod
    def create_mdc_rp(conf: dict, debug_output:bool = False):
        if conf['session']['con_type'] == 'ssh':
            session = SessionFactory.create_ssh(conf['session'])
            session.login(conf['credential']['username'], conf['credential']['password'])
            host_obj = Router(session, conf['model'])
        elif conf['session']['con_type'] == 'telnet':
            session = SessionFactory.create_telnet(conf['session'], debug_output)
            session.login(conf['credential'])
            host_obj = Router(session, conf['model'])
        elif conf['session']['con_type'] == 'serial':
            session = SessionFactory.create_serial(conf['session'], debug_output)
            session.login(conf['credential'])
            host_obj = Router(session, conf['model'])
        
        return host_obj