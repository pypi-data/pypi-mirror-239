from host import *
from behave import *
from steps import login, interface, common

@then('compare running config with exported configuration file')
def step_impl(context):
    with open(f'tftp/test.ini') as f:
        lines = f.read().replace(" ", "").split('\n')[:-1]
    for i in range(len(context.running_config)):
        assert context.running_config[i] == lines[
            i], f"from line {i} running config is different from ini"
