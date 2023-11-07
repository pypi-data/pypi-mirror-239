import sys
from guerrilla_aaron.host import *
from guerrilla_aaron.host import HostFactory
from guerrilla_aaron.topology.topology_info import prepare_json
from guerrilla_aaron.steps.common import login_and_measure_time

def _reset(context):
    context.dut["DUT"] = HostFactory.create_mdc_rp(
    context.dut_info["DUT"], 
    debug_output=sys.stdout)
    context.dut["DUT"].main().reload_factory_default()
    time.sleep(context.dut_info["DUT"]['reload_delay'])
    context.dut["DUT"].close()

def _backup(context):
    login_time = login_and_measure_time(context=context, device="DUT")
    print(f"Reload Factory Time: {context.dut_info['DUT']['reload_delay']} + {login_time:.2f} seconds")
    ret = context.dut["DUT"].main().export_config(
        tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"], 
        file_name="default.ini")
    assert ret['matched'] and '^Parse error' not in ret[
        'data'], f'Fail to prepare default config: {ret["data"]}'
    context.dut["DUT"].close()

def after_step(context, step):
    """
    In order to prevent traffic conflicts, internet port will be enabled for the DDNS case and disabled for all other cases.

        Args:
            step: specific step
    """
    
    if step.name == 'reload factory-default "DUT"':
        port = context.dut_info["DUT"]["testbed"]["internet_port"]
        flag = False
        tags = context.scenario.tags
        for t in tags:
            if 'ddns' in t or 'ping' in t:
                flag = True
        if not flag:
            context.dut["DUT"].go_config_if_ethernet(f'1/{port}').set_port_status(flag = 'disable')
        else:
            context.dut["DUT"].go_config_if_ethernet(f'1/{port}').set_port_status(flag = 'enable')

def before_all(context):
    prepare_json(context)
    # do reload factory to prepare default configuration for initializing with restoration
    if context.dut_info["DUT"]["init_method"] == "restore":
        _reset(context)
        _backup(context)


def before_scenario(context, scenario):
    prepare_json(context)


def after_scenario(context, scenario):
    pass


def after_feature(context, feature):
    if context.dut_info["DUT"]["init_method"] == "restore":
        print("reset to disable config encrypt setting for restoration")
        reset_list = ["config_encrypt", "user_account", "user_interface"]
        if any(x in feature.filename for x in reset_list):
            _reset(context)